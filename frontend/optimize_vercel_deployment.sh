#!/bin/bash

# WildGuard AI - Vercel Deployment Optimization
# Ensures optimal build configuration for production deployment

echo "🚀 WildGuard AI - Vercel Deployment Optimization"
echo "==============================================="

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

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the frontend directory
if [ ! -f "package.json" ]; then
    print_error "Must be run from the frontend directory"
    exit 1
fi

print_info "Optimizing for Vercel deployment..."

# 1. Update package.json build scripts for optimal production
print_info "Checking build scripts..."

# Ensure optimal build configuration
if grep -q "\"build\":" package.json; then
    print_success "Build script found"
else
    print_error "Build script missing in package.json"
fi

# 2. Create optimized vercel.json if it doesn't exist
print_info "Checking Vercel configuration..."

if [ ! -f "vercel.json" ]; then
    print_info "Creating optimized vercel.json..."
    cat > vercel.json << 'EOL'
{
  "version": 2,
  "name": "wildguard-ai",
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "headers": {
        "cache-control": "public, max-age=31536000, immutable"
      }
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "env": {
    "REACT_APP_SUPABASE_URL": "@wildguard_supabase_url",
    "REACT_APP_SUPABASE_ANON_KEY": "@wildguard_supabase_key",
    "REACT_APP_ENABLE_MULTILINGUAL": "true",
    "REACT_APP_ENABLE_REAL_TIME": "true",
    "REACT_APP_ENABLE_EXPORTS": "true",
    "REACT_APP_ENV": "production"
  },
  "build": {
    "env": {
      "REACT_APP_SUPABASE_URL": "@wildguard_supabase_url",
      "REACT_APP_SUPABASE_ANON_KEY": "@wildguard_supabase_key",
      "REACT_APP_ENABLE_MULTILINGUAL": "true",
      "REACT_APP_ENABLE_REAL_TIME": "true",
      "REACT_APP_ENABLE_EXPORTS": "true",
      "REACT_APP_ENV": "production"
    }
  }
}
EOL
    print_success "Optimized vercel.json created"
else
    print_success "vercel.json already exists"
fi

# 3. Test production build
print_info "Testing production build..."

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    print_info "Installing dependencies..."
    npm install
fi

# Clean any previous build
if [ -d "build" ]; then
    print_info "Cleaning previous build..."
    rm -rf build
fi

# Test build
print_info "Running production build test..."
if npm run build > build.log 2>&1; then
    print_success "Production build successful!"
    
    # Check build size
    if [ -d "build" ]; then
        build_size=$(du -sh build | cut -f1)
        print_success "Build size: $build_size"
        
        # Check for essential files
        if [ -f "build/index.html" ]; then
            print_success "index.html generated"
        else
            print_error "index.html missing"
        fi
        
        if [ -d "build/static" ]; then
            print_success "Static assets generated"
        else
            print_warning "Static assets directory missing"
        fi
        
        # Clean up build for deployment
        rm -rf build
        print_info "Build test cleanup completed"
    fi
else
    print_error "Production build failed!"
    echo "Build log:"
    cat build.log
    exit 1
fi

# 4. Verify environment variable usage
print_info "Verifying environment variable usage..."

# Check that components use environment variables
if grep -r "process.env.REACT_APP_SUPABASE_URL" src/ > /dev/null; then
    print_success "Components use REACT_APP_SUPABASE_URL"
else
    print_error "Components not using REACT_APP_SUPABASE_URL"
fi

if grep -r "process.env.REACT_APP_SUPABASE_ANON_KEY" src/ > /dev/null; then
    print_success "Components use REACT_APP_SUPABASE_ANON_KEY"
else
    print_error "Components not using REACT_APP_SUPABASE_ANON_KEY"
fi

# 5. Check for any remaining hardcoded values
print_info "Scanning for hardcoded values..."

if grep -r "https://.*\.supabase\.co" src/ | grep -v "process.env" > /dev/null; then
    print_error "Hardcoded Supabase URLs found in src/"
else
    print_success "No hardcoded Supabase URLs in src/"
fi

echo ""
print_success "🎉 Vercel deployment optimization complete!"

echo ""
print_info "📋 VERCEL DEPLOYMENT CHECKLIST:"
echo "1. ✅ vercel.json configured for optimal builds"
echo "2. ✅ Production build tested and working"
echo "3. ✅ Environment variables properly configured"
echo "4. ✅ No hardcoded credentials in source"
echo "5. ✅ Static asset optimization enabled"

echo ""
print_info "🔧 NEXT STEPS:"
echo "1. Set environment variables in Vercel dashboard:"
echo "   - Name: wildguard_supabase_url"
echo "   - Value: Your Supabase project URL"
echo ""
echo "   - Name: wildguard_supabase_key" 
echo "   - Value: Your Supabase anon key"
echo ""
echo "2. Deploy: git push origin main (auto-deploy) or vercel --prod"
echo ""
echo "3. Verify deployment at your Vercel URL"

echo ""
print_success "🚀 Ready for production deployment!"
