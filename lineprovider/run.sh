#!/bin/bash

set -e

echo "Starting migrations..."

alembic upgrade head

echo "Migrations completed successfully."

echo "Starting FastAPI application..."
uvicorn main:app --host ${APP_HOST} --port ${APP_PORT}
