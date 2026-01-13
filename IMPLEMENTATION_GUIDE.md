# FastAPI Template Skills Implementation Guide

This project is now fully adapted to follow the **fastapi-templates** skill from the Copilot Skills library.

## 🎯 Key Implementations

### 1. Repository Pattern (Generic CRUD)

```python
# app/repositories/base_repository.py
class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Generic CRUD operations for any model"""
    async def get(db, id) -> Optional[ModelType]
    async def get_multi(db, skip, limit) -> List[ModelType]
    async def create(db, obj_in) -> ModelType
    async def update(db, db_obj, obj_in) -> ModelType
    async def delete(db, id) -> bool
```

**Usage**: Specialized repositories inherit from base

```python
class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    async def get_by_email(db, email) -> Optional[User]
    async def get_by_username(db, username) -> Optional[User]
```

### 2. Service Layer (Business Logic)

```python
# app/services/user_service.py
class UserService:
    """Encapsulates user business logic"""
    async def create_user(db, user_in) -> User
    async def authenticate(db, username, password) -> Optional[User]
    async def update_user(db, user_id, user_in) -> Optional[User]
```

**Separation of Concerns**:

- API layer → Routes/HTTP handling
- Service layer → Business logic
- Repository layer → Data access

### 3. Dependency Injection

```python
# app/api/dependencies.py
async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """Dependency that validates and returns current user"""

# Usage in endpoints
@router.get("/me")
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user
```

### 4. Async/Await Patterns

```python
# All operations are async for performance
async def create_item(db: AsyncSession, item_in: ItemCreate) -> Item:
    # Async database operation
    item = await item_repository.create(db, item_in)
    await db.commit()
    return item

# No blocking operations
# Database, cache, and external API calls are all async
```

### 5. Error Handling & Exception Handlers

```python
# app/api/errors.py
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Consistent error responses
raise HTTPException(status_code=400, detail="User not found")
```

### 6. Application Lifespan

```python
# app/main.py
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    await init_db()
    await cache.connect()

    yield

    # Shutdown
    await cache.disconnect()
    await close_db()

app = FastAPI(lifespan=lifespan)
```

## 📦 Project Architecture

### Clean Layered Architecture

```
┌─────────────────────────────────────┐
│        API Layer (endpoints/)       │  ← HTTP Handlers
├─────────────────────────────────────┤
│      Service Layer (services/)      │  ← Business Logic
├─────────────────────────────────────┤
│   Repository Layer (repositories/)  │  ← Data Access
├─────────────────────────────────────┤
│      Core Layer (core/)             │  ← Configuration
├─────────────────────────────────────┤
│    Models & Schemas                 │  ← Data Models
├─────────────────────────────────────┤
│        Database                     │  ← PostgreSQL
└─────────────────────────────────────┘
```

### Data Flow

1. **Request arrives** at API endpoint
2. **Dependencies injected** (database, auth user)
3. **Service layer** processes business logic
4. **Repository layer** executes database queries
5. **Response serialized** via Pydantic schemas
6. **Response sent** to client

## 🏗️ File Organization

### `/app/api/` - Request/Response Handling

```
api/
├── __init__.py              # Main API router
├── dependencies.py          # Authentication, DB injection
├── errors.py               # Exception handlers
└── v1/
    ├── router.py           # API v1 router setup
    └── endpoints/
        ├── auth.py         # /auth endpoints
        ├── users.py        # /users endpoints
        ├── items.py        # /items endpoints
        └── health.py       # /health endpoint
```

### `/app/services/` - Business Logic

```
services/
├── user_service.py         # User CRUD, authentication
└── item_service.py         # Item CRUD operations
```

### `/app/repositories/` - Data Access

```
repositories/
├── base_repository.py      # Generic <Model, Create, Update>
├── user_repository.py      # User-specific queries
└── item_repository.py      # Item-specific queries
```

### `/app/core/` - Configuration & Utilities

```
core/
├── config.py              # Pydantic Settings
├── database.py            # AsyncSession management
├── security.py            # JWT, password hashing
├── logging.py             # Structured logging
└── cache.py              # Redis cache
```

## 🔐 Security Implementation

### JWT Authentication

```python
# Create token on login
access_token = create_access_token(subject=user.id)

# Verify token on protected routes
@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```

### Password Security

```python
# Hash password on registration
hashed = get_password_hash(plain_password)

# Verify on login
is_valid = verify_password(plain_password, hashed_password)
```

## 🧪 Testing

### Test Structure

```
tests/
├── conftest.py          # Fixtures & setup
├── test_auth.py         # Authentication tests
├── test_users.py        # User endpoint tests
└── test_items.py        # Item endpoint tests
```

### Test Patterns

```python
@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/api/v1/auth/register", json={...})
    assert response.status_code == 201
```

## 📊 Database Management

### Async SQLAlchemy

```python
# Using AsyncSession for non-blocking operations
async with AsyncSessionLocal() as session:
    result = await db.execute(select(User).where(...))
    user = result.scalars().first()
```

### Alembic Migrations

```bash
# Create migration
uv run alembic revision --autogenerate -m "Add user table"

# Apply migration
uv run alembic upgrade head
```

## 🚀 Development Workflow

### Setup

```bash
# Install dependencies
uv sync

# Copy environment template
cp .env.example .env
```

### Run Application

```bash
# Development server with auto-reload
uv run uvicorn app.main:app --reload

# Production with Gunicorn
uv run gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Testing

```bash
# Run all tests
uv run pytest

# With coverage
uv run pytest --cov=app --cov-report=html
```

### Code Quality

```bash
# Format code
uv run black .

# Lint
uv run ruff check . --fix

# Type check
uv run mypy app
```

## 📋 Endpoint Examples

### Authentication

```
POST /api/v1/auth/register
POST /api/v1/auth/login
```

### User Management (requires auth)

```
GET    /api/v1/users/me           # Get current user
PUT    /api/v1/users/me           # Update current user
GET    /api/v1/users              # List all (admin only)
GET    /api/v1/users/{id}         # Get user (admin only)
DELETE /api/v1/users/{id}         # Delete user (admin only)
```

### Item Management (requires auth)

```
POST   /api/v1/items              # Create item
GET    /api/v1/items              # List user's items
GET    /api/v1/items/{id}         # Get item
PUT    /api/v1/items/{id}         # Update item
DELETE /api/v1/items/{id}         # Delete item
```

### Health Check

```
GET /api/v1/health                # Health status
```

## 🛠️ Key Technologies

| Component       | Technology | Version |
| --------------- | ---------- | ------- |
| Framework       | FastAPI    | 0.109.0 |
| Async ORM       | SQLAlchemy | 2.0.25  |
| Validation      | Pydantic   | 2.5.3   |
| Database Driver | asyncpg    | 0.29.0  |
| Cache           | Redis      | 7.0+    |
| Package Manager | uv         | latest  |
| Python          | Python     | 3.12+   |
| Deployment      | Docker     | latest  |

## ✨ Best Practices Applied

✅ **Async All The Way** - No blocking operations
✅ **Type Hints** - Full typing support
✅ **Clean Architecture** - Layered separation
✅ **DRY Principle** - Generic repository, base classes
✅ **Error Handling** - Custom exception handlers
✅ **Security** - JWT, bcrypt, CORS
✅ **Testing** - Comprehensive test suite
✅ **Documentation** - API docs, README, guides
✅ **Code Quality** - Black, Ruff, MyPy
✅ **Docker** - Production-ready containers
✅ **CI/CD** - GitHub Actions pipeline
✅ **Logging** - Structured JSON logging

## 🎓 Learning Resources

See related documentation:

- `PROJECT_STRUCTURE.md` - Detailed file structure
- `ADAPTATION_SUMMARY.md` - Skills checklist
- `README.md` - Quick start guide
- `docs/API.md` - API documentation

---

**Ready to deploy!** 🚀 Follow the Quick Start guide in README.md to get started.
