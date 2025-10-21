from __future__ import annotations
import os
from typing import Any, Dict

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from server.services.conversations.client import handle_callback
from server.utils.responses import error_response

from ..config import Settings, get_settings
from ..models import ConversationCreatePayload
from ..services import get_conversation_service

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("/create")
# create new conversation entry
async def create_conversation(payload: ConversationCreatePayload) -> JSONResponse:
    user_id = payload.user_id or f"web-{os.getpid()}"

    conversation_service = get_conversation_service()
    conversation = conversation_service.create_conversation(
      user_id=user_id,
      voice_agent_id=payload.voice_agent_id,
      voice_execution_id=payload.voice_execution_id,
      payload=payload.payload,
    )
    return JSONResponse(
        {
            "ok": True,
            "conversation": conversation.model_dump(),
        }
    )


@router.get("/get/{conversation_id}")
# Get conversation by id
async def get_conversation(conversation_id: int) -> JSONResponse:
    conversation_service = get_conversation_service()
    conversation = conversation_service.get_conversation(conversation_id=conversation_id)
    return JSONResponse(
        {
            "ok": True,
            "conversation": conversation.model_dump(),
        }
    )


@router.post("/callback")
# callback endpoint for voice agents
async def conversation_callback(payload: Dict[str, Any]) -> JSONResponse:
    return await handle_callback(payload)

