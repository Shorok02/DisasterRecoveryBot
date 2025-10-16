# services/email_service.py

import random
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from config import EMAIL_SENDER, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT, OTP_EXPIRY_MINUTES
from db.database import save_otp


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email):
    otp = generate_otp()
    expiry = datetime.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)

    save_otp(email, otp, expiry)

    msg = MIMEText(f"Your Amana DR Bot verification code is: {otp}\nExpires in {OTP_EXPIRY_MINUTES} minutes.")
    msg["Subject"] = "Amana DR Bot OTP"
    msg["From"] = EMAIL_SENDER
    msg["To"] = email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print("Email send error:", e)
        return False
