from __future__ import annotations

import json
import sqlite3
from pathlib import Path


def _sqlite_path(database_url: str) -> str:
    if database_url == "sqlite:///:memory:":
        return ":memory:"
    prefix = "sqlite:///"
    if not database_url.startswith(prefix):
        raise ValueError("Only sqlite:/// DATABASE_URL is supported by this sample app")
    raw_path = database_url.removeprefix(prefix)
    if raw_path not in {":memory:", ""}:
        Path(raw_path).parent.mkdir(parents=True, exist_ok=True)
    return raw_path or "messenger_events.db"


def connect(database_url: str) -> sqlite3.Connection:
    conn = sqlite3.connect(_sqlite_path(database_url))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(database_url: str) -> None:
    with connect(database_url) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messenger_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id TEXT NOT NULL,
                recipient_id TEXT,
                message_id TEXT,
                incoming_text TEXT,
                reply_text TEXT,
                status TEXT NOT NULL,
                raw_event_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def save_event(
    database_url: str,
    *,
    sender_id: str,
    recipient_id: str | None,
    message_id: str | None,
    incoming_text: str | None,
    reply_text: str | None,
    status: str,
    raw_event: dict,
) -> None:
    with connect(database_url) as conn:
        conn.execute(
            """
            INSERT INTO messenger_events
                (sender_id, recipient_id, message_id, incoming_text, reply_text, status, raw_event_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                sender_id,
                recipient_id,
                message_id,
                incoming_text,
                reply_text,
                status,
                json.dumps(raw_event, ensure_ascii=False, sort_keys=True),
            ),
        )
        conn.commit()
