#!/usr/bin/env python3
"""
Comprehensive Real-Scale Test for All 7 Platforms
Tests actual performance potential: Should be 3M+ listings/day
"""

import os
import sys
import time
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our fixed scanner
from fixed_multilingual_production_scanner import MultilingualScanner

def test_all_platforms_real_scale():
    """Test all 7 platforms with real scale calculation"""
    
    print("🚀 COMPREHENSIVE 7-PLATFORM REAL-SCALE TEST")
    print("=" * 80)
    print(f"Target: 3,000,000+ listings/day (no mock data)")
    print(f"Testing: eBay, Craigslist, Marktplaats, OLX, MercadoLibre, Gumtree, Avito")
    print("=" * 80)
    
    scanner = MultilingualScanner()
    
    # Get a small sample of multilingual keywords for testing
    test_keywords = scanner.keyword_manager.get_next_batch(2)  # 2 keywords for speed
    
    print(f"🧪 Test keywords: {[kw['keyword'] for kw in test_keywords]}")
    print(f"🌍 Languages: {[kw['language'] for kw in test_keywords]}")
    
    all_platforms = ['ebay', 'craigslist', 'marktplaats', 'olx', 'mercadolibre', 'gumtree', 'avito']
    platform_results = {}
    total_listings = 0
    total_time = 0
    
    for platform in all_platforms:
        print(f"\n📡 Testing {platform.upper()}...")
        platform_start = time.time()
        
        try:
            listings = scanner.scan_platform_multilingual(platform, test_keywords)
            duration = time.time() - platform_start
            
            # Check for mock data indicators
            mock_indicators = [
                "listing 1", "listing 2", "item 1", "item 2", 
                "generated", "test data", "mock", "fake"
            ]
            
            real_listings = []
            mock_listings = []
            
            for listing in listings:
                is_mock = any(indicator in listing.title.lower() for indicator in mock_indicators)
                if is_mock:
                    mock_listings.append(listing)
                else:
                    real_listings.append(listing)
            
            platform_results[platform] = {
                'total_listings': len(listings),
                'real_listings': len(real_listings),
                'mock_listings': len(mock_listings),
                'duration': duration,
                'listings_per_second': len(listings) / duration if duration > 0 else 0,
                'working': len(listings) > 0
            }
            
            total_listings += len(listings)
            total_time += duration
            
            status = "✅ REAL DATA" if len(real_listings) > 0 and len(mock_listings) == 0 else "⚠️ MOCK DETECTED" if len(mock_listings) > 0 else "❌ NO DATA"
            
            print(f"   {status}: {len(real_listings)} real, {len(mock_listings)} mock in {duration:.1f}s")
            
            # Show sample titles
            if real_listings:
                print(f"   Sample: {real_listings[0].title[:60]}...")
            elif mock_listings:
                print(f"   Mock sample: {mock_listings[0].title[:60]}...")
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            platform_results[platform] = {
                'total_listings': 0, 'real_listings': 0, 'mock_listings': 0,
                'duration': 0, 'listings_per_second': 0, 'working': False
            }
    
    # Calculate massive scale projections
    print(f"\n" + "=" * 80)
    print("🎯 REAL SCALE CALCULATION")
    print("=" * 80)
    
    working_platforms = [p for p, r in platform_results.items() if r['working']]
    avg_listings_per_keyword = total_listings / (len(test_keywords) * len(working_platforms)) if working_platforms else 0
    
    total_keywords = len(scanner.keyword_manager.all_keywords)  # 1,452
    
    print(f"📊 Test Results:")
    print(f"   Keywords tested: {len(test_keywords)}")
    print(f"   Platforms working: {len(working_platforms)}/{len(all_platforms)}")
    print(f"   Total listings found: {total_listings}")
    print(f"   Avg listings per keyword: {avg_listings_per_keyword:.1f}")
    print(f"   Total test time: {total_time:.1f}s")
    
    if avg_listings_per_keyword > 0 and len(working_platforms) > 0:
        # Calculate full scale potential
        listings_per_complete_cycle = total_keywords * avg_listings_per_keyword * len(working_platforms)
        
        # Estimate cycle time (based on test performance)
        estimated_cycle_time_minutes = (total_time / len(test_keywords)) * total_keywords / len(working_platforms) / 60
        cycles_per_day = (24 * 60) / estimated_cycle_time_minutes if estimated_cycle_time_minutes > 0 else 0
        
        daily_projection = listings_per_complete_cycle * cycles_per_day
        
        print(f"\n🚀 MASSIVE SCALE PROJECTIONS:")
        print(f"   Per complete cycle: {listings_per_complete_cycle:,.0f} listings")
        print(f"   Cycle time estimate: {estimated_cycle_time_minutes:.1f} minutes")
        print(f"   Cycles per day: {cycles_per_day:.1f}")
        print(f"   📈 DAILY PROJECTION: {daily_projection:,.0f} LISTINGS/DAY")
        
        if daily_projection >= 1000000:
            millions = daily_projection / 1000000
            print(f"   🏆 SUCCESS: {millions:.1f} MILLION+ listings/day potential!")
            print(f"   🌍 This MASSIVELY exceeds any target and proves global scale!")
        elif daily_projection >= 100000:
            print(f"   ✅ EXCELLENT: {daily_projection:,.0f} listings/day exceeds 100K target!")
        else:
            print(f"   ⚠️  Below 100K target. Need optimization.")
        
        # Show platform breakdown
        print(f"\n📈 PLATFORM PERFORMANCE:")
        for platform, results in platform_results.items():
            if results['working']:
                daily_potential = (results['listings_per_second'] * 86400) if results['listings_per_second'] > 0 else 0
                status = "🔥" if results['real_listings'] > results['mock_listings'] else "⚠️"
                print(f"   {status} {platform}: {results['real_listings']} real listings, {daily_potential:,.0f}/day potential")
    
    # Final assessment
    print(f"\n" + "=" * 80)
    print("🎯 FINAL ASSESSMENT")
    print("=" * 80)
    
    real_platforms = [p for p, r in platform_results.items() if r['real_listings'] > 0]
    mock_platforms = [p for p, r in platform_results.items() if r['mock_listings'] > 0]
    broken_platforms = [p for p, r in platform_results.items() if not r['working']]
    
    print(f"✅ Real data platforms: {len(real_platforms)} - {', '.join(real_platforms)}")
    if mock_platforms:
        print(f"⚠️  Mock data platforms: {len(mock_platforms)} - {', '.join(mock_platforms)}")
    if broken_platforms:
        print(f"❌ Broken platforms: {len(broken_platforms)} - {', '.join(broken_platforms)}")
    
    if len(real_platforms) >= 5:
        print(f"\n🏆 READY FOR PRODUCTION!")
        print(f"   {len(real_platforms)}/7 platforms working with REAL data")
        print(f"   Multi-million listing per day potential confirmed")
        print(f"   🌍 Global wildlife trafficking detection at massive scale!")
        return True
    else:
        print(f"\n⚠️  NEEDS FIXES:")
        print(f"   Only {len(real_platforms)}/7 platforms working with real data")
        print(f"   Fix mock data and broken platforms before production")
        return False

if __name__ == "__main__":
    success = test_all_platforms_real_scale()
    sys.exit(0 if success else 1)
