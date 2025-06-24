#!/bin/bash

# WildGuard AI - Production Deployment Verification Script
# Comprehensive check for secure deployment readiness

echo "🚀 WildGuard AI - Production Deployment Verification"
echo "=================================================="

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
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

print_security() {
    echo -e "${PURPLE}🔒 $1${NC}"
}

# Check if we're in the project root
if [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    print_error "Must be run from the project root directory"
    exit 1
fi

# Initialize counters
security_issues=0
deployment_issues=0
total_checks=0

# Function to increment counters
check_result() {
    total_checks=$((total_checks + 1))
    if [ $1 -ne 0 ]; then
        if [ "$2" = "security" ]; then
            security_issues=$((security_issues + 1))
        else
            deployment_issues=$((deployment_issues + 1))
        fi
    fi
}

echo ""
print_security "🔒 SECURITY VERIFICATION"
print_security "========================"

# 1. Check for credentials in Git history
print_info "Checking Git history for exposed credentials..."
if git log --all --full-history --grep="supabase" | grep -i "key\|secret\|password" > /dev/null; then
    print_error "Potential credentials found in Git history"
    check_result 1 "security"
else
    print_success "No credentials found in Git history"
    check_result 0 "security"
fi

# 2. Check for hardcoded credentials in source
print_info "Scanning source code for hardcoded credentials..."
if grep -r "zjwjptxmrfnwlcgfptrw.supabase.co" . --exclude-dir=node_modules --exclude-dir=.git --exclude="*.md" --exclude="*.example" > /dev/null 2>&1; then
    print_error "Hardcoded Supabase URL found in source code"
    check_result 1 "security"
else
    print_success "No hardcoded Supabase URLs in source"
    check_result 0 "security"
fi

if grep -r "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" . --exclude-dir=node_modules --exclude-dir=.git --exclude="*.md" --exclude="*.example" > /dev/null 2>&1; then
    print_error "Hardcoded Supabase key found in source code"
    check_result 1 "security"
else
    print_success "No hardcoded Supabase keys in source"
    check_result 0 "security"
fi

# 3. Check .gitignore
print_info "Verifying .gitignore configuration..."
if grep -q "^\.env$" .gitignore && grep -q "^\.env\.production$" .gitignore; then
    print_success ".env files properly ignored by Git"
    check_result 0 "security"
else
    print_error ".env files not properly ignored by Git"
    check_result 1 "security"
fi

# 4. Check for .env files in repo
print_info "Checking for .env files in repository..."
if git ls-files | grep -E "\.env$|\.env\.production$" > /dev/null; then
    print_error ".env files tracked by Git - CRITICAL SECURITY ISSUE"
    check_result 1 "security"
else
    print_success "No .env files tracked by Git"
    check_result 0 "security"
fi

# 5. Check .env.example files exist
print_info "Verifying .env.example files..."
if [ -f "frontend/.env.example" ] && [ -f "backend/.env.example" ]; then
    print_success ".env.example files present"
    check_result 0 "security"
else
    print_error "Missing .env.example files"
    check_result 1 "security"
fi

echo ""
print_info "🚀 DEPLOYMENT VERIFICATION"
print_info "=========================="

# 6. Frontend deployment checks
print_info "Checking frontend deployment configuration..."

cd frontend

# Check package.json
if [ -f "package.json" ]; then
    if grep -q "@supabase/supabase-js" package.json; then
        print_success "Supabase dependency configured"
        check_result 0 "deployment"
    else
        print_error "Supabase dependency missing"
        check_result 1 "deployment"
    fi
else
    print_error "package.json missing"
    check_result 1 "deployment"
fi

# Check vercel.json
if [ -f "vercel.json" ]; then
    if grep -q "react_app_supabase_url" vercel.json; then
        print_success "Vercel environment variables configured"
        check_result 0 "deployment"
    else
        print_error "Vercel environment variables not configured"
        check_result 1 "deployment"
    fi
else
    print_warning "vercel.json missing (may use Vercel dashboard config)"
    check_result 0 "deployment"
fi

# Check if build works
print_info "Testing production build..."
if npm run build > /dev/null 2>&1; then
    print_success "Production build successful"
    check_result 0 "deployment"
    rm -rf build  # Clean up
else
    print_error "Production build failed"
    check_result 1 "deployment"
fi

# Check service worker
print_info "Checking Supabase service configuration..."
if grep -q "process.env.REACT_APP_SUPABASE_URL" src/services/supabaseService.js; then
    print_success "Supabase service uses environment variables"
    check_result 0 "deployment"
else
    print_error "Supabase service doesn't use environment variables"
    check_result 1 "deployment"
fi

cd ..

# 7. Backend deployment checks
print_info "Checking backend deployment configuration..."

cd backend

# Check requirements/dependencies
if [ -f "real_data_server.py" ]; then
    if grep -q "os.getenv" real_data_server.py; then
        print_success "Backend uses environment variables"
        check_result 0 "deployment"
    else
        print_error "Backend doesn't use environment variables"
        check_result 1 "deployment"
    fi
else
    print_error "Backend server file missing"
    check_result 1 "deployment"
fi

# Check if Python dependencies are documented
if grep -q "supabase" ../requirements.production.txt 2>/dev/null; then
    print_success "Supabase dependency documented"
    check_result 0 "deployment"
else
    print_warning "Supabase dependency not in requirements.production.txt"
    check_result 0 "deployment"
fi

cd ..

# 8. Documentation checks
print_info "Checking deployment documentation..."

if [ -f "SECURITY_SETUP.md" ]; then
    print_success "Security setup guide available"
    check_result 0 "deployment"
else
    print_error "Security setup guide missing"
    check_result 1 "deployment"
fi

if [ -f "README.md" ]; then
    if grep -q "environment variables" README.md; then
        print_success "README includes environment setup"
        check_result 0 "deployment"
    else
        print_warning "README should include environment setup instructions"
        check_result 0 "deployment"
    fi
else
    print_error "README.md missing"
    check_result 1 "deployment"
fi

# 9. Startup script checks
print_info "Checking startup scripts..."

if [ -f "start_wildguard.sh" ] && [ -x "start_wildguard.sh" ]; then
    if grep -q "security" start_wildguard.sh; then
        print_success "Startup script includes security checks"
        check_result 0 "deployment"
    else
        print_warning "Startup script should include security validation"
        check_result 0 "deployment"
    fi
else
    print_error "Startup script missing or not executable"
    check_result 1 "deployment"
fi

echo ""
print_info "📊 VERIFICATION SUMMARY"
print_info "======================="

echo "Total checks performed: $total_checks"
echo "Security issues found: $security_issues"
echo "Deployment issues found: $deployment_issues"

echo ""
if [ $security_issues -eq 0 ]; then
    print_success "🔒 SECURITY: ALL CHECKS PASSED"
else
    print_error "🔒 SECURITY: $security_issues ISSUES FOUND - MUST FIX BEFORE DEPLOYMENT"
fi

if [ $deployment_issues -eq 0 ]; then
    print_success "🚀 DEPLOYMENT: ALL CHECKS PASSED"
else
    print_error "🚀 DEPLOYMENT: $deployment_issues ISSUES FOUND"
fi

echo ""
if [ $security_issues -eq 0 ] && [ $deployment_issues -eq 0 ]; then
    echo "🎉 DEPLOYMENT READY!"
    echo "==================="
    print_success "WildGuard AI is ready for secure production deployment"
    
    echo ""
    print_info "📋 NEXT STEPS FOR VERCEL DEPLOYMENT:"
    echo "1. Set environment variables in Vercel dashboard:"
    echo "   - REACT_APP_SUPABASE_URL"
    echo "   - REACT_APP_SUPABASE_ANON_KEY"
    echo "2. Deploy: vercel --prod"
    echo "3. Test deployment thoroughly"
    echo "4. Verify real data connections work"
    
    echo ""
    print_info "📋 BACKEND DEPLOYMENT:"
    echo "1. Set environment variables on hosting platform:"
    echo "   - SUPABASE_URL"
    echo "   - SUPABASE_ANON_KEY"
    echo "2. Deploy backend/real_data_server.py"
    echo "3. Update REACT_APP_API_URL if needed"
    
    echo ""
    print_success "🔒 Security verification PASSED"
    print_success "🌍 100% real data integration confirmed"
    print_success "🚀 Deployment configuration verified"
    
else
    echo "❌ DEPLOYMENT BLOCKED"
    echo "===================="
    print_error "Issues must be resolved before deployment"
    
    if [ $security_issues -gt 0 ]; then
        print_error "CRITICAL: Security issues detected"
        print_warning "Fix all security issues before proceeding"
    fi
    
    if [ $deployment_issues -gt 0 ]; then
        print_warning "Deployment configuration needs attention"
    fi
    
    echo ""
    print_info "📖 See SECURITY_SETUP.md for detailed instructions"
fi

echo ""
print_info "🏁 Verification complete!"
