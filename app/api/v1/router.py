"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, health, items, users

api_v1_router = APIRouter()

# Include routers
api_v1_router.include_router(health.router, tags=["health"])
api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(users.router, prefix="/users", tags=["users"])
api_v1_router.include_router(items.router, prefix="/items", tags=["items"])
