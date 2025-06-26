#!/bin/bash

echo "🔧 WildGuard AI - Build Debug Script"
echo "=================================="

echo "📦 Cleaning previous builds..."
rm -rf build/
rm -rf node_modules/.cache/

echo "🏗️  Building production version..."
npm run build

echo "📊 Checking build output..."
if [ -d "build" ]; then
    echo "✅ Build directory created"
    echo "📁 Build contents:"
    ls -la build/
    
    if [ -f "build/index.html" ]; then
        echo "✅ index.html exists"
    else
        echo "❌ index.html missing"
    fi
    
    if [ -d "build/static" ]; then
        echo "✅ static directory exists"
        echo "📁 Static contents:"
        ls -la build/static/
    else
        echo "❌ static directory missing"
    fi
else
    echo "❌ Build failed - no build directory"
    exit 1
fi

echo "🚀 Build completed successfully!"