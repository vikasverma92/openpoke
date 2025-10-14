from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/composio", tags=["composio"])

@router.post("/callback")
# Disconnect Gmail account and clear cached profile data
async def composio_callback(payload: Request) -> JSONResponse:
    try:
        payload = await payload.json()
        
        # Log or inspect the payload for debugging
        print("Received callback from Composio:", payload)

        # Example: verify event type
        event_type = payload.get("event_type")
        data = payload.get("data", {})

        # Handle specific callback types
        if event_type == "ACTION_COMPLETED":
            # handle_action_completed(data)
            print("Action completed:", data)
        elif event_type == "ERROR":
            # handle_action_error(data)
            print("Error:", data)
        else:
            print("Unknown event type:", event_type)

        return JSONResponse(content={"status": "ok"}, status_code=200)

    except Exception as e:
        print("Error in callback handler:", e)
        raise HTTPException(status_code=400, detail="Invalid payload")
