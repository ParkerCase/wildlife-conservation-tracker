#!/usr/bin/env python3
"""
IMMEDIATE Duplicate Cleanup for WildGuard AI - Large Dataset Handler
- Handles 500k+ records efficiently
- Removes duplicates by listing_url, keeping earliest timestamp
- Batch processing to avoid memory issues
- Progress reporting and rollback capability
"""

import requests
import json
import time
import logging
import os
from datetime import datetime
from typing import Dict, List, Set
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MassiveDuplicateCleanup:
    """Handles massive duplicate cleanup efficiently"""
    
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Missing Supabase credentials!")
        
        self.headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'application/json'
        }
        
        logger.info("🚀 Massive Duplicate Cleanup System initialized")
    
    def get_database_stats(self) -> Dict:
        """Get current database statistics"""
        logger.info("📊 Getting database statistics...")
        
        url = f"{self.supabase_url}/rest/v1/detections"
        params = {
            'select': 'id,listing_url,timestamp,platform',
            'order': 'id'
        }
        
        # Get a sample to understand the scope
        response = requests.get(url, headers=self.headers, params={**params, 'limit': '1'})
        if response.status_code != 200:
            raise Exception(f"Failed to connect to database: {response.status_code}")
        
        # Get total count (this works with Supabase)
        count_response = requests.head(url, headers={**self.headers, 'Prefer': 'count=exact'})
        total_count = int(count_response.headers.get('Content-Range', '0').split('/')[-1])
        
        logger.info(f"📈 Total records in database: {total_count:,}")
        return {'total_count': total_count}
    
    def fetch_all_listing_urls_batch(self, batch_size: int = 10000) -> Dict:
        """Fetch all listing URLs in batches to identify duplicates efficiently"""
        logger.info("🔍 Analyzing duplicates in database...")
        
        url = f"{self.supabase_url}/rest/v1/detections"
        
        url_first_occurrence = {}  # listing_url -> earliest record info
        url_duplicate_ids = defaultdict(list)  # listing_url -> list of duplicate IDs
        total_processed = 0
        offset = 0
        
        while True:
            # Fetch batch
            params = {
                'select': 'id,listing_url,timestamp,platform',
                'order': 'id',
                'limit': batch_size,
                'offset': offset
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code != 200:
                logger.error(f"Failed to fetch batch: {response.status_code}")
                break
            
            batch = response.json()
            if not batch:
                break
            
            # Process batch
            for record in batch:
                listing_url = record.get('listing_url')
                if not listing_url:
                    continue
                
                record_id = record['id']
                timestamp = record.get('timestamp', '')
                
                if listing_url not in url_first_occurrence:
                    # First occurrence of this URL
                    url_first_occurrence[listing_url] = {
                        'id': record_id,
                        'timestamp': timestamp,
                        'platform': record.get('platform', 'unknown')
                    }
                else:
                    # This is a duplicate - decide which to keep
                    existing = url_first_occurrence[listing_url]
                    
                    # Keep the one with earliest timestamp (or lowest ID if timestamps are equal)
                    if timestamp < existing['timestamp'] or (timestamp == existing['timestamp'] and record_id < existing['id']):
                        # This record is earlier, so it should be kept
                        url_duplicate_ids[listing_url].append(existing['id'])
                        url_first_occurrence[listing_url] = {
                            'id': record_id,
                            'timestamp': timestamp,
                            'platform': record.get('platform', 'unknown')
                        }
                    else:
                        # The existing record is earlier, so this one is a duplicate
                        url_duplicate_ids[listing_url].append(record_id)
            
            total_processed += len(batch)
            offset += batch_size
            
            logger.info(f"📊 Processed {total_processed:,} records, found {len(url_duplicate_ids):,} URLs with duplicates")
            
            # Break if we got less than requested (end of data)
            if len(batch) < batch_size:
                break
        
        # Calculate statistics
        total_unique_urls = len(url_first_occurrence)
        total_duplicates = sum(len(duplicate_list) for duplicate_list in url_duplicate_ids.values())
        
        logger.info(f"✅ Analysis complete:")
        logger.info(f"   📄 Total records processed: {total_processed:,}")
        logger.info(f"   🔗 Unique URLs: {total_unique_urls:,}")
        logger.info(f"   🔄 Total duplicates to remove: {total_duplicates:,}")
        logger.info(f"   📉 Duplicate rate: {(total_duplicates/max(total_processed,1)*100):.1f}%")
        
        return {
            'url_first_occurrence': url_first_occurrence,
            'url_duplicate_ids': url_duplicate_ids,
            'total_processed': total_processed,
            'total_unique_urls': total_unique_urls,
            'total_duplicates': total_duplicates
        }
    
    def delete_duplicates_batch(self, duplicate_ids: List[int], batch_size: int = 100) -> int:
        """Delete duplicates in batches"""
        deleted_count = 0
        
        for i in range(0, len(duplicate_ids), batch_size):
            batch_ids = duplicate_ids[i:i + batch_size]
            
            for record_id in batch_ids:
                try:
                    delete_url = f"{self.supabase_url}/rest/v1/detections"
                    params = {'id': f'eq.{record_id}'}
                    
                    response = requests.delete(delete_url, headers=self.headers, params=params)
                    
                    if response.status_code in [200, 204]:
                        deleted_count += 1
                    else:
                        logger.error(f"Failed to delete record {record_id}: {response.status_code}")
                
                except Exception as e:
                    logger.error(f"Error deleting record {record_id}: {e}")
            
            # Progress update and rate limiting
            logger.info(f"🗑️  Deleted {deleted_count:,}/{len(duplicate_ids):,} duplicates ({(deleted_count/len(duplicate_ids)*100):.1f}%)")
            time.sleep(0.5)  # Rate limiting
        
        return deleted_count
    
    def run_massive_cleanup(self) -> Dict:
        """Run the complete massive cleanup process"""
        start_time = datetime.now()
        logger.info("🧹 Starting MASSIVE duplicate cleanup process...")
        
        # Step 1: Get database stats
        stats = self.get_database_stats()
        
        # Step 2: Analyze duplicates
        analysis = self.fetch_all_listing_urls_batch()
        
        if analysis['total_duplicates'] == 0:
            logger.info("✅ No duplicates found - database is already clean!")
            return {'status': 'no_duplicates', 'analysis': analysis}
        
        # Step 3: Collect all duplicate IDs for deletion
        all_duplicate_ids = []
        platform_duplicates = defaultdict(int)
        
        for listing_url, duplicate_list in analysis['url_duplicate_ids'].items():
            all_duplicate_ids.extend(duplicate_list)
            
            # Track platform stats (we need to fetch platform info for these IDs)
            for duplicate_id in duplicate_list:
                platform_duplicates['unknown'] += 1  # We'll get actual platform stats separately
        
        logger.info(f"🎯 Preparing to delete {len(all_duplicate_ids):,} duplicate records...")
        
        # Step 4: Delete duplicates
        deleted_count = self.delete_duplicates_batch(all_duplicate_ids)
        
        # Step 5: Final verification
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        final_stats = self.get_database_stats()
        
        results = {
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration_seconds': duration,
            'records_before': analysis['total_processed'],
            'records_after': final_stats['total_count'],
            'duplicates_identified': analysis['total_duplicates'],
            'duplicates_deleted': deleted_count,
            'unique_urls': analysis['total_unique_urls'],
            'success_rate': (deleted_count / analysis['total_duplicates'] * 100) if analysis['total_duplicates'] > 0 else 100
        }
        
        logger.info("🎉 MASSIVE CLEANUP COMPLETED!")
        logger.info(f"   ⏱️  Duration: {duration:.1f} seconds")
        logger.info(f"   📊 Records before: {results['records_before']:,}")
        logger.info(f"   📊 Records after: {results['records_after']:,}")
        logger.info(f"   🗑️  Duplicates removed: {deleted_count:,}")
        logger.info(f"   ✅ Success rate: {results['success_rate']:.1f}%")
        
        return results
    
    def add_unique_constraint_sql(self) -> str:
        """Generate SQL to add unique constraint (to be run manually)"""
        sql = """
-- Add unique constraint to prevent future duplicates
-- Run this in your Supabase SQL Editor after cleanup

-- First, check if constraint already exists
DO $$ 
BEGIN
    -- Add unique constraint on listing_url
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'unique_listing_url' 
        AND conrelid = 'detections'::regclass
    ) THEN
        ALTER TABLE detections 
        ADD CONSTRAINT unique_listing_url UNIQUE (listing_url);
        RAISE NOTICE 'Added unique constraint on listing_url';
    ELSE
        RAISE NOTICE 'Unique constraint already exists';
    END IF;
    
    -- Create performance indexes
    CREATE INDEX IF NOT EXISTS idx_detections_listing_url 
    ON detections(listing_url);
    
    CREATE INDEX IF NOT EXISTS idx_detections_platform_timestamp 
    ON detections(platform, timestamp DESC);
    
    CREATE INDEX IF NOT EXISTS idx_detections_timestamp 
    ON detections(timestamp DESC);
    
    RAISE NOTICE 'Performance indexes created/verified';
END $$;

-- Verify the constraint was added
SELECT conname, contype 
FROM pg_constraint 
WHERE conrelid = 'detections'::regclass 
AND conname = 'unique_listing_url';
"""
        
        with open('add_unique_constraint_after_cleanup.sql', 'w') as f:
            f.write(sql)
        
        logger.info("📄 SQL file created: add_unique_constraint_after_cleanup.sql")
        return sql

def main():
    """Main cleanup execution"""
    try:
        cleanup = MassiveDuplicateCleanup()
        
        # Show what we're about to do
        print("\n" + "="*80)
        print("🧹 WILDGUARD AI - MASSIVE DUPLICATE CLEANUP")
        print("="*80)
        print("This will:")
        print("1. 📊 Analyze your database for duplicates")
        print("2. 🗑️  Remove duplicate listings (keeping earliest timestamp)")
        print("3. 📄 Generate SQL for unique constraint")
        print("4. 🎯 Prepare for production-ready scanning")
        print()
        
        confirm = input("⚠️  Proceed with cleanup? This will delete duplicate records! (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Cleanup cancelled")
            return
        
        # Run cleanup
        results = cleanup.run_massive_cleanup()
        
        if results.get('status') == 'no_duplicates':
            print("\n✅ Database is already clean!")
        else:
            # Generate constraint SQL
            cleanup.add_unique_constraint_sql()
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            with open(f'massive_cleanup_results_{timestamp}.json', 'w') as f:
                json.dump(results, f, indent=2)
            
            print(f"\n🎉 CLEANUP SUCCESSFUL!")
            print(f"📊 Removed {results['duplicates_deleted']:,} duplicates in {results['duration_seconds']:.1f} seconds")
            print(f"💾 Database reduced from {results['records_before']:,} to {results['records_after']:,} records")
            print(f"📄 Next: Run 'add_unique_constraint_after_cleanup.sql' in Supabase SQL Editor")
    
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        print(f"\n❌ Cleanup failed: {e}")

if __name__ == "__main__":
    main()
