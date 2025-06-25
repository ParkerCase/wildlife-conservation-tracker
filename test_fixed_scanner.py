#!/usr/bin/env python3
"""
Quick test for the fixed production scanner
Verifies multilingual keywords loading and database connection
"""

import os
import sys
import json
import asyncio
import aiohttp
from datetime import datetime

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_multilingual_keywords():
    """Test loading of multilingual keywords"""
    print("🧪 Testing multilingual keyword loading...")
    
    try:
        with open('multilingual_wildlife_keywords.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        print(f"✅ Successfully loaded multilingual keywords file")
        print(f"📊 Total languages: {len(data['keywords_by_language'])}")
        
        all_keywords = []
        for lang, keywords in data['keywords_by_language'].items():
            all_keywords.extend(keywords)
            print(f"  🌍 {lang}: {len(keywords)} keywords")
        
        unique_keywords = list(set(all_keywords))
        print(f"📚 Total keywords: {len(all_keywords)}")
        print(f"🔧 Unique keywords: {len(unique_keywords)}")
        print(f"📈 Deduplication rate: {(len(all_keywords) - len(unique_keywords))/len(all_keywords)*100:.1f}%")
        
        # Show sample keywords from different languages
        print("\n🌐 Sample keywords by language:")
        for lang, keywords in list(data['keywords_by_language'].items())[:5]:
            sample = keywords[:3] if len(keywords) >= 3 else keywords
            print(f"  {lang}: {sample}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading multilingual keywords: {e}")
        return False

async def test_database_connection():
    """Test Supabase database connection"""
    print("\n🧪 Testing database connection...")
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not all([supabase_url, supabase_key]):
        print("❌ Missing Supabase environment variables")
        return False
    
    try:
        headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json"
        }
        
        # Test connection with a simple query
        url = f"{supabase_url}/rest/v1/detections?select=count&limit=1"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    print("✅ Database connection successful")
                    
                    # Get some stats
                    stats_url = f"{supabase_url}/rest/v1/detections?select=platform&limit=1000"
                    async with session.get(stats_url, headers=headers) as stats_resp:
                        if stats_resp.status == 200:
                            data = await stats_resp.json()
                            platforms = {}
                            for row in data:
                                platform = row.get('platform', 'unknown')
                                platforms[platform] = platforms.get(platform, 0) + 1
                            
                            print("📊 Current database stats (recent 1000 entries):")
                            for platform, count in sorted(platforms.items(), key=lambda x: x[1], reverse=True):
                                print(f"  {platform}: {count} listings")
                    
                    return True
                else:
                    print(f"❌ Database connection failed: {resp.status}")
                    return False
                    
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_scanner_imports():
    """Test that all required imports work"""
    print("\n🧪 Testing scanner imports...")
    
    try:
        from final_production_scanner import FinalProductionScanner
        print("✅ FinalProductionScanner import successful")
        
        from comprehensive_endangered_keywords import ALL_ENDANGERED_SPECIES_KEYWORDS
        print(f"✅ Fallback keywords available: {len(ALL_ENDANGERED_SPECIES_KEYWORDS)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

async def run_mini_test():
    """Run a minimal scanner test"""
    print("\n🧪 Running mini scanner test...")
    
    try:
        from final_production_scanner import FinalProductionScanner
        
        async with FinalProductionScanner() as scanner:
            print(f"✅ Scanner initialized with {len(scanner.all_keywords)} keywords")
            
            # Test keyword batch generation
            batch = scanner.get_next_keyword_batch(size=10)
            print(f"✅ Generated keyword batch: {len(batch)} keywords")
            print(f"  Sample keywords: {batch[:3]}")
            
            # Test threat score calculation
            sample_result = {
                'title': 'Test ivory carving for sale',
                'search_term': 'ivory',
                'platform': 'test'
            }
            threat_score = scanner.calculate_threat_score(sample_result)
            print(f"✅ Threat score calculation: {threat_score}")
            
        return True
        
    except Exception as e:
        print(f"❌ Mini test error: {e}")
        return False

async def main():
    """Run all tests"""
    print("🔧 WildGuard AI - Fixed Scanner Test Suite")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Multilingual keywords
    if test_multilingual_keywords():
        tests_passed += 1
    
    # Test 2: Database connection
    if await test_database_connection():
        tests_passed += 1
    
    # Test 3: Scanner imports
    if test_scanner_imports():
        tests_passed += 1
    
    # Test 4: Mini scanner test
    if await run_mini_test():
        tests_passed += 1
    
    print(f"\n📋 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The fixed scanner should work properly.")
        print("\n🚀 Ready to deploy:")
        print("  1. Commit the changes")
        print("  2. Run the 'Fixed Multilingual Production Scanner' GitHub Action")
        print("  3. Monitor for successful database insertions")
    else:
        print("⚠️ Some tests failed. Please fix the issues before deploying.")
        
    return tests_passed == total_tests

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)
