import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException
from dotenv import load_dotenv
import os

# Carica le variabili d'ambiente dal file .env
load_dotenv()

import logging

logger = logging.getLogger(__name__)

def send_email(to_email, subject, body):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    
    try:
        val = os.getenv("SMTP_PORT", "587")
        smtp_port = int(val)
    except (ValueError, TypeError):
        smtp_port = 587

    if not sender_email or not sender_password:
        logger.error("Email configuration is missing (SENDER_EMAIL or SENDER_PASSWORD)")
        raise HTTPException(status_code=500, detail="Configurazione email mancante nel server.")

    # SMTP setup
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Componi l'email
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail=f"Errore tecnico durante l'invio dell'email: {str(e)}")
