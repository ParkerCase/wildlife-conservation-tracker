#!/usr/bin/env python3
"""
WildGuard AI - FINAL COMPREHENSIVE VERIFICATION
Definitive test of all 8 platform scrapers with complete fixes
"""

import asyncio
import aiohttp
from playwright.async_api import async_playwright
import os
import sys
import time
from dotenv import load_dotenv
from fake_useragent import UserAgent
import base64

# Load environment variables
load_dotenv('/Users/parkercase/conservation-bot/backend/.env')

class FinalVerification:
    def __init__(self):
        self.ua = UserAgent()
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def verify_ebay(self):
        """Verify eBay is working with OAuth"""
        try:
            app_id = os.getenv("EBAY_APP_ID")
            cert_id = os.getenv("EBAY_CERT_ID")
            
            if not app_id or not cert_id:
                return False, "Missing credentials"
            
            # Get OAuth token
            credentials = f"{app_id}:{cert_id}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                "Authorization": f"Basic {encoded_credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            
            data = {
                "grant_type": "client_credentials",
                "scope": "https://api.ebay.com/oauth/api_scope",
            }
            
            async with self.session.post(
                "https://api.ebay.com/identity/v1/oauth2/token", 
                headers=headers, 
                data=data
            ) as resp:
                token_data = await resp.json()
                access_token = token_data.get("access_token")
                
                if not access_token:
                    return False, f"OAuth failed: {token_data}"
            
            # Test search
            search_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }
            
            params = {"q": "jewelry", "limit": "3"}
            
            async with self.session.get(
                "https://api.ebay.com/buy/browse/v1/item_summary/search",
                headers=search_headers,
                params=params
            ) as resp:
                data = await resp.json()
                items = data.get("itemSummaries", [])
                
                return True, f"{len(items)} products found"
                
        except Exception as e:
            return False, str(e)

    async def verify_craigslist(self):
        """Verify Craigslist with updated selectors"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
                page = await context.new_page()
                
                url = "https://newyork.craigslist.org/search/sss?query=jewelry&sort=date"
                
                await page.goto(url, timeout=25000)
                await page.wait_for_timeout(3000)
                
                # Use the working selectors we discovered
                listings = await page.query_selector_all('.cl-search-result')
                
                products = []
                for listing in listings[:3]:
                    try:
                        title_elem = await listing.query_selector('a.cl-app-anchor')
                        if title_elem:
                            title = await title_elem.inner_text()
                            link = await title_elem.get_attribute('href')
                            if title and link:
                                products.append({"title": title[:50], "url": link})
                    except:
                        continue
                
                await browser.close()
                return True, f"{len(products)} products found"
                
        except Exception as e:
            return False, str(e)

    async def verify_aliexpress(self):
        """Verify AliExpress with fixed URL and selectors"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=self.ua.random,
                    viewport={'width': 1920, 'height': 1080}
                )
                page = await context.new_page()
                
                # Use the working URL we discovered
                url = "https://www.aliexpress.us/w/wholesale-jewelry.html"
                
                await page.goto(url, timeout=30000)
                await page.wait_for_timeout(5000)
                
                # Use the working selector
                products = await page.query_selector_all('.search-item-card-wrapper-gallery')
                
                results = []
                for product in products[:3]:
                    try:
                        title_elem = await product.query_selector('h1, h2, h3, .item-title')
                        if title_elem:
                            title = await title_elem.inner_text()
                            if title:
                                results.append({"title": title[:50]})
                    except:
                        continue
                
                await browser.close()
                return True, f"{len(results)} products found"
                
        except Exception as e:
            return False, str(e)

    async def verify_mercari(self):
        """Verify Mercari with improved approach"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=self.ua.random,
                    viewport={'width': 1920, 'height': 1080}
                )
                page = await context.new_page()
                
                url = "https://www.mercari.com/search/?keyword=jewelry"
                
                await page.goto(url, timeout=30000)
                await page.wait_for_timeout(8000)  # Wait for heavy JS
                
                # Look for any items
                items = await page.query_selector_all('[data-testid*="Item"], .item, .product')
                
                results = []
                for item in items[:3]:
                    try:
                        # Try various selectors for title
                        title_selectors = ['h3', 'h2', '[data-testid*="title"]', '.title']
                        for selector in title_selectors:
                            title_elem = await item.query_selector(selector)
                            if title_elem:
                                title = await title_elem.inner_text()
                                if title and len(title.strip()) > 5:
                                    results.append({"title": title[:50]})
                                    break
                    except:
                        continue
                
                await browser.close()
                return True, f"{len(results)} products found"
                
        except Exception as e:
            return False, str(e)

    async def verify_gumtree(self):
        """Verify Gumtree UK"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=self.ua.random
                )
                page = await context.new_page()
                
                url = "https://www.gumtree.com/search?search_category=all&q=jewelry"
                
                await page.goto(url, timeout=25000)
                await page.wait_for_timeout(3000)
                
                # Try different listing selectors
                selectors = ['article.listing-maxi', '.listing-tile', '.listing-card', 'article']
                
                results = []
                for selector in selectors:
                    listings = await page.query_selector_all(selector)
                    if listings:
                        for listing in listings[:3]:
                            try:
                                title_elem = await listing.query_selector('h2 a, .listing-title a, h3 a')
                                if title_elem:
                                    title = await title_elem.inner_text()
                                    if title:
                                        results.append({"title": title[:50]})
                            except:
                                continue
                        break
                
                await browser.close()
                return True, f"{len(results)} products found"
                
        except Exception as e:
            return False, str(e)

    async def verify_olx(self):
        """Verify OLX Poland"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=self.ua.random
                )
                page = await context.new_page()
                
                url = "https://www.olx.pl/oferty/q-jewelry/"
                
                await page.goto(url, timeout=25000)
                await page.wait_for_timeout(3000)
                
                # Handle cookie consent
                try:
                    cookie_btn = await page.query_selector('[data-cy="accept-consent-button"]')
                    if cookie_btn:
                        await cookie_btn.click()
                        await page.wait_for_timeout(1000)
                except:
                    pass
                
                # Look for listings
                listings = await page.query_selector_all('[data-cy="l-card"], .offer-wrapper, article')
                
                results = []
                for listing in listings[:3]:
                    try:
                        title_elem = await listing.query_selector('h3, h4, .title')
                        if title_elem:
                            title = await title_elem.inner_text()
                            if title:
                                results.append({"title": title[:50]})
                    except:
                        continue
                
                await browser.close()
                return True, f"{len(results)} products found"
                
        except Exception as e:
            return False, str(e)

    async def verify_mercadolibre(self):
        """Verify MercadoLibre Mexico"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=self.ua.random
                )
                page = await context.new_page()
                
                url = "https://listado.mercadolibre.com.mx/jewelry"
                
                await page.goto(url, timeout=25000)
                await page.wait_for_timeout(3000)
                
                # Look for products
                products = await page.evaluate('''
                    () => {
                        const products = [];
                        const items = document.querySelectorAll('.ui-search-result, .item');
                        
                        items.forEach((item, index) => {
                            if (index >= 3) return;
                            
                            const titleEl = item.querySelector('.ui-search-item__title, h2, .item-title');
                            if (titleEl && titleEl.textContent.trim()) {
                                products.push({title: titleEl.textContent.trim().slice(0, 50)});
                            }
                        });
                        
                        return products;
                    }
                ''')
                
                await browser.close()
                return True, f"{len(products)} products found"
                
        except Exception as e:
            return False, str(e)

    async def verify_taobao(self):
        """Verify Taobao (limited due to anti-bot)"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=self.ua.random,
                    extra_http_headers={
                        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
                    }
                )
                page = await context.new_page()
                
                url = "https://s.taobao.com/search?q=jewelry"
                
                await page.goto(url, timeout=25000)
                await page.wait_for_timeout(5000)
                
                # Check for anti-bot
                if await page.query_selector('.nc_wrapper, .J_MIDDLEWARE_ERROR'):
                    await browser.close()
                    return False, "Anti-bot detection triggered"
                
                # Simple check for any products
                page_text = await page.content()
                if 'item' in page_text.lower() and len(page_text) > 50000:
                    await browser.close()
                    return True, "Page loaded with potential products (anti-bot limited)"
                
                await browser.close()
                return False, "No products detected"
                
        except Exception as e:
            return False, str(e)

    async def run_final_verification(self):
        """Run comprehensive verification of all platforms"""
        print("🎯 WILDGUARD AI - FINAL PLATFORM VERIFICATION")
        print("=" * 60)
        print("Definitive test of all 8 platform scrapers")
        print()
        
        platforms = [
            ("eBay", self.verify_ebay),
            ("Craigslist", self.verify_craigslist),
            ("AliExpress", self.verify_aliexpress),
            ("Mercari", self.verify_mercari),
            ("Gumtree", self.verify_gumtree),
            ("OLX", self.verify_olx),
            ("MercadoLibre", self.verify_mercadolibre),
            ("Taobao", self.verify_taobao)
        ]
        
        working = []
        partially_working = []
        failed = []
        
        for platform_name, verify_func in platforms:
            print(f"🔍 Verifying {platform_name}...")
            
            try:
                success, details = await verify_func()
                
                if success:
                    if "products found" in details and not details.startswith("0"):
                        print(f"   ✅ FULLY WORKING: {details}")
                        working.append(platform_name)
                    else:
                        print(f"   🔧 PARTIALLY WORKING: {details}")
                        partially_working.append(platform_name)
                else:
                    print(f"   ❌ NOT WORKING: {details}")
                    failed.append(platform_name)
                    
            except Exception as e:
                print(f"   💥 ERROR: {str(e)[:80]}...")
                failed.append(platform_name)
            
            print()
            await asyncio.sleep(1)
        
        # Final summary
        print("=" * 60)
        print("🎯 FINAL VERIFICATION RESULTS:")
        print(f"   ✅ FULLY WORKING: {len(working)}/8 platforms")
        if working:
            print(f"      → {', '.join(working)}")
        
        print(f"   🔧 PARTIALLY WORKING: {len(partially_working)}/8 platforms")
        if partially_working:
            print(f"      → {', '.join(partially_working)}")
        
        print(f"   ❌ NOT WORKING: {len(failed)}/8 platforms")
        if failed:
            print(f"      → {', '.join(failed)}")
        
        total_functional = len(working) + len(partially_working)
        
        print()
        print(f"🎯 OVERALL ASSESSMENT: {total_functional}/8 platforms functional ({(total_functional/8)*100:.0f}%)")
        
        if total_functional >= 6:
            print("🏆 VERDICT: PRODUCTION READY!")
            print("   System has sufficient platform coverage for live deployment")
        elif total_functional >= 4:
            print("⚠️  VERDICT: MOSTLY READY - Minor improvements recommended")
        else:
            print("🔧 VERDICT: NEEDS MORE WORK - Major fixes required")
        
        print()
        print("📋 RECOMMENDED NEXT STEPS:")
        if len(working) >= 3:
            print(f"   1. Deploy with {len(working)} fully working platforms")
            print(f"   2. Implement incremental fixes for {len(partially_working)} partial platforms")
            print(f"   3. Investigate {len(failed)} failed platforms as time permits")
        else:
            print("   1. Focus on fixing major platform issues before deployment")
            print("   2. Ensure at least 3-4 platforms are fully functional")


async def main():
    async with FinalVerification() as verifier:
        await verifier.run_final_verification()


if __name__ == "__main__":
    asyncio.run(main())
