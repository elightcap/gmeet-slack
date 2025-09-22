#!/bin/bash

# Stop script for Google Meet Slack Bot

set -e

echo "🛑 Stopping Google Meet Slack Bot..."

# Stop Docker containers
docker-compose down

echo "✅ Bot stopped successfully!"
echo ""
echo "To start the bot again:"
echo "  ./scripts/run.sh"
echo ""
echo "To remove all containers and volumes:"
echo "  docker-compose down -v"
