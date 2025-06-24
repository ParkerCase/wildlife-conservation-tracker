#!/bin/bash

echo "🚀 WildGuard AI - Vercel Deployment Fix Script"
echo "============================================="

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

print_info "Fixing Vercel deployment configuration..."

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    print_error "Must be run from project root directory"
    exit 1
fi

cd frontend

# Create or update vercel.json with secure configuration
print_info "Creating secure vercel.json configuration..."

cat > vercel.json << 'EOL'
{
  "version": 2,
  "name": "wildguard-frontend",
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
    "REACT_APP_SUPABASE_URL": "@react_app_supabase_url",
    "REACT_APP_SUPABASE_ANON_KEY": "@react_app_supabase_anon_key",
    "REACT_APP_ENABLE_MULTILINGUAL": "true",
    "REACT_APP_ENABLE_REAL_TIME": "true",
    "REACT_APP_ENABLE_EXPORTS": "true"
  }
}
EOL

print_success "vercel.json created with secure environment variable references"

print_info "Next steps for secure deployment:"
echo ""
echo "1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables"
echo "2. Add these variables:"
echo ""
echo "   REACT_APP_SUPABASE_URL = YOUR_SUPABASE_URL"
echo "   REACT_APP_SUPABASE_ANON_KEY = YOUR_SUPABASE_ANON_KEY"
echo ""
print_warning "SECURITY: Never put real credentials in vercel.json or source code!"
echo ""
echo "3. Get your credentials from Supabase Dashboard → Settings → API"
echo "4. Redeploy your project to apply the environment variables"

print_success "Vercel deployment configuration fixed securely!"

cd ..

print_info "📖 For detailed setup instructions, see SECURITY_SETUP.md"
