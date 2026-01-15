"""Health check endpoints."""

from datetime import UTC, datetime

from fastapi import APIRouter

from app import __version__
from app.schemas import HealthCheck

router = APIRouter()


@router.get("/")
async def health_check() -> HealthCheck:
    """
    Health check endpoint.

    Returns:
        HealthCheck: Health status

    """
    return HealthCheck(
        status="healthy",
        version=__version__,
        timestamp=datetime.now(tz=UTC),
    )
