"""Tests for user endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_password_hash
from app.models import User


@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    """Create test user."""
    user = User(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
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
async def test_read_current_user(
    client: AsyncClient,
    test_user: User,
    auth_headers: dict,
):
    """Test reading current user."""
    response = await client.get(
        "/api/v1/users/me",
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["username"] == test_user.username


@pytest.mark.asyncio
async def test_read_current_user_unauthorized(client: AsyncClient):
    """Test reading current user without authentication."""
    response = await client.get("/api/v1/users/me")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_current_user(
    client: AsyncClient,
    test_user: User,
    auth_headers: dict,
):
    """Test updating current user."""
    response = await client.put(
        "/api/v1/users/me",
        headers=auth_headers,
        json={
            "full_name": "Updated Name",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
