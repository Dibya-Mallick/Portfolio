"""Simple in-memory rate limiter."""

import time
from collections import defaultdict

from fastapi import HTTPException, Request, status


class RateLimiter:
    """Sliding-window in-memory rate limiter.

    Not suitable for multi-process deployments — swap to Redis for production.
    """

    def __init__(self, max_requests: int = 5, window_seconds: int = 60) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: dict[str, list[float]] = defaultdict(list)

    def _client_key(self, request: Request) -> str:
        """Derive a key from the client's IP address."""
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    async def check(self, request: Request) -> None:
        """Raise 429 if the client has exceeded the rate limit."""
        key = self._client_key(request)
        now = time.time()
        cutoff = now - self.window_seconds

        # Prune old entries
        self._hits[key] = [t for t in self._hits[key] if t > cutoff]

        if len(self._hits[key]) >= self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later.",
            )

        self._hits[key].append(now)


# Shared instance — 5 requests per 60 seconds for contact form
contact_rate_limiter = RateLimiter(max_requests=5, window_seconds=60)
