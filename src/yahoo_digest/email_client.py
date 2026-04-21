from dataclasses import dataclass
from datetime import date

from imap_tools import AND, MailBox


@dataclass
class Email:
    uid: str
    subject: str
    from_: str
    date: date
    body: str


def fetch_recent_emails(host: str, user: str, password: str, since: date) -> list[Email]:
    emails = []
    with MailBox(host).login(user, password) as mailbox:
        for msg in mailbox.fetch(AND(date_gte=since)):
            emails.append(
                Email(
                    uid=msg.uid,
                    subject=msg.subject,
                    from_=msg.from_,
                    date=msg.date.date(),
                    body=msg.text or msg.html or "",
                )
            )
    return emails
