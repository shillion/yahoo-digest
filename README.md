# yahoo-digest

Fetches your Yahoo inbox, uses Claude to classify emails, and sends a daily digest of anything important to your Gmail.

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
cp .env.example .env
# fill in .env with your Yahoo/Gmail app passwords and Anthropic API key
uv run python run.py
```

See `.env.example` for required variables.
