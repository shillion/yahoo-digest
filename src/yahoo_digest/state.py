import json
from datetime import datetime, timedelta
from pathlib import Path

STATE_DIR = Path.home() / ".yahoo-digest"
STATE_FILE = STATE_DIR / "state.json"


def last_run() -> datetime:
    if STATE_FILE.exists():
        data = json.loads(STATE_FILE.read_text())
        ts = data.get("last_run")
        if ts:
            return datetime.fromisoformat(ts)
    return datetime.now() - timedelta(days=1)


def save_run() -> None:
    STATE_DIR.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps({"last_run": datetime.now().isoformat()}))
