#!/bin/bash

# Wait for postgres
while ! nc -z $DB_HOST $DB_PORT; do
  echo "Waiting for postgres database startup..."
  sleep 2
done
echo "PostgreSQL started"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start server
echo "Starting server..."
if [ "$DJANGO_ENV" = "development" ]; then
    python manage.py runserver 0.0.0.0:8000
else
    gunicorn config.wsgi:application --bind 0.0.0.0:8000
fi