import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 25))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")

def send_reset_email(to_email: str, reset_link: str):
    subject = "Réinitialisation de votre mot de passe"
    body = f"Bonjour,\n\nPour réinitialiser votre mot de passe, cliquez sur le lien suivant :\n{reset_link}\n\nSi vous n'avez pas fait cette demande, ignorez cet email."
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            # Si vos paramètres SMTP nécessitent TLS
            if SMTP_USER and SMTP_PASSWORD:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(EMAIL_FROM, [to_email], msg.as_string())
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")
