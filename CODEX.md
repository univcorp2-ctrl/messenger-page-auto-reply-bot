# CODEX

## Project intent

Build and maintain a compliant Facebook Messenger Page auto-reply bot using official Meta Messenger Platform surfaces only.

## Safety constraints

Do not add code that:

- Reads a personal Messenger inbox through browser automation.
- Uses private Meta GraphQL endpoints or reverse-engineered APIs.
- Stores or reuses Facebook cookies.
- Circumvents rate limits, CAPTCHA, app review, or messaging policies.
- Exfiltrates message content to unapproved third-party services.

## Development commands

```bash
pip install -e '.[dev]'
ruff check .
pytest -q
uvicorn app.main:app --reload --port 8000
```

## Deployment notes

Production requires `VERIFY_TOKEN`, `PAGE_ACCESS_TOKEN`, `PAGE_ID`, and an HTTPS endpoint. Prefer setting `APP_SECRET` and enabling signature verification.
