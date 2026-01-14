"""User endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_active_user, get_current_superuser
from app.core.database import get_db
from app.models import User as UserModel
from app.schemas import MessageResponse, User, UserUpdate
from app.services.user_service import user_service

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_db)]
SuperUserDep = Annotated[UserModel, Depends(get_current_superuser)]
ActiveUserDep = Annotated[UserModel, Depends(get_current_active_user)]


@router.get("/me")
async def read_current_user(
    current_user: ActiveUserDep,
) -> User:
    """Get current user."""
    return current_user


@router.put("/me")
async def update_current_user(
    user_update: UserUpdate,
    current_user: ActiveUserDep,
    db: SessionDep,
) -> User:
    """Update current user."""
    user = await user_service.update_user(db, current_user.id, user_update)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    await db.commit()
    return user


@router.get("")
async def read_users(
    _: SuperUserDep,
    db: SessionDep,
    skip: int = 0,
    limit: int = 100,
) -> list[User]:
    """Get all users (admin only)."""
    users = await user_service.repository.get_multi(db, skip=skip, limit=limit)
    return [User.model_validate(user) for user in users]


@router.get("/{user_id}")
async def read_user(
    user_id: int,
    _: SuperUserDep,
    db: SessionDep,
) -> User:
    """Get user by ID (admin only)."""
    user = await user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: SuperUserDep,
    db: SessionDep,
) -> MessageResponse:
    """Delete user (admin only)."""
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself",
        )

    deleted = await user_service.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    await db.commit()
    return MessageResponse(message="User deleted successfully")
