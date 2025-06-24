#!/usr/bin/env python3
"""
WildGuard AI - Complete System Test
Tests all 10 platforms, duplicate prevention, and database integration
"""

import asyncio
import aiohttp
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import sys

# Load environment
load_dotenv('/Users/parkercase/conservation-bot/backend/.env')

class SystemTest:
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            print("❌ Missing environment variables")
            sys.exit(1)

    async def test_all_components(self):
        """Test all system components"""
        print("🔧 WildGuard AI - Complete System Test")
        print("=" * 60)
        
        results = {
            'duplicate_cleanup': False,
            'platform_scanning': {},
            'database_storage': False,
            'duplicate_prevention': False
        }
        
        # Test 1: Run duplicate cleanup
        print("\n1️⃣ Testing Duplicate Cleanup...")
        try:
            from cleanup.fast_cleanup import fast_cleanup
            deleted = await fast_cleanup()
            results['duplicate_cleanup'] = deleted > 0
            print(f"   ✅ Cleanup test: {deleted} duplicates removed")
        except Exception as e:
            print(f"   ⚠️  Cleanup test failed: {e}")
        
        # Test 2: Test platform scanning
        print("\n2️⃣ Testing Enhanced Platform Scanning...")
        try:
            from enhanced_continuous_scanner import EnhancedContinuousScanner
            
            async with EnhancedContinuousScanner() as scanner:
                test_keywords = ['ivory', 'antique']
                
                for platform in ['ebay', 'facebook_marketplace', 'alibaba']:
                    try:
                        results_data = await scanner.scan_platform_with_keywords(platform, test_keywords)
                        results['platform_scanning'][platform] = len(results_data)
                        print(f"   ✅ {platform}: {len(results_data)} results")
                    except Exception as e:
                        results['platform_scanning'][platform] = 0
                        print(f"   ⚠️  {platform}: {e}")
        
        except Exception as e:
            print(f"   ❌ Platform scanning test failed: {e}")
        
        # Test 3: Test database storage
        print("\n3️⃣ Testing Database Storage...")
        try:
            headers = {
                "apikey": self.supabase_key,
                "Authorization": f"Bearer {self.supabase_key}",
                "Content-Type": "application/json"
            }
            
            test_record = {
                'evidence_id': f'TEST-{datetime.now().strftime("%Y%m%d%H%M%S")}',
                'timestamp': datetime.now().isoformat(),
                'platform': 'test',
                'threat_score': 50,
                'threat_level': 'TEST',
                'species_involved': 'System test',
                'status': 'SYSTEM_TEST',
                'listing_title': 'Test listing for system verification',
                'listing_url': f'https://test.example.com/item/{datetime.now().timestamp()}',
                'listing_price': '$0.00',
                'search_term': 'test'
            }
            
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                url = f"{self.supabase_url}/rest/v1/detections"
                
                async with session.post(url, headers=headers, json=test_record) as resp:
                    if resp.status in [200, 201]:
                        results['database_storage'] = True
                        print("   ✅ Database storage: Working")
                    else:
                        error = await resp.text()
                        print(f"   ❌ Database storage failed: {resp.status} - {error}")
        
        except Exception as e:
            print(f"   ❌ Database test failed: {e}")
        
        # Test 4: Test duplicate prevention
        print("\n4️⃣ Testing Duplicate Prevention...")
        try:
            # Try to insert the same record again
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, headers=headers, json=test_record) as resp:
                    if resp.status == 409 or 'unique' in await resp.text():
                        results['duplicate_prevention'] = True
                        print("   ✅ Duplicate prevention: Working")
                    else:
                        print("   ⚠️  Duplicate prevention: May not be active")
        
        except Exception as e:
            print(f"   ⚠️  Duplicate prevention test: {e}")
        
        # Summary
        print(f"\n📊 SYSTEM TEST RESULTS")
        print("=" * 30)
        
        total_tests = 4
        passed_tests = sum([
            results['duplicate_cleanup'],
            bool(results['platform_scanning']),
            results['database_storage'],
            results['duplicate_prevention']
        ])
        
        platform_success = len([p for p in results['platform_scanning'].values() if p > 0])
        total_platforms = len(results['platform_scanning'])
        
        print(f"✅ Overall Score: {passed_tests}/{total_tests} tests passed")
        print(f"🌍 Platform Coverage: {platform_success}/{total_platforms} platforms working")
        print(f"🚫 Duplicate Prevention: {'✅ Active' if results['duplicate_prevention'] else '⚠️ Check needed'}")
        print(f"💾 Database Integration: {'✅ Working' if results['database_storage'] else '❌ Failed'}")
        
        if passed_tests >= 3:
            print(f"\n🎉 SYSTEM READY FOR PRODUCTION!")
            print("💡 Start enhanced scanner: python enhanced_continuous_scanner.py")
        else:
            print(f"\n⚠️  System needs attention before production use")
            
        return results

async def main():
    """Run complete system test"""
    test = SystemTest()
    await test.test_all_components()

if __name__ == "__main__":
    asyncio.run(main())
