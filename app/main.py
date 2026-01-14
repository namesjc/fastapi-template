"""Main FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.api import api_router
from app.api.errors import (
    database_exception_handler,
    general_exception_handler,
    integrity_error_handler,
    validation_exception_handler,
)
from app.core.cache import cache
from app.core.config import settings
from app.core.database import close_db, init_db
from app.core.logging import setup_logging
from app.middleware import LoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Args:
        app: FastAPI application
    """
    # Startup
    setup_logging()
    await init_db()
    await cache.connect()

    yield

    # Shutdown
    await cache.disconnect()
    await close_db()


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Production-ready FastAPI application with best practices",
    version="0.1.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# Add CORS middleware
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

# Add custom middleware
app.add_middleware(LoggingMiddleware)

# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root() -> dict[str, str | None]:
    """Root endpoint."""
    return {
        "message": "Welcome to FastAPI Production API",
        "version": "0.1.0",
        "docs": f"{settings.API_V1_PREFIX}/docs" if settings.DEBUG else None,
    }
