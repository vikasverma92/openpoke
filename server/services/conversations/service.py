from __future__ import annotations

from typing import Any, Dict, Optional

from ...logging_config import logger
from .models import ConversationRecord
from .store import ConversationStore
from .utils import (
    normalize_status,
    to_storage_timestamp,
    utc_now,
)


class ConversationService:
    """High-level trigger management with recurrence awareness."""

    def __init__(self, store: ConversationStore):
        self._store = store

    def create_conversation(
        self,
        *,
        user_id: str,
        voice_agent_id: str,
        voice_execution_id: str,
        payload: str,
        status: Optional[str] = None,
    ) -> ConversationRecord:
        now = utc_now()
        timestamp = to_storage_timestamp(now)
        record: Dict[str, Any] = {
            "user_id": user_id,
            "voice_agent_id": voice_agent_id,
            "voice_execution_id": voice_execution_id,
            "payload": payload,
            "status": normalize_status(status),
            "created_at": timestamp,
            "updated_at": timestamp,
        }
        conversation_id = self._store.insert(record)
        created = self._store.fetch_one(conversation_id)
        if not created:  # pragma: no cover - defensive
            raise RuntimeError("Failed to load trigger after insert")
        return created

    def update_conversation(
        self,
        conversation_id: int,
        *,
        voice_agent_id: str,
        voice_execution_id: str,
        payload: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Optional[ConversationRecord]:
        existing = self._store.fetch_one(conversation_id)
        if existing is None:
            return None

        fields: Dict[str, Any] = {}
        if payload is not None:
            fields["payload"] = payload

        normalized_status = None
        if status is not None:
            normalized_status = normalize_status(status)
            fields["status"] = normalized_status
        else:
            normalized_status = existing.status

        if not fields:
            return existing

        updated = self._store.update(voice_agent_id, voice_execution_id, fields)
        return self._store.fetch_one(conversation_id) if updated else existing

    def get_conversation(self, conversation_id: int) -> Optional[ConversationRecord]:
        return self._store.fetch_one(conversation_id)

    def mark_as_completed(self, voice_agent_id: str, *, voice_execution_id: str) -> None:
        self._store.update(
            voice_agent_id,
            voice_execution_id,
            {
                "status": "completed",
            },
        )

    def clear_all(self) -> None:
        self._store.clear_all()


__all__ = ["ConversationService"]
