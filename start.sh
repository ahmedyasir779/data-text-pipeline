#!/bin/bash
# Quick start script

echo "🚀 Starting Data & Text Pipeline..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running"
    echo "   Please start Docker and try again"
    exit 1
fi

# Check if docker-compose exists
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: docker-compose not installed"
    echo "   Install: sudo apt install docker-compose"
    exit 1
fi

# Create directories if they don't exist
mkdir -p data output .cache

# Start the application
docker-compose up -d

echo ""
echo "✅ Application started!"
echo ""
echo "   🌐 Open: http://localhost:8501"
echo ""
echo "   📊 View logs: docker-compose logs -f"
echo "   🛑 Stop app:  docker-compose down"
echo ""