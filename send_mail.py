import db
import os
import smtplib
from email.message import EmailMessage


# EMAIL_ADDRESS = os.environ.get("email_user")
# EMAIL_PASSWORD = os.environ.get("email_password")


connection = db.connect()
subject = input("What is email subject?")
email_content = input("Content of the email: ")
member_list = ["dayana.garvik@gmail.com", "trymhustoft@yahoo.no"]  # db.send_email(connection)
recipients = ', '.join(member_list)


message = EmailMessage()
message['Subject'] = subject
message['From'] = "dayana.garvik@gmail.com"  # EMAIL_ADDRESS
message['To'] = recipients
message.set_content(email_content)


with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(message)

