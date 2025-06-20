#!/usr/bin/env python3
"""
WildGuard AI - Mega Scaling Test
Quick test of the scaling strategies
"""

import asyncio
import aiohttp
from datetime import datetime, timedelta
import os
import base64
from fake_useragent import UserAgent
from playwright.async_api import async_playwright
from dotenv import load_dotenv
from supabase import create_client
import logging
from typing import List, Dict

load_dotenv('/Users/parkercase/conservation-bot/backend/.env')

# Focused keyword set for testing
TEST_KEYWORDS = {
    'direct_terms': [
        'antique', 'vintage', 'carved', 'collectible', 'artifact', 'rare', 'unique',
        'handmade', 'artisan', 'craft', 'traditional', 'decorative', 'ornamental',
        'art', 'artwork', 'painting', 'sculpture', 'jewelry', 'wood', 'wooden',
        'metal', 'bronze', 'silver', 'stone', 'ceramic', 'glass', 'instrument',
        'furniture', 'chair', 'table', 'clock', 'watch', 'vase', 'bowl'
    ]
}

class QuickScalingTest:
    """Quick test of scaling strategies"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.setup_supabase()
        
    def setup_supabase(self):
        try:
            SUPABASE_URL = os.getenv('SUPABASE_URL')
            SUPABASE_KEY = os.getenv('SUPABASE_KEY')
            self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        except:
            self.supabase = None

    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=300)
        connector = aiohttp.TCPConnector(limit=50, limit_per_host=10)
        self.session = aiohttp.ClientSession(
            timeout=timeout, 
            connector=connector,
            headers={'User-Agent': self.ua.random}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def test_scaling(self) -> Dict:
        """Test the scaling strategies"""
        print("🚀 TESTING SCALING STRATEGIES")
        print("=" * 60)
        
        keywords = TEST_KEYWORDS
        print(f"🎯 Using {len(keywords['direct_terms'])} keywords")
        
        # Run scaled versions of working platforms
        tasks = [
            ('ebay_scaled', self.scaled_ebay_test(keywords)),
            ('craigslist_scaled', self.scaled_craigslist_test(keywords)),
            ('olx_scaled', self.scaled_olx_test(keywords))
        ]
        
        results = {}
        total_results = 0
        
        for platform_name, task in tasks:
            print(f"\n🔍 Testing {platform_name.upper()}...")
            
            try:
                platform_results = await asyncio.wait_for(task, timeout=180)
                count = len(platform_results)
                total_results += count
                
                print(f"✅ {count} results")
                if count > 0:
                    for i, result in enumerate(platform_results[:2], 1):
                        title = result.get('title', 'No title')[:40]
                        price = result.get('price', 'No price')
                        print(f"   {i}. {title}... - {price}")
                
                results[platform_name] = platform_results
                
            except Exception as e:
                print(f"❌ Error: {str(e)[:50]}")
                results[platform_name] = []
        
        return {
            'total_results': total_results,
            'platform_breakdown': {p: len(r) for p, r in results.items()},
            'keywords_used': len(keywords['direct_terms'])
        }

    async def scaled_ebay_test(self, keywords: Dict) -> List[Dict]:
        """Test scaled eBay scanning"""
        results = []
        search_terms = keywords["direct_terms"][:15]  # Test with 15 terms
        
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

                    # Concurrent searches with higher limits
                    search_tasks = []
                    for term in search_terms:
                        params = {"q": term, "limit": "50"}  # Increased limit
                        task = self.search_ebay_single(headers, params, term)
                        search_tasks.append(task)
                    
                    # Execute searches in batches
                    batch_size = 8
                    for i in range(0, len(search_tasks), batch_size):
                        batch = search_tasks[i:i+batch_size]
                        batch_results = await asyncio.gather(*batch, return_exceptions=True)
                        
                        for batch_result in batch_results:
                            if isinstance(batch_result, list):
                                results.extend(batch_result)
                        
                        await asyncio.sleep(1)  # Rate limiting

        except Exception as e:
            logging.error(f"Scaled eBay test error: {e}")
        
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

    async def scaled_craigslist_test(self, keywords: Dict) -> List[Dict]:
        """Test scaled Craigslist scanning"""
        results = []
        search_terms = keywords["direct_terms"][:10]  # Test with 10 terms
        
        # More cities for testing
        cities = ["newyork", "losangeles", "chicago", "miami", "seattle", "atlanta"]
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            
            # Test with more cities and terms
            for city in cities[:4]:  # 4 cities
                for term in search_terms[:5]:  # 5 terms per city
                    context = await browser.new_context(
                        user_agent=self.ua.random,
                        viewport={'width': 1366, 'height': 768}
                    )
                    page = await context.new_page()
                    
                    try:
                        url = f"https://{city}.craigslist.org/search/sss?query={term}"
                        await page.goto(url, timeout=15000)
                        await page.wait_for_timeout(2000)
                        
                        items = await page.query_selector_all(".cl-search-result")
                        
                        for item in items[:15]:  # More items per search
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
                        logging.warning(f"Scaled Craigslist test {city} {term}: {e}")
                    
                    finally:
                        await page.close()
                        await context.close()
                    
                    await asyncio.sleep(1)
            
            await browser.close()
        
        return results

    async def scaled_olx_test(self, keywords: Dict) -> List[Dict]:
        """Test scaled OLX scanning"""
        results = []
        search_terms = keywords["direct_terms"][:8]  # Test with 8 terms
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            # Focus on working domain with more terms
            for term in search_terms:
                context = await browser.new_context(
                    user_agent=UserAgent().random,
                    viewport={'width': 1920, 'height': 1080}
                )
                page = await context.new_page()
                
                try:
                    url = f"https://www.olx.pl/oferty?q={term}"
                    
                    await page.goto(url, timeout=20000)
                    await page.wait_for_timeout(3000)
                    
                    items = await page.query_selector_all('[data-cy="l-card"], .offer-wrapper')
                    
                    for item in items[:20]:  # More items per search
                        try:
                            title_elem = await item.query_selector('h3, h4, .title')
                            price_elem = await item.query_selector('.price, [data-testid="ad-price"]')
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
                    logging.warning(f"Scaled OLX test {term}: {e}")
                
                finally:
                    await page.close()
                    await context.close()
                
                await asyncio.sleep(2)
            
            await browser.close()
        
        return results


async def run_scaling_test():
    """Run the scaling test"""
    print("🚀 SCALING STRATEGY TEST")
    print("=" * 70)
    
    async with QuickScalingTest() as tester:
        results = await tester.test_scaling()
        
        print(f"\n🎯 SCALING TEST RESULTS:")
        print(f"   📊 Total results: {results['total_results']:,}")
        print(f"   🔑 Keywords used: {results['keywords_used']}")
        
        print(f"\n📈 PLATFORM BREAKDOWN:")
        for platform, count in results['platform_breakdown'].items():
            print(f"   {platform}: {count:,} results")
        
        # Compare with baseline and project
        baseline = 821  # From our previous best test
        improvement = results['total_results'] / baseline if baseline > 0 else 0
        
        print(f"\n📊 SCALING ANALYSIS:")
        print(f"   Baseline results: {baseline}")
        print(f"   Scaled results: {results['total_results']}")
        print(f"   Improvement factor: {improvement:.1f}x")
        
        # Calculate projections
        daily_projection = results['total_results'] * 24
        print(f"   Daily projection: {daily_projection:,} listings")
        
        if daily_projection >= 100000:
            print(f"\n🏆 100K+ DAILY GOAL ACHIEVED!")
            print(f"   🎉 Daily capacity: {daily_projection:,}")
        else:
            shortfall = 100000 - daily_projection
            frequency_needed = 100000 / results['total_results']
            print(f"\n📊 Progress toward 100K daily:")
            print(f"   Current: {daily_projection:,} / 100,000")
            print(f"   Shortfall: {shortfall:,}")
            print(f"   OR run {frequency_needed:.1f} scans per hour")
        
        return results


if __name__ == "__main__":
    asyncio.run(run_scaling_test())
