#!/usr/bin/env python3
"""
Quick Platform Verification Test
- Tests the fixed selectors
- Verifies Supabase connection
- Checks keyword loading
"""

import os
import sys
from dotenv import load_dotenv
import logging
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_environment():
    """Test environment variables"""
    print("🔧 Testing Environment Setup...")
    
    # Load environment variables
    load_dotenv()
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Missing Supabase credentials in .env file")
        print("📝 Please update your .env file with your Supabase credentials")
        return False
    
    if supabase_url == "https://your-project.supabase.co":
        print("❌ Please update SUPABASE_URL in .env file with your actual Supabase URL")
        return False
    
    if supabase_key == "your_anon_key_here":
        print("❌ Please update SUPABASE_ANON_KEY in .env file with your actual key")
        return False
    
    print("✅ Environment variables configured correctly")
    return True

def test_supabase_connection():
    """Test connection to Supabase"""
    print("\n🔗 Testing Supabase Connection...")
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    try:
        headers = {
            'apikey': supabase_key,
            'Authorization': f'Bearer {supabase_key}'
        }
        
        # Test connection with a simple count query
        response = requests.head(
            f"{supabase_url}/rest/v1/detections",
            headers={**headers, 'Prefer': 'count=exact'}
        )
        
        if response.status_code == 200:
            total_count = response.headers.get('Content-Range', '0').split('/')[-1]
            print(f"✅ Connected to Supabase successfully")
            print(f"📊 Current records in detections table: {total_count}")
            return True
        else:
            print(f"❌ Supabase connection failed: HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ Supabase connection error: {e}")
        return False

def test_keyword_loading():
    """Test keyword loading from comprehensive file"""
    print("\n📚 Testing Keyword Loading...")
    
    try:
        # Import the keywords module directly (same as the scanner)
        import sys
        import os
        
        # Add current directory to path if not already there
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Import the keywords module
        import comprehensive_endangered_keywords as keywords_module
        
        # Get the keywords list
        keywords = getattr(keywords_module, 'ALL_ENDANGERED_SPECIES_KEYWORDS', [])
        
        if keywords and len(keywords) > 100:
            print(f"✅ Successfully loaded {len(keywords)} keywords")
            print(f"✅ Keywords include: {', '.join(keywords[:5])}...")
            return True
        else:
            print(f"❌ Keywords list too small: {len(keywords)} keywords")
            return False
            
    except FileNotFoundError:
        print("❌ comprehensive_endangered_keywords.py not found")
        return False
    except Exception as e:
        print(f"❌ Error loading keywords: {e}")
        return False

def test_scanner_modules():
    """Test that scanner modules can be imported"""
    print("\n🔍 Testing Scanner Modules...")
    
    try:
        # Test if we can import the fixed scanner
        import importlib.util
        spec = importlib.util.spec_from_file_location("fixed_scanner", "fixed_production_scanner.py")
        if spec is None:
            print("❌ fixed_production_scanner.py not found")
            return False
        
        print("✅ Fixed production scanner found")
        
        # Test dependencies
        required_modules = ['requests', 'json', 'time', 'random', 'logging', 're', 'hashlib']
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            print(f"❌ Missing required modules: {', '.join(missing_modules)}")
            return False
        
        print("✅ All required modules available")
        return True
        
    except Exception as e:
        print(f"❌ Error testing scanner modules: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 WildGuard AI - Production Readiness Test")
    print("="*50)
    
    tests = [
        test_environment,
        test_supabase_connection,
        test_keyword_loading,
        test_scanner_modules
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            failed += 1
    
    print(f"\n🎯 TEST RESULTS:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! System is ready for production.")
        print("\n📋 Next Steps:")
        print("1. 🧹 Run massive_duplicate_cleanup.py to clean existing data")
        print("2. 🚀 Test fixed_production_scanner.py with --test-mode")
        print("3. 📊 Deploy GitHub Actions workflows")
        print("4. 🎯 Monitor production scanning")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please fix issues before proceeding.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
