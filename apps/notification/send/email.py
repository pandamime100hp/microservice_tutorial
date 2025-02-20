import smtplib, os, json
from email.message import EmailMessage


def notification(body):
    try:
        message = json.loads(body)
        mp3_id = message["mp3_id"]
        sender_address = os.environ.get("EMAIL_ADDRESS")
        sender_password = os.environ.get("EMAIL_PASSWORD")
        receiver_address = message["username"]

        msg = EmailMessage()
        msg.set_content(f"Your mp3 is ready: {mp3_id}")
        msg["Subject"] = "Mp3 is ready"
        msg["From"] = sender_address
        msg["To"] = receiver_address

        server = smtplib.SMTP("smtp.gmail.com")
        server.starttls()
        server.login(sender_address, sender_password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        return f"internal server error: {e}"