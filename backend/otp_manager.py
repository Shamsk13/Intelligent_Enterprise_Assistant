import smtplib
import ssl
import random
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def generate_otp():
    """Generate a 6-digit OTP."""
    return str(random.randint(100000, 999999))


def send_otp(recipient_email, otp):
    """Send OTP to the given email using Gmail SMTP."""
    try:
        subject = "Your OTP Code"
        body = f"Your One-Time Password (OTP) is: {otp}"

        msg = EmailMessage()
        msg["From"] = EMAIL_SENDER
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.set_content(body)

        # Gmail SMTP server configuration
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"[INFO] Sent OTP {otp} to {recipient_email}")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to send OTP: {e}")
        return False
