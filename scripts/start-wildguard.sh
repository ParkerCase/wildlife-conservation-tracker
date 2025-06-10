#!/bin/bash

echo "🚀 Starting WildGuard AI Platform..."
echo "==============================================="

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $1 is already in use"
        return 1
    else
        return 0
    fi
}

# Function to kill process on port
kill_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "🔄 Killing process on port $1..."
        lsof -ti:$1 | xargs kill -9
        sleep 2
    fi
}

# Check and clean ports
echo "🔍 Checking ports..."
kill_port 5000
kill_port 3000
kill_port 3001

# Set up environment
echo "🔧 Setting up environment..."
cd "$(dirname "$0")/.."

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend/.env file..."
    cat > backend/.env << EOF
# WildGuard AI Backend Configuration
ANTHROPIC_API_KEY=demo_key
EBAY_APP_ID=demo_app_id
EBAY_DEV_ID=demo_dev_id
EBAY_CERT_ID=demo_cert_id
SUPABASE_URL=https://demo.supabase.co
SUPABASE_KEY=demo_key
FLASK_ENV=development
FLASK_DEBUG=True
SCAN_INTERVAL_MINUTES=15
DASHBOARD_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
EOF
fi

# Install frontend dependencies if needed
echo "📦 Checking frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "🔄 Installing frontend dependencies..."
    npm install
fi

# Install backend dependencies if needed
echo "📦 Checking backend dependencies..."
cd ../backend
if [ ! -d "venv" ]; then
    echo "🔄 Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "🔄 Activating virtual environment..."
source venv/bin/activate

echo "🔄 Installing backend dependencies..."
pip install -r requirements.txt

# Start backend
echo "🖥️  Starting backend server..."
cd ..
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python backend/src/api/app.py &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Test backend
echo "🧪 Testing backend connection..."
if curl -s http://localhost:5000/health > /dev/null; then
    echo "✅ Backend is running on http://localhost:5000"
else
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Start frontend
echo "🌐 Starting frontend..."
cd frontend
export PORT=3000
npm start &
FRONTEND_PID=$!

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 10

echo ""
echo "🎉 WildGuard AI Platform Started Successfully!"
echo "==============================================="
echo "📊 Frontend Dashboard: http://localhost:3000"
echo "🔗 Backend API: http://localhost:5000"
echo "🏥 Health Check: http://localhost:5000/health"
echo "📋 API Status: http://localhost:5000/api/stats/realtime"
echo ""
echo "💡 Press Ctrl+C to stop all services"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping WildGuard AI services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    kill_port 5000
    kill_port 3000
    echo "✅ All services stopped"
    exit 0
}

# Trap Ctrl+C and call cleanup
trap cleanup INT

# Wait for processes
wait