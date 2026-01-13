"""Project structure guide following fastapi-templates skill."""

# Production-Ready FastAPI Project Structure

## Directory Organization

```
fastapi-mcp/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   │
│   ├── api/                    # API routes
│   │   ├── __init__.py        # Router initialization
│   │   ├── dependencies.py    # Shared dependencies (auth, db)
│   │   ├── errors.py          # Exception handlers
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py      # API v1 router configuration
│   │       └── endpoints/     # Endpoint modules
│   │           ├── __init__.py
│   │           ├── auth.py    # Authentication endpoints
│   │           ├── users.py   # User management endpoints
│   │           ├── items.py   # Item management endpoints
│   │           └── health.py  # Health check endpoint
│   │
│   ├── core/                  # Core configuration & utilities
│   │   ├── __init__.py
│   │   ├── config.py          # Settings & environment variables
│   │   ├── database.py        # Database connection & session
│   │   ├── security.py        # Authentication & encryption
│   │   ├── logging.py         # Logging configuration
│   │   └── cache.py           # Redis cache utilities
│   │
│   ├── models/                # SQLAlchemy ORM models
│   │   └── __init__.py        # User, Item models
│   │
│   ├── schemas/               # Pydantic validation schemas
│   │   └── __init__.py        # Request/response schemas
│   │
│   ├── services/              # Business logic layer
│   │   ├── __init__.py
│   │   ├── user_service.py    # User business logic
│   │   └── item_service.py    # Item business logic
│   │
│   ├── repositories/          # Data access layer
│   │   ├── __init__.py
│   │   ├── base_repository.py # Generic CRUD operations
│   │   ├── user_repository.py # User-specific queries
│   │   └── item_repository.py # Item-specific queries
│   │
│   └── middleware/            # Custom middleware
│       └── __init__.py        # Logging & rate limiting
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Test configuration & fixtures
│   ├── test_auth.py          # Authentication tests
│   ├── test_users.py         # User endpoint tests
│   └── test_items.py         # Item endpoint tests
│
├── alembic/                  # Database migrations
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── scripts/
│   └── start.sh              # Production startup script
│
├── .github/workflows/
│   └── ci.yml               # GitHub Actions CI/CD
│
├── pyproject.toml           # Project metadata & dependencies
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Multi-service orchestration
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore rules
├── .pre-commit-config.yaml # Code quality hooks
├── Makefile                # Common tasks
├── README.md               # Project documentation
└── run.py                  # Development server
```

## Architecture Layers

### 1. API Layer (`app/api/`)

- **Purpose**: HTTP request/response handling
- **Contains**: Route handlers, request validation, response serialization
- **Example**: `endpoints/users.py` - User CRUD endpoints
- **Dependency**: Uses services and database dependencies

### 2. Service Layer (`app/services/`)

- **Purpose**: Business logic implementation
- **Contains**: User authentication, data processing, validations
- **Example**: `user_service.py` - User creation, authentication
- **Dependency**: Uses repositories for data access

### 3. Repository Layer (`app/repositories/`)

- **Purpose**: Data access abstraction
- **Contains**: Database queries, CRUD operations
- **Example**: `user_repository.py` - get_by_email, get_by_username
- **Dependency**: Uses SQLAlchemy models

### 4. Core Layer (`app/core/`)

- **Purpose**: Cross-cutting concerns
- **Contains**: Configuration, database, security, logging, caching
- **Not Dependent On**: Services, repositories, or API layers

### 5. Models & Schemas

- **Models** (`app/models/`): SQLAlchemy ORM models for database
- **Schemas** (`app/schemas/`): Pydantic models for validation

## Key Design Patterns

### Dependency Injection

```python
@router.get("/items")
async def read_items(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    # FastAPI injects dependencies automatically
    pass
```

### Repository Pattern

```python
# Repositories handle all data access
user = await user_repository.get_by_email(db, email)
users = await user_repository.get_multi(db, skip=0, limit=10)
```

### Service Layer

```python
# Services contain business logic
user = await user_service.create_user(db, user_data)
```

### Async/Await

```python
# All database operations are async
async def create_item(db: AsyncSession, item_in: ItemCreate):
    item = await item_repository.create(db, item_in)
    return item
```

## Request Flow

```
Client Request
    ↓
API Route Handler (endpoints/*.py)
    ↓
Dependency Injection (get_db, get_current_user)
    ↓
Service Layer (business logic)
    ↓
Repository Layer (data access)
    ↓
Database / External Services
    ↓
Response serialization (Pydantic schemas)
    ↓
Client Response
```

## Configuration Management

### Environment Variables

```python
# config.py uses pydantic-settings
DATABASE_URL = "postgresql+asyncpg://..."
SECRET_KEY = "your-secret-key"
APP_ENV = "development"
DEBUG = True
```

### Database Session

```python
# Dependency provides session for each request
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
```

## Security Implementation

- **Authentication**: JWT tokens via `core/security.py`
- **Password Hashing**: bcrypt with passlib
- **Dependency-based**: `get_current_user` dependency
- **Role-based Access**: `get_current_superuser` for admin endpoints

## Testing Strategy

- **Unit Tests**: Test services and repositories
- **Integration Tests**: Test endpoints with test database
- **Fixtures**: Reusable test data and mocks
- **Async Support**: `pytest-asyncio` for async tests

## Skills Applied

✅ Repository Pattern - Data access abstraction
✅ Service Layer - Business logic separation
✅ Dependency Injection - FastAPI's built-in DI
✅ Async/Await - Fully asynchronous application
✅ Error Handling - Custom exception handlers
✅ Testing - Comprehensive test suite
✅ Middleware - Logging and rate limiting
✅ Docker - Container orchestration
✅ CI/CD - GitHub Actions pipeline
✅ Code Quality - Black, Ruff, MyPy

"""
