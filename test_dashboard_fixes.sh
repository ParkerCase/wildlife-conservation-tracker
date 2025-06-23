#!/bin/bash

echo "🔧 Testing WildGuard Dashboard Fixes..."
echo ""

# Navigate to frontend directory
cd /Users/parkercase/conservation-bot/frontend

echo "📦 Installing dependencies..."
npm install

echo ""
echo "🧪 Testing build process..."
npm run build

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful! All React errors should be resolved."
    echo ""
    echo "🚀 Starting development server..."
    echo "   Navigate to http://localhost:3000 to test the dashboard"
    echo ""
    echo "🔍 What to test:"
    echo "   1. Mission Control: Try the time range dropdown"
    echo "   2. Threats: Should load without timeout errors"
    echo "   3. Evidence Archive: Should show 50+ evidence items"
    echo "   4. Analytics: Charts should render properly"
    echo "   5. Intelligence Reports: Should show real data"
    echo ""
    npm start
else
    echo ""
    echo "❌ Build failed. Check the error messages above."
    echo "   Most likely issues:"
    echo "   - Missing dependencies"
    echo "   - Syntax errors in components"
    echo "   - Import/export issues"
fi
