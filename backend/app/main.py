"""Portfolio API — FastAPI application entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan handler for startup/shutdown tasks."""
    logger.info("Starting Portfolio API (env=%s)", settings.APP_ENV)
    # TODO: Add startup tasks (e.g. warm caches, verify DB connection)
    yield
    # TODO: Add shutdown tasks (e.g. close connection pools)
    logger.info("Shutting down Portfolio API")


app = FastAPI(
    title="Portfolio API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount versioned router
app.include_router(v1_router, prefix="/api/v1")


@app.get("/")
async def root() -> dict:
    """Root endpoint — basic API info."""
    return {"message": "Portfolio API", "version": "1.0.0"}
