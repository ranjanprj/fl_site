import json
import constants as cons
import tweepy
import keys
import stripe
import constants as cons




def retrieve_customer_id(token,emailAddr):
    customer = stripe.Customer.create(
      email = emailAddr,
      source = token,
    )












if __name__ == "__main__":
    test_stripe_pay()
