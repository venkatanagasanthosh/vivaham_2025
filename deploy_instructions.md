# Heroku Deployment Instructions

## Prerequisites
1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Create a Heroku account: https://heroku.com
3. Install Git if not already installed

## Step 1: Login to Heroku
```bash
heroku login
```

## Step 2: Create Heroku App
```bash
# Navigate to backend directory
cd backend

# Create a new Heroku app (choose a unique name)
heroku create your-app-name

# Or let Heroku generate a name
heroku create
```

## Step 3: Set Environment Variables
```bash
# Set Django settings module
heroku config:set DJANGO_SETTINGS_MODULE=vivaham_backend.settings_prod

# Set a strong secret key
heroku config:set SECRET_KEY="your-super-secret-key-here"

# The DATABASE_URL will be automatically set when you add PostgreSQL
```

## Step 4: Add PostgreSQL Database
```bash
# Add PostgreSQL addon (free tier)
heroku addons:create heroku-postgresql:essential-0

# Check database URL was set
heroku config:get DATABASE_URL
```

## Step 5: Initialize Git Repository (if not already done)
```bash
# Initialize git in backend directory
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit for Heroku deployment"
```

## Step 6: Deploy to Heroku
```bash
# Add Heroku as remote
heroku git:remote -a your-app-name

# Deploy to Heroku
git push heroku main
```

## Step 7: Run Migrations
```bash
# Migrations will run automatically due to release command in Procfile
# But you can also run them manually:
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

## Step 8: Check Application
```bash
# Open your app
heroku open

# Check logs if there are issues
heroku logs --tail
```

## Step 9: Update Flutter App
After successful deployment, update your Flutter app's API base URL:

In `lib/services/auth_service.dart`, change:
```dart
final String _baseUrl = 'http://192.168.29.191:8000/api';
```

To:
```dart
final String _baseUrl = 'https://your-app-name.herokuapp.com/api';
```

## Useful Commands
```bash
# View logs
heroku logs --tail

# Open app in browser
heroku open

# Run Django shell
heroku run python manage.py shell

# Scale app (free tier has limitations)
heroku ps:scale web=1

# Check app status
heroku ps

# Environment variables
heroku config
```

## Troubleshooting
1. **Build fails**: Check requirements.txt has all dependencies
2. **Database errors**: Ensure PostgreSQL addon is added
3. **Static files not loading**: Check whitenoise configuration
4. **CORS errors**: Update CORS_ALLOWED_ORIGINS in settings_prod.py

## Important Notes
- Free tier apps sleep after 30 minutes of inactivity
- Free tier has limited database storage (10K rows)
- Consider upgrading for production use
- Always use HTTPS URLs for production Flutter app 