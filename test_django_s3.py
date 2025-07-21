#!/usr/bin/env python3
"""
Test S3 upload through Django with current settings
"""

import os
import sys
import django
from django.core.files.base import ContentFile
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vivaham_backend.settings')
django.setup()

def test_django_s3_upload():
    """Test S3 upload through Django"""
    print("=== Testing Django S3 Upload ===")
    
    # Check Django settings
    print(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'Not set')}")
    print(f"MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'Not set')}")
    print(f"AWS_STORAGE_BUCKET_NAME: {getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'Not set')}")
    
    try:
        # Import the Photo model
        from api.models import Photo, Profile, User
        
        # Create a test user and profile
        test_user, created = User.objects.get_or_create(
            username='test_s3_user',
            defaults={'email': 'test@example.com'}
        )
        
        if created:
            print(f"✅ Created test user: {test_user.username}")
        
        profile, created = Profile.objects.get_or_create(user=test_user)
        if created:
            print(f"✅ Created test profile for user: {test_user.username}")
        
        # Create a test image file
        test_image_content = b'fake_image_data_for_testing'
        test_filename = f'test_image_{os.getpid()}.jpg'
        
        print(f"Creating test photo with filename: {test_filename}")
        
        # Create photo object
        photo = Photo.objects.create(profile=profile)
        
        # Save the test image
        photo.image.save(test_filename, ContentFile(test_image_content), save=True)
        
        print(f"✅ Photo created successfully!")
        print(f"   Photo ID: {photo.id}")
        print(f"   Image URL: {photo.image.url if photo.image else 'No URL'}")
        print(f"   Image name: {photo.image.name if photo.image else 'No name'}")
        
        # Check if file exists in S3
        if photo.image:
            try:
                # Try to access the file
                photo.image.open()
                print(f"✅ File can be opened successfully")
                photo.image.close()
            except Exception as e:
                print(f"❌ Error opening file: {e}")
        
        # Clean up
        try:
            photo.delete()
            print(f"✅ Test photo cleaned up")
        except Exception as e:
            print(f"⚠️ Could not clean up test photo: {e}")
            
    except Exception as e:
        print(f"❌ Error testing Django S3 upload: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n=== Test Complete ===")

if __name__ == '__main__':
    test_django_s3_upload() 