#!/usr/bin/env python3
"""
WildGuard AI - Quick Production Test
Verify the scaling is working before full deployment
"""

import asyncio
import aiohttp
from datetime import datetime
import os
import base64
from fake_useragent import UserAgent
from playwright.async_api import async_playwright
from dotenv import load_dotenv
from supabase import create_client
from typing import Dict

load_dotenv('/Users/parkercase/conservation-bot/backend/.env')

class QuickProductionTest:
    """Quick test to verify scaling works"""
    
    def __init__(self):
        self.ua = UserAgent()
        
    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=180)
        connector = aiohttp.TCPConnector(limit=30, limit_per_host=10)
        self.session = aiohttp.ClientSession(
            timeout=timeout, 
            connector=connector,
            headers={'User-Agent': self.ua.random}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def quick_test(self) -> Dict:
        """Quick test of production scaling"""
        print("🚀 QUICK PRODUCTION TEST")
        print("=" * 60)
        
        # Test with a focused keyword set
        keywords = ['antique', 'vintage', 'carved', 'collectible', 'jewelry', 'art', 'wood', 'bronze']
        print(f"🎯 Using {len(keywords)} test keywords")
        
        # Run concurrent tests
        tasks = [
            ('ebay_mega', self.test_ebay_mega(keywords)),
            ('craigslist_mega', self.test_craigslist_mega(keywords)),
            ('olx_mega', self.test_olx_mega(keywords))
        ]
        
        results = {}
        total_results = 0
        
        for platform_name, task in tasks:
            print(f"\n🔍 Testing {platform_name.upper()}...")
            
            try:
                platform_results = await asyncio.wait_for(task, timeout=120)
                count = len(platform_results)
                total_results += count
                
                print(f"✅ {count} results")
                if count > 0:
                    for i, result in enumerate(platform_results[:3], 1):
                        title = result.get('title', 'No title')[:35]
                        price = result.get('price', 'No price')
                        print(f"   {i}. {title}... - {price}")
                
                results[platform_name] = platform_results
                
            except Exception as e:
                print(f"❌ Error: {str(e)[:40]}...")
                results[platform_name] = []
        
        return {
            'total_results': total_results,
            'platform_breakdown': {p: len(r) for p, r in results.items()},
            'keywords_used': len(keywords)
        }

    async def test_ebay_mega(self, keywords):
        """Test eBay with enhanced scaling"""
        results = []
        
        try:
            # Get OAuth token
            app_id = os.getenv("EBAY_APP_ID")
            cert_id = os.getenv("EBAY_CERT_ID")
            
            credentials = f"{app_id}:{cert_id}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers_auth = {
                "Authorization": f"Basic {encoded_credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            
            data = {
                "grant_type": "client_credentials",
                "scope": "https://api.ebay.com/oauth/api_scope",
            }

            async with self.session.post(
                "https://api.ebay.com/identity/v1/oauth2/token", 
                headers=headers_auth, data=data
            ) as resp:
                if resp.status == 200:
                    token_data = await resp.json()
                    oauth_token = token_data["access_token"]
                    
                    headers = {
                        "Authorization": f"Bearer {oauth_token}",
                        "Content-Type": "application/json",
                    }

                    # Test with multiple categories and higher limits
                    categories = ["", "20081", "550"]  # All, Antiques, Art
                    
                    search_tasks = []
                    for term in keywords:
                        for category in categories:
                            params = {"q": term, "limit": "100"}  # Max limit
                            if category:
                                params["category_ids"] = category
                            
                            task = self.search_ebay_single(headers, params, term)
                            search_tasks.append(task)
                    
                    # Execute in batches
                    batch_size = 8
                    for i in range(0, len(search_tasks), batch_size):
                        batch = search_tasks[i:i+batch_size]
                        batch_results = await asyncio.gather(*batch, return_exceptions=True)
                        
                        for batch_result in batch_results:
                            if isinstance(batch_result, list):
                                results.extend(batch_result)
                        
                        await asyncio.sleep(0.5)

        except Exception as e:
            print(f"eBay mega test error: {e}")
        
        return results

    async def search_ebay_single(self, headers, params, term):
        """Single eBay search"""
        try:
            async with self.session.get(
                "https://api.ebay.com/buy/browse/v1/item_summary/search",
                headers=headers, params=params
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    items = data.get("itemSummaries", [])
                    
                    return [{
                        "title": item.get("title", ""),
                        "price": item.get("price", {}).get("value", ""),
                        "url": item.get("itemWebUrl", ""),
                        "search_term": term,
                        "platform": "ebay"
                    } for item in items]
        except:
            pass
        return []

    async def test_craigslist_mega(self, keywords):
        """Test Craigslist with enhanced scaling"""
        results = []
        
        # Test with more cities
        cities = ["newyork", "losangeles", "chicago", "houston", "seattle", "atlanta"]
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            
            for city in cities[:4]:  # Test 4 cities
                for term in keywords[:4]:  # 4 terms per city
                    context = await browser.new_context(
                        user_agent=self.ua.random,
                        viewport={'width': 1366, 'height': 768}
                    )
                    page = await context.new_page()
                    
                    try:
                        url = f"https://{city}.craigslist.org/search/sss?query={term}"
                        await page.goto(url, timeout=8000)
                        await page.wait_for_timeout(1000)
                        
                        items = await page.query_selector_all(".cl-search-result")
                        
                        for item in items[:25]:  # More items per search
                            try:
                                title_elem = await item.query_selector("a.cl-app-anchor")
                                price_elem = await item.query_selector(".priceinfo")
                                
                                if title_elem:
                                    title = await title_elem.inner_text()
                                    price = await price_elem.inner_text() if price_elem else ""
                                    link = await title_elem.get_attribute("href")
                                    
                                    if link and link.startswith("/"):
                                        link = f"https://{city}.craigslist.org{link}"
                                    
                                    if title and link:
                                        results.append({
                                            "title": title.strip(),
                                            "price": price.strip(),
                                            "url": link,
                                            "search_term": term,
                                            "platform": "craigslist"
                                        })
                            except:
                                continue
                        
                    except Exception as e:
                        pass
                    
                    finally:
                        await page.close()
                        await context.close()
                    
                    await asyncio.sleep(0.5)
            
            await browser.close()
        
        return results

    async def test_olx_mega(self, keywords):
        """Test OLX with enhanced scaling"""
        results = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            for term in keywords[:6]:  # Test 6 keywords
                context = await browser.new_context(
                    user_agent=UserAgent().random,
                    viewport={'width': 1920, 'height': 1080}
                )
                page = await context.new_page()
                
                try:
                    url = f"https://www.olx.pl/oferty?q={term}"
                    
                    await page.goto(url, timeout=10000)
                    await page.wait_for_timeout(2000)
                    
                    items = await page.query_selector_all('[data-cy="l-card"]')
                    
                    for item in items[:30]:  # More items per search
                        try:
                            title_elem = await item.query_selector('h3, h4')
                            price_elem = await item.query_selector('.price')
                            link_elem = await item.query_selector('a')
                            
                            if title_elem and link_elem:
                                title = await title_elem.inner_text()
                                price = await price_elem.inner_text() if price_elem else ""
                                link = await link_elem.get_attribute('href')
                                
                                if link and not link.startswith('http'):
                                    link = f"https://www.olx.pl{link}"
                                
                                if title and link and len(title.strip()) > 3:
                                    results.append({
                                        "title": title.strip(),
                                        "price": price.strip(),
                                        "url": link,
                                        "search_term": term,
                                        "platform": "olx"
                                    })
                        except:
                            continue
                
                except Exception as e:
                    pass
                
                finally:
                    await page.close()
                    await context.close()
                
                await asyncio.sleep(1)
            
            await browser.close()
        
        return results


async def run_quick_test():
    """Run the quick production test"""
    print("🚀 QUICK PRODUCTION SCALING TEST")
    print("=" * 70)
    
    start_time = datetime.now()
    
    async with QuickProductionTest() as tester:
        results = await tester.quick_test()
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print(f"\n🎯 QUICK TEST RESULTS:")
        print(f"   📊 Total results: {results['total_results']:,}")
        print(f"   🔑 Keywords used: {results['keywords_used']}")
        print(f"   ⏱️  Duration: {duration.total_seconds():.1f} seconds")
        
        print(f"\n📈 PLATFORM BREAKDOWN:")
        for platform, count in results['platform_breakdown'].items():
            print(f"   {platform}: {count:,} results")
        
        # Project to daily capacity
        if results['total_results'] > 0:
            daily_projection = results['total_results'] * 24
            
            print(f"\n🚀 SCALING PROJECTIONS:")
            print(f"   Per scan: {results['total_results']:,} listings")
            print(f"   Daily (24 scans): {daily_projection:,} listings")
            
            if daily_projection >= 100000:
                print(f"\n🏆 100K+ DAILY GOAL ACHIEVED!")
                print(f"   🎉 Daily capacity: {daily_projection:,}")
                exceed = daily_projection - 100000
                print(f"   🚀 Exceeds target by: {exceed:,} listings")
            else:
                shortfall = 100000 - daily_projection
                multiplier = 100000 / results['total_results']
                print(f"\n📊 Path to 100K daily:")
                print(f"   Current: {daily_projection:,} / 100,000")
                print(f"   Shortfall: {shortfall:,}")
                print(f"   Scaling needed: {multiplier:.1f}x per scan")
                print(f"   OR {100000 / results['total_results']:.1f} scans per hour")
        
        return results


if __name__ == "__main__":
    asyncio.run(run_quick_test())
