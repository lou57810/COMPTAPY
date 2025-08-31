#!/bin/sh

echo "🚀 Applying database migrations..."
python manage.py migrate --noinput

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "📊 Importing PGC (Plan Comptable Général)..."
python manage.py loaddata api/fixtures/pgc.json 2>/dev/null || echo "⚠️ PGC déjà importé ou erreur"

echo "🔥 Starting Gunicorn..."
exec gunicorn comptapi.wsgi:application --bind 0.0.0.0:$PORT

