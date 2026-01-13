"""Item endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_active_user
from app.core.database import get_db
from app.models import User as UserModel
from app.schemas import Item, ItemCreate, ItemUpdate, MessageResponse
from app.services.item_service import item_service

router = APIRouter()


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_in: ItemCreate,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Item:
    """Create a new item."""
    item = await item_service.create_item(db, item_in, current_user.id)
    await db.commit()
    return item


@router.get("", response_model=list[Item])
async def read_items(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> list[Item]:
    """Get all items for current user."""
    return await item_service.get_user_items(db, current_user.id, skip=skip, limit=limit)


@router.get("/{item_id}", response_model=Item)
async def read_item(
    item_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Item:
    """Get item by ID."""
    item = await item_service.get_item(db, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges",
        )

    return item


@router.put("/{item_id}", response_model=Item)
async def update_item(
    item_id: int,
    item_update: ItemUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Item:
    """Update item."""
    item = await item_service.get_item(db, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges",
        )

    updated_item = await item_service.update_item(db, item_id, item_update)
    await db.commit()
    return updated_item


@router.delete("/{item_id}", response_model=MessageResponse)
async def delete_item(
    item_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """Delete item."""
    item = await item_service.get_item(db, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges",
        )

    await item_service.delete_item(db, item_id)
    await db.commit()

    return MessageResponse(message="Item deleted successfully")
