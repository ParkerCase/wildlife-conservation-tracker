#!/bin/bash

echo "🚀 Deploying WildGuard AI to Vercel..."

# Navigate to frontend directory
cd /Users/parkercase/conservation-bot/frontend

# Add and commit the vercel.json fix
echo "📝 Committing Vercel configuration fix..."
git add vercel.json
git commit -m "Fix Vercel deployment - Update config for React app"

# Push to trigger Vercel rebuild
echo "🚀 Pushing to GitHub to trigger Vercel deployment..."
git push origin main

echo ""
echo "✅ Changes pushed to GitHub!"
echo ""
echo "🔧 NEXT STEPS - Set up Vercel Environment Variables:"
echo ""
echo "1. Go to: https://vercel.com/dashboard"
echo "2. Select your 'wildlife-conservation-tracker' project"
echo "3. Go to Settings → Environment Variables"
echo "4. Add these variables:"
echo ""
echo "   Variable Name: REACT_APP_SUPABASE_URL"
echo "   Value: YOUR_SUPABASE_URL_HERE"
echo "   Environment: Production, Preview, Development"
echo ""
echo "   Variable Name: REACT_APP_SUPABASE_ANON_KEY"
echo "   Value: YOUR_SUPABASE_ANON_KEY_HERE"
echo "   Environment: Production, Preview, Development"
echo ""
echo "5. Click 'Redeploy' to trigger a new build with the environment variables"
echo ""
echo "📖 Get your credentials from:"
echo "   → Supabase Dashboard → Settings → API"
echo "   → Copy Project URL and anon public key"
echo ""
echo "🔒 SECURITY REMINDER:"
echo "   → Never commit real credentials to Git"
echo "   → Use environment variables only"
echo "   → See SECURITY_SETUP.md for details"
