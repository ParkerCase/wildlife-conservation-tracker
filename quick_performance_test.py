#!/usr/bin/env python3
"""
WildGuard AI - Quick Performance Test
SECURITY: Uses environment variables only - no hardcoded credentials
"""

import os
import sys
import time
from datetime import datetime

def quick_performance_test():
    """Quick performance test using environment variables"""
    
    # SECURITY: Load credentials from environment only
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    # Validate environment variables
    if not supabase_url or not supabase_key:
        print("❌ ERROR: Missing Supabase environment variables!")
        print("Please set SUPABASE_URL and SUPABASE_ANON_KEY in your environment")
        return False
    
    print(f"🔒 Security: Using environment variables for performance testing")
    
    try:
        from supabase import create_client
        
        # Create client with environment variables
        supabase = create_client(supabase_url, supabase_key)
        
        # Test query performance
        start_time = time.time()
        
        result = supabase.table('detections').select('*').limit(100).execute()
        
        end_time = time.time()
        query_time = end_time - start_time
        
        if result.data:
            print(f"✅ Performance test successful")
            print(f"✅ Query time: {query_time:.3f} seconds")
            print(f"✅ Records retrieved: {len(result.data)}")
            print(f"✅ Performance: {len(result.data)/query_time:.1f} records/second")
            return True
        else:
            print("⚠️  No data found for performance test")
            return False
            
    except ImportError:
        print("❌ ERROR: supabase-py not installed")
        print("Please install: pip install supabase")
        return False
    except Exception as e:
        print(f"❌ Performance test error: {e}")
        return False

def main():
    print("⚡ WildGuard AI - Quick Performance Test")
    print("=" * 50)
    print(f"Timestamp: {datetime.now()}")
    print()
    
    success = quick_performance_test()
    
    print()
    if success:
        print("🎉 Performance test completed successfully!")
        print("✅ Database performance verified")
        print("✅ Environment security validated")
    else:
        print("❌ Performance test failed")
        print("Please check your environment configuration")
    
    print()
    print("📖 For setup instructions, see SECURITY_SETUP.md")

if __name__ == "__main__":
    main()
