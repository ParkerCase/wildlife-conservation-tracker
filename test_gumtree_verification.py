#!/usr/bin/env python3
"""
Test Gumtree Scanner to Verify It Actually Works
"""

import asyncio
import aiohttp
import logging
from datetime import datetime
import sys
import os

# Add project paths
sys.path.append('/Users/parkercase/conservation-bot')

logging.basicConfig(level=logging.INFO)

async def test_gumtree_real_scan():
    """Test Gumtree scanner with real requests"""
    
    print("🔍 TESTING GUMTREE SCANNER - REAL VERIFICATION")
    print("=" * 60)
    
    try:
        from production_new_platforms import ProductionGumtreeScanner
        
        scanner = ProductionGumtreeScanner()
        
        # Test keywords
        test_keywords = {
            'direct_terms': ['ivory', 'antique', 'carved', 'vintage']
        }
        
        timeout = aiohttp.ClientTimeout(total=120)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            
            print(f"🌍 Testing Gumtree domains: {scanner.domains}")
            print(f"🎯 Keywords: {test_keywords['direct_terms']}")
            print()
            
            start_time = datetime.now()
            
            # Run actual scan
            results = await scanner.scan_production(test_keywords, session)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print(f"📊 GUMTREE TEST RESULTS:")
            print(f"   Duration: {duration:.1f} seconds")
            print(f"   Results found: {len(results)}")
            print()
            
            if results:
                print("✅ GUMTREE IS WORKING!")
                print()
                
                # Show sample results by domain
                domains_found = {}
                for result in results:
                    domain = result.get('domain', 'unknown')
                    if domain not in domains_found:
                        domains_found[domain] = []
                    domains_found[domain].append(result)
                
                for domain, domain_results in domains_found.items():
                    print(f"🌍 {domain} ({len(domain_results)} results):")
                    for i, result in enumerate(domain_results[:3], 1):
                        title = result.get('title', 'No title')[:60]
                        price = result.get('price', 'No price')
                        region = result.get('region', 'Unknown')
                        print(f"   {i}. {title}... - {price} ({region})")
                    
                    if len(domain_results) > 3:
                        print(f"   ... and {len(domain_results) - 3} more")
                    print()
                
                # Performance metrics
                results_per_minute = (len(results) / duration) * 60
                daily_projection = results_per_minute * 60 * 24  # 24 hours
                
                print(f"📈 PERFORMANCE METRICS:")
                print(f"   Results per minute: {results_per_minute:.1f}")
                print(f"   Daily projection: {daily_projection:.0f} listings")
                print()
                
                # Check for quality indicators
                quality_indicators = 0
                for result in results:
                    if result.get('title') and len(result['title']) > 10:
                        quality_indicators += 1
                
                quality_percentage = (quality_indicators / len(results)) * 100
                print(f"📊 QUALITY ASSESSMENT:")
                print(f"   Quality listings: {quality_indicators}/{len(results)} ({quality_percentage:.1f}%)")
                
                if quality_percentage > 80:
                    print("   ✅ HIGH QUALITY - Good titles and data")
                elif quality_percentage > 60:
                    print("   ⚠️ MODERATE QUALITY - Some data issues")
                else:
                    print("   ❌ LOW QUALITY - Possible parsing issues")
                
                return True
                
            else:
                print("❌ GUMTREE NOT WORKING - No results found")
                print("   This could indicate:")
                print("   • Website structure changes")
                print("   • Anti-bot measures")
                print("   • Network connectivity issues")
                print("   • Selector updates needed")
                return False
                
    except ImportError:
        print("❌ Import error - production_new_platforms.py not found")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_gumtree_with_browser():
    """Test Gumtree with browser automation for verification"""
    
    print("\n🌐 BROWSER VERIFICATION TEST")
    print("=" * 40)
    
    try:
        from playwright.async_api import async_playwright
        from fake_useragent import UserAgent
        
        ua = UserAgent()
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=ua.random,
                viewport={'width': 1366, 'height': 768}
            )
            
            page = await context.new_page()
            
            # Test UK Gumtree
            test_url = "https://www.gumtree.com/search?search_category=all&q=antique"
            
            print(f"🔍 Testing: {test_url}")
            
            await page.goto(test_url, timeout=30000)
            await page.wait_for_timeout(3000)
            
            # Check if page loaded
            title = await page.title()
            print(f"   Page title: {title}")
            
            # Try to find listings
            selectors_to_try = [
                '.user-ad-collection-new-design',
                '.user-ad-row',
                '.user-ad-collection', 
                '.listing-link',
                '[data-q="ad-title"]',
                'article',
                '.listing-maxi'
            ]
            
            found_items = False
            for selector in selectors_to_try:
                try:
                    items = await page.query_selector_all(selector)
                    if items:
                        print(f"   ✅ Found {len(items)} items with selector: {selector}")
                        found_items = True
                        
                        # Test first item
                        if items:
                            first_item = items[0]
                            item_text = await first_item.inner_text()
                            print(f"   Sample item: {item_text[:100]}...")
                        
                        break
                except:
                    continue
            
            if not found_items:
                print("   ❌ No items found with any selector")
                
                # Check page content
                content = await page.content()
                if "gumtree" in content.lower():
                    print("   ✅ On Gumtree site")
                    if "search" in content.lower():
                        print("   ✅ Search page loaded")
                        if "result" in content.lower():
                            print("   ⚠️ Results might be present but selectors need updating")
                        else:
                            print("   ❌ No search results found")
                    else:
                        print("   ❌ Not a search page")
                else:
                    print("   ❌ Not on Gumtree site")
            
            await browser.close()
            
            return found_items
            
    except Exception as e:
        print(f"❌ Browser test error: {e}")
        return False

async def main():
    """Run complete Gumtree verification"""
    
    print("🧪 GUMTREE VERIFICATION TEST")
    print("=" * 60)
    print("Testing if Gumtree scanner actually works...")
    print()
    
    # Test 1: Production scanner
    scanner_works = await test_gumtree_real_scan()
    
    # Test 2: Browser verification
    browser_works = await test_gumtree_with_browser()
    
    print("\n🎯 FINAL VERIFICATION RESULTS:")
    print(f"   Production Scanner: {'✅ WORKING' if scanner_works else '❌ NOT WORKING'}")
    print(f"   Browser Test: {'✅ WORKING' if browser_works else '❌ NOT WORKING'}")
    
    if scanner_works and browser_works:
        print("\n🎉 GUMTREE VERIFICATION: COMPLETE SUCCESS!")
        print("   • Scanner is working correctly")
        print("   • Website is accessible")
        print("   • Real data is being returned")
        print("   • Can proceed with frontend integration")
        return True
    elif scanner_works or browser_works:
        print("\n⚠️ GUMTREE VERIFICATION: PARTIAL SUCCESS")
        print("   • Some functionality working")
        print("   • May need selector updates")
        print("   • Can proceed with caution")
        return True
    else:
        print("\n❌ GUMTREE VERIFICATION: FAILED")
        print("   • Scanner not working")
        print("   • Website may have changed")
        print("   • Need to fix before frontend integration")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
