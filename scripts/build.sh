#!/bin/bash

# Build script for Google Meet Slack Bot

set -e

echo "🐳 Building Google Meet Slack Bot Docker image..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please copy env.example to .env and configure it."
    exit 1
fi

# Check if credentials directory exists
if [ ! -d "credentials" ]; then
    echo "📁 Creating credentials directory..."
    mkdir -p credentials
fi

# Check if credentials.json exists
if [ ! -f "credentials/credentials.json" ]; then
    echo "⚠️  credentials.json not found in credentials/ directory."
    echo "   Please place your Google OAuth2 credentials file there."
    echo "   You can download it from Google Cloud Console."
fi

# Build the Docker image
echo "🔨 Building Docker image..."
docker build -t gmeetslack-bot:latest .

echo "✅ Build complete!"
echo ""
echo "To run the bot:"
echo "  docker-compose up -d"
echo ""
echo "To run with web interface:"
echo "  docker-compose --profile web up -d"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
