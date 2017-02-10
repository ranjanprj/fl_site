import smtplib
import json

def reset_password(channel,pl):
    payload = json.loads(pl)
    print("Printing payload")
    print(payload)
    try:
        print("connecting")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        print("login")
        server.login("kabootal@gmail.com", "ajzuktqvlcppdsuk")

        msg = """
            <h4>This is an email to reset your password</h4>
            http://ec2-52-90-180-17.compute-1.amazonaws.com:8080/reset_password?email={0}&token={1}
        """.format(payload['email'],payload['token'])
        print("sending")
        server.sendmail("kabootal@gmail.com", payload['email'], msg)
        server.quit()
    except Exception as e :
        print(e)
