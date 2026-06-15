#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time

import httpx


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a local Messenger webhook sample")
    parser.add_argument("--url", default="http://localhost:8000/webhook")
    parser.add_argument("--sender-id", default="LOCAL_TEST_USER")
    parser.add_argument("--page-id", default="LOCAL_TEST_PAGE")
    parser.add_argument("--text", default="料金を教えてください")
    args = parser.parse_args()

    payload = {
        "object": "page",
        "entry": [
            {
                "id": args.page_id,
                "time": int(time.time()),
                "messaging": [
                    {
                        "sender": {"id": args.sender_id},
                        "recipient": {"id": args.page_id},
                        "timestamp": int(time.time() * 1000),
                        "message": {"mid": "local-mid", "text": args.text},
                    }
                ],
            }
        ],
    }

    response = httpx.post(args.url, json=payload, timeout=10.0)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
