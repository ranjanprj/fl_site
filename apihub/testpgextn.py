

import constants as cons
from locale import currency



def make_stripe_payment():
    
    from pgextn.payments import StripePayment
    
    pg_conn = cons.get_pg_conn()    
    c = pg_conn.cursor()


    token = 'tok_19dgAUC8Isc8Asv3SLUGgaaL'
    customer_payment_email = "ranjan.new2@example.com"
    customer_app_email = "ranjanprj@gmail.com"
    service_name = "carwash_service"
    payment_provider = "stripe"
    booking_id = 1
    amount = 123
    currency = "USD"
    
    stripe_payment = StripePayment(token,customer_payment_email, customer_app_email, service_name,payment_provider, booking_id)
    
     # make a payment entry
    sql = stripe_payment.set_payment_status("initiated",amount,currency)
    pg_conn.commit()
    
    c.execute(sql)
    
    # get pub key
    sql = stripe_payment.get_pub_key()
    
    c.execute(sql)
    result = c.fetchone()    
    service_payment_info_id = result[0]
    pub_key = result[1]
      
    
    
    # check whether customer id already exists
    sql = stripe_payment.get_customer_id()
    
    c.execute(sql)    
    result = c.fetchone()
     
    customer_id = None if result is None else result[0]
    
    
    try:        
        # if not then create and store
        if customer_id is None:
            customer = stripe_payment.create_customer(pub_key,token)  
            
            customer_id = customer.id
            # Store customer id for future use
            sql = stripe_payment.store_customer_id(customer_id,service_payment_info_id)
            c.execute(sql)
            pg_conn.commit()
            
        try:        
            # Now charge payment
            stripe_payment.make_payment(pub_key,customer_id,amount,currency)
                          
            # change the status
            sql = stripe_payment.set_payment_status("successful",amount,currency)
            
            c.execute(sql)
            pg_conn.commit()
        except Exception as e:
            print(e)     
            sql = stripe_payment.set_payment_status("failed",amount,currency,"Charging Customer Failed   " + str(e).replace("'","''"))        
            c.execute(sql)
            pg_conn.commit()   
            raise e
                
    except Exception as e:     
        print(e)
        sql = stripe_payment.set_payment_status("failed",amount,currency,"Creating Customer Failed  " + str(e).replace("'","''"))        
        c.execute(sql)
        pg_conn.commit()    
        raise e    
    
         
        
        
    
    pg_conn.close()
    
    
 

status = ''
from pgextn.payments import StripePayment

status = "Initiating StripePayment object"
stripe_payment = StripePayment(token,customer_payment_email, customer_app_email, service_name,payment_provider, booking_id)


 # make a payment entry
sql = stripe_payment.set_payment_status("initiated",amount,currency)


plpy.execute(sql)

status = status + " Getting Pub key"
# get pub key
sql = stripe_payment.get_pub_key()

result = plpy.execute(sql,1)
service_payment_info_id = result[0]
pub_key = result[0]
  

status = status + " Checking Customer ID"
# check whether customer id already exists
sql = stripe_payment.get_customer_id()

result = plpy.execute(sql,1)    

 
customer_id = None if result is None else result[0]


try:        
    # if not then create and store
    status = status + " Customer does not exist create and store"
    if customer_id is None:
        customer = stripe_payment.create_customer(pub_key,token)  
        
        customer_id = customer.id
        # Store customer id for future use
        sql = stripe_payment.store_customer_id(customer_id,service_payment_info_id)
        plpy.execute(sql)
        
        
    try:        
        status = status + " Now charge the customer"
        # Now charge payment
        stripe_payment.make_payment(pub_key,customer_id,amount,currency)
                      
        # change the status
        sql = stripe_payment.set_payment_status("successful",amount,currency)
        
        plpy.execute(sql)
        status = status + " Success charged"
    except Exception as e:
        print(e)     
        sql = stripe_payment.set_payment_status("failed",amount,currency,"Charging Customer Failed   " + str(e).replace("'","''"))        
        plpy.execute(sql)
        status = status + " failure in charging"  + " " + str(e)
        
            
except Exception as e:     
    print(e)
    sql = stripe_payment.set_payment_status("failed",amount,currency,"Creating Customer Failed  " + str(e).replace("'","''"))        
    plpy.execute(sql)      
    status = status + " failure in creating customer" + " " + str(e)
    
return status

 
if __name__ == "__main__":
    make_stripe_payment()