#!/bin/bash
echo "🔍 Testing WildGuard AI connection..."

# Test backend
echo "Testing backend API..."
if curl -s http://localhost:5000/health > /dev/null; then
    echo "✅ Backend is running"
else
    echo "❌ Backend is not responding"
fi

# Test dashboard API
echo "Testing dashboard API..."
if curl -s http://localhost:5000/api/stats/realtime > /dev/null; then
    echo "✅ Dashboard API is working"
else
    echo "❌ Dashboard API is not responding"
fi

# Test frontend
echo "Testing frontend..."
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is running"
else
    echo "❌ Frontend is not responding"
fi
