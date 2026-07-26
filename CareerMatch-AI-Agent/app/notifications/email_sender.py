import smtplib
from email.message import EmailMessage


def send_email(subject: str, body: str, to_address: str, from_address: str, smtp_server: str = "localhost") -> bool:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = from_address
    message["To"] = to_address
    message.set_content(body)

    try:
        with smtplib.SMTP(smtp_server) as server:
            server.send_message(message)
        return True
    except Exception as exc:
        print(f"Warning: failed to send email via {smtp_server}: {exc}")
        return False
