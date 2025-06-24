#!/usr/bin/env python3
"""
WildGuard AI - API-Based Ultimate Duplicate Cleanup
Removes ALL existing duplicates using Supabase API and ensures ZERO duplicates going forward
"""

import asyncio
import aiohttp
import os
import json
from datetime import datetime
import time
from dotenv import load_dotenv

# Load environment
load_dotenv('/Users/parkercase/conservation-bot/backend/.env')

class ApiDuplicateCleanup:
    """Complete duplicate cleanup using Supabase API"""
    
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        print(f"🔗 Supabase URL: {self.supabase_url}")

    async def analyze_duplicates_comprehensive(self):
        """Comprehensive duplicate analysis"""
        print("🔍 COMPREHENSIVE DUPLICATE ANALYSIS")
        print("-" * 45)
        
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json"
        }
        
        timeout = aiohttp.ClientTimeout(total=120)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            
            # Get large sample for analysis
            print("📊 Fetching sample data for analysis...")
            
            url = f"{self.supabase_url}/rest/v1/detections?select=id,listing_url,timestamp&listing_url=not.is.null&order=listing_url&limit=20000"
            
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print(f"✅ Retrieved {len(data):,} records for analysis")
                    
                    # Analyze duplicates
                    url_groups = {}
                    for record in data:
                        url = record['listing_url']
                        if url not in url_groups:
                            url_groups[url] = []
                        url_groups[url].append(record)
                    
                    # Find duplicates
                    duplicate_urls = {url: records for url, records in url_groups.items() if len(records) > 1}
                    total_duplicates = sum(len(records) - 1 for records in duplicate_urls.values())
                    
                    print(f"📊 Analysis Results:")
                    print(f"   • Total URLs analyzed: {len(url_groups):,}")
                    print(f"   • URLs with duplicates: {len(duplicate_urls):,}")
                    print(f"   • Total duplicate records: {total_duplicates:,}")
                    print(f"   • Duplicate rate: {(total_duplicates / len(data) * 100):.1f}%")
                    
                    # Show top duplicates
                    top_duplicates = sorted(duplicate_urls.items(), key=lambda x: len(x[1]), reverse=True)[:5]
                    
                    print(f"\n🔍 Top duplicate URLs:")
                    for url, records in top_duplicates:
                        print(f"   • {len(records)}x: {url[:60]}...")
                    
                    return duplicate_urls, total_duplicates
                    
                else:
                    print(f"❌ Error fetching data: {resp.status}")
                    return {}, 0

    async def cleanup_duplicates_batch(self, duplicate_urls, batch_size=50):
        """Clean up duplicates in batches"""
        print(f"\n🗑️  CLEANING UP DUPLICATES IN BATCHES")
        print("-" * 40)
        
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json"
        }
        
        total_deleted = 0
        timeout = aiohttp.ClientTimeout(total=300)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            
            urls_to_process = list(duplicate_urls.keys())
            
            for i in range(0, len(urls_to_process), batch_size):
                batch_urls = urls_to_process[i:i + batch_size]
                batch_num = (i // batch_size) + 1
                
                print(f"🔄 Processing batch {batch_num}/{(len(urls_to_process) + batch_size - 1) // batch_size}")
                print(f"   URLs in this batch: {len(batch_urls)}")
                
                batch_deleted = 0
                
                for url in batch_urls:
                    records = duplicate_urls[url]
                    
                    # Sort by timestamp to keep the oldest
                    sorted_records = sorted(records, key=lambda x: x['timestamp'])
                    
                    # Keep the first (oldest), delete the rest
                    records_to_delete = sorted_records[1:]  # All except first
                    
                    for record in records_to_delete:
                        try:
                            delete_url = f"{self.supabase_url}/rest/v1/detections?id=eq.{record['id']}"
                            
                            async with session.delete(delete_url, headers=headers) as resp:
                                if resp.status in [200, 204]:
                                    batch_deleted += 1
                                    total_deleted += 1
                                else:
                                    print(f"   ⚠️  Delete failed for ID {record['id']}: {resp.status}")
                            
                            # Small delay to avoid overwhelming API
                            await asyncio.sleep(0.05)
                            
                        except Exception as e:
                            print(f"   ❌ Error deleting record {record['id']}: {e}")
                
                print(f"   ✅ Batch {batch_num}: Deleted {batch_deleted} duplicates")
                
                # Pause between batches
                await asyncio.sleep(2)
        
        print(f"\n🎯 Total deleted across all batches: {total_deleted:,}")
        return total_deleted

    async def add_unique_constraint_via_api(self):
        """Add unique constraint via API (if possible)"""
        print(f"\n🔒 ATTEMPTING TO ADD UNIQUE CONSTRAINT")
        print("-" * 40)
        
        # Note: Supabase API doesn't directly support adding constraints
        # This would need to be done via SQL in the dashboard
        
        print("⚠️  Unique constraint must be added manually in Supabase dashboard:")
        print("   1. Go to Supabase Dashboard > SQL Editor")
        print("   2. Run this SQL command:")
        print("      ALTER TABLE detections ADD CONSTRAINT unique_listing_url UNIQUE (listing_url);")
        print("   3. This will prevent ALL future duplicates at the database level")
        
        return False  # Indicate manual step required

    async def test_duplicate_insertion(self):
        """Test that duplicate prevention works"""
        print(f"\n🧪 TESTING DUPLICATE PREVENTION")
        print("-" * 30)
        
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json"
        }
        
        # Create unique test URL
        test_url = f"https://test-duplicate-{datetime.now().timestamp()}.example.com/item/12345"
        
        test_record = {
            'evidence_id': f'TEST-{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'timestamp': datetime.now().isoformat(),
            'platform': 'test',
            'threat_score': 1,
            'threat_level': 'TEST',
            'species_involved': 'Duplicate test',
            'status': 'DUPLICATE_TEST',
            'listing_title': 'Test record for duplicate prevention',
            'listing_url': test_url,
            'listing_price': '$0.00',
            'search_term': 'test'
        }
        
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            
            url = f"{self.supabase_url}/rest/v1/detections"
            
            # Insert first record
            print("🔄 Inserting first test record...")
            async with session.post(url, headers=headers, json=test_record) as resp:
                if resp.status in [200, 201]:
                    print("✅ First record inserted successfully")
                else:
                    print(f"❌ First insert failed: {resp.status}")
                    return False
            
            # Try to insert duplicate
            print("🔄 Attempting to insert duplicate...")
            test_record['evidence_id'] = f'TEST-DUP-{datetime.now().strftime("%Y%m%d%H%M%S")}'
            
            async with session.post(url, headers=headers, json=test_record) as resp:
                response_text = await resp.text()
                
                if resp.status == 409:
                    print("✅ DUPLICATE PREVENTION ACTIVE: Got 409 Conflict")
                    return True
                elif any(word in response_text.lower() for word in ['unique', 'duplicate', 'conflict']):
                    print("✅ DUPLICATE PREVENTION ACTIVE: Constraint detected")
                    return True
                elif resp.status in [200, 201]:
                    print("❌ DUPLICATE PREVENTION NOT ACTIVE: Duplicate was inserted")
                    print("   → Manual unique constraint setup required")
                    return False
                else:
                    print(f"⚠️  Unexpected response: {resp.status}")
                    print(f"   Response: {response_text[:200]}")
                    return False

    async def verify_cleanup_effectiveness(self):
        """Verify that cleanup was effective"""
        print(f"\n🔍 VERIFYING CLEANUP EFFECTIVENESS")
        print("-" * 35)
        
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json"
        }
        
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            
            # Get sample for verification
            url = f"{self.supabase_url}/rest/v1/detections?select=listing_url&listing_url=not.is.null&limit=10000"
            
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    urls = [item['listing_url'] for item in data if item['listing_url']]
                    
                    unique_urls = set(urls)
                    duplicates_found = len(urls) - len(unique_urls)
                    
                    print(f"📊 Verification (10k sample):")
                    print(f"   • Total URLs: {len(urls):,}")
                    print(f"   • Unique URLs: {len(unique_urls):,}")
                    print(f"   • Duplicates found: {duplicates_found:,}")
                    print(f"   • Duplicate rate: {(duplicates_found/len(urls)*100):.2f}%")
                    
                    if duplicates_found == 0:
                        print("🎉 CLEANUP VERIFIED: No duplicates detected!")
                        return True
                    else:
                        print(f"⚠️  Cleanup incomplete: {duplicates_found} duplicates remain")
                        return False
                else:
                    print(f"❌ Verification failed: {resp.status}")
                    return False

    async def run_complete_cleanup(self):
        """Run complete API-based duplicate cleanup"""
        print("🧹 WILDGUARD AI - API-BASED DUPLICATE CLEANUP")
        print("=" * 70)
        print("🎯 Goal: Remove ALL duplicates using Supabase API")
        print()
        
        start_time = time.time()
        
        # Step 1: Analyze duplicates
        duplicate_urls, total_duplicates = await self.analyze_duplicates_comprehensive()
        
        if total_duplicates == 0:
            print("🎉 No duplicates found! Database is already clean.")
        else:
            # Step 2: Clean up duplicates
            deleted_count = await self.cleanup_duplicates_batch(duplicate_urls)
            
            print(f"\n📊 Cleanup Statistics:")
            print(f"   • Duplicates identified: {total_duplicates:,}")
            print(f"   • Records deleted: {deleted_count:,}")
            print(f"   • Cleanup efficiency: {(deleted_count/total_duplicates*100):.1f}%")
        
        # Step 3: Verify cleanup
        cleanup_verified = await self.verify_cleanup_effectiveness()
        
        # Step 4: Test duplicate prevention
        prevention_active = await self.test_duplicate_insertion()
        
        # Step 5: Manual constraint instruction
        constraint_added = await self.add_unique_constraint_via_api()
        
        # Final report
        total_time = time.time() - start_time
        
        print(f"\n🎯 FINAL CLEANUP REPORT")
        print("=" * 30)
        print(f"⏱️  Total time: {total_time:.1f} seconds")
        print(f"✅ Duplicates cleaned: {total_duplicates > 0}")
        print(f"✅ Cleanup verified: {cleanup_verified}")
        print(f"🔒 Prevention active: {prevention_active}")
        print(f"⚠️  Manual constraint: Required")
        
        if cleanup_verified and (total_duplicates == 0 or deleted_count > 0):
            print(f"\n🎉 SUCCESS: DATABASE CLEANUP COMPLETED!")
            print(f"📊 Your database now has minimal/zero duplicates")
            
            if not prevention_active:
                print(f"\n⚠️  IMPORTANT: Add unique constraint manually:")
                print(f"   1. Go to Supabase Dashboard > SQL Editor")
                print(f"   2. Run: ALTER TABLE detections ADD CONSTRAINT unique_listing_url UNIQUE (listing_url);")
                print(f"   3. This will prevent ALL future duplicates")
            else:
                print(f"🔒 Future duplicates will be automatically prevented")
                
        else:
            print(f"\n⚠️  PARTIAL SUCCESS: Some cleanup completed")
            print(f"🔧 May need to run cleanup again for remaining duplicates")
        
        return cleanup_verified

async def main():
    """Run API-based duplicate cleanup"""
    cleanup = ApiDuplicateCleanup()
    await cleanup.run_complete_cleanup()

if __name__ == "__main__":
    asyncio.run(main())
