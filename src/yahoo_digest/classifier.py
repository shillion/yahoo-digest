import json

from anthropic import Anthropic

from .email_client import Email

SYSTEM_PROMPT = """You are an email classifier. Given a list of emails, classify each one.
Return a JSON array with one object per email, in the same order.
Each object must have:
  - "uid": the email uid (string)
  - "category": one of "spam", "newsletter", "important", "action-required"
  - "reason": one sentence explaining why (only for important/action-required, else null)
  - "summary": one sentence summary (only for important/action-required, else null)

Classify as "important" if it's from a real person or contains genuinely useful info
(e.g. a bill, a shipping notice, a friend).
Classify as "action-required" if something needs a response, payment, or decision.
Be aggressive about classifying marketing, political emails, solicitations,
and newsletters as "newsletter" and junk as "spam".
Ignore emails sent to a broad audience, including newsletters, mass event invites, and
general notices — classify these as "newsletter".
Return only the JSON array — no explanation, no markdown."""


BATCH_SIZE = 10


def _classify_batch(emails: list[Email]) -> list[dict]:
    client = Anthropic()
    email_list = [
        {"uid": e.uid, "from": e.from_, "subject": e.subject, "body": e.body[:500]}
        for e in emails
    ]
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": json.dumps(email_list)}],
    )
    text = response.content[0].text.strip()
    if not text:
        raise ValueError(f"Empty response from Claude (stop_reason={response.stop_reason})")
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    return json.loads(text)


def classify_emails(emails: list[Email]) -> list[dict]:
    if not emails:
        return []

    results = []
    for i in range(0, len(emails), BATCH_SIZE):
        batch = emails[i : i + BATCH_SIZE]
        results.extend(_classify_batch(batch))
    return results
