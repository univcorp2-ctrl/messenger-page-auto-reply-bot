#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import json

from app.messenger import send_messenger_text
from app.settings import get_settings


async def _run() -> None:
    parser = argparse.ArgumentParser(description="Send a real Messenger text via Send API")
    parser.add_argument("--recipient-id", required=True, help="Page-scoped user ID from a webhook event")
    parser.add_argument("--text", required=True)
    args = parser.parse_args()

    settings = get_settings()
    result = await send_messenger_text(
        page_id=settings.page_id,
        page_access_token=settings.page_access_token,
        recipient_id=args.recipient_id,
        text=args.text,
        graph_api_version=settings.graph_api_version,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
