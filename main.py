import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

import functions_framework
from flask import Request, typing

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
        subject = f"Lembrete de Pagamento - {receiver['name']}"
        body = f"""
        Olá {receiver['name']}, hoje é o dia de fechamento da minha fatura.
        
        Você tem até o dia 02/{datetime.now().month + 1} para pagar o que me deve.
        
        Item(s) comprados com meu cartão: {','.join(receiver['items'])}
        
        Valor total: {receiver['value']}

        Meu pix é: {PIX_KEY}

        Se já realizou o pagamento, desconsidere essa mensagem.

        Esta é uma mensagem automática, não responda à este email.
        """
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
