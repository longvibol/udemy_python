import smtplib
import imghdr
from email.message import EmailMessage

PASSWORD = "vdydzkmaukvebhik"
SENDER_EMAIL = "vibollong@gmail.com"
RECEIVER_EMAIL = "khcamtech@gmail.com"

def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message["From"] = SENDER_EMAIL
    email_message["To"] = RECEIVER_EMAIL
    email_message.set_content("Hey, we just saw a new customer!")

    with open(image_path, "rb") as file:
        content = file.read()

    subtype = imghdr.what(None, content) or "jpeg"  # fallback
    email_message.add_attachment(content, maintype="image", subtype=subtype, filename="photo.jpg")

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(SENDER_EMAIL, PASSWORD)
        smtp.send_message(email_message)

if __name__ == "__main__":
    send_email(image_path="images/19.jpg")
