#!/bin/bash
# This script handles starting the application with the correct port for Railway

# Use the PORT environment variable provided by Railway, or default to 8000
PORT=${PORT:-8000}

echo "PORT is set to: $PORT"
echo "Current directory: $(pwd)"
echo "Listing files in current directory:"
ls -la

echo "Starting application on port $PORT"
exec gunicorn tastytrails.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --workers 1