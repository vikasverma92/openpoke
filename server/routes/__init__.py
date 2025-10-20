from __future__ import annotations

from fastapi import APIRouter

from .chat import router as chat_router
from .gmail import router as gmail_router
from .meta import router as meta_router
from .composio import router as composio_router
from .conversations import router as conversations_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(meta_router)
api_router.include_router(chat_router)
api_router.include_router(gmail_router)
api_router.include_router(composio_router)
api_router.include_router(conversations_router)

__all__ = ["api_router"]
