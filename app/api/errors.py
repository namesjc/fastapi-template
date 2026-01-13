"""Custom exception handlers."""

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.logging import get_logger

logger = get_logger(__name__)


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle validation errors.

    Args:
        request: Request object
        exc: Validation exception

    Returns:
        JSON error response
    """
    logger.warning(
        "Validation error",
        extra={
            "url": str(request.url),
            "errors": exc.errors(),
        },
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body,
        },
    )


async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """
    Handle database integrity errors.

    Args:
        request: Request object
        exc: Integrity error

    Returns:
        JSON error response
    """
    logger.error(
        "Database integrity error",
        extra={
            "url": str(request.url),
            "error": str(exc),
        },
    )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Database constraint violation",
        },
    )


async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """
    Handle general database errors.

    Args:
        request: Request object
        exc: SQLAlchemy exception

    Returns:
        JSON error response
    """
    logger.error(
        "Database error",
        extra={
            "url": str(request.url),
            "error": str(exc),
        },
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Database error occurred",
        },
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle general exceptions.

    Args:
        request: Request object
        exc: Exception

    Returns:
        JSON error response
    """
    logger.error(
        "Unhandled exception",
        extra={
            "url": str(request.url),
            "error": str(exc),
            "type": type(exc).__name__,
        },
        exc_info=True,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
        },
    )
