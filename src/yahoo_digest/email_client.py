import time
from dataclasses import dataclass
from datetime import datetime

from imap_tools import AND, MailBox


@dataclass
class Email:
    uid: str
    subject: str
    from_: str
    date: datetime
    body: str


def fetch_recent_emails(host: str, user: str, password: str, since: datetime) -> list[Email]:
    last_err = None
    for attempt in range(3):
        try:
            emails = []
            with MailBox(host).login(user, password) as mailbox:
                for msg in mailbox.fetch(AND(date_gte=since.date())):
                    if msg.date and msg.date.replace(tzinfo=None) >= since:
                        emails.append(
                            Email(
                                uid=msg.uid,
                                subject=msg.subject,
                                from_=msg.from_,
                                date=msg.date,
                                body=msg.text or msg.html or "",
                            )
                        )
            return emails
        except Exception as e:
            last_err = e
            if attempt < 2:
                time.sleep(10)
    raise RuntimeError(f"IMAP fetch failed after 3 attempts: {last_err}") from last_err
