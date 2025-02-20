import smtplib
from datetime import datetime
import functions_framework
from email.mime.text import MIMEText
from config import config_vars
import os

APP_EMAIL_PASSWORD = os.getenv("APP_EMAIL_PASSWORD")

@functions_framework.http
def send_email(request):
    # Using Gmail SMTP (Make sure to enable Less Secure Apps or use App Password)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    try:
        sender_email = config_vars["sender_email"]
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, APP_EMAIL_PASSWORD)
    except Exception as e:
        print(f"Failed to connect to smtp server {e}")

    for receiver in config_vars["recievers"]:
        subject = f"Lembrete de Pagamento - {receiver['name']}"
        body = f"""
        Olá {receiver['name']}, hoje é o dia de fechamento da minha fatura.
        
        Você tem até o dia 05/{datetime.now().month} para pagar o que me deve.
        
        Item(s) comprados com meu cartão: {','.join(receiver['items'])}
        
        Valor total: {receiver['value']}

        Meu pix é: 097.396.584-31

        Se já realizou o pagamento, desconsidere essa mensagem.

        Esta é uma mensagem automática, não responda à este email.
        """
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = ", ".join(receiver['emails'])
        try:
            server.sendmail(sender_email, receiver['emails'], msg.as_string())
            server.quit()
            return "Email sent successfully"
        except Exception as e:
            return str(e)
