import smtplib, os, json
from email.message import EmailMessage
import logging

logger = logging.getLogger(__name__)

def notification(message):
    try:
        sender_address = os.environ.get("GMAIL_ADDRESS")
        sender_password = os.environ.get("GMAIL_PASSWORD")
        receiver_address = message["email"]

        msg = EmailMessage()
        msg.set_content(f"{message['readme_content']}")
        msg["Subject"] = f"{message['repo_name']} readme file"
        msg["From"] = sender_address
        msg["To"] = receiver_address

        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.starttls()
        session.login(sender_address, sender_password)
        session.send_message(msg, sender_address, receiver_address)
        session.quit()
        logger.info("Mail Sent")

    except Exception as err:
        logger.error(f"Failed to send email: {err}")
        return err

    return None

