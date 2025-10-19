from __future__ import annotations

import sqlite3
import threading
from pathlib import Path
from typing import Any, Dict, Optional

from ...logging_config import logger
from .models import ConversationRecord
from .utils import to_storage_timestamp, utc_now


class ConversationStore:
    """Low-level persistence for triggers backed by SQLite."""

    def __init__(self, db_path: Path):
        self._db_path = db_path
        self._lock = threading.Lock()
        self._ensure_directory()
        self._ensure_schema()

    def _ensure_directory(self) -> None:
        try:
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning(
                "trigger directory creation failed",
                extra={"error": str(exc)},
            )

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, timeout=30, isolation_level=None)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_schema(self) -> None:
        schema_sql = """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            voice_agent_id TEXT NOT NULL,
            voice_execution_id TEXT NOT NULL,
            payload TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'queued',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """
        index_sql = """
        CREATE INDEX IF NOT EXISTS idx_conversations_voice_agent_id_voice_execution_id
        ON conversations (voice_agent_id, voice_execution_id);
        """
        with self._lock, self._connect() as conn:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute(schema_sql)
            conn.execute(index_sql)

    def insert(self, payload: Dict[str, Any]) -> int:
        with self._lock, self._connect() as conn:
            columns = ", ".join(payload.keys())
            placeholders = ", ".join([":" + key for key in payload.keys()])
            sql = f"INSERT INTO conversations ({columns}) VALUES ({placeholders})"
            conn.execute(sql, payload)
            conversation_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            return int(conversation_id)

    def fetch_one(self, conversation_id: int) -> Optional[ConversationRecord]:
        with self._lock, self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM conversations WHERE id = ?",
                (conversation_id,),
            ).fetchone()
        return self._row_to_record(row) if row else None

    def update(self, voice_agent_id: str, voice_execution_id: str, fields: Dict[str, Any]) -> bool:
        if not fields:
            return False
        assignments = ", ".join(f"{key} = :{key}" for key in fields.keys())
        sql = (
            f"UPDATE conversations SET {assignments}, updated_at = :updated_at"
            " WHERE voice_agent_id = :voice_agent_id AND voice_execution_id = :voice_execution_id"
        )
        payload = {
            **fields,
            "updated_at": to_storage_timestamp(utc_now()),
            "voice_agent_id": voice_agent_id,
            "voice_execution_id": voice_execution_id,
        }
        with self._lock, self._connect() as conn:
            cursor = conn.execute(sql, payload)
            return cursor.rowcount > 0

    def clear_all(self) -> None:
        with self._lock, self._connect() as conn:
            conn.execute("DELETE FROM conversations")

    def _row_to_record(self, row: sqlite3.Row) -> ConversationRecord:
        data = dict(row)
        return ConversationRecord.model_validate(data)


__all__ = ["ConversationStore"]
