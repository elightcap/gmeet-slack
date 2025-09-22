#!/bin/bash

# Run script for Google Meet Slack Bot

set -e

echo "🚀 Starting Google Meet Slack Bot..."

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
    exit 1
fi

# Create logs directory
mkdir -p logs

# Start the bot
echo "🐳 Starting Docker containers..."
docker-compose up -d

echo "✅ Bot started successfully!"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop the bot:"
echo "  docker-compose down"
echo ""
echo "To restart the bot:"
echo "  docker-compose restart"
