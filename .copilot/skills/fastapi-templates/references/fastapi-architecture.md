# FastAPI Architecture Guide

This guide covers the recommended architecture for production-ready FastAPI applications.

## Layered Architecture

FastAPI applications should follow a clean architecture with clear separation of concerns:

```
┌─────────────────────────────────┐
│    API Layer (Endpoints)         │
│  (Route handlers, validation)    │
├─────────────────────────────────┤
│   Dependency Injection Layer     │
│   (Dependencies, middleware)     │
├─────────────────────────────────┤
│   Service Layer                  │
│   (Business logic)               │
├─────────────────────────────────┤
│   Repository Layer               │
│   (Data access)                  │
├─────────────────────────────────┤
│   Database Layer                 │
│   (SQLAlchemy, models)           │
└─────────────────────────────────┘
```

## Layer Responsibilities

### 1. API Layer (Endpoints)

- Handle HTTP requests and responses
- Validate request data using Pydantic schemas
- Call services to process business logic
- Return appropriate HTTP status codes and responses

```python
@router.post("/users/", response_model=User)
async def create_user(
    user_in: UserCreate,
    service: UserService = Depends()
):
    return await service.create(user_in)
```

### 2. Dependency Injection Layer

- Provide dependencies to endpoints
- Manage authentication and authorization
- Handle cross-cutting concerns

```python
async def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> User:
    # Validate token and return user
    pass
```

### 3. Service Layer

- Implement business logic
- Orchestrate repositories
- Handle domain-specific validation
- Implement use cases

```python
class UserService:
    async def create_user(self, user_in: UserCreate) -> User:
        # Check if email exists
        # Hash password
        # Create user via repository
        pass
```

### 4. Repository Layer

- Encapsulate data access logic
- Provide CRUD operations
- Use generic base repository for common operations
- Handle queries and database operations

```python
class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db, email: str) -> Optional[User]:
        pass
```

### 5. Database Layer

- Define SQLAlchemy models
- Configure database connection
- Manage sessions
- Handle migrations with Alembic

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
```

## Configuration Management

Use `pydantic-settings` for environment-based configuration:

```python
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    DEBUG: bool = False

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
```

## Error Handling

Implement consistent error handling across layers:

```python
# Custom exceptions
class UserNotFound(Exception):
    pass

# In endpoints
@router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_repository.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user
```

## Middleware and Lifecycle

Use FastAPI's lifespan context manager for startup/shutdown:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.connect()
    yield
    # Shutdown
    await db.disconnect()

app = FastAPI(lifespan=lifespan)
```

## Testing Strategy

Test each layer independently:

- **Unit Tests**: Test services and repositories in isolation
- **Integration Tests**: Test multiple layers together
- **End-to-End Tests**: Test complete request flows

Use dependency injection to mock dependencies in tests.
