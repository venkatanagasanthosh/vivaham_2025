#!/usr/bin/env python3
"""
Test S3 upload using credentials from Django settings
"""

import boto3
from datetime import datetime

# Import Django settings
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vivaham_backend.settings')
django.setup()

from django.conf import settings

def test_s3_from_settings():
    """Test S3 upload using credentials from Django settings"""
    print("=== Testing S3 Upload with Credentials from Django Settings ===")
    
    # Get credentials from Django settings
    aws_access_key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    aws_secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
    aws_bucket = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)
    aws_region = getattr(settings, 'AWS_S3_REGION_NAME', 'ap-south-1')
    
    print(f"AWS_ACCESS_KEY_ID: {'✓ Set' if aws_access_key else '✗ Not set'}")
    print(f"AWS_SECRET_ACCESS_KEY: {'✓ Set' if aws_secret_key else '✗ Not set'}")
    print(f"AWS_STORAGE_BUCKET_NAME: {'✓ Set' if aws_bucket else '✗ Not set'}")
    print(f"AWS_S3_REGION_NAME: {aws_region}")
    
    if not all([aws_access_key, aws_secret_key, aws_bucket]):
        print("❌ Missing credentials in Django settings")
        return
    
    try:
        # Create S3 client with credentials from settings
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )
        
        # Test bucket access
        try:
            response = s3_client.head_bucket(Bucket=aws_bucket)
            print(f"✅ Successfully connected to S3 bucket: {aws_bucket}")
        except Exception as e:
            print(f"❌ Error accessing bucket: {e}")
            return
        
        # Test upload to profile_photos folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_content = f"Test image data created at {timestamp}".encode('utf-8')
        test_key = f"profile_photos/test_image_{timestamp}.jpg"
        
        try:
            s3_client.put_object(
                Bucket=aws_bucket,
                Key=test_key,
                Body=test_content,
                ContentType='image/jpeg'
            )
            print(f"✅ Successfully uploaded test file: {test_key}")
            
            # Verify upload
            response = s3_client.head_object(Bucket=aws_bucket, Key=test_key)
            print(f"✅ File verified in S3: {test_key}")
            print(f"   Size: {response['ContentLength']} bytes")
            print(f"   URL: https://{aws_bucket}.s3.{aws_region}.amazonaws.com/{test_key}")
            
            # Clean up
            s3_client.delete_object(Bucket=aws_bucket, Key=test_key)
            print(f"✅ Test file cleaned up")
            
        except Exception as e:
            print(f"❌ Failed to upload test file: {e}")
            return
        
        # List existing files in profile_photos folder
        try:
            response = s3_client.list_objects_v2(
                Bucket=aws_bucket, 
                Prefix='profile_photos/',
                MaxKeys=10
            )
            objects = response.get('Contents', [])
            print(f"✅ Found {len(objects)} files in profile_photos/ folder")
            
            if objects:
                print("Files in profile_photos/ folder:")
                for obj in objects:
                    print(f"  - {obj['Key']} (Size: {obj['Size']} bytes, Modified: {obj['LastModified']})")
            else:
                print("  No files found in profile_photos/ folder")
                
        except Exception as e:
            print(f"⚠️ Could not list objects: {e}")
            
    except Exception as e:
        print(f"❌ Error testing S3 upload: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n=== Test Complete ===")

if __name__ == '__main__':
    test_s3_from_settings() 