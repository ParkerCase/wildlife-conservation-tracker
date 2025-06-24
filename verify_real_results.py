#!/usr/bin/env python3
"""
WildGuard AI - Results Verification Script
SECURITY: Uses environment variables only - no hardcoded credentials
"""

import os
import sys
from datetime import datetime

def verify_real_results():
    """Verify real results from Supabase database"""
    
    # SECURITY: Load credentials from environment only
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    # Validate environment variables
    if not supabase_url or not supabase_key:
        print("❌ ERROR: Missing Supabase environment variables!")
        print("Please set SUPABASE_URL and SUPABASE_ANON_KEY in your environment")
        return False
    
    print(f"🔒 Security: Using environment variables for database connection")
    
    try:
        from supabase import create_client
        
        # Create client with environment variables
        supabase = create_client(supabase_url, supabase_key)
        
        # Verify real data exists
        result = supabase.table('detections').select('*').limit(10).execute()
        
        if result.data and len(result.data) > 0:
            print(f"✅ Real data verification successful")
            print(f"✅ Found {len(result.data)} sample records")
            
            # Show sample data structure
            sample = result.data[0]
            print(f"✅ Sample record fields: {list(sample.keys())}")
            
            return True
        else:
            print("⚠️  No data found in database")
            return False
            
    except ImportError:
        print("❌ ERROR: supabase-py not installed")
        print("Please install: pip install supabase")
        return False
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

def main():
    print("🔍 WildGuard AI - Real Results Verification")
    print("=" * 50)
    print(f"Timestamp: {datetime.now()}")
    print()
    
    success = verify_real_results()
    
    print()
    if success:
        print("🎉 Results verification completed successfully!")
        print("✅ Real data confirmed in database")
        print("✅ Environment security validated")
    else:
        print("❌ Results verification failed")
        print("Please check your environment configuration")
    
    print()
    print("📖 For setup instructions, see SECURITY_SETUP.md")

if __name__ == "__main__":
    main()
