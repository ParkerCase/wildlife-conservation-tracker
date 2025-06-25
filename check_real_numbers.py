#!/usr/bin/env python3
"""
Quick Database Check - Get Real Numbers and Platform Distribution
"""

import os
from supabase import create_client

def check_real_database():
    """Check actual database numbers"""
    
    # Load environment variables
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ Missing environment variables")
        return
    
    supabase = create_client(supabase_url, supabase_key)
    
    try:
        # Get total count
        total_result = supabase.table('detections').select('*', count='exact').execute()
        total_count = total_result.count
        
        print(f"📊 Total Detections: {total_count:,}")
        
        # Get platform distribution
        platform_result = supabase.table('detections').select('platform').execute()
        platform_counts = {}
        
        for record in platform_result.data:
            platform = record.get('platform', 'unknown').lower()
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        print(f"\n🌍 Platform Distribution:")
        sorted_platforms = sorted(platform_counts.items(), key=lambda x: x[1], reverse=True)
        for platform, count in sorted_platforms:
            percentage = (count / total_count * 100) if total_count > 0 else 0
            print(f"   {platform}: {count:,} ({percentage:.1f}%)")
        
        # Get species count
        species_result = supabase.table('detections').select('search_term').execute()
        unique_species = set()
        for record in species_result.data:
            search_term = record.get('search_term')
            if search_term:
                unique_species.add(search_term.lower())
        
        print(f"\n🐾 Species Protected: {len(unique_species)}")
        
        # Get recent activity
        from datetime import datetime, timedelta
        yesterday = (datetime.now() - timedelta(days=1)).isoformat()
        recent_result = supabase.table('detections').select('*', count='exact').gte('timestamp', yesterday).execute()
        recent_count = recent_result.count
        
        print(f"📈 Recent Activity (24h): {recent_count:,}")
        
        return {
            'total_detections': total_count,
            'platforms': dict(sorted_platforms),
            'species_protected': len(unique_species),
            'recent_activity': recent_count
        }
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return None

if __name__ == "__main__":
    check_real_database()
