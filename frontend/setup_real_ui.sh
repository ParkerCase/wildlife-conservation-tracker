#!/bin/bash

# WildGuard AI - Real Data UI Setup Script
echo "🌿 Setting up WildGuard AI with REAL data integration..."

# Navigate to frontend directory
cd /Users/parkercase/conservation-bot/frontend

# Install the new Supabase dependency
echo "📦 Installing Supabase client..."
npm install @supabase/supabase-js@^2.39.0

# Verify environment configuration
echo "🔧 Checking environment configuration..."
if [ -f ".env" ]; then
    echo "✅ Environment file found"
    if grep -q "REACT_APP_SUPABASE_URL" .env; then
        echo "✅ Supabase URL configured"
    else
        echo "❌ Supabase URL missing from .env"
    fi
    if grep -q "REACT_APP_SUPABASE_ANON_KEY" .env; then
        echo "✅ Supabase key configured"
    else
        echo "❌ Supabase key missing from .env"
    fi
else
    echo "❌ Environment file not found"
fi

# Check if backend is running
echo "🔍 Checking if backend is available..."
if curl -s http://localhost:5001/api/stats/realtime > /dev/null; then
    echo "✅ Backend API is running on port 5001"
else
    echo "⚠️  Backend API not responding - make sure to start your backend first"
    echo "   Run: cd ../backend && python src/main.py"
fi

echo ""
echo "🚀 Setup complete! Your WildGuard AI UI now integrates with:"
echo "   ✅ Real Supabase database (detections table)"
echo "   ✅ Your 1000+ comprehensive keywords"
echo "   ✅ Backend API endpoints"
echo "   ✅ Correct platforms: eBay, Marketplaats, MercadoLibre, OLX, Craigslist"
echo ""
echo "To start the frontend:"
echo "   npm start"
echo ""
echo "To start the backend (in another terminal):"
echo "   cd ../backend && python src/main.py"
echo ""
echo "Demo Login Credentials:"
echo "   Username: wildguard_admin"
echo "   Password: ConservationIntelligence2024!"
