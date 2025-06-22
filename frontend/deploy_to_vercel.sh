#!/bin/bash

echo "🚀 Deploying WildGuard AI to Vercel..."

# Navigate to frontend directory
cd /Users/parkercase/conservation-bot/frontend

# Add and commit the vercel.json fix
echo "📝 Committing Vercel configuration fix..."
git add vercel.json .env.production
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
echo "   Value: https://hgnefrvllutcagdutcaa.supabase.co"
echo "   Environment: Production, Preview, Development"
echo ""
echo "   Variable Name: REACT_APP_SUPABASE_ANON_KEY"
echo "   Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhnbmVmcnZsbHV0Y2FnZHV0Y2FhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkzMjU4NzcsImV4cCI6MjA2NDkwMTg3N30.ftaP4Xa1vTXumTlcPy0OwdG1s-4JSYz10-ENiWB_QZ0"
echo "   Environment: Production, Preview, Development"
echo ""
echo "5. Click 'Redeploy' to trigger a new build with the environment variables"
echo ""
echo "🌐 Your sites:"
echo "   → https://conservatron.vercel.app"
echo "   → https://conservatron.parkercase.co"
echo ""
echo "🔐 Demo Login:"
echo "   Username: wildguard_admin"
echo "   Password: ConservationIntelligence2024!"
