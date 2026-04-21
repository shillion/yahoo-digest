import smtplib
from datetime import date
from email.mime.text import MIMEText


def send_digest(smtp_user: str, smtp_password: str, to_address: str, body: str) -> None:
    msg = MIMEText(body)
    msg["Subject"] = f"Yahoo Digest — {date.today()}"
    msg["From"] = smtp_user
    msg["To"] = to_address

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_address, msg.as_string())
