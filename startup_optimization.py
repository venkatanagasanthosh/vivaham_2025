#!/usr/bin/env python3
"""
Startup optimization script for Railway deployment
This script helps reduce cold start times by pre-loading common modules
"""

import os
import sys
import django
from django.conf import settings

def optimize_startup():
    """Pre-load modules and warm up connections to reduce cold start time"""
    print("🚀 Optimizing startup performance...")
    
    # Pre-load common modules
    try:
        import boto3
        import psycopg2
        import rest_framework
        import corsheaders
        print("✅ Common modules pre-loaded")
    except ImportError as e:
        print(f"⚠️ Some modules not available: {e}")
    
    # Setup Django early
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vivaham_backend.settings')
        django.setup()
        print("✅ Django setup completed")
    except Exception as e:
        print(f"⚠️ Django setup issue: {e}")
    
    # Warm up database connection
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection warmed up")
    except Exception as e:
        print(f"⚠️ Database warm-up issue: {e}")
    
    # Pre-load S3 client if credentials are available
    try:
        if (os.environ.get('AWS_ACCESS_KEY_ID') and 
            os.environ.get('AWS_SECRET_ACCESS_KEY') and 
            os.environ.get('AWS_STORAGE_BUCKET_NAME')):
            import boto3
            s3_client = boto3.client('s3')
            print("✅ S3 client pre-loaded")
        else:
            print("ℹ️ S3 credentials not found - skipping S3 warm-up")
    except Exception as e:
        print(f"⚠️ S3 warm-up issue: {e}")
    
    print("🎉 Startup optimization completed!")

if __name__ == '__main__':
    optimize_startup() 