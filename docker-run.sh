#!/bin/bash
# Helper script to run Docker container

echo "🐳 Running Data-Text Pipeline in Docker..."

docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/.cache:/app/.cache \
  data-text-pipeline:latest \
  python cli.py "$@"

echo "✓ Complete! Check output/ directory"