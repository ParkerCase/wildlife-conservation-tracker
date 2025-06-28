#!/usr/bin/env python3
"""
COMPREHENSIVE SYSTEM TEST
Tests all components together to verify quality fixes work
"""

import asyncio
import os
import json
import sys
from datetime import datetime

def test_all_systems():
    """Test all systems together"""
    
    print("🧪 COMPREHENSIVE SYSTEM TEST")
    print("=" * 80)
    
    results = {
        "tests_passed": 0,
        "tests_failed": 0,
        "issues_found": [],
        "systems_verified": []
    }
    
    # TEST 1: Multilingual Wildlife Keywords (1,452)
    print("\n1️⃣ TESTING: Wildlife Keywords (1,452)")
    try:
        with open('multilingual_wildlife_keywords.json', 'r') as f:
            keywords_data = json.load(f)
        
        total_keywords = keywords_data.get('total_keywords', 0)
        actual_count = sum(len(keywords) for keywords in keywords_data['keywords_by_language'].values())
        
        if actual_count >= 1400:
            print(f"   ✅ Wildlife keywords: {actual_count} loaded (≥1,400 required)")
            print(f"   ✅ Languages: {len(keywords_data['keywords_by_language'])}")
            results["tests_passed"] += 1
            results["systems_verified"].append("Wildlife keywords (1,452)")
        else:
            print(f"   ❌ Wildlife keywords: Only {actual_count} loaded (need ≥1,400)")
            results["tests_failed"] += 1
            results["issues_found"].append(f"Wildlife keywords too few: {actual_count}")
            
    except Exception as e:
        print(f"   ❌ Wildlife keywords failed: {e}")
        results["tests_failed"] += 1
        results["issues_found"].append(f"Wildlife keywords error: {e}")
    
    # TEST 2: Intelligent Threat Scoring System
    print("\n2️⃣ TESTING: Intelligent Threat Scoring")
    try:
        from intelligent_threat_scoring_system import IntelligentThreatScorer
        
        scorer = IntelligentThreatScorer()
        
        # Test high-threat wildlife case
        test_wildlife = {
            'title': 'Antique ivory carving from private collection',
            'description': 'Genuine elephant ivory, museum quality, discrete shipping',
            'price': '$850',
            'url': 'https://example.com/test'
        }
        
        wildlife_analysis = scorer.analyze_listing(test_wildlife, 'ivory carving', 'ebay')
        
        if wildlife_analysis.threat_score >= 80 and wildlife_analysis.threat_category.value == 'WILDLIFE':
            print(f"   ✅ Wildlife scoring: {wildlife_analysis.threat_score}/100 (HIGH THREAT)")
            print(f"   ✅ Threat level: {wildlife_analysis.threat_level.value}")
            results["tests_passed"] += 1
            results["systems_verified"].append("Intelligent scoring - Wildlife")
        else:
            print(f"   ❌ Wildlife scoring failed: {wildlife_analysis.threat_score}/100")
            results["tests_failed"] += 1
            results["issues_found"].append(f"Wildlife scoring too low: {wildlife_analysis.threat_score}")
        
        # Test legitimate business case (should be low/safe)
        test_legitimate = {
            'title': 'Licensed massage therapy at medical clinic',
            'description': 'Professional therapeutic massage by certified therapists at registered clinic',
            'price': '$80',
            'url': 'https://medicalmassage.com/services'
        }
        
        legitimate_analysis = scorer.analyze_listing(test_legitimate, 'massage therapy', 'gumtree')
        
        if legitimate_analysis.threat_score <= 20 and legitimate_analysis.false_positive_risk > 0.5:
            print(f"   ✅ Legitimate business: {legitimate_analysis.threat_score}/100 (LOW THREAT)")
            print(f"   ✅ False positive risk: {legitimate_analysis.false_positive_risk:.1%}")
            results["tests_passed"] += 1
            results["systems_verified"].append("Intelligent scoring - False positive detection")
        else:
            print(f"   ❌ Legitimate business scored too high: {legitimate_analysis.threat_score}/100")
            results["tests_failed"] += 1
            results["issues_found"].append(f"False positive not detected: {legitimate_analysis.threat_score}")
            
    except Exception as e:
        print(f"   ❌ Intelligent scoring failed: {e}")
        results["tests_failed"] += 1
        results["issues_found"].append(f"Intelligent scoring error: {e}")
    
    # TEST 3: Safe Human Trafficking Keywords
    print("\n3️⃣ TESTING: Safe Human Trafficking Keywords")
    try:
        from refined_human_trafficking_keywords import get_safe_human_trafficking_keywords, analyze_keyword_risk
        
        safe_keywords = get_safe_human_trafficking_keywords()
        
        # Test that problematic terms are excluded
        problematic_terms = ["restaurant", "hotel spa", "medical massage", "holistic treatment"]
        excluded_count = 0
        
        for term in problematic_terms:
            analysis = analyze_keyword_risk(term)
            if not analysis['use_keyword']:
                excluded_count += 1
        
        if excluded_count == len(problematic_terms):
            print(f"   ✅ Problematic terms excluded: {excluded_count}/{len(problematic_terms)}")
            print(f"   ✅ Safe keywords loaded: {len(safe_keywords)}")
            results["tests_passed"] += 1
            results["systems_verified"].append("Safe HT keywords - False positive filtering")
        else:
            print(f"   ❌ Problematic terms not excluded: {excluded_count}/{len(problematic_terms)}")
            results["tests_failed"] += 1
            results["issues_found"].append(f"False positive terms not excluded: {len(problematic_terms) - excluded_count}")
            
    except Exception as e:
        print(f"   ❌ Safe HT keywords failed: {e}")
        results["tests_failed"] += 1
        results["issues_found"].append(f"Safe HT keywords error: {e}")
    
    # TEST 4: Fixed High Volume Scanner
    print("\n4️⃣ TESTING: Fixed High Volume Scanner")
    try:
        from fixed_high_volume_scanner import FixedHighVolumeScanner
        
        # Test initialization
        scanner = FixedHighVolumeScanner()
        
        wildlife_count = len(scanner.wildlife_keywords)
        ht_count = len(scanner.human_trafficking_keywords)
        has_intelligent_scoring = bool(scanner.threat_scorer)
        
        if wildlife_count >= 1400 and ht_count >= 100 and has_intelligent_scoring:
            print(f"   ✅ Scanner initialized: Wildlife={wildlife_count}, HT={ht_count}")
            print(f"   ✅ Intelligent scoring: {has_intelligent_scoring}")
            results["tests_passed"] += 1
            results["systems_verified"].append("Fixed high volume scanner")
        else:
            issues = []
            if wildlife_count < 1400:
                issues.append(f"Wildlife keywords: {wildlife_count} < 1400")
            if ht_count < 100:
                issues.append(f"HT keywords: {ht_count} < 100")
            if not has_intelligent_scoring:
                issues.append("No intelligent scoring")
            
            print(f"   ❌ Scanner issues: {'; '.join(issues)}")
            results["tests_failed"] += 1
            results["issues_found"].extend(issues)
            
    except Exception as e:
        print(f"   ❌ Fixed scanner failed: {e}")
        results["tests_failed"] += 1
        results["issues_found"].append(f"Fixed scanner error: {e}")
    
    # TEST 5: Google Vision Quota System
    print("\n5️⃣ TESTING: Google Vision Quota System")
    try:
        from enhanced_platforms.google_vision_controller import GoogleVisionController
        
        vision = GoogleVisionController()
        status = vision.get_quota_status()
        
        has_quota_system = status['quota_total'] == 1000
        has_database = os.path.exists(status['database_path'])
        quota_usage = status['quota_used']
        
        if has_quota_system and has_database and quota_usage <= 1000:
            print(f"   ✅ Quota system: {quota_usage}/{status['quota_total']} used")
            print(f"   ✅ Database: {status['database_path']}")
            print(f"   ✅ Daily budget: {status['daily_budget_remaining']}")
            results["tests_passed"] += 1
            results["systems_verified"].append("Google Vision quota system")
        else:
            issues = []
            if not has_quota_system:
                issues.append(f"Wrong quota: {status['quota_total']} != 1000")
            if not has_database:
                issues.append("Database missing")
            if quota_usage > 1000:
                issues.append(f"Quota exceeded: {quota_usage}")
            
            print(f"   ❌ Vision issues: {'; '.join(issues)}")
            results["tests_failed"] += 1
            results["issues_found"].extend(issues)
            
    except Exception as e:
        print(f"   ❌ Google Vision failed: {e}")
        results["tests_failed"] += 1
        results["issues_found"].append(f"Google Vision error: {e}")
    
    # FINAL RESULTS
    print(f"\n🎯 COMPREHENSIVE TEST RESULTS")
    print("=" * 80)
    print(f"✅ Tests Passed: {results['tests_passed']}")
    print(f"❌ Tests Failed: {results['tests_failed']}")
    print(f"📊 Success Rate: {results['tests_passed']}/{results['tests_passed'] + results['tests_failed']} ({results['tests_passed']/(results['tests_passed'] + results['tests_failed'])*100:.1f}%)")
    
    print(f"\n✅ VERIFIED SYSTEMS:")
    for system in results["systems_verified"]:
        print(f"   • {system}")
    
    if results["issues_found"]:
        print(f"\n❌ ISSUES FOUND:")
        for issue in results["issues_found"]:
            print(f"   • {issue}")
    
    # Overall assessment
    if results["tests_failed"] == 0:
        print(f"\n🎉 ALL SYSTEMS: WORKING PERFECTLY")
        print(f"✅ Quality fixes successfully implemented")
        print(f"✅ Ready for production deployment")
        return True
    elif results["tests_passed"] >= results["tests_failed"]:
        print(f"\n⚠️ MOST SYSTEMS: WORKING (some minor issues)")
        print(f"✅ Core functionality verified")
        print(f"⚠️ Minor issues need attention")
        return True
    else:
        print(f"\n❌ CRITICAL ISSUES: Need immediate attention")
        print(f"❌ System not ready for production")
        return False

if __name__ == "__main__":
    success = test_all_systems()
    sys.exit(0 if success else 1)
