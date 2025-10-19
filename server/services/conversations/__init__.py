from __future__ import annotations

from pathlib import Path

from .models import ConversationRecord
from .service import ConversationService
from .store import ConversationStore


_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
_default_db_path = _DATA_DIR / "conversations.db"
_conversation_store = ConversationStore(_default_db_path)
_conversation_service = ConversationService(_conversation_store)


def get_conversation_service() -> ConversationService:
    return _conversation_service


__all__ = [
    "ConversationRecord",
    "ConversationService",
    "get_conversation_service",
]
