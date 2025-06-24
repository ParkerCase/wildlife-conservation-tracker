#!/usr/bin/env python3
"""
WildGuard AI - Enhanced Duplicate Cleanup Script
Handles large datasets with pagination and batch processing
"""

import os
import asyncio
import aiohttp
from datetime import datetime
import time
from dotenv import load_dotenv
import sys
import json

# Load environment variables
load_dotenv('/Users/parkercase/conservation-bot/backend/.env')

class EnhancedDuplicateCleanup:
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            print("❌ Missing SUPABASE_URL or SUPABASE_KEY environment variables")
            sys.exit(1)
        
        print(f"✅ Connected to: {self.supabase_url[:50]}...")

    async def delete_duplicates_smart(self, session):
        """Smart duplicate deletion using window functions"""
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        
        print("🧹 Starting smart duplicate removal...")
        
        total_deleted = 0
        batch_num = 0
        
        while True:
            batch_num += 1
            start_time = time.time()
            
            # Use RPC call to delete duplicates in batches
            # This is more efficient than REST API for large operations
            rpc_url = f"{self.supabase_url}/rest/v1/rpc/delete_duplicate_listings"
            
            # If RPC doesn't exist, fall back to manual approach
            # Find duplicates manually
            query_url = f"{self.supabase_url}/rest/v1/detections"
            params = {
                "select": "id,listing_url,timestamp",
                "listing_url": "not.is.null",
                "order": "listing_url,timestamp",
                "limit": "2000"  # Process 2000 at a time
            }
            
            async with session.get(query_url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    print(f"❌ Error fetching records: {resp.status}")
                    break
                
                records = await resp.json()
                
                if len(records) < 2:
                    print("✅ No more records to process")
                    break
                
                # Find duplicates in this batch
                seen_urls = {}
                ids_to_delete = []
                
                for record in records:
                    url = record['listing_url']
                    record_id = record['id']
                    timestamp = record['timestamp']
                    
                    if url in seen_urls:
                        # This is a duplicate, mark for deletion
                        # Keep the older one (first occurrence)
                        existing_timestamp = seen_urls[url]['timestamp']
                        if timestamp > existing_timestamp:
                            ids_to_delete.append(record_id)
                        else:
                            # Current record is older, delete the previous one
                            ids_to_delete.append(seen_urls[url]['id'])
                            seen_urls[url] = {'id': record_id, 'timestamp': timestamp}
                    else:
                        seen_urls[url] = {'id': record_id, 'timestamp': timestamp}
                
                if not ids_to_delete:
                    print("✅ No duplicates found in this batch")
                    break
                
                # Delete the duplicates
                delete_count = 0
                for i in range(0, len(ids_to_delete), 100):  # Delete 100 at a time
                    batch_ids = ids_to_delete[i:i+100]
                    
                    for record_id in batch_ids:
                        delete_url = f"{self.supabase_url}/rest/v1/detections?id=eq.{record_id}"
                        
                        async with session.delete(delete_url, headers=headers) as delete_resp:
                            if delete_resp.status in [200, 204]:
                                delete_count += 1
                            else:
                                error_text = await delete_resp.text()
                                print(f"⚠️  Delete failed for ID {record_id}: {error_text}")
                    
                    await asyncio.sleep(0.1)  # Small delay between deletions
                
                total_deleted += delete_count
                duration = time.time() - start_time
                
                print(f"✅ Batch {batch_num}: Processed {len(records)} records, deleted {delete_count} duplicates in {duration:.1f}s")
                print(f"   • Total deleted so far: {total_deleted:,}")
                
                # Stop if we didn't delete anything
                if delete_count == 0:
                    break
                
                await asyncio.sleep(1)  # Pause between batches
        
        return total_deleted

    async def cleanup_duplicates_by_url(self, session):
        """Alternative approach: process duplicates URL by URL"""
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json"
        }
        
        print("🔍 Finding URLs with multiple occurrences...")
        
        # Get URLs that appear more than once
        # Note: This is a simplified approach, may need multiple runs
        query_url = f"{self.supabase_url}/rest/v1/detections"
        params = {
            "select": "listing_url",
            "listing_url": "not.is.null",
            "limit": "10000"
        }
        
        async with session.get(query_url, headers=headers, params=params) as resp:
            if resp.status != 200:
                print(f"❌ Error fetching URLs: {resp.status}")
                return 0
            
            records = await resp.json()
            
            # Count URL occurrences
            url_counts = {}
            for record in records:
                url = record['listing_url']
                url_counts[url] = url_counts.get(url, 0) + 1
            
            # Find URLs with duplicates
            duplicate_urls = [url for url, count in url_counts.items() if count > 1]
            
            print(f"📊 Found {len(duplicate_urls)} URLs with duplicates in this batch")
            
            total_deleted = 0
            
            # Process each duplicate URL
            for i, url in enumerate(duplicate_urls[:100], 1):  # Limit to 100 URLs per run
                print(f"🔧 Processing URL {i}/{min(len(duplicate_urls), 100)}: {url[:50]}...")
                
                # Get all records for this URL
                url_query = f"{self.supabase_url}/rest/v1/detections"
                url_params = {
                    "select": "id,timestamp",
                    "listing_url": f"eq.{url}",
                    "order": "timestamp"
                }
                
                async with session.get(url_query, headers=headers, params=url_params) as url_resp:
                    if url_resp.status == 200:
                        url_records = await url_resp.json()
                        
                        if len(url_records) > 1:
                            # Keep the first (oldest) record, delete the rest
                            ids_to_delete = [r['id'] for r in url_records[1:]]
                            
                            deleted_count = 0
                            for record_id in ids_to_delete:
                                delete_url = f"{self.supabase_url}/rest/v1/detections?id=eq.{record_id}"
                                
                                async with session.delete(delete_url, headers=headers) as delete_resp:
                                    if delete_resp.status in [200, 204]:
                                        deleted_count += 1
                                
                                await asyncio.sleep(0.05)  # Small delay
                            
                            total_deleted += deleted_count
                            print(f"   ✅ Deleted {deleted_count} duplicates for this URL")
                
                if i % 10 == 0:
                    await asyncio.sleep(2)  # Longer pause every 10 URLs
            
            return total_deleted

    async def run_cleanup(self):
        """Run the enhanced cleanup process"""
        print("🧹 WildGuard AI - Enhanced Duplicate Cleanup")
        print("=" * 60)
        
        timeout = aiohttp.ClientTimeout(total=600)  # 10 minute timeout
        async with aiohttp.ClientSession(timeout=timeout) as session:
            
            # Try the URL-by-URL approach first (more reliable for large datasets)
            print("🚀 Starting URL-by-URL duplicate cleanup...")
            deleted_count = await self.cleanup_duplicates_by_url(session)
            
            print(f"\n📊 Cleanup Results:")
            print(f"   • Records deleted: {deleted_count:,}")
            
            if deleted_count > 0:
                print("✅ Partial cleanup completed")
                print("💡 Run this script multiple times to clean all duplicates")
            else:
                print("🎉 No duplicates found to clean")
            
            print("\n🔧 Next Steps:")
            print("   1. Run this script multiple times until no more deletions")
            print("   2. Add unique constraint in Supabase dashboard")
            print("   3. Update scanner code to handle constraint")
            
            return deleted_count > 0

async def main():
    """Main entry point"""
    cleanup = EnhancedDuplicateCleanup()
    await cleanup.run_cleanup()

if __name__ == "__main__":
    asyncio.run(main())
