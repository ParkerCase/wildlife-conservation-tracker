#!/usr/bin/env python3
"""
WildGuard AI - Duplicate Cleanup Script
Efficiently removes ~337k duplicate records in batches
"""

import os
import asyncio
import aiohttp
from datetime import datetime
import time
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv('/Users/parkercase/conservation-bot/backend/.env')

class DuplicateCleanup:
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            print("❌ Missing SUPABASE_URL or SUPABASE_KEY environment variables")
            sys.exit(1)
        
        print(f"✅ Connected to: {self.supabase_url[:50]}...")

    async def get_duplicate_stats(self, session):
        """Get current duplicate statistics"""
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json"
        }
        
        # Get total counts
        url = f"{self.supabase_url}/rest/v1/detections?select=listing_url&listing_url=not.is.null&listing_url=neq."
        
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                total_records = len(data)
                unique_urls = len(set(item['listing_url'] for item in data if item['listing_url']))
                duplicates = total_records - unique_urls
                
                return {
                    'total': total_records,
                    'unique': unique_urls,
                    'duplicates': duplicates
                }
            else:
                print(f"❌ Error getting stats: {resp.status}")
                return None

    async def get_urls_to_keep(self, session):
        """Get the oldest record ID for each unique URL"""
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json"
        }
        
        # Get all records with URLs, ordered by timestamp
        url = f"{self.supabase_url}/rest/v1/detections?select=id,listing_url,timestamp&listing_url=not.is.null&listing_url=neq.&order=listing_url,timestamp"
        
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                
                # Find the first occurrence of each URL
                seen_urls = set()
                ids_to_keep = []
                
                for record in data:
                    url = record['listing_url']
                    if url not in seen_urls:
                        seen_urls.add(url)
                        ids_to_keep.append(record['id'])
                
                return ids_to_keep
            else:
                print(f"❌ Error getting URLs: {resp.status}")
                return []

    async def delete_duplicates_batch(self, session, ids_to_keep, batch_size=1000):
        """Delete duplicate records in batches"""
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json"
        }
        
        # Get IDs to delete (records with URLs that are NOT in ids_to_keep)
        url = f"{self.supabase_url}/rest/v1/detections?select=id&listing_url=not.is.null&listing_url=neq."
        
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                all_records = await resp.json()
                all_ids = {record['id'] for record in all_records}
                ids_to_keep_set = set(ids_to_keep)
                ids_to_delete = all_ids - ids_to_keep_set
                
                print(f"📊 Found {len(ids_to_delete):,} records to delete")
                
                # Delete in batches
                deleted_count = 0
                batch_num = 0
                
                ids_list = list(ids_to_delete)
                for i in range(0, len(ids_list), batch_size):
                    batch_num += 1
                    batch_ids = ids_list[i:i + batch_size]
                    
                    # Create filter for this batch
                    id_filter = f"id=in.({','.join(map(str, batch_ids))})"
                    delete_url = f"{self.supabase_url}/rest/v1/detections?{id_filter}"
                    
                    start_time = time.time()
                    
                    async with session.delete(delete_url, headers=headers) as delete_resp:
                        if delete_resp.status in [200, 204]:
                            batch_deleted = len(batch_ids)
                            deleted_count += batch_deleted
                            duration = time.time() - start_time
                            
                            print(f"✅ Batch {batch_num}: Deleted {batch_deleted:,} records in {duration:.1f}s")
                            print(f"   • Total deleted: {deleted_count:,}")
                            print(f"   • Remaining: {len(ids_to_delete) - deleted_count:,}")
                        else:
                            error_text = await delete_resp.text()
                            print(f"❌ Batch {batch_num} failed: {delete_resp.status} - {error_text}")
                    
                    # Brief pause between batches
                    await asyncio.sleep(0.5)
                
                return deleted_count
            else:
                print(f"❌ Error getting records to delete: {resp.status}")
                return 0

    async def add_unique_constraint(self, session):
        """Add unique constraint to prevent future duplicates"""
        # Note: This requires database admin access, may need to be done manually
        print("⚠️  Adding unique constraint requires database admin access")
        print("   Run this SQL manually in Supabase dashboard:")
        print("   ALTER TABLE detections ADD CONSTRAINT unique_listing_url UNIQUE (listing_url);")

    async def run_cleanup(self):
        """Run the complete cleanup process"""
        print("🧹 WildGuard AI - Duplicate Cleanup Starting...")
        print("=" * 60)
        
        timeout = aiohttp.ClientTimeout(total=300)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            
            # Step 1: Get current stats
            print("📊 Getting current duplicate statistics...")
            stats = await self.get_duplicate_stats(session)
            
            if not stats:
                print("❌ Could not get duplicate statistics")
                return False
            
            print(f"   • Total records with URLs: {stats['total']:,}")
            print(f"   • Unique URLs: {stats['unique']:,}")
            print(f"   • Duplicates to remove: {stats['duplicates']:,}")
            
            if stats['duplicates'] == 0:
                print("🎉 No duplicates found! Database is already clean.")
                await self.add_unique_constraint(session)
                return True
            
            # Step 2: Get IDs to keep
            print("\n🔍 Finding records to keep (oldest for each URL)...")
            ids_to_keep = await self.get_urls_to_keep(session)
            
            if not ids_to_keep:
                print("❌ Could not determine records to keep")
                return False
            
            print(f"✅ Will keep {len(ids_to_keep):,} records")
            
            # Step 3: Delete duplicates
            print(f"\n🗑️  Deleting {stats['duplicates']:,} duplicate records...")
            deleted_count = await self.delete_duplicates_batch(session, ids_to_keep)
            
            # Step 4: Verify cleanup
            print(f"\n🔍 Verifying cleanup...")
            final_stats = await self.get_duplicate_stats(session)
            
            if final_stats:
                print(f"📊 Final results:")
                print(f"   • Total records: {final_stats['total']:,}")
                print(f"   • Unique URLs: {final_stats['unique']:,}")
                print(f"   • Remaining duplicates: {final_stats['duplicates']:,}")
                print(f"   • Records deleted: {deleted_count:,}")
                
                if final_stats['duplicates'] == 0:
                    print("🎉 SUCCESS: All duplicates removed!")
                    await self.add_unique_constraint(session)
                    return True
                else:
                    print(f"⚠️  Still have {final_stats['duplicates']:,} duplicates")
                    return False
            
            return False

async def main():
    """Main entry point"""
    cleanup = DuplicateCleanup()
    success = await cleanup.run_cleanup()
    
    if success:
        print("\n✅ Duplicate cleanup completed successfully!")
        print("🔧 Next steps:")
        print("   1. Add unique constraint manually in Supabase")
        print("   2. Update scanner code to handle duplicates")
        print("   3. Run test scan to verify")
    else:
        print("\n❌ Cleanup encountered issues")
        print("💡 Try running again or check database permissions")

if __name__ == "__main__":
    asyncio.run(main())
