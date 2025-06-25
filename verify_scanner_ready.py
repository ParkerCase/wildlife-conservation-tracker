#!/usr/bin/env python3
"""
Core scanner logic verification - no database required
"""

import json
import sys
import os

def verify_scanner_ready():
    """Verify the scanner is ready for deployment"""
    print("🔍 WildGuard AI - Scanner Readiness Check")
    print("=" * 50)
    
    checks_passed = 0
    total_checks = 5
    
    # Check 1: Multilingual keywords file exists and is valid
    print("1️⃣ Checking multilingual keywords...")
    try:
        with open('multilingual_wildlife_keywords.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        total_keywords = sum(len(keywords) for keywords in data['keywords_by_language'].values())
        languages = len(data['keywords_by_language'])
        
        if total_keywords >= 1400 and languages >= 15:
            print(f"   ✅ {total_keywords:,} keywords across {languages} languages")
            checks_passed += 1
        else:
            print(f"   ❌ Insufficient keywords: {total_keywords} (need 1400+)")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Check 2: Fixed scanner file exists
    print("2️⃣ Checking fixed scanner files...")
    required_files = [
        'final_production_scanner.py',
        'final_production_scanner_fixed.py',
        'comprehensive_endangered_keywords.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if not missing_files:
        print("   ✅ All required scanner files present")
        checks_passed += 1
    else:
        print(f"   ❌ Missing files: {missing_files}")
    
    # Check 3: GitHub workflow file
    print("3️⃣ Checking GitHub Actions workflow...")
    workflow_path = '.github/workflows/fixed-multilingual-scanner.yml'
    if os.path.exists(workflow_path):
        print("   ✅ Fixed multilingual scanner workflow ready")
        checks_passed += 1
    else:
        print("   ❌ Missing GitHub Actions workflow")
    
    # Check 4: Scanner configuration
    print("4️⃣ Checking scanner configuration...")
    try:
        # Test loading the scanner class
        sys.path.append('.')
        from final_production_scanner import FinalProductionScanner
        
        # Check if it can initialize (without async context)
        scanner = FinalProductionScanner.__new__(FinalProductionScanner)
        scanner.ua = None
        scanner.session = None
        scanner.seen_urls = set()
        scanner.all_keywords = ['test']
        scanner.platforms = ['ebay', 'avito']
        
        # Test core methods
        batch = ['ivory', 'rhino horn', 'tiger bone']
        threat_score = scanner.calculate_threat_score({
            'title': 'ivory carving',
            'search_term': 'ivory',
            'platform': 'ebay'
        })
        
        if 50 <= threat_score <= 100:
            print(f"   ✅ Scanner logic working (threat score: {threat_score})")
            checks_passed += 1
        else:
            print(f"   ❌ Invalid threat score: {threat_score}")
            
    except Exception as e:
        print(f"   ❌ Scanner configuration error: {e}")
    
    # Check 5: Keywords are properly distributed
    print("5️⃣ Checking keyword distribution...")
    try:
        with open('multilingual_wildlife_keywords.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check that we have good coverage across languages
        en_keywords = len(data['keywords_by_language'].get('en', []))
        other_keywords = sum(len(keywords) for lang, keywords in data['keywords_by_language'].items() if lang != 'en')
        
        if en_keywords >= 900 and other_keywords >= 400:
            print(f"   ✅ Good distribution: {en_keywords} English, {other_keywords} other languages")
            checks_passed += 1
        else:
            print(f"   ❌ Poor distribution: {en_keywords} English, {other_keywords} other")
            
    except Exception as e:
        print(f"   ❌ Distribution check error: {e}")
    
    # Results
    print("\n" + "=" * 50)
    print(f"📋 Readiness Check: {checks_passed}/{total_checks} checks passed")
    
    if checks_passed == total_checks:
        print("\n🎉 SCANNER IS READY FOR DEPLOYMENT!")
        print("\n🚀 Next steps:")
        print("  1. Commit and push all changes")
        print("  2. Go to GitHub Actions → 'Fixed Multilingual Production Scanner'")
        print("  3. Click 'Run workflow' and choose duration (recommend 3 hours)")
        print("  4. Monitor logs for successful database insertions")
        print("\n📊 Expected improvements:")
        print("  • 1,450 multilingual keywords (vs 966 basic)")
        print("  • 50+ keywords per batch (vs 12)")
        print("  • Smart platform weighting based on success data")
        print("  • Fixed database storage with confidence_score")
        return True
    else:
        print("\n⚠️ SCANNER NOT READY")
        print("Please fix the failed checks before deploying.")
        return False

if __name__ == "__main__":
    success = verify_scanner_ready()
    sys.exit(0 if success else 1)
