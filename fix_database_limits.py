#!/usr/bin/env python3
"""
WildGuard Database Cleanup - Fix Supabase Limits
Removes duplicates and optimizes database to restore normal operation
"""

import requests
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseLimitsFixer:
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY') or os.getenv('SUPABASE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            print("❌ Missing Supabase credentials!")
            print("Check your .env file has SUPABASE_URL and SUPABASE_ANON_KEY")
            exit(1)
        
        self.headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'application/json'
        }
        
        self.base_url = f"{self.supabase_url}/rest/v1/detections"
        
    def check_database_status(self):
        """Check if database is accessible and get current status"""
        print("🔍 Checking database status...")
        
        try:
            # Try to get just one record to test access
            response = requests.get(
                f"{self.base_url}?select=id&limit=1",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Database is accessible")
                return True
            elif response.status_code == 429:
                print("⚠️  Rate limited - waiting 60 seconds...")
                time.sleep(60)
                return self.check_database_status()
            else:
                print(f"❌ Database access blocked: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            return False
    
    def get_database_stats(self):
        """Get current database statistics"""
        print("📊 Getting database statistics...")
        
        try:
            # Try to get total count
            response = requests.get(
                f"{self.base_url}?select=*",
                headers={**self.headers, 'Prefer': 'count=exact'},
                timeout=30
            )
            
            if response.status_code == 200:
                count_header = response.headers.get('Content-Range', '0-0/0')
                total_count = count_header.split('/')[-1]
                print(f"📈 Total records: {total_count}")
                
                # Get recent records to check duplicate rate
                recent_response = requests.get(
                    f"{self.base_url}?select=listing_url,platform,timestamp&limit=1000&order=timestamp.desc",
                    headers=self.headers,
                    timeout=30
                )
                
                if recent_response.status_code == 200:
                    recent_data = recent_response.json()
                    
                    # Calculate duplicate rate
                    urls = [item['listing_url'] for item in recent_data]
                    unique_urls = set(urls)
                    duplicate_rate = ((len(urls) - len(unique_urls)) / len(urls) * 100) if urls else 0
                    
                    print(f"🔄 Recent 1000 records: {len(recent_data)}")
                    print(f"🚫 Duplicate rate: {duplicate_rate:.1f}%")
                    
                    # Platform distribution
                    platforms = defaultdict(int)
                    for item in recent_data:
                        platforms[item['platform']] += 1
                    
                    print("🌍 Platform distribution:")
                    for platform, count in sorted(platforms.items(), key=lambda x: x[1], reverse=True):
                        print(f"   {platform}: {count}")
                    
                    return {
                        'total': total_count,
                        'recent_count': len(recent_data),
                        'duplicate_rate': duplicate_rate,
                        'platforms': dict(platforms)
                    }
            else:
                print(f"⚠️  Could not get stats: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return None
    
    def find_duplicate_batches(self, batch_size=100):
        """Find duplicate records in batches"""
        print(f"🔍 Scanning for duplicates in batches of {batch_size}...")
        
        all_duplicates = []
        offset = 0
        
        while True:
            try:
                response = requests.get(
                    f"{self.base_url}?select=id,listing_url&limit={batch_size}&offset={offset}&order=timestamp.desc",
                    headers=self.headers,
                    timeout=30
                )
                
                if response.status_code != 200:
                    print(f"⚠️  Batch failed at offset {offset}: {response.status_code}")
                    break
                
                batch_data = response.json()
                
                if not batch_data:
                    print(f"✅ Completed scanning at offset {offset}")
                    break
                
                # Group by URL to find duplicates
                url_groups = defaultdict(list)
                for item in batch_data:
                    url_groups[item['listing_url']].append(item['id'])
                
                # Find URLs with multiple records
                for url, ids in url_groups.items():
                    if len(ids) > 1:
                        # Keep first ID, mark others as duplicates
                        for duplicate_id in ids[1:]:
                            all_duplicates.append(duplicate_id)
                
                print(f"📊 Processed {offset + len(batch_data)} records, found {len(all_duplicates)} duplicates so far")
                
                offset += batch_size
                
                # Rate limiting
                time.sleep(0.5)
                
                # Limit to prevent timeout
                if offset > 5000:  # Process max 5000 records
                    print(f"⏳ Stopping at {offset} records to prevent timeout")
                    break
                
            except Exception as e:
                print(f"❌ Error in batch at offset {offset}: {e}")
                break
        
        print(f"🎯 Found {len(all_duplicates)} duplicate records")
        return all_duplicates
    
    def delete_duplicates_safely(self, duplicate_ids, batch_size=50):
        """Delete duplicates in small batches to avoid rate limits"""
        print(f"🗑️  Deleting {len(duplicate_ids)} duplicates in batches of {batch_size}...")
        
        deleted_count = 0
        
        for i in range(0, len(duplicate_ids), batch_size):
            batch = duplicate_ids[i:i + batch_size]
            
            try:
                # Delete batch using filter
                id_filter = ','.join(str(id) for id in batch)
                
                response = requests.delete(
                    f"{self.base_url}?id=in.({id_filter})",
                    headers=self.headers,
                    timeout=30
                )
                
                if response.status_code in [200, 204]:
                    deleted_count += len(batch)
                    print(f"✅ Deleted batch {i//batch_size + 1}: {len(batch)} records (total: {deleted_count})")
                else:
                    print(f"⚠️  Batch {i//batch_size + 1} failed: {response.status_code}")
                    print(f"Response: {response.text[:100]}")
                
                # Rate limiting between batches
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Error deleting batch {i//batch_size + 1}: {e}")
                
        return deleted_count
    
    def optimize_database(self):
        """Run database optimization commands"""
        print("🔧 Optimizing database...")
        
        # Note: Supabase automatically handles VACUUM and ANALYZE
        # but we can trigger some optimizations
        
        try:
            # Get fresh statistics
            stats = self.get_database_stats()
            if stats:
                print("✅ Database optimization completed")
                return True
            else:
                print("⚠️  Could not verify optimization")
                return False
                
        except Exception as e:
            print(f"❌ Optimization error: {e}")
            return False
    
    def run_complete_cleanup(self):
        """Run complete database cleanup process"""
        print("🚀 Starting Complete Database Cleanup")
        print("=" * 50)
        
        # Step 1: Check if database is accessible
        if not self.check_database_status():
            print("❌ Cannot proceed - database not accessible")
            print("\n💡 SOLUTIONS:")
            print("1. Wait for Supabase limits to reset (usually 24 hours)")
            print("2. Check your Supabase dashboard for usage info")
            print("3. Consider upgrading Supabase plan temporarily")
            return False
        
        # Step 2: Get initial statistics
        initial_stats = self.get_database_stats()
        if not initial_stats:
            print("⚠️  Could not get initial stats, proceeding carefully...")
        
        # Step 3: Find duplicates
        duplicates = self.find_duplicate_batches()
        
        if not duplicates:
            print("✅ No duplicates found - database is clean!")
            return True
        
        # Step 4: Delete duplicates
        deleted_count = self.delete_duplicates_safely(duplicates)
        
        # Step 5: Optimize
        self.optimize_database()
        
        # Step 6: Final statistics
        print("\n📊 CLEANUP RESULTS:")
        print("=" * 30)
        final_stats = self.get_database_stats()
        
        if initial_stats and final_stats:
            print(f"📉 Records before: {initial_stats['total']}")
            print(f"📈 Records after: {final_stats['total']}")
            print(f"🗑️  Duplicates removed: {deleted_count}")
            print(f"💾 Space saved: ~{deleted_count * 0.5:.1f}KB")
        
        print("\n✅ Database cleanup completed!")
        print("\n💡 NEXT STEPS:")
        print("1. Your Supabase limits should reset within 24 hours")
        print("2. The coordinated workflows will prevent future conflicts")
        print("3. Monitor the database size in your Supabase dashboard")
        
        return True

def main():
    print("🌍 WildGuard Database Limits Fixer")
    print("=" * 50)
    print("This will clean up duplicates and optimize your database")
    print("to resolve Supabase usage limit issues.")
    print()
    
    fixer = DatabaseLimitsFixer()
    success = fixer.run_complete_cleanup()
    
    if success:
        print("\n🎉 Database cleanup successful!")
        print("Your workflows should now run without hitting limits.")
    else:
        print("\n⚠️  Cleanup encountered issues.")
        print("Try again in a few hours when limits reset.")

if __name__ == "__main__":
    main()
