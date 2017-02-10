import smtplib

try:
    print("connecting")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    print("login")
    server.login("kabootal@gmail.com", "ajzuktqvlcppdsuk")

    msg = "YOUR MESSAGE!"
    print("sending")
    server.sendmail("kabootal@gmail.com", "company.ranjan@gmail.com", msg)
    server.quit()
except Exception as e :
    print(e)
