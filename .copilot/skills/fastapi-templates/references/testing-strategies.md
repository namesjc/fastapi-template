# FastAPI Testing Strategies

Comprehensive guide for testing FastAPI applications at all levels.

## Testing Layers

### 1. Unit Tests

Test individual components in isolation with mocked dependencies:

```python
# test_user_service.py
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_create_user():
    # Mock repository
    mock_repo = AsyncMock()

    service = UserService()
    service.repository = mock_repo

    user_data = UserCreate(
        email="test@example.com",
        password="secure123"
    )

    # Mock the create method
    expected_user = User(id=1, email="test@example.com")
    mock_repo.create.return_value = expected_user

    result = await service.create_user(MagicMock(), user_data)

    assert result.email == "test@example.com"
    mock_repo.create.assert_called_once()
```

### 2. Integration Tests

Test multiple layers working together:

```python
# test_user_endpoints.py
@pytest.mark.asyncio
async def test_create_user_integration(client, db_session):
    """Test user creation endpoint with real database."""
    response = await client.post(
        "/api/v1/users/",
        json={
            "email": "integration@example.com",
            "password": "secure123",
            "full_name": "Integration Test"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "integration@example.com"

    # Verify data was persisted
    user = await db_session.get(User, data["id"])
    assert user is not None
```

### 3. End-to-End Tests

Test complete user workflows:

```python
@pytest.mark.asyncio
async def test_user_workflow(client):
    """Test complete user registration and authentication workflow."""

    # 1. Create user
    create_response = await client.post(
        "/api/v1/users/",
        json={
            "email": "e2e@example.com",
            "password": "secure123",
            "full_name": "E2E Test"
        }
    )
    assert create_response.status_code == 201

    # 2. Login
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "e2e@example.com",
            "password": "secure123"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # 3. Get current user
    user_response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert user_response.status_code == 200
    assert user_response.json()["email"] == "e2e@example.com"
```

## Test Configuration

### pytest Fixtures

Create reusable test fixtures:

```python
# conftest.py
import pytest
import asyncio
from httpx import AsyncClient

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def db_session():
    """Create test database session."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncSessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with AsyncSessionLocal() as session:
        yield session

@pytest.fixture
async def client(db_session):
    """Create test client with mocked database."""
    def override_get_db():
        return db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
```

### Test Database Setup

Use in-memory SQLite for fast testing:

```python
# Use in tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Or file-based for debugging
TEST_DATABASE_URL = "sqlite+aiosqlite:///test.db"
```

## Testing Patterns

### Testing Authentication

```python
@pytest.mark.asyncio
async def test_protected_endpoint_without_token(client):
    """Test that protected endpoint requires auth."""
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_protected_endpoint_with_token(client, auth_token):
    """Test that protected endpoint works with valid token."""
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
```

### Testing Error Cases

```python
@pytest.mark.asyncio
async def test_create_user_invalid_email(client):
    """Test that invalid email is rejected."""
    response = await client.post(
        "/api/v1/users/",
        json={
            "email": "invalid-email",
            "password": "secure123"
        }
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_duplicate_user(client):
    """Test that duplicate email is rejected."""
    user_data = {
        "email": "duplicate@example.com",
        "password": "secure123"
    }

    await client.post("/api/v1/users/", json=user_data)

    response = await client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 400
```

### Testing Pagination

```python
@pytest.mark.asyncio
async def test_list_items_pagination(client, db_session):
    """Test pagination on list endpoints."""
    # Create 25 items
    for i in range(25):
        await item_service.create(
            db_session,
            ItemCreate(name=f"Item {i}", price=100)
        )

    # Test first page
    response = await client.get("/api/v1/items/?skip=0&limit=10")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 10

    # Test second page
    response = await client.get("/api/v1/items/?skip=10&limit=10")
    items = response.json()
    assert len(items) == 10
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_users.py

# Run specific test
pytest tests/test_users.py::test_create_user

# Run with verbose output
pytest -v

# Run async tests
pytest -v tests/ -m asyncio

# Run in parallel
pytest -n auto
```

## Test Best Practices

1. **Test Behavior, Not Implementation**: Focus on what the function does, not how
2. **Use Descriptive Names**: Test names should describe what they test
3. **Arrange-Act-Assert**: Organize tests clearly
4. **One Assertion Per Test**: Keep tests focused
5. **Use Fixtures**: Share common setup code
6. **Mock External Dependencies**: Use AsyncMock for external calls
7. **Test Edge Cases**: Empty lists, invalid input, etc.
8. **Test Error Paths**: Both success and failure cases
9. **Keep Tests Fast**: Use in-memory database, minimize I/O
10. **Clean Up**: Use fixtures to ensure proper cleanup

## Coverage Goals

- **Repositories**: 90%+ coverage (critical data access)
- **Services**: 80%+ coverage (business logic)
- **Endpoints**: 70%+ coverage (main workflows)
- **Overall Target**: 75%+ coverage

```bash
# Generate coverage report
pytest --cov=app --cov-report=html
```
