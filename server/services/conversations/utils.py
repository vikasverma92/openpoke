from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from ...logging_config import logger


UTC = timezone.utc
DEFAULT_STATUS = "queued"
VALID_STATUSES = {"queued", "initiated", "ringing", "in-progress", "call-disconnected", "completed"}


def utc_now() -> datetime:
    """Return the current time in UTC."""

    return datetime.now(UTC)


def to_storage_timestamp(moment: datetime) -> str:
    """Normalize timestamps before writing to SQLite."""

    return moment.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def normalize_status(status: Optional[str]) -> str:
    """Clamp trigger status to the known set."""

    if not status:
        return DEFAULT_STATUS
    normalized = status.lower()
    if normalized not in VALID_STATUSES:
        logger.warning(
            "invalid status supplied; defaulting to active",
            extra={"status": status},
        )
        return DEFAULT_STATUS
    return normalized


__all__ = [
    "UTC",
    "DEFAULT_STATUS",
    "VALID_STATUSES",
    "normalize_status",
    "to_storage_timestamp",
    "utc_now",
]
