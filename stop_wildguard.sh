#!/bin/bash

# WildGuard AI - System Stop Script
# Gracefully stops backend and frontend services

echo "🛑 WildGuard AI - Stopping System Services"
echo "=========================================="

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

# Function to kill process if it exists
kill_process() {
    if [ ! -z "$1" ] && kill -0 $1 2>/dev/null; then
        kill $1 2>/dev/null
        sleep 2
        if kill -0 $1 2>/dev/null; then
            kill -9 $1 2>/dev/null
        fi
        return 0
    else
        return 1
    fi
}

# Read process IDs if they exist
if [ -f ".wildguard_processes" ]; then
    source .wildguard_processes
    
    print_info "Stopping tracked processes..."
    
    if kill_process $BACKEND_PID; then
        print_success "Backend server stopped (PID: $BACKEND_PID)"
    else
        print_warning "Backend process not found or already stopped"
    fi
    
    if kill_process $FRONTEND_PID; then
        print_success "Frontend server stopped (PID: $FRONTEND_PID)"
    else
        print_warning "Frontend process not found or already stopped"
    fi
    
    # Clean up process file
    rm .wildguard_processes
    print_success "Process tracking file cleaned up"
else
    print_warning "No process tracking file found"
fi

# Kill any remaining processes on ports 3000 and 5000
print_info "Checking for remaining processes on ports 3000 and 5000..."

# Kill processes on port 3000 (React frontend)
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    print_info "Stopping processes on port 3000..."
    lsof -ti:3000 | xargs kill -9 2>/dev/null
    print_success "Port 3000 freed"
else
    print_info "Port 3000 is already free"
fi

# Kill processes on port 5000 (Python backend)
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
    print_info "Stopping processes on port 5000..."
    lsof -ti:5000 | xargs kill -9 2>/dev/null
    print_success "Port 5000 freed"
else
    print_info "Port 5000 is already free"
fi

# Kill any remaining Node.js processes related to WildGuard
print_info "Cleaning up any remaining WildGuard processes..."
pkill -f "react-scripts" 2>/dev/null || true
pkill -f "wildguard" 2>/dev/null || true
pkill -f "real_data_server" 2>/dev/null || true

echo ""
echo "✅ WILDGUARD AI SERVICES STOPPED"
echo "================================"
print_success "All WildGuard AI services have been stopped"
print_success "Ports 3000 and 5000 are now available"
print_success "System resources have been freed"

echo ""
echo "🔧 TO RESTART WILDGUARD AI:"
echo "./start_wildguard.sh"

echo ""
print_info "System shutdown complete!"
