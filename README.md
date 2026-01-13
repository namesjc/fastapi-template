# FastAPI Production-Ready Application

A comprehensive, production-ready FastAPI application with best practices, including authentication, database integration, caching, testing, and Docker support.

## Features

- ✅ **FastAPI** - Modern, fast web framework
- ✅ **Async/Await** - Fully asynchronous with SQLAlchemy 2.0
- ✅ **PostgreSQL** - Production-ready database with async support
- ✅ **Redis** - Caching layer
- ✅ **JWT Authentication** - Secure token-based auth
- ✅ **Alembic** - Database migrations
- ✅ **Pydantic v2** - Data validation and settings
- ✅ **Testing** - Comprehensive test suite with pytest
- ✅ **Docker** - Containerized deployment
- ✅ **CI/CD** - GitHub Actions workflow
- ✅ **Logging** - Structured JSON logging
- ✅ **Middleware** - Request logging and rate limiting
- ✅ **Error Handling** - Custom exception handlers
- ✅ **CORS** - Configurable CORS support
- ✅ **Code Quality** - Black, Ruff, MyPy

## Project Structure

```
fastapi-mcp/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py  # API dependencies
│   │   ├── errors.py        # Error handlers
│   │   └── v1/
│   │       ├── auth.py      # Authentication endpoints
│   │       ├── users.py     # User endpoints
│   │       ├── items.py     # Item endpoints
│   │       └── health.py    # Health check
│   ├── core/
│   │   ├── config.py        # Settings management
│   │   ├── database.py      # Database connection
│   │   ├── security.py      # Security utilities
│   │   ├── cache.py         # Redis cache
│   │   └── logging.py       # Logging configuration
│   ├── models/
│   │   └── __init__.py      # SQLAlchemy models
│   ├── schemas/
│   │   └── __init__.py      # Pydantic schemas
│   └── middleware/
│       └── __init__.py      # Custom middleware
├── tests/
│   ├── conftest.py          # Test configuration
│   ├── test_auth.py         # Auth tests
│   ├── test_users.py        # User tests
│   └── test_items.py        # Item tests
├── alembic/                 # Database migrations
├── scripts/
│   └── start.sh            # Production startup script
├── .github/
│   └── workflows/
│       └── ci.yml          # CI/CD pipeline
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── .env.example
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 14+
- Redis 7+
- Docker & Docker Compose (optional)
- [uv](https://astral.sh/uv/) - Fast Python package manager (optional but recommended)

### Local Development

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd fastapi-mcp
   ```

2. **Install dependencies with uv**

   ```bash
   # Install uv first (if not already installed)
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install project dependencies
   uv sync
   ```

   Or use pip (traditional method):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start PostgreSQL and Redis** (if not using Docker)

   ```bash
   # Using Homebrew on macOS
   brew services start postgresql@16
   brew services start redis
   ```

5. **Run database migrations**

   ```bash
   uv run alembic upgrade head
   ```

6. **Start the application**

   ```bash
   uv run uvicorn app.main:app --reload
   ```

7. **Access the API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - Health: http://localhost:8000/api/v1/health

### Using Docker

1. **Start all services**

   ```bash
   docker-compose up -d
   ```

2. **View logs**

   ```bash
   docker-compose logs -f app
   ```

3. **Stop services**
   ```bash
   docker-compose down
   ```

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get token

### Users

- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users` - List all users (admin)
- `GET /api/v1/users/{id}` - Get user by ID (admin)
- `DELETE /api/v1/users/{id}` - Delete user (admin)

### Items

- `POST /api/v1/items` - Create item
- `GET /api/v1/items` - List user's items
- `GET /api/v1/items/{id}` - Get item by ID
- `PUT /api/v1/items/{id}` - Update item
- `DELETE /api/v1/items/{id}` - Delete item

### Health

- `GET /api/v1/health` - Health check endpoint

## Testing

### Run all tests

```bash
uv run pytest
```

### Run with coverage

```bash
uv run pytest --cov=app --cov-report=html
```

### Run specific test file

```bash
uv run pytest tests/test_auth.py -v
```

## Database Migrations

### Create a new migration

```bash
uv run alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations

```bash
uv run alembic upgrade head
```

### Rollback migration

```bash
uv run alembic downgrade -1
```

## Code Quality

### Format code

```bash
uv run black .
```

### Lint code

```bash
uv run ruff check .
```

### Type checking

```bash
uv run mypy app
```

### Run pre-commit hooks

```bash
pre-commit install
pre-commit run --all-files
```

## Configuration

Configuration is managed through environment variables and `.env` file:

- `APP_NAME` - Application name
- `APP_ENV` - Environment (development/production)
- `DEBUG` - Debug mode
- `SECRET_KEY` - JWT secret key
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `CORS_ORIGINS` - Allowed CORS origins

## Production Deployment

### Using Docker

1. Build production image

   ```bash
   docker build -t fastapi-app:latest .
   ```

2. Run with production settings
   ```bash
   docker run -d \
     --name fastapi-app \
     -p 8000:8000 \
     -e APP_ENV=production \
     -e DATABASE_URL=your-db-url \
     -e REDIS_URL=your-redis-url \
     -e SECRET_KEY=your-secret-key \
     fastapi-app:latest
   ```

### Using Gunicorn

```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

## Security Best Practices

- ✅ JWT token authentication
- ✅ Password hashing with bcrypt
- ✅ Environment-based configuration
- ✅ CORS protection
- ✅ Rate limiting middleware
- ✅ SQL injection protection (SQLAlchemy)
- ✅ Input validation (Pydantic)
- ✅ Secure headers

## Monitoring

### Health Check

```bash
curl http://localhost:8000/api/v1/health
```

Response:

```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2026-01-13T..."
}
```

### Logs

Logs are output in JSON format for easy parsing:

```json
{
  "timestamp": "2026-01-13 12:00:00",
  "level": "INFO",
  "logger": "app.api",
  "message": "Request completed",
  "method": "GET",
  "url": "/api/v1/users/me",
  "status_code": 200,
  "process_time": "0.045s"
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - feel free to use this project for your own purposes.

## Support

For issues and questions, please open an issue on GitHub.
