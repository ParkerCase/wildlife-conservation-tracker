#!/usr/bin/env python3
"""
Quick test script to verify multilingual scanner setup
"""

import os
import json
import sys
import requests
from datetime import datetime

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ dotenv loaded")
except ImportError:
    print("⚠️ dotenv not available, using direct env vars")

def test_multilingual_keywords():
    """Test loading multilingual keywords"""
    try:
        multilingual_file = "multilingual_wildlife_keywords.json"
        if os.path.exists(multilingual_file):
            with open(multilingual_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            keywords_by_language = data.get('keywords_by_language', {})
            total_keywords = sum(len(keywords) for keywords in keywords_by_language.values())
            
            print(f"✅ Multilingual keywords loaded: {total_keywords} total")
            print(f"✅ Languages available: {len(keywords_by_language)}")
            
            # Show sample from each language
            for lang_code, keywords in list(keywords_by_language.items())[:5]:
                lang_name = data.get('language_info', {}).get(lang_code, lang_code)
                print(f"   {lang_name} ({lang_code}): {len(keywords)} keywords")
                if keywords:
                    print(f"      Sample: {keywords[0]}")
            
            return True, total_keywords
        else:
            print(f"❌ Multilingual file not found: {multilingual_file}")
            return False, 0
    except Exception as e:
        print(f"❌ Error loading multilingual keywords: {e}")
        return False, 0

def test_supabase_connection():
    """Test Supabase connection"""
    try:
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        print(f"📡 Testing Supabase connection...")
        print(f"   URL: {supabase_url}")
        print(f"   Key: {supabase_key[:20]}..." if supabase_key else "   Key: None")
        
        if not supabase_url or not supabase_key:
            print("❌ Missing Supabase credentials")
            return False
        
        # Test connection by getting count
        check_url = f"{supabase_url}/rest/v1/detections"
        check_params = {'select': 'count'}
        headers = {
            'apikey': supabase_key,
            'Authorization': f'Bearer {supabase_key}'
        }
        
        response = requests.get(check_url, params=check_params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Supabase connection successful")
            print(f"✅ Response status: {response.status_code}")
            return True
        else:
            print(f"❌ Supabase connection failed: {response.status_code}")
            print(f"Response: {response.text[:100]}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Supabase connection: {e}")
        return False

def test_save_sample_listing():
    """Test saving a sample listing"""
    try:
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not supabase_url or not supabase_key:
            print("❌ Cannot test save: Missing Supabase credentials")
            return False
        
        # Create a test listing
        evidence_id = f"TEST-MULTILINGUAL-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        insert_url = f"{supabase_url}/rest/v1/detections"
        insert_headers = {
            'apikey': supabase_key,
            'Authorization': f'Bearer {supabase_key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        }
        
        data = {
            'evidence_id': evidence_id,
            'timestamp': datetime.now().isoformat(),
            'platform': 'test_multilingual',
            'threat_score': 85,
            'threat_level': 'TEST',
            'species_involved': 'Test multilingual scanner: 象牙 (elephant ivory in Chinese)',
            'alert_sent': False,
            'status': 'MULTILINGUAL_TEST_ZH',
            'listing_title': 'Test multilingual detection',
            'listing_url': f'https://test.example.com/test-{evidence_id}',
            'listing_price': 'Test price',
            'search_term': '象牙'
        }
        
        response = requests.post(insert_url, json=data, headers=insert_headers, timeout=10)
        
        if response.status_code in [200, 201]:
            print(f"✅ Test listing saved successfully")
            print(f"✅ Evidence ID: {evidence_id}")
            return True
        else:
            print(f"❌ Failed to save test listing: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error saving test listing: {e}")
        return False

def main():
    print("🧪 TESTING MULTILINGUAL SCANNER SETUP")
    print("=" * 60)
    
    # Test 1: Multilingual keywords
    keywords_ok, total_keywords = test_multilingual_keywords()
    
    # Test 2: Supabase connection
    print(f"\n" + "-" * 40)
    supabase_ok = test_supabase_connection()
    
    # Test 3: Save sample listing
    print(f"\n" + "-" * 40)
    save_ok = test_save_sample_listing()
    
    # Summary
    print(f"\n" + "=" * 60)
    print("🎯 TEST RESULTS:")
    print(f"   Keywords loaded: {'✅' if keywords_ok else '❌'} ({total_keywords} total)")
    print(f"   Supabase connection: {'✅' if supabase_ok else '❌'}")
    print(f"   Database save test: {'✅' if save_ok else '❌'}")
    
    if keywords_ok and supabase_ok and save_ok:
        print(f"\n🎉 ALL TESTS PASSED! Multilingual scanner ready!")
        print(f"🚀 You can now run the full multilingual scanner")
        return 0
    else:
        print(f"\n⚠️ Some tests failed. Check configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
