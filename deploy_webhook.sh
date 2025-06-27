#!/bin/bash

# eBay Webhook Deployment Script
# This script helps deploy the webhook endpoints to Vercel

echo "🚀 Deploying eBay Webhook Endpoints to Vercel"
echo "=============================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI is not installed. Please install it first:"
    echo "   npm i -g vercel"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ vercel.json not found. Please run this script from the project root."
    exit 1
fi

# Check if API directory exists
if [ ! -d "api" ]; then
    echo "❌ API directory not found. Please ensure the webhook files are created."
    exit 1
fi

echo "✅ Pre-deployment checks passed"

# Deploy to Vercel
echo "📦 Deploying to Vercel..."
vercel --prod

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Deployment successful!"
    echo ""
    echo "🔗 Your webhook endpoints are now available at:"
    echo "   Main webhook: https://your-domain.vercel.app/api/webhook/ebay/"
    echo "   Account deletion: https://your-domain.vercel.app/api/webhook/ebay/account-deletion"
    echo "   Test endpoint: https://your-domain.vercel.app/api/webhook/ebay/test"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Replace 'your-domain' with your actual Vercel domain"
    echo "   2. Update your eBay application webhook URL"
    echo "   3. Test the webhook endpoints"
    echo "   4. Monitor for successful deliveries"
    echo ""
    echo "📖 See EBAY_WEBHOOK_SETUP.md for detailed instructions"
else
    echo "❌ Deployment failed. Please check the error messages above."
    exit 1
fi 