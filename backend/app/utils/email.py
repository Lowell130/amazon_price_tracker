import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException
from app.config import SENDER_EMAIL, SENDER_PASSWORD, SMTP_SERVER, SMTP_PORT
import logging
import os # Re-adding os because it might be needed if I didn't import everything, but I'll import everything.
# Actually I'll use smtplib directly.

logger = logging.getLogger(__name__)

def send_email(to_email, subject, body):
    sender_email = SENDER_EMAIL
    sender_password = SENDER_PASSWORD
    smtp_server = SMTP_SERVER
    smtp_port = SMTP_PORT

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
