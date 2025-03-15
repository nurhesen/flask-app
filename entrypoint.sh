#!/bin/sh
set -e

if [ "$1" = "pytest" ]; then
    shift
    exec pytest "$@"
else
    echo "Waiting for MySQL to be available..."
    while ! nc -z db 3306; do
      sleep 1
    done
    echo "MySQL is up - executing migrations..."
    
    alembic upgrade head
    
    echo "Starting FastAPI application..."
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000
fi
