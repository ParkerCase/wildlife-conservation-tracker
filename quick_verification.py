#!/usr/bin/env python3
"""
Quick Platform Verification - Test imports and basic functionality
"""

import sys
import os
from datetime import datetime

# Add project paths
sys.path.append('/Users/parkercase/conservation-bot')
sys.path.append('/Users/parkercase/conservation-bot/src')

def test_imports():
    """Test if all platform imports work"""
    print("🔍 TESTING PLATFORM IMPORTS")
    print("=" * 40)
    
    try:
        from src.monitoring.platform_scanner import PlatformScanner
        print("✅ PlatformScanner imported successfully")
        
        # Check what platforms are available
        scanner = PlatformScanner()
        platforms = scanner.platforms
        
        print(f"\n📊 AVAILABLE PLATFORMS: {len(platforms)}")
        for platform_name, platform_obj in platforms.items():
            print(f"   ✅ {platform_name.upper()}: {type(platform_obj).__name__}")
        
        return True, platforms
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False, {}

def test_supabase():
    """Test Supabase connection"""
    print("\n🔍 TESTING SUPABASE CONNECTION")
    print("-" * 40)
    
    try:
        from dotenv import load_dotenv
        from supabase import create_client
        
        load_dotenv('/Users/parkercase/conservation-bot/backend/.env')
        
        SUPABASE_URL = os.getenv('SUPABASE_URL')
        SUPABASE_KEY = os.getenv('SUPABASE_KEY')
        
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("❌ Supabase credentials missing")
            return False
            
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Test with a simple query
        result = supabase.table('detections').select("*").limit(1).execute()
        print("✅ Supabase connection working")
        print(f"📊 Database accessible - sample record count: {len(result.data)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Supabase error: {e}")
        return False

def quick_platform_test():
    """Quick test of one platform"""
    print("\n🔍 QUICK PLATFORM TEST (eBay only)")
    print("-" * 40)
    
    try:
        import asyncio
        from src.monitoring.platform_scanner import EbayScanner
        import aiohttp
        
        async def test_ebay():
            scanner = EbayScanner()
            test_keywords = {'direct_terms': ['ivory']}
            
            async with aiohttp.ClientSession() as session:
                results = await asyncio.wait_for(
                    scanner.scan(test_keywords, session),
                    timeout=30.0
                )
                
                if results:
                    print(f"✅ eBay working: {len(results)} results")
                    for i, result in enumerate(results[:2], 1):
                        title = result.get('title', 'No title')[:40]
                        price = result.get('price', 'No price')
                        print(f"   {i}. {title}... - {price}")
                    return len(results)
                else:
                    print("❌ eBay: No results")
                    return 0
        
        return asyncio.run(test_ebay())
        
    except Exception as e:
        print(f"❌ eBay test error: {e}")
        return 0

def main():
    """Quick verification"""
    print("🧪 WILDGUARD AI - QUICK PLATFORM VERIFICATION")
    print("=" * 60)
    
    # Test imports
    imports_ok, platforms = test_imports()
    
    # Test Supabase
    supabase_ok = test_supabase()
    
    # Quick platform test
    if imports_ok:
        ebay_results = quick_platform_test()
    else:
        ebay_results = 0
    
    # Summary
    print(f"\n🎯 QUICK VERIFICATION SUMMARY")
    print("=" * 40)
    print(f"✅ Platform imports: {'WORKING' if imports_ok else 'FAILED'}")
    print(f"✅ Supabase connection: {'WORKING' if supabase_ok else 'FAILED'}")
    print(f"✅ eBay test results: {ebay_results} listings")
    
    if imports_ok:
        print(f"📊 Total platforms available: {len(platforms)}")
        print(f"📋 Platform list: {', '.join(platforms.keys())}")
    
    # Quick assessment
    if imports_ok and supabase_ok and ebay_results > 0:
        print(f"\n🎉 VERDICT: SYSTEM IS WORKING!")
        print("   ✅ All imports successful")
        print("   ✅ Database connection active") 
        print("   ✅ At least eBay platform operational")
        print("   🚀 Ready for full platform testing")
    elif imports_ok and supabase_ok:
        print(f"\n⚠️  VERDICT: MOSTLY WORKING")
        print("   ✅ Infrastructure ready")
        print("   🔧 Platform scanning needs debugging")
    else:
        print(f"\n❌ VERDICT: NEEDS FIXES")
        print("   🔧 Fix import or database issues first")

if __name__ == "__main__":
    main()
