#!/bin/sh
set -e

echo "🎨 RTSP Frontend Starting..."

# Verify Vite is installed
if ! command -v npx >/dev/null 2>&1; then
    echo "❌ npx not found"
    exit 1
fi

# Check if vite is accessible
if ! npx vite --version >/dev/null 2>&1; then
    echo "📦 Vite not found, installing dependencies..."
    yarn install
fi

echo "✅ Vite is ready"
echo "🚀 Starting development server..."

exec "$@"
