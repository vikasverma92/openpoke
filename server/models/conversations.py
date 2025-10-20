from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ConversationCreatePayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="user_id")
    voice_agent_id: str = Field(alias="voice_agent_id")
    voice_execution_id: str = Field(alias="voice_execution_id")
    payload: str = Field(alias="payload")
