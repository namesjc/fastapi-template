# Async/Await Best Practices

This guide covers best practices for writing async code in FastAPI applications.

## Core Principles

### 1. Async All The Way

Always use async for I/O operations (database, HTTP requests, file operations):

```python
# Good: Async database operation
async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

# Bad: Blocking database operation
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
```

### 2. Use Async Drivers

Always use async database drivers:

- **PostgreSQL**: `asyncpg` instead of `psycopg2`
- **MySQL**: `aiomysql` instead of `mysql-python`
- **MongoDB**: `motor` instead of `pymongo`
- **SQLite**: `aiosqlite`

```python
# Correct connection string for async PostgreSQL
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/db"

# Create async engine
engine = create_async_engine(DATABASE_URL)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
```

### 3. Session Management

Properly manage database sessions in async context:

```python
async def get_db() -> AsyncSession:
    """Dependency for database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

### 4. Async Context Managers

Use async context managers for resource management:

```python
# Correct: Using async context manager
async with AsyncSessionLocal() as session:
    user = await session.get(User, user_id)

# Application lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.connect()
    yield
    # Shutdown
    await db.disconnect()
```

### 5. Avoid Blocking Operations

Never use blocking operations in async functions:

```python
# Bad: Blocking operations in async function
async def process_user(user_id: int):
    time.sleep(5)  # ❌ Blocks the event loop!
    user = await get_user(user_id)
    return user

# Good: Use async equivalents
async def process_user(user_id: int):
    await asyncio.sleep(5)  # ✓ Non-blocking
    user = await get_user(user_id)
    return user
```

### 6. Concurrent Operations

Use `asyncio.gather()` or `asyncio.TaskGroup` for concurrent operations:

```python
# Concurrent database queries
async def get_user_with_data(user_id: int, db: AsyncSession):
    user_task = user_repository.get(db, user_id)
    orders_task = order_repository.get_by_user(db, user_id)

    user, orders = await asyncio.gather(
        user_task,
        orders_task
    )
    return {"user": user, "orders": orders}

# Python 3.11+ TaskGroup
async def get_multiple_users(db: AsyncSession, user_ids: List[int]):
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(user_repository.get(db, uid))
            for uid in user_ids
        ]
    return tasks
```

### 7. Background Tasks

Use FastAPI's background tasks for non-blocking operations:

```python
from fastapi import BackgroundTasks

@router.post("/users/")
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks
):
    user = await user_service.create_user(db, user_in)

    # Send email in background
    background_tasks.add_task(send_email, user.email)

    return user
```

### 8. Error Handling in Async Code

Properly handle exceptions in async operations:

```python
async def safe_operation():
    try:
        result = await some_async_operation()
        return result
    except asyncio.TimeoutError:
        # Handle timeout
        raise HTTPException(status_code=504, detail="Operation timeout")
    except Exception as e:
        # Handle other errors
        logger.error(f"Operation failed: {e}")
        raise HTTPException(status_code=500, detail="Internal error")
```

### 9. Timeouts

Always set timeouts for async operations:

```python
from httpx import AsyncClient

async def fetch_external_api():
    async with AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get("https://api.example.com/data")
            return response.json()
        except asyncio.TimeoutError:
            raise HTTPException(status_code=504, detail="API timeout")

# Database query timeout
async def get_user_with_timeout(db: AsyncSession, user_id: int):
    try:
        user = await asyncio.wait_for(
            user_repository.get(db, user_id),
            timeout=5.0
        )
        return user
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Query timeout")
```

### 10. Async Comprehensions

Use async comprehensions for async iterations:

```python
# Async list comprehension
users = [user async for user in async_generator()]

# Async dict comprehension
user_map = {u.id: u async for u in fetch_users()}

# Async filtering
active_users = [u async for u in fetch_users() if u.is_active]
```

## Common Pitfalls to Avoid

1. **Mixing sync and async**: Always use async drivers and operations
2. **Blocking the event loop**: Never use `time.sleep()`, `requests`, or other blocking libraries
3. **Not handling exceptions**: Always wrap async operations in try-except
4. **Creating too many tasks**: Use task pools or semaphores to limit concurrency
5. **Not managing resources**: Always use async context managers
6. **Forgetting await**: Always await async functions

## Performance Tips

1. **Use connection pooling**: SQLAlchemy manages this automatically
2. **Batch operations**: Query multiple records at once
3. **Cache results**: Use `@cache` decorator for expensive operations
4. **Limit concurrent connections**: Use semaphores for external API calls
5. **Monitor with logging**: Log async operation performance

```python
import logging
import time

logger = logging.getLogger(__name__)

async def timed_operation():
    start = time.time()
    result = await expensive_operation()
    duration = time.time() - start
    logger.info(f"Operation took {duration:.2f}s")
    return result
```
