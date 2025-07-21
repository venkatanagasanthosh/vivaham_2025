#!/usr/bin/env python3
"""
Test script to check photo upload endpoints
"""
import requests
import tempfile
import os

def test_upload_endpoint(base_url, description):
    """Test photo upload endpoint"""
    print(f"\n=== Testing {description} ===")
    print(f"URL: {base_url}")
    
    # Create a test image file
    test_content = b"fake_image_data_for_testing"
    
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
        tmp_file.write(test_content)
        tmp_file_path = tmp_file.name
    
    try:
        # Test the upload endpoint
        url = f"{base_url}/me/profile/upload-photos/"
        files = {'photo': ('test.jpg', test_content, 'image/jpeg')}
        
        print(f"Sending POST request to: {url}")
        response = requests.post(url, files=files, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code == 401:
            print("❌ Authentication required - this endpoint needs a valid token")
        elif response.status_code in [200, 201]:
            print("✅ Upload endpoint is accessible")
        else:
            print(f"⚠️ Unexpected response code")
            
    except requests.exceptions.ConnectTimeout:
        print("❌ Connection timeout - server not responding")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - server not reachable")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up
        try:
            os.unlink(tmp_file_path)
        except:
            pass

def main():
    """Test both local and production endpoints"""
    print("🔍 Testing Photo Upload Endpoints")
    
    # Test local development
    test_upload_endpoint(
        "http://192.168.29.191:8000/api",
        "Local Development (192.168.29.191:8000)"
    )
    
    # Test local development on localhost
    test_upload_endpoint(
        "http://localhost:8000/api",
        "Local Development (localhost:8000)"
    )
    
    # Test production
    test_upload_endpoint(
        "https://vivaham2025-production.up.railway.app/api",
        "Production Railway"
    )
    
    print(f"\n=== Test Complete ===")

if __name__ == "__main__":
    main() 