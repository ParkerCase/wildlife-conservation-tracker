#!/bin/bash

echo "🎨 Installing Professional WildGuard AI UI"
echo "=========================================="

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

cd frontend

echo "🧹 Cleaning up old dependencies..."
rm -rf node_modules package-lock.json

echo "📦 Installing professional UI dependencies..."
npm install \
  @nivo/core@^0.84.0 \
  @nivo/line@^0.84.0 \
  @nivo/bar@^0.84.0 \
  @nivo/pie@^0.84.0 \
  @nivo/stream@^0.84.0 \
  @nivo/radar@^0.84.0 \
  @nivo/heatmap@^0.84.0 \
  react-router-dom@^6.8.0 \
  framer-motion@^10.16.0 \
  react-hot-toast@^2.4.1 \
  date-fns@^2.30.0 \
  clsx@^2.0.0 \
  --legacy-peer-deps

echo "✅ Dependencies installed successfully!"
echo ""
echo "🚀 To start the professional UI:"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "🎉 Your new UI includes:"
echo "   • Beautiful modern charts (Nivo)"
echo "   • Smooth animations (Framer Motion)"
echo "   • Professional notifications"
echo "   • Multi-page navigation"
echo "   • Enterprise-grade design"
echo "   • Mobile responsive layout"
echo ""
echo "💡 Make sure your backend is running on port 5001!"