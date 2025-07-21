# Railway S3 Setup - Fix Image Upload Issue

## Problem
- Images upload successfully but don't appear in S3 bucket
- Flask app shows 404 errors when loading image URLs
- Production (Railway) not configured with S3 environment variables

## Solution: Add Environment Variables to Railway

### Step 1: Access Railway Dashboard
1. Go to [railway.app](https://railway.app)
2. Open your `vivaham` project
3. Click on your **backend service**
4. Click on **"Variables"** tab

### Step 2: Add These 4 Environment Variables

**Click "New Variable" for each one:**

| Variable Name | Variable Value |
|---------------|----------------|
| `AWS_ACCESS_KEY_ID` | `AKIA2K4GQ6QQCVIVPIMF` |
| `AWS_SECRET_ACCESS_KEY` | `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` |
| `AWS_STORAGE_BUCKET_NAME` | `storageofprofiles` |
| `AWS_S3_REGION_NAME` | `ap-south-1` |

### Step 3: Deploy the Updated Code
After adding the variables, Railway will automatically redeploy. If not:
1. Click **"Deploy"** button
2. Wait for deployment to complete

## How to Verify It's Working

### Option 1: Check Debug Endpoint
Visit: `https://your-railway-url/api/debug/environment/`

You should see:
```json
{
  "environment_check": {
    "AWS_ACCESS_KEY_ID_set": true,
    "AWS_SECRET_ACCESS_KEY_set": true,
    "AWS_STORAGE_BUCKET_NAME_set": true,
    "AWS_S3_REGION_NAME_set": true,
    "all_aws_vars_set": true
  },
  "django_settings": {
    "DEFAULT_FILE_STORAGE": "storages.backends.s3boto3.S3Boto3Storage",
    "MEDIA_URL": "https://storageofprofiles.s3.amazonaws.com/"
  }
}
```

### Option 2: Test Photo Upload
1. Upload a photo through your Flutter app
2. Check your S3 bucket - the photo should appear
3. Photo should load correctly in the app (no more 404 errors)

### Option 3: Check Railway Logs
In Railway dashboard, click **"View Logs"**. You should see:
```
Production S3 Configuration: Using S3 bucket storageofprofiles in region ap-south-1
```

## Expected Results After Fix

✅ **Before Fix (Current Issue):**
- Upload shows "success" but no file in S3
- 404 errors when loading images
- Images only work on development device

✅ **After Fix:**
- Photos actually upload to S3 bucket
- Images load correctly on all devices
- No more 404 errors

## Troubleshooting

### If images still don't upload to S3:
1. Double-check environment variable names (case-sensitive)
2. Verify Railway has redeployed after adding variables
3. Check Railway logs for error messages
4. Test the debug endpoint to confirm variables are set

### If Railway won't redeploy:
1. Make a small change to any file
2. Commit and push to trigger deployment
3. Or manually click "Deploy" in Railway

### Cost Monitoring:
- Your current S3 usage is minimal (few MB)
- Current budget limit: $2
- Monitor usage in AWS console

## Security Notes

⚠️ **IMPORTANT:** These are test credentials with limited permissions
- Only has access to the `storageofprofiles` bucket
- No access to other AWS services
- Consider rotating credentials after testing

## Next Steps After Testing

1. ✅ Verify photo uploads work
2. ✅ Test on multiple devices
3. 🔄 Consider creating dedicated IAM user for production
4. 🔄 Set up automated backups if needed 