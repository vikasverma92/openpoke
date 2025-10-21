
from typing import TYPE_CHECKING, Any, Dict, Optional

from fastapi.responses import JSONResponse
from fastapi import status

from server.logging_config import logger
from server.utils.responses import error_response

if TYPE_CHECKING:  # pragma: no cover - typing only
    from ...agents.interaction_agent.runtime import InteractionAgentRuntime

def _resolve_interaction_runtime() -> "InteractionAgentRuntime":
    from ...agents.interaction_agent.runtime import InteractionAgentRuntime

    return InteractionAgentRuntime()

async def dispatch_summary(summary: str) -> None:
    runtime = _resolve_interaction_runtime()
    try:
        contextualized = f"Important email watcher notification:\n{summary}"
        await runtime.handle_agent_message(contextualized)
    except Exception as exc:  # pragma: no cover - defensive
        logger.error(
            "Failed to dispatch important email summary",
            extra={"error": str(exc)},
        )

async def handle_callback(payload: Dict[str, Any]) -> JSONResponse:
    call_status = payload.get("status")
    agent_id = payload.get("agent_id")
    transcript = payload.get("transcript") or "Call completed but transcript is not available"
    recording_url = payload.get("telephony_data", {}).get("recording_url")

    print("bolna callback", call_status, agent_id, transcript, recording_url)
    
    try:
        if call_status == "completed":
            await dispatch_summary(transcript)
        
        return JSONResponse({
            "ok": True,
        })
    except Exception as exc:
        return error_response(
            "Failed to initiate Gmail connect",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )
