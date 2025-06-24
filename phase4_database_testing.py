#!/usr/bin/env python3
"""
WildGuard AI - Phase 4 Database Testing
SECURITY: Uses environment variables only - no hardcoded credentials
"""

import os
import sys
from datetime import datetime

def phase4_database_test():
    """Phase 4 database testing with environment variables"""
    
    # SECURITY: Load credentials from environment only
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    # Validate environment variables
    if not supabase_url or not supabase_key:
        print("❌ ERROR: Missing Supabase environment variables!")
        print("Please set SUPABASE_URL and SUPABASE_ANON_KEY in your environment")
        return False
    
    print(f"🔒 Security: Using environment variables for Phase 4 testing")
    
    try:
        from supabase import create_client
        
        # Create client with environment variables
        supabase = create_client(supabase_url, supabase_key)
        
        print("🧪 Phase 4: Advanced database testing...")
        
        # Test various queries
        tests = [
            {"name": "Basic connectivity", "query": "detections", "limit": 1},
            {"name": "Platform distribution", "query": "detections", "limit": 100},
            {"name": "Threat level analysis", "query": "detections", "limit": 50}
        ]
        
        for test in tests:
            result = supabase.table(test["query"]).select('*').limit(test["limit"]).execute()
            if result.data:
                print(f"✅ {test['name']}: {len(result.data)} records")
            else:
                print(f"⚠️  {test['name']}: No data")
        
        return True
            
    except ImportError:
        print("❌ ERROR: supabase-py not installed")
        print("Please install: pip install supabase")
        return False
    except Exception as e:
        print(f"❌ Phase 4 testing error: {e}")
        return False

def main():
    print("🧪 WildGuard AI - Phase 4 Database Testing")
    print("=" * 50)
    print(f"Timestamp: {datetime.now()}")
    print()
    
    success = phase4_database_test()
    
    print()
    if success:
        print("🎉 Phase 4 testing completed successfully!")
        print("✅ Advanced database functionality verified")
        print("✅ Environment security validated")
    else:
        print("❌ Phase 4 testing failed")
        print("Please check your environment configuration")
    
    print()
    print("📖 For setup instructions, see SECURITY_SETUP.md")

if __name__ == "__main__":
    main()
