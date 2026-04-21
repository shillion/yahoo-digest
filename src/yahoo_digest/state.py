import json
from datetime import date, datetime
from pathlib import Path

STATE_DIR = Path.home() / ".yahoo-digest"
STATE_FILE = STATE_DIR / "state.json"


def ran_today() -> bool:
    if not STATE_FILE.exists():
        return False
    data = json.loads(STATE_FILE.read_text())
    last_run = data.get("last_run")
    if not last_run:
        return False
    return datetime.fromisoformat(last_run).date() == date.today()


def save_run() -> None:
    STATE_DIR.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps({"last_run": datetime.now().isoformat()}))
