#!/bin/bash

# Heroku Deployment Script for Vivaham Backend
echo "🚀 Starting Heroku deployment for Vivaham Backend..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed. Please install it first:"
    echo "   https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if user is logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "🔐 Please login to Heroku first:"
    heroku login
fi

# Get app name from user
read -p "Enter your Heroku app name (or press Enter to let Heroku generate one): " APP_NAME

# Create Heroku app
if [ -z "$APP_NAME" ]; then
    echo "📱 Creating new Heroku app..."
    heroku create
else
    echo "📱 Creating Heroku app: $APP_NAME"
    heroku create $APP_NAME
fi

# Get the actual app name (in case it was auto-generated)
APP_NAME=$(heroku apps:info --json | grep -o '"name":"[^"]*' | grep -o '[^"]*$')
echo "✅ Created app: $APP_NAME"

# Set environment variables
echo "⚙️ Setting environment variables..."
heroku config:set DJANGO_SETTINGS_MODULE=vivaham_backend.settings_prod

# Generate a strong secret key
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
heroku config:set SECRET_KEY="$SECRET_KEY"

# Add PostgreSQL database
echo "🗄️ Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:essential-0

# Initialize git repository
echo "📂 Initializing Git repository..."
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit for Heroku deployment"

# Add Heroku remote
heroku git:remote -a $APP_NAME

# Deploy to Heroku
echo "🚀 Deploying to Heroku..."
git push heroku main

# Wait for deployment to complete
echo "⏳ Waiting for deployment to complete..."
sleep 10

# Run migrations
echo "🔄 Running database migrations..."
heroku run python manage.py migrate

# Create superuser prompt
echo "👤 You may want to create a superuser account:"
echo "   heroku run python manage.py createsuperuser"

# Display success information
echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📱 Your app URL: https://$APP_NAME.herokuapp.com"
echo "🔧 Admin panel: https://$APP_NAME.herokuapp.com/admin/"
echo "📊 API endpoints: https://$APP_NAME.herokuapp.com/api/"
echo ""
echo "📝 Next steps:"
echo "1. Update your Flutter app's base URL to: https://$APP_NAME.herokuapp.com/api"
echo "2. Test your API endpoints"
echo "3. Create a superuser: heroku run python manage.py createsuperuser"
echo ""
echo "🔍 Useful commands:"
echo "   heroku logs --tail           # View logs"
echo "   heroku open                  # Open app in browser"
echo "   heroku run python manage.py shell  # Django shell"
echo ""
echo "✅ Deployment complete!" 