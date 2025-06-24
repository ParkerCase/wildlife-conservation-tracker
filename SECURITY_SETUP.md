# 🔒 WildGuard AI - Security Setup Guide

## 🚨 CRITICAL: Environment Variables Setup

**NEVER commit credentials to Git!** Follow this guide to set up your environment securely.

---

## 📋 **Required Environment Variables**

### Frontend (.env)
```bash
# Copy example file
cp frontend/.env.example frontend/.env

# Edit with your actual values
REACT_APP_SUPABASE_URL=https://your-project.supabase.co
REACT_APP_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Backend (.env)
```bash
# Copy example file
cp backend/.env.example backend/.env

# Edit with your actual values
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 🔑 **Get Your Supabase Credentials**

1. **Login to Supabase Dashboard**: https://supabase.com/dashboard
2. **Select Your Project**: Click on your WildGuard project
3. **Go to Settings**: Click on the gear icon ⚙️
4. **API Section**: Find your credentials:
   - **Project URL**: Copy this as your `SUPABASE_URL`
   - **Project API Keys** → **anon public**: Copy as your `SUPABASE_ANON_KEY`

---

## ⚡ **Quick Setup Commands**

```bash
# 1. Copy environment files
cp frontend/.env.example frontend/.env
cp backend/.env.example backend/.env

# 2. Edit frontend environment
nano frontend/.env
# Replace 'your_supabase_url_here' with your actual URL
# Replace 'your_supabase_anon_key_here' with your actual key

# 3. Edit backend environment  
nano backend/.env
# Replace 'your_supabase_url_here' with your actual URL
# Replace 'your_supabase_anon_key_here' with your actual key

# 4. Verify files are not tracked by Git
git status
# .env files should NOT appear in the list
```

---

## 🛡️ **Security Checklist**

### ✅ Local Development:
- [ ] `.env` files exist in both frontend and backend
- [ ] `.env` files contain your actual Supabase credentials
- [ ] `.env` files are listed in `.gitignore`
- [ ] No credentials are hardcoded in source files
- [ ] `git status` does not show `.env` files

### ✅ Production Deployment:
- [ ] Environment variables set in Vercel dashboard
- [ ] Environment variables set in your backend hosting platform
- [ ] No credentials in Git repository
- [ ] Environment validation works in deployed app

---

## 🚀 **Vercel Deployment Setup**

### Frontend Environment Variables (Vercel Dashboard):
1. Go to your Vercel project settings
2. Navigate to **Environment Variables**
3. Add these variables:

```
REACT_APP_SUPABASE_URL = https://your-project.supabase.co
REACT_APP_SUPABASE_ANON_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
REACT_APP_ENABLE_MULTILINGUAL = true
REACT_APP_ENABLE_REAL_TIME = true
```

### Backend Deployment:
Set these variables in your backend hosting platform:
```
SUPABASE_URL = https://your-project.supabase.co
SUPABASE_ANON_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 🔍 **Verification Commands**

### Test Frontend Connection:
```bash
cd frontend
npm start
# Should start without errors
# Check browser console for "Supabase client initialized"
```

### Test Backend Connection:
```bash
cd backend
python3 real_data_server.py
# Should show "✅ Supabase client initialized successfully"
# Test: curl http://localhost:5000/health
```

### Verify No Secrets in Git:
```bash
git log --all --full-history -- "*.env*"
# Should show no commits with actual .env files

grep -r "supabase.co" . --exclude-dir=node_modules --exclude-dir=.git
# Should only show example files or documentation
```

---

## 🚨 **If You Accidentally Committed Secrets**

### Immediate Actions:
1. **Revoke the exposed keys** in Supabase dashboard
2. **Generate new keys** in Supabase
3. **Update your local .env files** with new keys
4. **Remove secrets from Git history**:

```bash
# Remove the file from Git history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch backend/real_data_server.py' \
  --prune-empty --tag-name-filter cat -- --all

# Force push to update remote
git push origin --force --all
```

### Update Production:
- Update environment variables in Vercel
- Update environment variables in backend hosting
- Test all deployments with new credentials

---

## 📋 **Environment File Templates**

### frontend/.env
```bash
REACT_APP_SUPABASE_URL=https://your-project.supabase.co
REACT_APP_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
REACT_APP_API_URL=http://localhost:5000
REACT_APP_ENABLE_MULTILINGUAL=true
REACT_APP_ENABLE_REAL_TIME=true
REACT_APP_ENABLE_EXPORTS=true
```

### backend/.env
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
FLASK_ENV=development
FLASK_DEBUG=true
```

---

## 🎯 **After Setup Verification**

Once you've set up your environment variables correctly:

```bash
# 1. Start the system
./start_wildguard.sh

# 2. Verify connections
curl http://localhost:5000/health
# Should return: "database_status": "connected"

# 3. Test frontend
open http://localhost:3000
# Should load dashboard with real data

# 4. Check for errors
# No "Missing Supabase environment variables" errors
# No hardcoded credentials warnings
```

---

**🔒 Remember: Keep your credentials secure and never commit them to version control!**

