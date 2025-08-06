#!/bin/bash
set -e

# Check if required environment variables are set
if [ -z "$STRIPE_SECRET_KEY" ]; then
    echo "Error: STRIPE_SECRET_KEY environment variable is not set"
    exit 1
fi

if [ -z "$ADMIN_API_KEY" ]; then
    echo "Error: ADMIN_API_KEY environment variable is not set"
    exit 1
fi

# Start the application
echo "Starting Buy Me a Beer application..."
uvicorn src.app:app --host 0.0.0.0 --port ${PORT:-8000}