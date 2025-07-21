#!/usr/bin/env python3
"""
Test local S3 configuration with Django settings
"""
import os
import sys
import django
from django.core.files.base import ContentFile

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vivaham_backend.settings')
django.setup()

def test_local_s3():
    """Test local S3 configuration"""
    from django.conf import settings
    
    print("=== Local Django S3 Configuration ===")
    print(f"AWS_ACCESS_KEY_ID: {'✓ Set' if settings.AWS_ACCESS_KEY_ID else '✗ Not set'}")
    print(f"AWS_SECRET_ACCESS_KEY: {'✓ Set' if settings.AWS_SECRET_ACCESS_KEY else '✗ Not set'}")
    print(f"AWS_STORAGE_BUCKET_NAME: {settings.AWS_STORAGE_BUCKET_NAME}")
    print(f"USE_S3: {getattr(settings, 'USE_S3', 'Not set')}")
    print(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    
    if getattr(settings, 'USE_S3', False):
        print("\n✅ S3 is configured - testing upload...")
        
        # Test S3 upload through Django
        try:
            from api.models import User, Profile, Photo
            
            # Get or create a test user
            user, created = User.objects.get_or_create(
                username='test_s3_local',
                defaults={'email': 'test@local.com'}
            )
            
            profile, created = Profile.objects.get_or_create(user=user)
            
            # Create a test image
            test_content = b'test image content for local S3 upload'
            test_file = ContentFile(test_content, name='test_local_s3.jpg')
            
            # Create photo through Django model
            photo = Photo.objects.create(profile=profile, image=test_file)
            
            print(f"✅ Photo created successfully!")
            print(f"   Photo ID: {photo.id}")
            print(f"   Image URL: {photo.image.url}")
            print(f"   Storage: {photo.image.storage.__class__.__name__}")
            
            # Clean up
            photo.delete()
            
        except Exception as e:
            print(f"❌ S3 upload test failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("\n❌ S3 is NOT configured - uploads will go to local storage")
        print("Check Django startup logs for S3 configuration messages")

if __name__ == "__main__":
    test_local_s3() 