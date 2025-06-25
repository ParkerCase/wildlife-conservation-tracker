#!/usr/bin/env bash
# Update .env files with real Supabase credentials

echo "🔧 UPDATING .ENV FILES WITH REAL SUPABASE CREDENTIALS"
echo "================================================================"

read -p "Enter your Supabase Project URL (https://yourproject.supabase.co): " SUPABASE_URL
read -p "Enter your Supabase Anon Key (eyJ...): " SUPABASE_KEY

echo ""
echo "📝 Updating frontend/.env..."
sed -i.bak "s|REACT_APP_SUPABASE_URL=.*|REACT_APP_SUPABASE_URL=${SUPABASE_URL}|" frontend/.env
sed -i.bak "s|REACT_APP_SUPABASE_ANON_KEY=.*|REACT_APP_SUPABASE_ANON_KEY=${SUPABASE_KEY}|" frontend/.env

echo "📝 Updating backend/.env..."
sed -i.bak "s|SUPABASE_URL=.*|SUPABASE_URL=${SUPABASE_URL}|" backend/.env
sed -i.bak "s|SUPABASE_ANON_KEY=.*|SUPABASE_ANON_KEY=${SUPABASE_KEY}|" backend/.env

echo ""
echo "✅ Local .env files updated!"
echo ""
echo "🚀 NOW ADD THESE TO GITHUB ACTIONS SECRETS:"
echo "=========================================="
echo "Secret Name: SUPABASE_URL"
echo "Secret Value: ${SUPABASE_URL}"
echo ""
echo "Secret Name: SUPABASE_ANON_KEY" 
echo "Secret Value: ${SUPABASE_KEY}"
echo ""
echo "Secret Name: SUPABASE_KEY"
echo "Secret Value: ${SUPABASE_KEY}"
echo ""
echo "📋 GITHUB SETUP STEPS:"
echo "1. Go to GitHub → Your Repository"
echo "2. Settings → Secrets and variables → Actions"  
echo "3. Click 'New repository secret'"
echo "4. Add each secret above"
echo "5. Re-run your GitHub Actions"
