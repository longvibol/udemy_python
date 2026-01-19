import smtplib, ssl

class Email:
    def send(message):
        host = "smtp.gmail.com"
        port = 465

        USERNAME = "vibollong@gmail.com"
        PASSWORD = "vdydzkmaukvebhik"

        RECEIVER_EMAIL = "vibollong@gmail.com"
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(USERNAME, PASSWORD)
            server.sendmail(USERNAME, RECEIVER_EMAIL, message)
