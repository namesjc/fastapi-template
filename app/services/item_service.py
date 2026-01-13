"""Item service."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.item_repository import item_repository
from app.schemas import Item, ItemCreate, ItemUpdate


class ItemService:
    """Business logic for items."""

    def __init__(self) -> None:
        """Initialize item service."""
        self.repository = item_repository

    async def create_item(
        self,
        db: AsyncSession,
        item_in: ItemCreate,
        owner_id: int,
    ) -> Item:
        """Create new item for user."""
        item_dict = item_in.model_dump()
        item_dict["owner_id"] = owner_id
        item = await self.repository.create(db, ItemCreate(**item_dict))
        return Item.model_validate(item)

    async def get_item(
        self,
        db: AsyncSession,
        item_id: int,
    ) -> Item | None:
        """Get item by ID."""
        item = await self.repository.get(db, item_id)
        if not item:
            return None
        return Item.model_validate(item)

    async def get_user_items(
        self,
        db: AsyncSession,
        owner_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Item]:
        """Get all items for a user."""
        items = await self.repository.get_by_owner(db, owner_id)
        return [Item.model_validate(item) for item in items[skip : skip + limit]]

    async def update_item(
        self,
        db: AsyncSession,
        item_id: int,
        item_in: ItemUpdate,
    ) -> Item | None:
        """Update item."""
        item = await self.repository.get(db, item_id)
        if not item:
            return None

        updated_item = await self.repository.update(db, item, item_in)
        return Item.model_validate(updated_item)

    async def delete_item(
        self,
        db: AsyncSession,
        item_id: int,
    ) -> bool:
        """Delete item."""
        return await self.repository.delete(db, item_id)


item_service = ItemService()
