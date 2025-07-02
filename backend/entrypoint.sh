#!/bin/bash
set -e

echo "🚀 Starting RTSP Stream Viewer (Cloud Run Mode)"

# Get Cloud Run's dynamic port
PORT=${PORT:-8080}
echo "🔍 DEBUG: Cloud Run assigned PORT=$PORT"

# Skip Redis check for now to isolate the port issue
echo "⚠️ Skipping Redis check for debugging..."

echo "📊 Running migrations..."
python manage.py migrate --noinput 2>/dev/null || echo "Migration skipped"

echo "🎬 Starting ASGI server with Daphne on port $PORT..."
exec daphne -b 0.0.0.0 -p $PORT streamviewer.asgi:application
