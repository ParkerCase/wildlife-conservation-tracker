#!/bin/bash

# WildGuard AI - Quick Local Setup for Testing
# Creates environment files with placeholder values for testing

echo "🔧 WildGuard AI - Quick Local Setup"
echo "=================================="

# Colors
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

# Check if we're in the project root
if [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    echo -e "${RED}❌ Must be run from the project root directory${NC}"
    exit 1
fi

print_info "Setting up environment files for local testing..."

# Frontend environment setup
if [ ! -f "frontend/.env" ]; then
    print_info "Creating frontend/.env from example..."
    cp frontend/.env.example frontend/.env
    print_success "Frontend .env created"
    print_warning "Please edit frontend/.env with your actual Supabase credentials"
else
    print_success "Frontend .env already exists"
fi

# Backend environment setup  
if [ ! -f "backend/.env" ]; then
    print_info "Creating backend/.env from example..."
    cp backend/.env.example backend/.env
    print_success "Backend .env created"
    print_warning "Please edit backend/.env with your actual Supabase credentials"
else
    print_success "Backend .env already exists"
fi

echo ""
print_info "📝 NEXT STEPS:"
echo "1. Edit frontend/.env with your Supabase credentials:"
echo "   - REACT_APP_SUPABASE_URL=https://your-project.supabase.co"
echo "   - REACT_APP_SUPABASE_ANON_KEY=your_supabase_anon_key"
echo ""
echo "2. Edit backend/.env with the same credentials:"
echo "   - SUPABASE_URL=https://your-project.supabase.co"
echo "   - SUPABASE_ANON_KEY=your_supabase_anon_key"
echo ""
echo "3. Get credentials from Supabase Dashboard → Settings → API"
echo ""
echo "4. Start the system: ./start_wildguard.sh"

echo ""
print_info "📖 Detailed instructions: See SECURITY_SETUP.md"

echo ""
if [ -f "frontend/.env" ] && [ -f "backend/.env" ]; then
    print_success "🎉 Environment files ready! Configure credentials and run ./start_wildguard.sh"
else
    print_warning "Environment setup incomplete"
fi
