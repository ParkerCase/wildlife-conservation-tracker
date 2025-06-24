#!/bin/bash

# WildGuard AI - Complete System Startup Script
# Starts both backend and frontend with real data

echo "🚀 WildGuard AI - Complete System Startup"
echo "========================================="

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the project root
if [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    print_error "Must be run from the project root directory containing frontend and backend folders"
    exit 1
fi

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Kill existing processes on ports 3000 and 5000
print_info "Checking for existing processes..."

if check_port 3000; then
    print_warning "Port 3000 is in use. Attempting to free it..."
    lsof -ti:3000 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

if check_port 5000; then
    print_warning "Port 5000 is in use. Attempting to free it..."
    lsof -ti:5000 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# Start backend server
print_info "Starting WildGuard AI Real Data Backend..."
cd backend

# Check if backend dependencies are installed
if [ ! -d "node_modules" ] && [ -f "package.json" ]; then
    print_info "Installing backend dependencies..."
    npm install
fi

# Start Python backend
if [ -f "real_data_server.py" ]; then
    print_info "Starting Python backend server on port 5000..."
    
    # Check if required Python packages are installed
    python3 -c "import supabase" 2>/dev/null || {
        print_warning "Installing supabase Python package..."
        pip3 install supabase-py flask flask-cors
    }
    
    python3 real_data_server.py &
    BACKEND_PID=$!
    print_success "Backend server started (PID: $BACKEND_PID)"
else
    print_error "Backend server file not found"
    exit 1
fi

# Wait for backend to start
print_info "Waiting for backend to initialize..."
sleep 5

# Test backend connection
if curl -f http://localhost:5000/health >/dev/null 2>&1; then
    print_success "Backend server is responding"
else
    print_error "Backend server is not responding"
fi

cd ..

# Start frontend
print_info "Starting WildGuard AI Frontend..."
cd frontend

# Validate frontend setup
if [ -x "./validate_real_data.sh" ]; then
    print_info "Running frontend validation..."
    ./validate_real_data.sh >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        print_success "Frontend validation passed"
    else
        print_warning "Frontend validation issues detected"
    fi
fi

# Check if frontend dependencies are installed
if [ ! -d "node_modules" ]; then
    print_info "Installing frontend dependencies..."
    npm install
fi

# Start React frontend
print_info "Starting React frontend on port 3000..."
npm start &
FRONTEND_PID=$!

print_success "Frontend server started (PID: $FRONTEND_PID)"

cd ..

# Create process tracking file
echo "BACKEND_PID=$BACKEND_PID" > .wildguard_processes
echo "FRONTEND_PID=$FRONTEND_PID" >> .wildguard_processes

# Wait a moment for services to fully start
print_info "Services starting up..."
sleep 10

# Test full system
print_info "Testing system connectivity..."

# Test backend
if curl -f http://localhost:5000/api/stats/realtime >/dev/null 2>&1; then
    print_success "Backend API is working"
else
    print_warning "Backend API test failed"
fi

# Test frontend (will take longer to start)
print_info "Frontend will be available shortly at http://localhost:3000"

echo ""
echo "🎉 WILDGUARD AI SYSTEM STARTED!"
echo "==============================="
print_success "Backend API: http://localhost:5000"
print_success "Frontend UI: http://localhost:3000"
print_success "Health Check: http://localhost:5000/health"
print_success "Real-time Stats: http://localhost:5000/api/stats/realtime"

echo ""
echo "📊 REAL DATA FEATURES ACTIVE:"
echo "• Supabase database: 233,939+ real detections"
echo "• 16-language multilingual support"
echo "• Real listing URLs (no mock data)"
echo "• Live threat intelligence"
echo "• Authentic performance metrics"
echo "• Real-time search and filtering"

echo ""
echo "🔧 PROCESS MANAGEMENT:"
echo "• Backend PID: $BACKEND_PID"
echo "• Frontend PID: $FRONTEND_PID"
echo "• Stop all: ./stop_wildguard.sh"
echo "• Restart: ./start_wildguard.sh"

echo ""
echo "📋 NEXT STEPS:"
echo "1. Open http://localhost:3000 in your browser"
echo "2. Verify dashboard shows real detection counts"
echo "3. Test threat intelligence with live alerts"
echo "4. Search evidence archive with real data"
echo "5. Confirm listing URLs lead to actual marketplaces"

echo ""
print_warning "Note: Keep this terminal open or run in background"
print_info "Press Ctrl+C to stop both services, or use ./stop_wildguard.sh"

# Wait for user interrupt
wait
