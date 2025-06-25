#!/usr/bin/env python3
"""
Quick script to show your Supabase credentials for GitHub Actions setup
"""
import os

print("🔍 SUPABASE CREDENTIALS FOR GITHUB ACTIONS SETUP")
print("=" * 60)

# Check local environment
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY') or os.getenv('SUPABASE_ANON_KEY')

if supabase_url and supabase_key:
    print("✅ Found local credentials!")
    print(f"\n📋 ADD THESE TO GITHUB ACTIONS SECRETS:")
    print(f"SUPABASE_URL = {supabase_url}")
    print(f"SUPABASE_ANON_KEY = {supabase_key}")
    print(f"SUPABASE_KEY = {supabase_key}")
else:
    print("❌ Local credentials not found in environment variables")
    print("\n🔧 TO GET YOUR CREDENTIALS:")
    print("1. Go to https://app.supabase.com")
    print("2. Select your project")
    print("3. Go to Settings → API")
    print("4. Copy Project URL and anon public key")

# Check .env files
env_files = ['.env', 'frontend/.env', 'backend/.env']
for env_file in env_files:
    if os.path.exists(env_file):
        print(f"\n📄 Found {env_file} - checking for credentials...")
        try:
            with open(env_file, 'r') as f:
                content = f.read()
                if 'SUPABASE_URL' in content:
                    lines = content.split('\n')
                    for line in lines:
                        if line.startswith('SUPABASE_URL') or line.startswith('REACT_APP_SUPABASE_URL'):
                            print(f"   {line}")
                        elif line.startswith('SUPABASE_ANON_KEY') or line.startswith('REACT_APP_SUPABASE_ANON_KEY'):
                            print(f"   {line}")
        except Exception as e:
            print(f"   Error reading {env_file}: {e}")

print("\n" + "=" * 60)
print("🚀 NEXT STEPS:")
print("1. Copy the credentials above")
print("2. Add them to GitHub → Settings → Secrets and variables → Actions")
print("3. Re-run your GitHub Action")
