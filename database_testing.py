#!/usr/bin/env python3
"""
WildGuard AI - Database Testing and Verification Script
SECURITY: Uses environment variables only - no hardcoded credentials
"""

import os
import sys
from datetime import datetime

def test_database_connection():
    """Test Supabase database connection with environment variables"""
    
    # SECURITY: Load credentials from environment only
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    # Validate environment variables
    if not supabase_url or not supabase_key:
        print("❌ ERROR: Missing Supabase environment variables!")
        print("Please set SUPABASE_URL and SUPABASE_ANON_KEY in your environment")
        print("Example:")
        print("export SUPABASE_URL=your_supabase_url")
        print("export SUPABASE_ANON_KEY=your_supabase_key")
        return False
    
    print(f"🔒 Security: Using environment variables for database connection")
    
    try:
        from supabase import create_client
        
        # Create client with environment variables
        supabase = create_client(supabase_url, supabase_key)
        
        print("✅ Supabase client created successfully")
        
        # Test connection with a simple query
        result = supabase.table('detections').select('id').limit(1).execute()
        
        if result.data:
            print(f"✅ Database connection successful")
            print(f"✅ Database contains data: {len(result.data)} record(s) retrieved")
            return True
        else:
            print("⚠️  Database connection successful but no data found")
            return True
            
    except ImportError:
        print("❌ ERROR: supabase-py not installed")
        print("Please install: pip install supabase")
        return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def main():
    print("🧪 WildGuard AI - Database Connection Test")
    print("=" * 50)
    print(f"Timestamp: {datetime.now()}")
    print()
    
    success = test_database_connection()
    
    print()
    if success:
        print("🎉 Database test completed successfully!")
        print("✅ Environment variables configured properly")
        print("✅ Supabase connection working")
    else:
        print("❌ Database test failed")
        print("Please check your environment configuration")
    
    print()
    print("📖 For setup instructions, see SECURITY_SETUP.md")

if __name__ == "__main__":
    main()
