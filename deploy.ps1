# Heroku Deployment Script for Vivaham Backend (PowerShell)
Write-Host "🚀 Starting Heroku deployment for Vivaham Backend..." -ForegroundColor Green

# Check if Heroku CLI is installed
try {
    heroku --version | Out-Null
} catch {
    Write-Host "❌ Heroku CLI is not installed. Please install it first:" -ForegroundColor Red
    Write-Host "   https://devcenter.heroku.com/articles/heroku-cli" -ForegroundColor Yellow
    exit 1
}

# Check if user is logged in to Heroku
try {
    heroku auth:whoami | Out-Null
} catch {
    Write-Host "🔐 Please login to Heroku first:" -ForegroundColor Yellow
    heroku login
}

# Get app name from user
$APP_NAME = Read-Host "Enter your Heroku app name (or press Enter to let Heroku generate one)"

# Create Heroku app
if ([string]::IsNullOrEmpty($APP_NAME)) {
    Write-Host "📱 Creating new Heroku app..." -ForegroundColor Blue
    heroku create
    # Get the generated app name
    $APP_NAME = (heroku apps:info --json | ConvertFrom-Json).name
} else {
    Write-Host "📱 Creating Heroku app: $APP_NAME" -ForegroundColor Blue
    heroku create $APP_NAME
}

Write-Host "✅ Created app: $APP_NAME" -ForegroundColor Green

# Set environment variables
Write-Host "⚙️ Setting environment variables..." -ForegroundColor Blue
heroku config:set DJANGO_SETTINGS_MODULE=vivaham_backend.settings_prod

# Generate a strong secret key
$SECRET_KEY = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
heroku config:set SECRET_KEY="$SECRET_KEY"

# Add PostgreSQL database
Write-Host "🗄️ Adding PostgreSQL database..." -ForegroundColor Blue
heroku addons:create heroku-postgresql:essential-0

# Initialize git repository
Write-Host "📂 Initializing Git repository..." -ForegroundColor Blue
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit for Heroku deployment"

# Add Heroku remote
heroku git:remote -a $APP_NAME

# Deploy to Heroku
Write-Host "🚀 Deploying to Heroku..." -ForegroundColor Blue
git push heroku main

# Wait for deployment to complete
Write-Host "⏳ Waiting for deployment to complete..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Run migrations
Write-Host "🔄 Running database migrations..." -ForegroundColor Blue
heroku run python manage.py migrate

# Create superuser prompt
Write-Host "👤 You may want to create a superuser account:" -ForegroundColor Yellow
Write-Host "   heroku run python manage.py createsuperuser" -ForegroundColor Gray

# Display success information
Write-Host ""
Write-Host "🎉 Deployment completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📱 Your app URL: https://$APP_NAME.herokuapp.com" -ForegroundColor Cyan
Write-Host "🔧 Admin panel: https://$APP_NAME.herokuapp.com/admin/" -ForegroundColor Cyan
Write-Host "📊 API endpoints: https://$APP_NAME.herokuapp.com/api/" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Yellow
Write-Host "1. Update your Flutter app's base URL to: https://$APP_NAME.herokuapp.com/api" -ForegroundColor Gray
Write-Host "2. Test your API endpoints" -ForegroundColor Gray
Write-Host "3. Create a superuser: heroku run python manage.py createsuperuser" -ForegroundColor Gray
Write-Host ""
Write-Host "🔍 Useful commands:" -ForegroundColor Yellow
Write-Host "   heroku logs --tail           # View logs" -ForegroundColor Gray
Write-Host "   heroku open                  # Open app in browser" -ForegroundColor Gray
Write-Host "   heroku run python manage.py shell  # Django shell" -ForegroundColor Gray
Write-Host ""
Write-Host "✅ Deployment complete!" -ForegroundColor Green 