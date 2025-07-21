#!/usr/bin/env python3
"""
Test Railway photo upload with realistic small file
"""
import requests
import tempfile
import os
from PIL import Image
import io

def create_test_image(width=100, height=100, format='JPEG'):
    """Create a small test image"""
    # Create a simple colored image
    img = Image.new('RGB', (width, height), color='red')
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format=format)
    img_bytes.seek(0)
    
    return img_bytes.getvalue()

def test_railway_upload():
    """Test Railway upload endpoint with small image"""
    print("🧪 Testing Railway Photo Upload")
    
    # Create a very small test image (should be < 5MB)
    try:
        test_image = create_test_image(200, 200, 'JPEG')
        print(f"✅ Created test image: {len(test_image)} bytes")
    except Exception as e:
        print(f"❌ Failed to create test image: {e}")
        return
    
    # Test Railway endpoint
    url = "https://vivaham2025-production.up.railway.app/api/me/profile/upload-photos/"
    files = {'photo': ('test.jpg', test_image, 'image/jpeg')}
    
    print(f"📤 Sending test upload to: {url}")
    print(f"📊 File size: {len(test_image)} bytes")
    
    try:
        response = requests.post(url, files=files, timeout=30)
        
        print(f"📋 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text[:500]}...")
        
        if response.status_code == 401:
            print("✅ Good! Endpoint is accessible (authentication required)")
        elif response.status_code == 400:
            if "Failed to process uploaded files" in response.text:
                print("❌ Still having multipart parsing issues")
            else:
                print("✅ Multipart parsing works! (Got validation error instead)")
        elif response.status_code in [200, 201]:
            print("✅ Upload successful!")
        else:
            print(f"⚠️ Unexpected response: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    
    print("🏁 Test complete")

if __name__ == "__main__":
    test_railway_upload() 