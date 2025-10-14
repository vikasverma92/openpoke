from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from ..config import Settings, get_settings
from ..models import GmailConnectPayload, GmailDisconnectPayload, GmailStatusPayload
from ..services import disconnect_account, fetch_status, initiate_connect

router = APIRouter(prefix="/gmail", tags=["gmail"])


@router.post("/connect")
# Initiate Gmail OAuth connection flow through Composio
async def gmail_connect(payload: GmailConnectPayload, settings: Settings = Depends(get_settings)) -> JSONResponse:
    return initiate_connect(payload, settings)


@router.post("/status")
# Check the current Gmail connection status and user information
async def gmail_status(payload: GmailStatusPayload) -> JSONResponse:
    return fetch_status(payload)


@router.post("/disconnect")
# Disconnect Gmail account and clear cached profile data
async def gmail_disconnect(payload: GmailDisconnectPayload) -> JSONResponse:
    return disconnect_account(payload)

@router.post("/composio/callback")
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

