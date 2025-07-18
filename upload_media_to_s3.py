import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# Settings (can be replaced with Django settings import if needed)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'AKIA2K4GQ6QQGKNRX37P')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', 'NUOSIXtUDTQ21jNwLgxy0tLoS4cIukM8pQeeAePF')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'storageofprofiles')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'ap-south-1')

LOCAL_MEDIA_DIR = os.path.join(os.path.dirname(__file__), 'media', 'profile_photos')
S3_PREFIX = 'profile_photos/'

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_S3_REGION_NAME
)

def upload_file(file_path, s3_key):
    try:
        s3_client.upload_file(file_path, AWS_STORAGE_BUCKET_NAME, s3_key)
        print(f"Uploaded: {s3_key}")
        return True
    except (NoCredentialsError, ClientError) as e:
        print(f"Failed to upload {s3_key}: {e}")
        return False

def main():
    if not os.path.exists(LOCAL_MEDIA_DIR):
        print(f"Local media directory does not exist: {LOCAL_MEDIA_DIR}")
        return

    uploaded = 0
    failed = 0
    for filename in os.listdir(LOCAL_MEDIA_DIR):
        local_path = os.path.join(LOCAL_MEDIA_DIR, filename)
        if os.path.isfile(local_path):
            s3_key = S3_PREFIX + filename
            if upload_file(local_path, s3_key):
                uploaded += 1
            else:
                failed += 1

    print(f"\nUpload complete. Success: {uploaded}, Failed: {failed}")

if __name__ == "__main__":
    main()