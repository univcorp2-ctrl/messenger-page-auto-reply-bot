from __future__ import annotations

import httpx


class MessengerConfigError(RuntimeError):
    """Raised when required Messenger configuration is missing."""


async def send_messenger_text(
    *,
    page_id: str | None,
    page_access_token: str | None,
    recipient_id: str,
    text: str,
    graph_api_version: str,
) -> dict:
    """Send a text message via the official Meta Send API.

    The recipient_id must be the Page-scoped ID obtained from a Messenger webhook.
    This sample uses messaging_type=RESPONSE and is intended for standard replies
    inside Meta's allowed messaging window.
    """
    if not page_id:
        raise MessengerConfigError("PAGE_ID is not configured")
    if not page_access_token:
        raise MessengerConfigError("PAGE_ACCESS_TOKEN is not configured")

    url = f"https://graph.facebook.com/{graph_api_version}/{page_id}/messages"
    payload = {
        "messaging_type": "RESPONSE",
        "recipient": {"id": recipient_id},
        "message": {"text": text[:2000]},
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(url, params={"access_token": page_access_token}, json=payload)
        response.raise_for_status()
        return response.json()
