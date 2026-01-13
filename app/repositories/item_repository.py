"""Item repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Item
from app.repositories.base_repository import BaseRepository
from app.schemas import ItemCreate, ItemUpdate


class ItemRepository(BaseRepository[Item, ItemCreate, ItemUpdate]):
    """Item-specific repository."""

    async def get_by_owner(self, db: AsyncSession, owner_id: int) -> list[Item]:
        """Get all items for a specific owner."""
        result = await db.execute(select(Item).where(Item.owner_id == owner_id))
        return result.scalars().all()


item_repository = ItemRepository(Item)
