"""Authentication endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import create_access_token
from app.schemas import Token, User, UserCreate
from app.services.user_service import user_service

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_db)]
OAuth2FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: SessionDep,
) -> User:
    """Register a new user."""
    try:
        user = await user_service.create_user(db, user_in)
        await db.commit()
    except ValueError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    else:
        return user


@router.post("/login")
async def login(
    db: SessionDep,
    form_data: OAuth2FormDep,
) -> Token:
    """Login and get access token."""
    user = await user_service.authenticate(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    access_token = create_access_token(subject=user.id)
    return Token(access_token=access_token)
