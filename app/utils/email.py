import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException

def send_email(to_email, subject, body):
    sender_email = "blackfdayit@gmail.com"
    sender_password = "zxbt cnqg ckqe tqbq"
    
    # SMTP setup
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
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
        print(f"Error sending email: {e}")