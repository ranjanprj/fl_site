import stripe
from decimal import Decimal

class StripePayment:
    def __init__(self,conn,token,customer_payment_email, customer_app_email, service_name,payment_provider, booking_id):

        self.conn = conn
        self.token = token
        self.customer_payment_email = customer_payment_email
        self.customer_app_email = customer_app_email
        self.service_name = service_name
        self.payment_provider = payment_provider
        self.booking_id = booking_id
        print(self.token,token)
        print(customer_app_email)

    def get_pub_key(self):
        sql = """
					select
						p.id, p.pub_key
					from
						service_payment_info as p inner join service as s on
						p.service_id = s.id
					where
						s.service_name = '{0}'
						and p.payment_provider = '{1}';
					"""
        result = self.conn.execute(sql.format(self.service_name,self.payment_provider),1)
        # self.conn.execute(sql.format(self.service_name,self.payment_provider))
        # result = self.conn.fetchone()
        return {"service_payment_info_id" : result[0][0], "pub_key" : result[0][1]} if result is not None else {"service_payment_info_id" : None, "pub_key":None}

    def get_customer_id(self):
        sql = """
					select
						cpi.customer_id
					from
						customer_payment_info as cpi inner join service_payment_info as pi on
						cpi.service_payment_info_id = pi.service_id
					where
						cpi.customer_payment_email = '{0}'
						and cpi.customer_app_email = '{1}'
						and pi.payment_provider = '{2}'

					"""
        result = self.conn.execute(sql.format(self.customer_payment_email,self.customer_app_email,self.payment_provider),1)
        # self.conn.execute(sql.format(self.customer_payment_email,self.customer_app_email,self.payment_provider))
        # result = self.conn.fetchone()
        return result[0][0]


    def create_customer(self):
        print("token ",self.token)
        
        stripe.api_key = self.stripe_api_key
        print(self.stripe_api_key)
        customer = stripe.Customer.create(
          email = self.customer_payment_email,
          source = self.token
        )
        return customer


    def store_customer_id(self):
        sql = """
                    insert
                    into
                        public.customer_payment_info(
                            customer_payment_email,
                            customer_app_email,
                            customer_id,
                            service_payment_info_id
                        )
                    values(
                        '{0}',
                        '{1}',
                        '{2}',
                         {3}
                    );

                    """
        #result = self.conn.execute(sql.format(self.customer_payment_email,self.customer_app_email,self.token,self.customer_id,self.service_payment_info_id),1)
        self.conn.execute(sql.format(self.customer_payment_email,self.customer_app_email,self.customer_id,self.service_payment_info_id))


    def charge_payment(self,amount,currency):
        status = 'failed'
        try:
            # make a payment entry
            amt = Decimal(amount)
            sql = """
                            insert
                        	into
                        		public.customer_payments(
                        			amount,
                        			currency,
                        			payment_status,
                        			booking_id
                        		)
                        	values(
                        		 {0},
                                '{1}',
                                '{2}',
                                 {3}
                        	);
    
                            """
            self.conn.execute(sql.format(amt,currency,'initiated',self.booking_id))
            plpy.info("Inserted the status in customer_payments")
            # Get the pub key and other details
            sid_pub = StripePayment.get_pub_key(self)
            self.stripe_api_key = sid_pub['pub_key']
            
            stripe.api_key = self.stripe_api_key
            self.service_payment_info_id = sid_pub['service_payment_info_id']
            plpy.info("Got the Stipe pub key and service payment info id")
            # Check whether customer exists otherwise create one
            self.customer_id = StripePayment.get_customer_id(self)
            
            if self.customer_id is None:
                customer = StripePayment.create_customer(self)
                self.customer_id = customer.id
                StripePayment.store_customer_id(self)
                
            # Now charge payment
            plpy.info("Got the Customer ID ")
            try:
                if self.customer_id is None:
                    plpy.error("Customer ID is not present")
                    
                plpy.info("Trying to charge the customer ")
                charge = stripe.Charge.create(
                  amount=amount,
                  currency=currency,
                  customer=self.customer_id
                )
                plpy.info("Customer has been charged")
                # change the status
                result = self.conn.execute("""
                        update
                            public.customer_payments
                        SET payment_status = 'successful'
                        WHERE booking_id = {0}
                        """.format(self.booking_id))
                status = 'success'
            except Exception as e:
                # change the status to failed
                plpy.info("EXCEPTION ->",e)
                result = self.conn.execute("""
                        update
                            public.customer_payments
                        SET payment_status = 'failed'
                        WHERE booking_id = {0}
                        """.format(self.booking_id))
                
        except Exception as e:
            plpy.info("Exception while calling charge_payment",e)
        finally:
            return status