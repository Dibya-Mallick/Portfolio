"""Health check endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict:
    """Liveness probe — always returns healthy if the process is up."""
    return {"status": "healthy"}


@router.get("/ready")
async def ready(db: AsyncSession = Depends(get_db)) -> dict:
    """Readiness probe — checks database connectivity."""
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "not ready", "database": "unavailable"},
        ) from exc
