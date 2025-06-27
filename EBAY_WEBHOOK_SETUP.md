# eBay Webhook Setup Guide

## Overview

This guide will help you set up the eBay webhook endpoints and update your eBay application settings to resolve the compliance issue.

## Current Issue

eBay has notified you that your webhook endpoint `https://wildlife-conservation-tracker-production.up.railway.app/webhook/ebay/account-deletion` is no longer responding. You need to update this to your new Vercel deployment.

## Solution

### 1. Deploy to Vercel

First, deploy your updated codebase to Vercel:

```bash
# Make sure you're in the project root
cd /Users/parkercase/conservation-bot

# Deploy to Vercel
vercel --prod
```

### 2. Get Your New Webhook URL

After deployment, your new webhook URLs will be:

- **Main webhook endpoint**: `https://conservatron.parkercase.co/api/webhook/ebay/`
- **Account deletion specific**: `https://conservatron.parkercase.co/api/webhook/ebay/account-deletion`
- **Test endpoint**: `https://conservatron.parkercase.co/api/webhook/ebay/test`
- **Verification endpoint**: `https://conservatron.parkercase.co/api/webhook/ebay/verification`

### 3. Generate Verification Token

eBay requires a verification token between 32-80 characters. Generate one:

```bash
# Generate a secure verification token
openssl rand -base64 48 | tr -d "=+/" | cut -c1-64
```

Or use this pre-generated token:

```
WildGuardAI_2024_Webhook_Verification_Token_For_eBay_Integration_Security
```

### 4. Test the Webhook

Before updating eBay, test your webhook:

```bash
# Test GET request
curl https://conservatron.parkercase.co/api/webhook/ebay/test

# Test POST request
curl -X POST https://conservatron.parkercase.co/api/webhook/ebay/test \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# Test verification endpoint
curl "https://conservatron.parkercase.co/api/webhook/ebay/verification?challenge_code=test123"
```

### 5. Update eBay Application Settings

1. **Log into eBay Developer Portal**:

   - Go to https://developer.ebay.com/
   - Sign in with your eBay developer account

2. **Navigate to Your Application**:

   - Go to "My Account" → "Application Keys"
   - Find your application (likely "Wildlife Conservation Tracker" or similar)

3. **Update Webhook URL**:

   - Look for "Notification URL" or "Webhook URL" settings
   - Replace the old Railway URL with your new Vercel URL:
     ```
     OLD: https://wildlife-conservation-tracker-production.up.railway.app/webhook/ebay/account-deletion
     NEW: https://conservatron.parkercase.co/api/webhook/ebay/account-deletion
     ```

4. **Add Verification Token**:

   - Look for "Verification Token" or "Webhook Verification Token" field
   - Enter the verification token you generated:
     ```
     WildGuardAI_2024_Webhook_Verification_Token_For_eBay_Integration_Security
     ```

5. **Save Changes**:
   - Save the updated webhook URL and verification token
   - eBay will automatically test the new endpoint

### 6. Verify Webhook Registration

After updating, eBay should automatically test your webhook. You can also manually test it:

```bash
# Test the account deletion endpoint specifically
curl -X POST https://conservatron.parkercase.co/api/webhook/ebay/account-deletion \
  -H "Content-Type: application/json" \
  -H "x-ebay-verification-token: WildGuardAI_2024_Webhook_Verification_Token_For_eBay_Integration_Security" \
  -d '{
    "metadata": {
      "topic": "MARKETPLACE_ACCOUNT_DELETION",
      "schemaVersion": "1.0",
      "deprecated": false
    },
    "data": {
      "accountInfo": {
        "accountId": "test-account-123"
      },
      "deletionReason": "Test deletion"
    },
    "eventId": "test-event-123",
    "eventDate": "2024-01-01T00:00:00.000Z",
    "publishDate": "2024-01-01T00:00:00.000Z",
    "publishAttemptCount": 1,
    "topic": "MARKETPLACE_ACCOUNT_DELETION"
  }'
```

### 7. Monitor Webhook Activity

Check your Vercel function logs to ensure webhooks are being received:

1. Go to your Vercel dashboard
2. Select your project
3. Go to "Functions" tab
4. Check the logs for `/api/webhook/ebay/` function

### 8. Compliance Timeline

- **Immediate**: Update the webhook URL and verification token in eBay Developer Portal
- **Within 24 hours**: eBay should start sending notifications to the new endpoint
- **Within 30 days**: eBay will verify the endpoint is working properly

## Webhook Endpoints Created

### 1. Main Webhook Handler (`/api/webhook/ebay/`)

- Handles all types of eBay notifications
- Routes to specific handlers based on topic
- Supports: account deletion, item sold, item updated, item ended
- Includes verification token validation

### 2. Account Deletion Specific (`/api/webhook/ebay/account-deletion`)

- Dedicated endpoint for account deletion notifications
- Matches the exact URL mentioned in the eBay email
- Includes verification token validation

### 3. Test Endpoint (`/api/webhook/ebay/test`)

- For testing webhook accessibility
- Supports both GET and POST requests
- Useful for debugging

### 4. Verification Endpoint (`/api/webhook/ebay/verification`)

- Handles eBay's webhook verification process
- Supports challenge-response verification
- Required for webhook validation

## Webhook Data Structure

eBay sends webhooks in this format:

```json
{
  "metadata": {
    "topic": "MARKETPLACE_ACCOUNT_DELETION",
    "schemaVersion": "1.0",
    "deprecated": false
  },
  "data": {
    "accountInfo": {
      "accountId": "string"
    },
    "deletionReason": "string"
  },
  "eventId": "string",
  "eventDate": "2024-01-01T00:00:00.000Z",
  "publishDate": "2024-01-01T00:00:00.000Z",
  "publishAttemptCount": 1,
  "topic": "MARKETPLACE_ACCOUNT_DELETION"
}
```

## Verification Token

The verification token is used to:

- Validate that webhooks are coming from eBay
- Ensure webhook security
- Meet eBay's compliance requirements

**Token**: `WildGuardAI_2024_Webhook_Verification_Token_For_eBay_Integration_Security`

## Troubleshooting

### Webhook Not Responding

1. Check Vercel function logs
2. Verify the URL is correct
3. Ensure the function is deployed
4. Test with the test endpoint

### 500 Errors

1. Check function logs for errors
2. Verify JSON parsing
3. Check for missing environment variables

### 404 Errors

1. Verify the API route is correct
2. Check Vercel deployment status
3. Ensure the file structure matches

### Verification Token Issues

1. Ensure the token is between 32-80 characters
2. Check that the token is properly configured in eBay
3. Verify the token is being sent in headers

## Security Considerations

- The webhook endpoints are public but only accept POST requests
- Verification tokens provide additional security
- Monitor webhook logs for suspicious activity
- Implement rate limiting if needed

## Next Steps

1. Deploy the updated code to Vercel
2. Generate and configure the verification token
3. Update your eBay application webhook URL and token
4. Test the webhook endpoints
5. Monitor for successful webhook deliveries
6. Consider implementing additional webhook types as needed

## Support

If you encounter issues:

1. Check Vercel function logs
2. Test with the test endpoint
3. Verify eBay application settings
4. Contact eBay Developer Support if needed
