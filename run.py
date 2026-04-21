import os

from dotenv import load_dotenv

from src.yahoo_digest.classifier import classify_emails
from src.yahoo_digest.digest import build_digest
from src.yahoo_digest.email_client import fetch_recent_emails
from src.yahoo_digest.sender import send_digest
from src.yahoo_digest.state import last_run, save_run

load_dotenv()


def main() -> None:
    since = last_run()
    save_run()

    emails = fetch_recent_emails(
        host="imap.mail.yahoo.com",
        user=os.environ["YAHOO_USER"],
        password=os.environ["YAHOO_APP_PASSWORD"],
        since=since,
    )
    print(f"Fetched {len(emails)} emails since {since}.")

    if not emails:
        print("Nothing new.")
        return

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


if __name__ == "__main__":
    main()
