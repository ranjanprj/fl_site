from decimal import Decimal
import stripe

class StripePayment:
    def __init__(self,token,customer_payment_email, customer_app_email, service_name,payment_provider, booking_id):

        
        self.token = token
        self.customer_payment_email = customer_payment_email
        self.customer_app_email = customer_app_email
        self.service_name = service_name
        self.payment_provider = payment_provider
        self.booking_id = booking_id
       
        
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
        return sql.format(self.service_name,self.payment_provider)
    
#         result = self.conn.execute(sql.format(self.service_name,self.payment_provider),1)
#         return {"service_payment_info_id" : result[0][0], "pub_key" : result[0][1]} if result is not None else {"service_payment_info_id" : None, "pub_key":None}
#     
#         self.conn.execute(sql.format(self.service_name,self.payment_provider))
#         result = self.conn.fetchone()
#         print("PUB KEY ",result)
#         return {"service_payment_info_id" : result[0], "pub_key" : result[1]} if result is not None else {"service_payment_info_id" : None, "pub_key":None}
        

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
        return sql.format(self.customer_payment_email,self.customer_app_email,self.payment_provider)
#         result = self.conn.execute(sql.format(self.customer_payment_email,self.customer_app_email,self.payment_provider),1)
#         return None if result is None else result[0][0]
#      
#         self.conn.execute(sql.format(self.customer_payment_email,self.customer_app_email,self.payment_provider))
#         result = self.conn.fetchone()
#         return None if result is None else result[0]
          


    
    def store_customer_id(self,customer_id,service_payment_info_id):
        self.customer_id = customer_id
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
                    )

                    """
        #result = self.conn.execute(sql.format(self.customer_payment_email,self.customer_app_email,self.token,self.customer_id,self.service_payment_info_id),1)
#         self.conn.execute(sql.format(self.customer_payment_email,self.customer_app_email,self.customer_id,self.service_payment_info_id))
        return sql.format(self.customer_payment_email,self.customer_app_email,customer_id,service_payment_info_id)

    def set_payment_status(self,status,amount,currency,error_log = ""):
        sql = """
                            insert
                            into
                                public.customer_payments(
                                    amount,
                                    currency,
                                    payment_status,
                                    booking_id,
                                    error_log
                                )
                            values(
                                 {0},
                                '{1}',
                                '{2}',
                                 {3},
                                '{4}'
                            )
    
                            """
        return sql.format(amount,currency,status,self.booking_id,error_log)
    
    def create_customer(self,pub_key,token):
        stripe.api_key = pub_key
        
        customer = stripe.Customer.create(
                email = self.customer_payment_email,
                source = token
            )
        return customer    
    
    
    def make_payment(self,pub_key,customer_id,amount,currency):    
    # if not then create and store
        stripe.api_key = pub_key        
            
        # Now charge payment
        charge = stripe.Charge.create(
            amount=Decimal(amount),
            currency=currency,
            customer=customer_id
        )
              
       
