from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ConversationRecord(BaseModel):
    """Serialized trigger representation returned to callers."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: str
    voice_agent_id: str
    voice_execution_id: str
    payload: str
    status: str
    created_at: str
    updated_at: str


__all__ = ["ConversationRecord"]
