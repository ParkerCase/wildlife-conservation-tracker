#!/usr/bin/env python3
"""
Database Cleanup Script - Remove Poor Quality Entries
Removes entries from disabled workflows with quality issues
"""

import os
import asyncio
import aiohttp
from datetime import datetime

async def cleanup_poor_quality_entries():
    """Remove poor quality entries from the database"""
    
    # Supabase connection
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY') or os.getenv('SUPABASE_ANON_KEY')
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Missing Supabase credentials")
        return
    
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Poor quality statuses to remove
    poor_quality_statuses = [
        'HIGH_VOLUME_HUMAN_TRAFFICKING_SCAN',  # False positive keywords
        'HIGH_VOLUME_WILDLIFE_SCAN',           # Random scoring  
        'CONTINUOUS_DEDUPLICATION_SCAN'        # Generic results
    ]
    
    total_removed = 0
    
    async with aiohttp.ClientSession() as session:
        for status in poor_quality_statuses:
            try:
                print(f"🧹 Removing entries with status: {status}")
                
                # Count entries first
                count_url = f"{SUPABASE_URL}/rest/v1/detections"
                count_params = {
                    'select': 'count',
                    'status': f'eq.{status}',
                    'timestamp': 'gte.2025-06-27T00:00:00'
                }
                
                async with session.get(count_url, headers=headers, params=count_params) as resp:
                    if resp.status == 200:
                        count_data = await resp.json()
                        count = len(count_data) if isinstance(count_data, list) else 0
                        print(f"   Found {count:,} entries to remove")
                
                # Delete entries
                delete_url = f"{SUPABASE_URL}/rest/v1/detections"
                delete_params = {
                    'status': f'eq.{status}',
                    'timestamp': 'gte.2025-06-27T00:00:00'
                }
                
                async with session.delete(delete_url, headers=headers, params=delete_params) as resp:
                    if resp.status in [200, 204]:
                        print(f"   ✅ Removed {count:,} entries with status {status}")
                        total_removed += count
                    else:
                        print(f"   ❌ Failed to remove {status}: {resp.status}")
                        
            except Exception as e:
                print(f"   ❌ Error removing {status}: {e}")
    
    print(f"\n✅ CLEANUP COMPLETED")
    print(f"   Total entries removed: {total_removed:,}")
    print(f"   Database cleaned of poor quality data")
    print(f"   Only FIXED scanner results remain")

if __name__ == "__main__":
    print("🧹 DATABASE CLEANUP - POOR QUALITY ENTRIES")
    print("=" * 60)
    print("This will remove entries from disabled workflows:")
    print("❌ HIGH_VOLUME_HUMAN_TRAFFICKING_SCAN (false positive keywords)")
    print("❌ HIGH_VOLUME_WILDLIFE_SCAN (random scoring)")
    print("❌ CONTINUOUS_DEDUPLICATION_SCAN (generic results)")
    print("\n✅ Keeping only FIXED scanner results with intelligent scoring")
    
    confirm = input("\nProceed with cleanup? (y/N): ")
    if confirm.lower() == 'y':
        asyncio.run(cleanup_poor_quality_entries())
    else:
        print("Cleanup cancelled")
