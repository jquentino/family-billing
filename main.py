import os
import smtplib
from email.mime.text import MIMEText

import functions_framework
from flask import Request, typing
from templates import content_generators

APP_EMAIL_ADDRESS = os.getenv("APP_EMAIL_ADDRESS")
APP_EMAIL_PASSWORD = os.getenv("APP_EMAIL_PASSWORD")
PIX_KEY = os.getenv("PIX_KEY")


@functions_framework.http
def send_email(request: Request) -> typing.ResponseReturnValue:
    # Using Gmail SMTP (Make sure to enable Less Secure Apps or use App Password)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(APP_EMAIL_ADDRESS, APP_EMAIL_PASSWORD)
    except Exception as e:
        return f"Failed to connect to smtp server {e}"

    recievers_data = request.json
    for receiver in recievers_data["recievers"]:
        lang = receiver.get("lang", "en")
        content_gen = content_generators[lang]
        subject = content_gen.subject(receiver["name"])
        body = content_gen.body(
            name=receiver["name"],
            payment_day=receiver.get("payment_day", 2),
            items=receiver["items"],
            value=receiver["value"],
            pix_key=PIX_KEY,
        )
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = APP_EMAIL_ADDRESS
        msg["To"] = ", ".join(receiver["emails"])
        try:
            server.sendmail(APP_EMAIL_ADDRESS, receiver["emails"], msg.as_string())
            server.quit()
            return "Email sent successfully"
        except Exception as e:
            return str(e)
