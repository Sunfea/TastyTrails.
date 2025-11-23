@echo off
REM Railway Deployment Script for TastyTrails (Windows)

echo Starting Railway deployment process...

REM Check if railway CLI is installed
railway --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Railway CLI could not be found. Please install it first:
    echo Visit https://railway.app/cli to download and install the Railway CLI
    exit /b 1
)

REM Login to Railway (if not already logged in)
echo Checking Railway login status...
railway login

REM Create new project or use existing one
echo Creating or selecting Railway project...
railway init

REM Set environment variables
echo Setting environment variables...
railway env set DEBUG=False
railway env set ALLOWED_HOSTS=localhost,127.0.0.1,*.railway.app
railway env set CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://*.railway.app

REM Deploy the application
echo Deploying application...
railway up

REM Run migrations
echo Running database migrations...
railway run python manage.py migrate

REM Collect static files
echo Collecting static files...
railway run python manage.py collectstatic --noinput

echo Deployment completed successfully!
echo Visit your application at: 
railway url

pause