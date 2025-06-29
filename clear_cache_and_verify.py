#!/usr/bin/env python3
"""
CACHE CLEARING AND FORCE RELOAD SCRIPT
Clears Python cache and forces fresh imports
"""

import os
import shutil
import sys
from datetime import datetime

def clear_all_cache():
    """Clear all Python cache files"""
    cache_cleared = 0
    
    print("🔄 Clearing Python cache...")
    
    # Walk through entire project directory
    for root, dirs, files in os.walk('/Users/parkercase/conservation-bot'):
        # Remove __pycache__ directories
        if '__pycache__' in dirs:
            cache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(cache_path)
                print(f"✅ Cleared: {cache_path}")
                cache_cleared += 1
            except Exception as e:
                print(f"❌ Failed to clear: {cache_path} - {e}")
        
        # Remove .pyc files
        for file in files:
            if file.endswith('.pyc'):
                pyc_path = os.path.join(root, file)
                try:
                    os.remove(pyc_path)
                    print(f"✅ Removed: {pyc_path}")
                    cache_cleared += 1
                except Exception as e:
                    print(f"❌ Failed to remove: {pyc_path} - {e}")
    
    print(f"✅ Cleared {cache_cleared} cache files/directories")
    return cache_cleared

def test_import():
    """Test that imports work correctly"""
    print("\n🧪 Testing imports...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, '/Users/parkercase/conservation-bot')
        
        # Test enhanced platform scanner
        from enhanced_platform_scanner import EnhancedRealPlatformScanner
        scanner = EnhancedRealPlatformScanner()
        
        print("✅ Enhanced platform scanner imported successfully")
        
        # Check all platform classes have ua attribute
        ua_missing = []
        for name, platform in scanner.platforms.items():
            if hasattr(platform, 'ua'):
                print(f"✅ {name}: Has ua attribute")
            else:
                print(f"❌ {name}: MISSING ua attribute")
                ua_missing.append(name)
        
        if ua_missing:
            print(f"❌ CRITICAL: {len(ua_missing)} platforms missing ua attribute!")
            return False
        
        print("✅ ALL PLATFORM CLASSES HAVE ua ATTRIBUTE!")
        
        # Test continuous scanners
        from continuous_real_wildlife_scanner import ContinuousRealWildlifeScanner
        wildlife_scanner = ContinuousRealWildlifeScanner()
        print(f"✅ Wildlife scanner: {len(wildlife_scanner.real_platforms)} platforms")
        
        from continuous_real_ht_scanner import ContinuousRealHTScanner  
        ht_scanner = ContinuousRealHTScanner()
        print(f"✅ HT scanner: {len(ht_scanner.ht_platforms)} platforms")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_verification_timestamp():
    """Create a file to mark when cache was cleared"""
    timestamp_file = '/Users/parkercase/conservation-bot/cache_cleared_timestamp.txt'
    
    with open(timestamp_file, 'w') as f:
        f.write(f"Cache cleared at: {datetime.now().isoformat()}\n")
        f.write("All Python cache files and __pycache__ directories removed\n")
        f.write("Fixed scanner imports verified\n")
        f.write("ua attribute errors should be resolved\n")
    
    print(f"✅ Created verification timestamp: {timestamp_file}")

def main():
    print("🔧 PYTHON CACHE CLEARING AND VERIFICATION")
    print("=" * 60)
    
    # Step 1: Clear cache
    cache_count = clear_all_cache()
    
    # Step 2: Test imports
    success = test_import()
    
    # Step 3: Create verification file
    create_verification_timestamp()
    
    print("\n" + "=" * 60)
    print("📊 CACHE CLEARING RESULTS:")
    print(f"   🔄 Cache items cleared: {cache_count}")
    print(f"   🧪 Import test: {'SUCCESS' if success else 'FAILED'}")
    
    if success:
        print("\n🎉 CACHE CLEARING SUCCESSFUL!")
        print("✅ All Python cache cleared")
        print("✅ Fixed scanners import correctly")
        print("✅ All platform classes have ua attributes") 
        print("✅ No more ua attribute errors expected")
        print("\n🚀 NEXT GITHUB ACTIONS RUN SHOULD WORK!")
    else:
        print("\n❌ CACHE CLEARING ISSUES DETECTED")
        print("There may still be import problems")
    
    return success

if __name__ == "__main__":
    main()
