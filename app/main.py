from __future__ import annotations

import hashlib
import hmac
import json
from collections.abc import Iterable
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse

from app.db import init_db, save_event
from app.messenger import MessengerConfigError, send_messenger_text
from app.reply_engine import build_reply
from app.settings import get_settings

app = FastAPI(title="Messenger Page Auto Reply Bot", version="0.1.0")


@app.on_event("startup")
def startup() -> None:
    settings = get_settings()
    init_db(settings.database_url)


@app.get("/health")
def health() -> dict[str, str | bool]:
    return {"ok": True, "service": "messenger-page-auto-reply-bot"}


@app.get("/webhook", response_class=PlainTextResponse)
def verify_webhook(
    hub_mode: str | None = Query(default=None, alias="hub.mode"),
    hub_verify_token: str | None = Query(default=None, alias="hub.verify_token"),
    hub_challenge: str | None = Query(default=None, alias="hub.challenge"),
) -> str:
    settings = get_settings()
    if hub_mode == "subscribe" and hub_verify_token == settings.verify_token and hub_challenge:
        return hub_challenge
    raise HTTPException(status_code=403, detail="Webhook verification failed")


@app.post("/webhook")
async def receive_webhook(request: Request) -> dict[str, Any]:
    settings = get_settings()
    raw_body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")

    if not _signature_is_valid(raw_body, signature, settings.app_secret):
        raise HTTPException(status_code=403, detail="Invalid X-Hub-Signature-256")

    try:
        payload = json.loads(raw_body.decode("utf-8") or "{}")
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="Invalid JSON") from exc

    results: list[dict[str, Any]] = []
    for event in _iter_messaging_events(payload):
        message = event.get("message") or {}
        sender_id = (event.get("sender") or {}).get("id")
        recipient_id = (event.get("recipient") or {}).get("id")
        text = message.get("text")
        message_id = message.get("mid")

        if not sender_id or not text or message.get("is_echo"):
            continue

        reply_text = build_reply(text) if settings.auto_reply_enabled else None
        status = "received"
        api_response: dict[str, Any] | None = None
        error: str | None = None

        if reply_text and settings.send_real_messages:
            try:
                api_response = await send_messenger_text(
                    page_id=settings.page_id,
                    page_access_token=settings.page_access_token,
                    recipient_id=sender_id,
                    text=reply_text,
                    graph_api_version=settings.graph_api_version,
                )
                status = "sent"
            except MessengerConfigError as exc:
                status = "skipped_missing_config"
                error = str(exc)
            except httpx.HTTPStatusError as exc:
                status = "send_api_error"
                error = f"{exc.response.status_code}: {exc.response.text}"
        elif reply_text:
            status = "dry_run"

        save_event(
            settings.database_url,
            sender_id=sender_id,
            recipient_id=recipient_id,
            message_id=message_id,
            incoming_text=text,
            reply_text=reply_text,
            status=status,
            raw_event=event,
        )

        results.append(
            {
                "sender_id": sender_id,
                "message_id": message_id,
                "status": status,
                "reply_text": reply_text,
                "api_response": api_response,
                "error": error,
            }
        )

    return {"ok": True, "processed": len(results), "results": results}


def _iter_messaging_events(payload: dict[str, Any]) -> Iterable[dict[str, Any]]:
    for entry in payload.get("entry", []):
        for event in entry.get("messaging", []):
            yield event


def _signature_is_valid(raw_body: bytes, signature: str | None, app_secret: str | None) -> bool:
    if not app_secret:
        return True
    if not signature or not signature.startswith("sha256="):
        return False
    expected = "sha256=" + hmac.new(app_secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
