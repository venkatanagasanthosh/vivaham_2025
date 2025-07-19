# Railway AWS S3 Environment Variables Setup

## Required Environment Variables

Add these environment variables to your Railway project:

### 1. AWS_ACCESS_KEY_ID
- **Description**: Your AWS Access Key ID
- **Value**: Your AWS IAM user's access key ID
- **Example**: `AKIAIOSFODNN7EXAMPLE`

### 2. AWS_SECRET_ACCESS_KEY
- **Description**: Your AWS Secret Access Key
- **Value**: Your AWS IAM user's secret access key
- **Example**: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

### 3. AWS_STORAGE_BUCKET_NAME
- **Description**: Your S3 bucket name
- **Value**: The name of your S3 bucket
- **Example**: `vivaham-media-bucket`

### 4. AWS_S3_REGION_NAME
- **Description**: Your S3 bucket region
- **Value**: The AWS region where your bucket is located
- **Example**: `ap-south-1`

## How to Add Environment Variables in Railway:

1. Go to your Railway project dashboard
2. Click on your service (backend)
3. Go to the "Variables" tab
4. Click "New Variable" for each of the above variables
5. Enter the variable name and value
6. Click "Add"

## AWS S3 Bucket Setup:

### 1. Create S3 Bucket:
```bash
# Using AWS CLI (optional)
aws s3 mb s3://your-bucket-name --region ap-south-1
```

### 2. Configure Bucket Permissions:
- Go to S3 Console → Your Bucket → Permissions
- Update bucket policy for public read access (if needed):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::your-bucket-name/*"
        }
    ]
}
```

### 3. CORS Configuration (if needed):
```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "POST", "PUT", "DELETE"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": []
    }
]
```

## IAM User Permissions:

Create an IAM user with this policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name",
                "arn:aws:s3:::your-bucket-name/*"
            ]
        }
    ]
}
```

## Testing the Configuration:

After setting up the environment variables, your Django app will automatically use S3 for file storage. You can test by:

1. Uploading a file through your API
2. Checking if it appears in your S3 bucket
3. Verifying the file URL is accessible

## Security Notes:

- Never commit AWS credentials to version control
- Use IAM roles when possible instead of access keys
- Regularly rotate your access keys
- Use the principle of least privilege for IAM permissions 