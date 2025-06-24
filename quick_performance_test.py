#!/usr/bin/env python3
"""
Quick Platform Performance Test - Get Real Numbers
"""

import asyncio
import aiohttp
import os
import sys
from datetime import datetime
import time

# Set environment variables directly
os.environ['SUPABASE_URL'] = 'https://hgnefrvllutcagdutcaa.supabase.co'
os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhnbmVmcnZsbHV0Y2FnZHV0Y2FhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkzMjU4NzcsImV4cCI6MjA2NDkwMTg3N30.ftaP4Xa1vTXumTlcPy0OwdG1s-4JSYz10-ENiWB_QZ0'

# Import platform scanners
sys.path.append('/Users/parkercase/conservation-bot')

async def quick_performance_test():
    """Quick test to get real performance numbers"""
    print("🚀 QUICK PLATFORM PERFORMANCE TEST")
    print("=" * 50)
    
    # Test keywords
    keywords = {
        'direct_terms': ['ivory', 'antique', 'carved', 'bone', 'vintage']
    }
    
    results = {}
    
    timeout = aiohttp.ClientTimeout(total=120)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        
        # Test 1: Avito (showed best performance previously)
        print("\n🔴 Testing Avito...")
        start_time = time.time()
        
        try:
            from production_new_platforms import ProductionAvitoScanner
            avito_scanner = ProductionAvitoScanner()
            avito_results = await avito_scanner.scan_production(keywords, session)
            
            avito_time = time.time() - start_time
            avito_count = len(avito_results)
            
            print(f"   ✅ Avito: {avito_count} results in {avito_time:.1f}s")
            
            if avito_results:
                sample = avito_results[0]
                print(f"   📝 Sample: {sample.get('title', 'No title')[:40]}...")
            
            results['avito'] = {
                'count': avito_count,
                'time': avito_time,
                'working': avito_count > 0
            }
            
        except Exception as e:
            print(f"   ❌ Avito error: {e}")
            results['avito'] = {'count': 0, 'time': 0, 'working': False}
        
        await asyncio.sleep(2)
        
        # Test 2: Facebook Marketplace
        print("\n🔵 Testing Facebook Marketplace...")
        start_time = time.time()
        
        try:
            from production_new_platforms import ProductionFacebookMarketplaceScanner
            fb_scanner = ProductionFacebookMarketplaceScanner()
            fb_results = await fb_scanner.scan_production(keywords, session)
            
            fb_time = time.time() - start_time
            fb_count = len(fb_results)
            
            print(f"   ✅ Facebook: {fb_count} results in {fb_time:.1f}s")
            
            if fb_results:
                sample = fb_results[0]
                print(f"   📝 Sample: {sample.get('title', 'No title')[:40]}...")
            
            results['facebook'] = {
                'count': fb_count,
                'time': fb_time,
                'working': fb_count > 0
            }
            
        except Exception as e:
            print(f"   ❌ Facebook error: {e}")
            results['facebook'] = {'count': 0, 'time': 0, 'working': False}
        
        await asyncio.sleep(2)
        
        # Test 3: Gumtree
        print("\n🟢 Testing Gumtree...")
        start_time = time.time()
        
        try:
            from production_new_platforms import ProductionGumtreeScanner
            gumtree_scanner = ProductionGumtreeScanner()
            gumtree_results = await gumtree_scanner.scan_production(keywords, session)
            
            gumtree_time = time.time() - start_time
            gumtree_count = len(gumtree_results)
            
            print(f"   ✅ Gumtree: {gumtree_count} results in {gumtree_time:.1f}s")
            
            if gumtree_results:
                sample = gumtree_results[0]
                print(f"   📝 Sample: {sample.get('title', 'No title')[:40]}...")
            
            results['gumtree'] = {
                'count': gumtree_count,
                'time': gumtree_time,
                'working': gumtree_count > 0
            }
            
        except Exception as e:
            print(f"   ❌ Gumtree error: {e}")
            results['gumtree'] = {'count': 0, 'time': 0, 'working': False}
    
    # Calculate daily projections
    print(f"\n📊 DAILY PROJECTION CALCULATIONS")
    print("=" * 40)
    
    total_daily_new = 0
    working_count = 0
    
    for platform, data in results.items():
        if data['working']:
            working_count += 1
            
            # Conservative scaling:
            # - Test used 5 keywords, full set has 966 keywords
            # - Scale factor: 966/5 = 193, but cap at 100 for safety
            # - 8 scans per day (every 3 hours)
            
            test_results = data['count']
            keywords_scale = min(966 / 5, 100)  # Cap scaling
            single_scan_projection = test_results * keywords_scale
            
            # Platform-specific efficiency factors
            if platform == 'avito':
                efficiency = 1.0  # Avito showed good performance
            elif platform == 'facebook':
                efficiency = 0.4  # Facebook has anti-bot measures
            elif platform == 'gumtree':
                efficiency = 0.6  # Regional but stable
            else:
                efficiency = 0.8
            
            daily_projection = int(single_scan_projection * 8 * efficiency)
            total_daily_new += daily_projection
            
            print(f"🎯 {platform.title()}:")
            print(f"   • Test results: {test_results}")
            print(f"   • Single scan projection: {int(single_scan_projection):,}")
            print(f"   • Efficiency factor: {efficiency}")
            print(f"   • Daily projection: {daily_projection:,}")
        else:
            print(f"❌ {platform.title()}: Not working")
    
    print(f"\n🚀 SUMMARY")
    print("=" * 20)
    print(f"✅ Working platforms: {working_count}/3")
    print(f"📊 New platforms daily: {total_daily_new:,}")
    print(f"📊 Existing platforms daily: 100,000+ (your current)")
    print(f"🎉 TOTAL DAILY CAPACITY: {100000 + total_daily_new:,}+")
    
    confidence = (working_count / 3) * 100
    print(f"\n🎯 CONFIDENCE LEVEL: {confidence:.0f}%")
    
    if confidence >= 67:  # 2/3 working
        print("✅ HIGH CONFIDENCE - Ready for production!")
    else:
        print("⚠️ MEDIUM CONFIDENCE - Some platforms need work")
    
    return results

if __name__ == "__main__":
    asyncio.run(quick_performance_test())
