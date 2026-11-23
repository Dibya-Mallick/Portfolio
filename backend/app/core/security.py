"""Security utilities for API key and token verification."""

from fastapi import Header, HTTPException, status

from app.core.config import settings


async def verify_api_key(x_api_key: str = Header(...)) -> str:
    """Verify the API key provided in the request header.

    TODO: Implement proper API key verification against stored keys.
    This is a placeholder for future admin route protection.
    """
    if not settings.SECRET_KEY or x_api_key != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
    return x_api_key
