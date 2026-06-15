from fastapi.testclient import TestClient

from app.main import app
from app.settings import get_settings


def test_webhook_verification_success() -> None:
    settings = get_settings()
    with TestClient(app) as client:
        response = client.get(
            "/webhook",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": settings.verify_token,
                "hub.challenge": "challenge-ok",
            },
        )
    assert response.status_code == 200
    assert response.text == "challenge-ok"


def test_webhook_verification_failure() -> None:
    with TestClient(app) as client:
        response = client.get(
            "/webhook",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": "wrong",
                "hub.challenge": "challenge-ng",
            },
        )
    assert response.status_code == 403


def test_receive_webhook_dry_run() -> None:
    settings = get_settings()
    settings.send_real_messages = False
    payload = {
        "object": "page",
        "entry": [
            {
                "id": "PAGE_ID",
                "messaging": [
                    {
                        "sender": {"id": "USER_ID"},
                        "recipient": {"id": "PAGE_ID"},
                        "timestamp": 1234567890,
                        "message": {"mid": "m_1", "text": "料金を教えてください"},
                    }
                ],
            }
        ],
    }

    with TestClient(app) as client:
        response = client.post("/webhook", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["processed"] == 1
    assert body["results"][0]["status"] == "dry_run"
    assert "料金" in body["results"][0]["reply_text"]
