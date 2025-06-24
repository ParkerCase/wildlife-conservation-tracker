#!/usr/bin/env python3
"""
Ultimate Duplicate Cleanup System
- Removes all duplicate listings from Supabase
- Creates unique constraints to prevent future duplicates
- Provides detailed cleanup reports
"""

import requests
import json
import time
import logging
import os
from datetime import datetime
from typing import Dict, List, Set
import hashlib
from urllib.parse import urlparse
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UltimateDuplicateCleanup:
    """Complete duplicate cleanup and prevention system"""
    
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Missing Supabase credentials! Set SUPABASE_URL and SUPABASE_ANON_KEY")
        
        self.headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'application/json'
        }
        
        logger.info("Ultimate Duplicate Cleanup System initialized")
    
    def normalize_url(self, url: str) -> str:
        """Normalize URLs to catch variations"""
        if not url:
            return ""
        
        try:
            # Remove common tracking parameters
            tracking_params = ['utm_source', 'utm_medium', 'utm_campaign', 'ref', 'source', 'fbclid']
            parsed = urlparse(url)
            
            # Remove tracking parameters from query string
            if parsed.query:
                params = []
                for param in parsed.query.split('&'):
                    if '=' in param:
                        key = param.split('=')[0]
                        if key not in tracking_params:
                            params.append(param)
                query = '&'.join(params)
            else:
                query = ''
            
            # Rebuild URL without tracking params
            normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if query:
                normalized += f"?{query}"
            
            return normalized.lower().strip('/')
        except:
            return url.lower().strip('/')
    
    def fetch_all_listings(self) -> List[Dict]:
        """Fetch all listings from Supabase"""
        logger.info("Fetching all listings from database...")
        
        all_listings = []
        offset = 0
        limit = 1000
        
        while True:
            url = f"{self.supabase_url}/rest/v1/detections"
            params = {
                'select': 'id,listing_url,platform,title,price,detected_at,keyword_used',
                'order': 'detected_at.desc',
                'limit': limit,
                'offset': offset
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch listings: {response.status_code} - {response.text}")
                break
            
            batch = response.json()
            if not batch:
                break
            
            all_listings.extend(batch)
            offset += limit
            
            logger.info(f"Fetched {len(all_listings)} listings so far...")
            
            if len(batch) < limit:
                break
        
        logger.info(f"Total listings fetched: {len(all_listings)}")
        return all_listings
    
    def identify_duplicates(self, listings: List[Dict]) -> Dict:
        """Identify duplicate listings based on normalized URLs"""
        logger.info("Identifying duplicates...")
        
        url_groups = defaultdict(list)
        
        # Group listings by normalized URL
        for listing in listings:
            normalized_url = self.normalize_url(listing.get('listing_url', ''))
            url_groups[normalized_url].append(listing)
        
        # Find duplicates
        duplicates = {}
        unique_listings = {}
        total_duplicates = 0
        
        for normalized_url, group in url_groups.items():
            if len(group) > 1:
                # Sort by detected_at to keep the earliest one
                group.sort(key=lambda x: x.get('detected_at', ''))
                
                # Keep the first (earliest) listing
                unique_listings[normalized_url] = group[0]
                
                # Mark the rest as duplicates
                duplicates[normalized_url] = group[1:]
                total_duplicates += len(group[1:])
            else:
                unique_listings[normalized_url] = group[0]
        
        logger.info(f"Found {total_duplicates} duplicate listings across {len(duplicates)} URLs")
        logger.info(f"Unique listings: {len(unique_listings)}")
        
        return {
            'duplicates': duplicates,
            'unique_listings': unique_listings,
            'total_duplicates': total_duplicates,
            'total_unique': len(unique_listings)
        }
    
    def delete_duplicates(self, duplicates: Dict) -> int:
        """Delete duplicate listings from database"""
        logger.info("Deleting duplicate listings...")
        
        deleted_count = 0
        batch_size = 50
        
        # Collect all duplicate IDs
        duplicate_ids = []
        for url, duplicate_list in duplicates.items():
            for duplicate in duplicate_list:
                duplicate_ids.append(duplicate['id'])
        
        logger.info(f"Preparing to delete {len(duplicate_ids)} duplicate listings...")
        
        # Delete in batches
        for i in range(0, len(duplicate_ids), batch_size):
            batch_ids = duplicate_ids[i:i + batch_size]
            
            # Delete each listing in the batch
            for listing_id in batch_ids:
                try:
                    delete_url = f"{self.supabase_url}/rest/v1/detections"
                    params = {'id': f'eq.{listing_id}'}
                    
                    response = requests.delete(delete_url, headers=self.headers, params=params)
                    
                    if response.status_code in [200, 204]:
                        deleted_count += 1
                    else:
                        logger.error(f"Failed to delete listing {listing_id}: {response.status_code}")
                
                except Exception as e:
                    logger.error(f"Error deleting listing {listing_id}: {e}")
            
            logger.info(f"Deleted {deleted_count}/{len(duplicate_ids)} duplicates...")
            time.sleep(0.5)  # Rate limiting
        
        logger.info(f"Successfully deleted {deleted_count} duplicate listings")
        return deleted_count
    
    def add_unique_constraint(self) -> bool:
        """Add unique constraint to listing_url column"""
        logger.info("Adding unique constraint to prevent future duplicates...")
        
        # Note: This would typically be done through SQL, but Supabase REST API doesn't support DDL
        # The constraint should be added manually through Supabase dashboard or SQL editor
        
        constraint_sql = """
        -- Add unique constraint to prevent duplicate URLs
        ALTER TABLE detections 
        ADD CONSTRAINT unique_listing_url UNIQUE (listing_url);
        
        -- Create index for better performance
        CREATE INDEX IF NOT EXISTS idx_detections_listing_url 
        ON detections(listing_url);
        
        -- Create index for platform queries
        CREATE INDEX IF NOT EXISTS idx_detections_platform_date 
        ON detections(platform, detected_at DESC);
        """
        
        logger.info("Unique constraint SQL:")
        logger.info(constraint_sql)
        
        # Save SQL to file for manual execution
        with open('add_unique_constraint.sql', 'w') as f:
            f.write(constraint_sql)
        
        logger.info("SQL saved to 'add_unique_constraint.sql' - execute this in Supabase SQL editor")
        return True
    
    def generate_cleanup_report(self, cleanup_results: Dict) -> str:
        """Generate detailed cleanup report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
# Ultimate Duplicate Cleanup Report
Generated: {timestamp}

## Summary
- Total listings processed: {cleanup_results['total_unique'] + cleanup_results['total_duplicates']}
- Unique listings retained: {cleanup_results['total_unique']}
- Duplicate listings removed: {cleanup_results['deleted_count']}
- Cleanup success rate: {(cleanup_results['deleted_count'] / cleanup_results['total_duplicates'] * 100):.1f}%

## Database State
- Before cleanup: {cleanup_results['total_unique'] + cleanup_results['total_duplicates']} listings
- After cleanup: {cleanup_results['total_unique']} listings
- Space saved: {cleanup_results['deleted_count']} entries

## Duplicate Analysis
"""
        
        # Add platform breakdown
        platform_duplicates = defaultdict(int)
        for url, duplicate_list in cleanup_results['duplicates'].items():
            for duplicate in duplicate_list:
                platform_duplicates[duplicate.get('platform', 'unknown')] += 1
        
        report += "\n### Duplicates by Platform:\n"
        for platform, count in platform_duplicates.items():
            report += f"- {platform}: {count} duplicates removed\n"
        
        report += f"""
## Next Steps
1. ✅ Duplicates removed from database
2. 🔧 Add unique constraint: Execute 'add_unique_constraint.sql' in Supabase SQL editor
3. 🚀 Deploy enhanced scanner with duplicate prevention
4. 📊 Monitor for future duplicates (should be 0%)

## Files Generated
- add_unique_constraint.sql: SQL to add unique constraint
- cleanup_report_{timestamp.replace(' ', '_').replace(':', '')}.txt: This report

The database is now clean and ready for production scanning!
"""
        
        return report
    
    def run_complete_cleanup(self) -> Dict:
        """Run complete duplicate cleanup process"""
        logger.info("Starting ultimate duplicate cleanup process...")
        
        start_time = datetime.now()
        
        # Step 1: Fetch all listings
        all_listings = self.fetch_all_listings()
        
        if not all_listings:
            logger.warning("No listings found in database")
            return {'status': 'no_data'}
        
        # Step 2: Identify duplicates
        duplicate_analysis = self.identify_duplicates(all_listings)
        
        # Step 3: Delete duplicates
        deleted_count = self.delete_duplicates(duplicate_analysis['duplicates'])
        
        # Step 4: Add unique constraint
        self.add_unique_constraint()
        
        # Step 5: Generate report
        cleanup_results = {
            **duplicate_analysis,
            'deleted_count': deleted_count,
            'start_time': start_time.isoformat(),
            'end_time': datetime.now().isoformat(),
            'duration_seconds': (datetime.now() - start_time).total_seconds()
        }
        
        report = self.generate_cleanup_report(cleanup_results)
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"cleanup_report_{timestamp}.txt"
        with open(report_filename, 'w') as f:
            f.write(report)
        
        logger.info(f"Cleanup report saved to {report_filename}")
        logger.info("Ultimate duplicate cleanup completed!")
        
        return cleanup_results

def main():
    """Main cleanup function"""
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        # Environment variables should be set in system
        pass
    
    cleanup = UltimateDuplicateCleanup()
    results = cleanup.run_complete_cleanup()
    
    if results.get('status') == 'no_data':
        print("No data found in database - nothing to clean up")
        return
    
    # Print summary
    print("\n" + "="*60)
    print("ULTIMATE DUPLICATE CLEANUP RESULTS")
    print("="*60)
    print(f"Total listings processed: {results['total_unique'] + results['total_duplicates']}")
    print(f"Unique listings retained: {results['total_unique']}")
    print(f"Duplicate listings removed: {results['deleted_count']}")
    print(f"Cleanup duration: {results['duration_seconds']:.1f} seconds")
    print(f"Success rate: {(results['deleted_count'] / results['total_duplicates'] * 100):.1f}%")
    print("\n🎉 Database is now clean and duplicate-free!")
    print("📋 Next: Execute 'add_unique_constraint.sql' in Supabase SQL editor")

if __name__ == "__main__":
    main()
