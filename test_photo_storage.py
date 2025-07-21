#!/usr/bin/env python3
"""
Test what storage backend Photo model actually uses
"""
import os
import sys
import django
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vivaham_backend.settings')
django.setup()

def test_photo_storage():
    """Test actual storage backend used by Photo model"""
    from api.models import Photo, Profile, User
    from django.conf import settings
    
    print("=== Photo Storage Test ===")
    print(f"DEFAULT_FILE_STORAGE setting: {settings.DEFAULT_FILE_STORAGE}")
    print(f"default_storage class: {default_storage.__class__}")
    
    # Create test objects
    user, _ = User.objects.get_or_create(
        username='storage_test',
        defaults={'email': 'test@test.com'}
    )
    profile, _ = Profile.objects.get_or_create(user=user)
    
    # Create a test image content
    test_content = b'test image content for storage test'
    test_file = ContentFile(test_content, name='storage_test.jpg')
    
    # Create photo and check storage
    print(f"\n📤 Creating Photo object...")
    photo = Photo(profile=profile)
    
    # Check the storage BEFORE saving
    field_storage = photo.image.storage
    print(f"Photo.image.storage class: {field_storage.__class__}")
    print(f"Photo.image.storage == default_storage: {field_storage == default_storage}")
    
    # Save the image
    photo.image.save('storage_test.jpg', test_file, save=False)
    photo.save()
    
    # Check storage AFTER saving
    print(f"\n💾 After saving:")
    print(f"Photo ID: {photo.id}")
    print(f"Photo.image.storage class: {photo.image.storage.__class__}")
    print(f"Photo.image.name: {photo.image.name}")
    print(f"Photo.image.url: {photo.image.url}")
    
    # Test if file exists where we expect
    if hasattr(photo.image.storage, 'bucket_name'):
        print(f"✅ Using S3 storage - bucket: {photo.image.storage.bucket_name}")
    else:
        print(f"❌ Using local storage - location: {getattr(photo.image.storage, 'location', 'unknown')}")
    
    # Clean up
    photo.delete()
    print(f"✅ Test photo cleaned up")

if __name__ == "__main__":
    test_photo_storage() 