"""Version 1 API router — aggregates all endpoint routers."""

from fastapi import APIRouter

from app.api.v1.analytics import router as analytics_router
from app.api.v1.contact import router as contact_router
from app.api.v1.feedback import router as feedback_router
from app.api.v1.health import router as health_router

router = APIRouter()

router.include_router(health_router)
router.include_router(contact_router)
router.include_router(analytics_router)
router.include_router(feedback_router)
