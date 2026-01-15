#!/bin/bash
set -e

# Check if we should run migrations
# if [ "$MIGRATION_ENABLED" = "true" ]; then
#     # Run Alembic migrations
#     echo "Running database migrations..."

#     if [ -f "/app/alembic.ini" ]; then
#         # Run alembic upgrade head
#         if alembic upgrade head; then
#             echo "Database migrations completed successfully"
#         else
#             echo "Database migration failed"
#             exit 1
#         fi
#     else
#         echo "alembic.ini not found, skipping migrations"
#     fi
# else
#     echo "Skipping database migrations (RUN_MIGRATIONS=$RUN_MIGRATIONS)"
# fi

# Execute the main command
echo "Starting application..."
exec fastapi run app/main.py --host 0.0.0.0 --port 8000
