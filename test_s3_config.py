#!/usr/bin/env python3
"""
Test script to verify AWS S3 configuration
Run this script to check if S3 is properly configured
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vivaham_backend.settings')
django.setup()

def test_s3_configuration():
    """Test S3 configuration and connectivity"""
    print("=== Testing S3 Configuration ===")
    
    # Check environment variables
    aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_bucket = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    aws_region = os.environ.get('AWS_S3_REGION_NAME', 'ap-south-1')
    
    print(f"AWS_ACCESS_KEY_ID: {'✓ Set' if aws_access_key else '✗ Not set'}")
    print(f"AWS_SECRET_ACCESS_KEY: {'✓ Set' if aws_secret_key else '✗ Not set'}")
    print(f"AWS_STORAGE_BUCKET_NAME: {'✓ Set' if aws_bucket else '✗ Not set'}")
    print(f"AWS_S3_REGION_NAME: {aws_region}")
    
    # Check Django settings
    print(f"\n=== Django Settings ===")
    print(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'Not set')}")
    print(f"MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'Not set')}")
    
    if hasattr(settings, 'AWS_S3_CUSTOM_DOMAIN'):
        print(f"AWS_S3_CUSTOM_DOMAIN: {settings.AWS_S3_CUSTOM_DOMAIN}")
    
    # Test S3 connectivity if credentials are available
    if aws_access_key and aws_secret_key and aws_bucket:
        try:
            import boto3
            from botocore.exceptions import ClientError, NoCredentialsError
            
            print(f"\n=== Testing S3 Connectivity ===")
            
            # Create S3 client
            s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=aws_region
            )
            
            # Test bucket access
            try:
                response = s3_client.head_bucket(Bucket=aws_bucket)
                print(f"✓ Successfully connected to S3 bucket: {aws_bucket}")
                
                # List objects in bucket
                try:
                    response = s3_client.list_objects_v2(Bucket=aws_bucket, MaxKeys=5)
                    object_count = response.get('KeyCount', 0)
                    print(f"✓ Bucket contains {object_count} objects")
                except ClientError as e:
                    print(f"⚠ Could not list objects: {e}")
                    
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == '404':
                    print(f"✗ Bucket '{aws_bucket}' does not exist")
                elif error_code == '403':
                    print(f"✗ Access denied to bucket '{aws_bucket}'")
                else:
                    print(f"✗ Error accessing bucket: {e}")
                    
        except ImportError:
            print("✗ boto3 is not installed")
        except NoCredentialsError:
            print("✗ AWS credentials not found")
        except Exception as e:
            print(f"✗ Error testing S3 connectivity: {e}")
    else:
        print("\n⚠ AWS credentials not complete - skipping S3 connectivity test")
    
    print(f"\n=== Test Complete ===")

if __name__ == '__main__':
    test_s3_configuration() 