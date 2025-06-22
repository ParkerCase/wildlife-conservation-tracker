#!/bin/bash

echo "🚨 VERCEL DEPLOYMENT FIX - Complete Reset"
echo "==========================================="
echo ""

# Navigate to the project root (where the frontend is)
cd /Users/parkercase/conservation-bot

# Add a new commit to force Vercel to rebuild
echo "⚡ Creating force rebuild trigger..."
echo "# Force rebuild $(date)" >> README.md
git add .
git commit -m "🚀 Force Vercel rebuild - Deploy React app properly"
git push origin main

echo ""
echo "✅ Forced new commit pushed to GitHub!"
echo ""
echo "🔧 MANUAL VERCEL STEPS (REQUIRED):"
echo ""
echo "1. Go to: https://vercel.com/parker-cases-projects/wildlife-conservation-tracker/settings"
echo ""
echo "2. **IMPORTANT**: Change these Build & Development Settings:"
echo "   Framework Preset: 'Create React App' (NOT Static)"
echo "   Root Directory: 'frontend' (NOT '.')"
echo "   Build Command: 'npm run build'"
echo "   Output Directory: 'build'"
echo "   Install Command: 'npm install'"
echo ""
echo "3. Go to Environment Variables and add:"
echo "   REACT_APP_SUPABASE_URL = https://hgnefrvllutcagdutcaa.supabase.co"
echo "   REACT_APP_SUPABASE_ANON_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhnbmVmcnZsbHV0Y2FnZHV0Y2FhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkzMjU4NzcsImV4cCI6MjA2NDkwMTg3N30.ftaP4Xa1vTXumTlcPy0OwdG1s-4JSYz10-ENiWB_QZ0"
echo ""
echo "4. Click 'Save' and then 'Redeploy'"
echo ""
echo "5. OR Alternative: Delete the Vercel project and reimport it:"
echo "   - Delete: https://vercel.com/parker-cases-projects/wildlife-conservation-tracker/settings/advanced"
echo "   - Reimport: https://vercel.com/new with framework 'Create React App' and root 'frontend'"
echo ""
echo "🌐 After fixing, check:"
echo "   → https://conservatron.vercel.app"
echo "   → https://conservatron.parkercase.co"
echo ""
echo "🔐 Demo Login:"
echo "   Username: wildguard_admin"
echo "   Password: ConservationIntelligence2024!"
