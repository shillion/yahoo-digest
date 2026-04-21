from datetime import date

from .email_client import Email


def build_digest(emails: list[Email], classifications: list[dict]) -> str:
    important = [c for c in classifications if c["category"] in ("important", "action-required")]

    if not important:
        return f"Yahoo Digest — {date.today()}\n\nNothing important today."

    email_map = {e.uid: e for e in emails}
    lines = [f"Yahoo Digest — {date.today()}\n", f"{len(important)} item(s) need your attention:\n"]

    for c in important:
        email = email_map.get(c["uid"])
        if not email:
            continue
        tag = "ACTION REQUIRED" if c["category"] == "action-required" else "IMPORTANT"
        lines.append(f"[{tag}] {email.subject}")
        lines.append(f"  From: {email.from_}")
        lines.append(f"  {c['summary']}")
        if c["reason"]:
            lines.append(f"  Why flagged: {c['reason']}")
        lines.append("")

    return "\n".join(lines)
