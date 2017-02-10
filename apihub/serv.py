from bottle import route, run, template, static_file, get, post, request, redirect
import psycopg2
import time as t
from multiprocessing import Process
import pglisten
import stripe

@post('/login') # or @route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if username == 'ranjanprj' and password == 'ranjanprj' :
        redirect('/static/www/interestedin.html')
    else:
        return "<p>Login failed.</p>"

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')


@get("/reset_password")
def reset_password():
    email = request.GET.get("email")
    token = request.GET.get("token")
    return """
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
        <title>Bootstrap 101 Template</title>

        <!-- Bootstrap -->
        <link href="/static/bootstrap/css/bootstrap.min.css" rel="stylesheet">

    </head>

    <body>
        <!-- Reset -->
        <div id="reset_pass_container" class="container">
            <h1>Reset Password</h1>
            <div id="reset_pass_error" class="alert alert-danger" style="display:none">
                <strong>Error</strong> in Login in, email password do not match <a href="">Reset Password</a>
            </div>


            <form id="reset_pass_form" method="POST">
                <div class="form-group">
                    <label for="exampleInputPassword1">Password</label>
                    <input type="password" class="form-control" placeholder="Password" name="pass" value="ranjanprj">
                </div>
                <div class="form-group">
                    <label for="exampleInputPassword1">Repeat Password</label>
                    <input type="password" class="form-control" placeholder="Password" name="repeat_pass" value="ranjanprj">
                </div>
                <input type="hidden" class="form-control" placeholder="email" name="email" value="{0}">
                <input type="hidden" class="form-control" placeholder="token" name="token" value="{1}">

                <button type="submit" class="btn btn-success btn-lg">Login</button>
                <button class="btn btn-primary  btn-lg">Sign Up</button>
            </form>

        </div>
          <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
        <script src="/static/libs/jquery.js"></script>

        <!-- Include all compiled plugins (below), or include individual files as needed -->
        <script src="/static/bootstrap/js/bootstrap.min.js"></script>
        <script src="/static/www/js/intrstedin.js"></script>

    </body>

    </html>

    """.format(email,token)

@post("/stripe_charge")
def your_charge_code():
    print(request.forms.get("stripeToken"))
    print(request)
    stripe.api_key = "sk_test_7WVtEpXXGMIHSeYL8IA1csUk"

    # Token is created using Stripe.js or Checkout!
    # Get the payment token submitted by the form:
    token = request.forms.get("stripeToken")
    print("Token ->",token)
    # Create a Customer:
    # customer = stripe.Customer.create(
    #   email = "ranjan.new1@example.com",
    #   source = token,
    # )
    # print("CUSTOMER ID {0}".format(customer.id))
    # # Charge the Customer instead of the card:
    # charge = stripe.Charge.create(
    #   amount=3254,
    #   currency="usd",
    #   customer=customer.id,
    # )



    # YOUR CODE: Save the customer ID and other info in a database for later.

    # YOUR CODE (LATER): When it's time to charge the customer again, retrieve the customer ID.
    charge = stripe.Charge.create(
      amount=1500, # $15.00 this time
      currency="usd",
      customer=customer.id, # Previously stored, then retrieved
    )

def traffic_job():
    pglisten.pg_listen()
    while True:
        # print("Running Job")
        # sleep_time = randint(15,20)
        sleep_for_24hrs = 24*3600
        sleep_for_30sec = 30
        t.sleep(60*10)
        # t.sleep(sleep_for_30sec)
        # print("Running Twitter Timeline Job")




def main():
    traffic_processor = Process(target=traffic_job)
    #traffic_processor.start()
    run(host='0.0.0.0', port=8080, reloader= True)


if __name__ == '__main__':
    main()
