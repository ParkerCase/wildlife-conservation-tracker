#!/usr/bin/env python3
"""
FORCE CACHE CLEAR AND VERIFICATION SCRIPT
Ensures the fixed scanners are being used and clears any cached imports
"""

import sys
import os
import importlib
from datetime import datetime

def clear_python_cache():
    """Clear Python cache to force reload of fixed modules"""
    print("🔄 Clearing Python cache...")
    
    # Clear __pycache__ directories
    for root, dirs, files in os.walk('/Users/parkercase/conservation-bot'):
        if '__pycache__' in dirs:
            import shutil
            cache_path = os.path.join(root, '__pycache__')
            shutil.rmtree(cache_path)
            print(f"✅ Cleared cache: {cache_path}")
    
    # Clear sys.modules cache for our scanners
    modules_to_clear = [
        'enhanced_platform_scanner',
        'continuous_real_wildlife_scanner', 
        'continuous_real_ht_scanner'
    ]
    
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
            print(f"✅ Cleared module cache: {module}")

def test_fixed_imports():
    """Test that the fixed scanners import properly"""
    print("\n🧪 Testing fixed scanner imports...")
    
    try:
        sys.path.insert(0, '/Users/parkercase/conservation-bot')
        
        # Test enhanced platform scanner
        from enhanced_platform_scanner import EnhancedRealPlatformScanner
        scanner = EnhancedRealPlatformScanner()
        
        print("✅ Enhanced platform scanner imports successfully")
        
        # Test that all platform classes have ua attribute
        for name, platform in scanner.platforms.items():
            if hasattr(platform, 'ua'):
                print(f"✅ {name}: Has ua attribute")
            else:
                print(f"❌ {name}: MISSING ua attribute")
                return False
        
        # Test wildlife scanner
        from continuous_real_wildlife_scanner import ContinuousRealWildlifeScanner
        wildlife_scanner = ContinuousRealWildlifeScanner()
        print(f"✅ Wildlife scanner: {len(wildlife_scanner.real_platforms)} platforms configured")
        
        # Test HT scanner  
        from continuous_real_ht_scanner import ContinuousRealHTScanner
        ht_scanner = ContinuousRealHTScanner()
        print(f"✅ HT scanner: {len(ht_scanner.ht_platforms)} platforms configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def check_file_timestamps():
    """Check when the scanner files were last modified"""
    print("\n📅 Checking file timestamps...")
    
    files_to_check = [
        'enhanced_platform_scanner.py',
        'continuous_real_wildlife_scanner.py',
        'continuous_real_ht_scanner.py'
    ]
    
    for filename in files_to_check:
        filepath = f'/Users/parkercase/conservation-bot/{filename}'
        if os.path.exists(filepath):
            mtime = os.path.getmtime(filepath)
            mod_time = datetime.fromtimestamp(mtime)
            print(f"✅ {filename}: Modified {mod_time}")
        else:
            print(f"❌ {filename}: File not found")

def main():
    print("🔧 FIXING SCANNER CACHE AND IMPORT ISSUES")
    print("=" * 60)
    
    # Step 1: Clear cache
    clear_python_cache()
    
    # Step 2: Check file timestamps
    check_file_timestamps()
    
    # Step 3: Test imports
    success = test_fixed_imports()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL FIXES VERIFIED!")
        print("✅ Fixed scanners are ready")
        print("✅ All platform classes have ua attributes")
        print("✅ Imports working correctly")
        print("\n🚀 The next GitHub Actions run should work properly!")
    else:
        print("❌ ISSUES STILL DETECTED")
        print("The fixes may not have taken effect properly")
    
    return success

if __name__ == "__main__":
    main()
