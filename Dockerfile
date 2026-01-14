# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#         gcc \
#         postgresql-client \
#         curl \
#     && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./

# Install Python dependencies with uv
RUN uv sync --frozen --no-cache

# Copy application code
COPY ./app ./app
# COPY ./alembic ./alembic
# COPY ./alembic.ini ./alembic.ini

# RUN uv run alembic upgrade head

# Create non-root user
# RUN useradd -m -u 1000 appuser && \
#     chown -R appuser:appuser /app
# USER appuser

# Expose port
EXPOSE 8000

# Run application
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
