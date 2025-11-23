#!/bin/bash

# Railway Deployment Script for TastyTrails

echo "Starting Railway deployment process..."

# Check if railway CLI is installed
if ! command -v railway &> /dev/null
then
    echo "Railway CLI could not be found. Please install it first:"
    echo "curl -fsSL https://railway.app/install.sh | sh"
    exit 1
fi

# Login to Railway (if not already logged in)
echo "Checking Railway login status..."
railway login

# Create new project or use existing one
echo "Creating or selecting Railway project..."
railway init

# Set environment variables
echo "Setting environment variables..."
railway env set DEBUG=False
railway env set ALLOWED_HOSTS=localhost,127.0.0.1,*.railway.app
railway env set CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://*.railway.app

# Deploy the application
echo "Deploying application..."
railway up

# Run migrations
echo "Running database migrations..."
railway run python manage.py migrate

# Collect static files
echo "Collecting static files..."
railway run python manage.py collectstatic --noinput

echo "Deployment completed successfully!"
echo "Visit your application at: $(railway url)"