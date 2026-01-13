"""Tests for item endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_password_hash
from app.models import Item, User


@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    """Create test user."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpass123"),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user: User) -> dict:
    """Get authentication headers."""
    token = create_access_token(subject=test_user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_item(
    client: AsyncClient,
    test_user: User,
    auth_headers: dict,
):
    """Test creating an item."""
    response = await client.post(
        "/api/v1/items",
        headers=auth_headers,
        json={
            "title": "Test Item",
            "description": "Test Description",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Item"
    assert data["description"] == "Test Description"
    assert data["owner_id"] == test_user.id


@pytest.mark.asyncio
async def test_read_items(
    client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession,
):
    """Test reading items."""
    # Create test items
    item1 = Item(title="Item 1", owner_id=test_user.id)
    item2 = Item(title="Item 2", owner_id=test_user.id)
    db_session.add_all([item1, item2])
    await db_session.commit()

    response = await client.get(
        "/api/v1/items",
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_read_item(
    client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession,
):
    """Test reading a specific item."""
    # Create test item
    item = Item(title="Test Item", owner_id=test_user.id)
    db_session.add(item)
    await db_session.commit()
    await db_session.refresh(item)

    response = await client.get(
        f"/api/v1/items/{item.id}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item.id
    assert data["title"] == "Test Item"


@pytest.mark.asyncio
async def test_update_item(
    client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession,
):
    """Test updating an item."""
    # Create test item
    item = Item(title="Test Item", owner_id=test_user.id)
    db_session.add(item)
    await db_session.commit()
    await db_session.refresh(item)

    response = await client.put(
        f"/api/v1/items/{item.id}",
        headers=auth_headers,
        json={
            "title": "Updated Item",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Item"


@pytest.mark.asyncio
async def test_delete_item(
    client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession,
):
    """Test deleting an item."""
    # Create test item
    item = Item(title="Test Item", owner_id=test_user.id)
    db_session.add(item)
    await db_session.commit()
    await db_session.refresh(item)

    response = await client.delete(
        f"/api/v1/items/{item.id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    # Verify item is deleted
    response = await client.get(
        f"/api/v1/items/{item.id}",
        headers=auth_headers,
    )
    assert response.status_code == 404
