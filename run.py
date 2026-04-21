import os
from datetime import date, timedelta

from dotenv import load_dotenv

load_dotenv()

from src.yahoo_digest.classifier import classify_emails
from src.yahoo_digest.digest import build_digest
from src.yahoo_digest.email_client import fetch_recent_emails
from src.yahoo_digest.sender import send_digest
from src.yahoo_digest.state import ran_today, save_run


def main() -> None:
    if ran_today():
        print("Already ran today. Exiting.")
        return

    emails = fetch_recent_emails(
        host="imap.mail.yahoo.com",
        user=os.environ["YAHOO_USER"],
        password=os.environ["YAHOO_APP_PASSWORD"],
        since=date.today() - timedelta(days=1),
    )
    print(f"Fetched {len(emails)} emails.")

    classifications = classify_emails(emails)
    digest = build_digest(emails, classifications)
    print(digest)

    send_digest(
        smtp_user=os.environ["GMAIL_USER"],
        smtp_password=os.environ["GMAIL_APP_PASSWORD"],
        to_address=os.environ["GMAIL_USER"],
        body=digest,
    )
    print("Digest sent.")
    save_run()


if __name__ == "__main__":
    main()
