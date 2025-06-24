#!/usr/bin/env python3
"""
WildGuard AI - Production-Ready Cleanup Script
Uses batch processing for 332k+ duplicates
"""

import os
import asyncio
import aiohttp
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('/Users/parkercase/conservation-bot/backend/.env')

async def fast_cleanup():
    """Fast cleanup using batch operations"""
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json"
    }
    
    print("🚀 Fast cleanup starting...")
    total_deleted = 0
    
    timeout = aiohttp.ClientTimeout(total=300)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        
        # Run multiple cleanup iterations
        for iteration in range(50):  # Up to 50 iterations
            print(f"\n🔄 Iteration {iteration + 1}/50")
            
            # Get a batch of records to process
            url = f"{supabase_url}/rest/v1/detections"
            params = {
                "select": "id,listing_url,timestamp",
                "listing_url": "not.is.null",
                "order": "listing_url,timestamp",
                "limit": "5000"  # Larger batches
            }
            
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    print(f"❌ Error: {resp.status}")
                    break
                
                records = await resp.json()
                if len(records) < 2:
                    print("✅ No more records to process")
                    break
                
                # Group by URL and find duplicates
                url_groups = {}
                for record in records:
                    url = record['listing_url']
                    if url not in url_groups:
                        url_groups[url] = []
                    url_groups[url].append(record)
                
                # Find IDs to delete (keep oldest for each URL)
                ids_to_delete = []
                for url, group in url_groups.items():
                    if len(group) > 1:
                        # Sort by timestamp, keep first (oldest)
                        sorted_group = sorted(group, key=lambda x: x['timestamp'])
                        ids_to_delete.extend([r['id'] for r in sorted_group[1:]])
                
                if not ids_to_delete:
                    print("   No duplicates found in this batch")
                    continue
                
                # Delete in smaller chunks
                deleted_this_round = 0
                for i in range(0, len(ids_to_delete), 50):
                    chunk = ids_to_delete[i:i+50]
                    id_list = ','.join(map(str, chunk))
                    
                    delete_url = f"{supabase_url}/rest/v1/detections?id=in.({id_list})"
                    
                    async with session.delete(delete_url, headers=headers) as delete_resp:
                        if delete_resp.status in [200, 204]:
                            deleted_this_round += len(chunk)
                        else:
                            error = await delete_resp.text()
                            print(f"⚠️  Delete error: {error}")
                    
                    await asyncio.sleep(0.1)
                
                total_deleted += deleted_this_round
                print(f"   ✅ Deleted {deleted_this_round} duplicates")
                print(f"   📊 Total deleted: {total_deleted:,}")
                
                if deleted_this_round == 0:
                    print("   No more duplicates found")
                    break
                
                await asyncio.sleep(1)
        
        print(f"\n🎉 Fast cleanup completed!")
        print(f"📊 Total records deleted: {total_deleted:,}")
        
        return total_deleted

if __name__ == "__main__":
    asyncio.run(fast_cleanup())
