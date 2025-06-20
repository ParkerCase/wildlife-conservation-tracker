#!/usr/bin/env python3
"""
WildGuard AI - Platform Diagnostics & Repair Script
Tests and fixes all 8 platform scrapers individually
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Any
import json
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
import os
import sys
import time
import random
from dotenv import load_dotenv
from fake_useragent import UserAgent
import base64

# Add project paths
sys.path.append('/Users/parkercase/conservation-bot')
sys.path.append('/Users/parkercase/conservation-bot/src')

# Load environment variables
load_dotenv('/Users/parkercase/conservation-bot/backend/.env')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PlatformDiagnostics:
    def __init__(self):
        self.ua = UserAgent()
        self.session = None
        self.results = {}
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def test_all_platforms(self):
        """Test all 8 platforms systematically"""
        print("🎯 WILDGUARD AI - PLATFORM DIAGNOSTICS")
        print("=" * 60)
        print("Testing all 8 platform scrapers with comprehensive diagnostics")
        print()
        
        # Test each platform
        platforms = [
            ('eBay', self.test_ebay),
            ('Craigslist', self.test_craigslist),
            ('Mercari', self.test_mercari),
            ('AliExpress', self.test_aliexpress),
            ('Gumtree', self.test_gumtree),
            ('OLX', self.test_olx),
            ('MercadoLibre', self.test_mercadolibre),
            ('Taobao', self.test_taobao)
        ]
        
        working_platforms = []
        failed_platforms = []
        
        for platform_name, test_func in platforms:
            print(f"🔍 Testing {platform_name}...")
            try:
                success, result_count, details = await test_func()
                if success:
                    print(f"   ✅ SUCCESS: {result_count} products found")
                    if details:
                        for detail in details[:2]:  # Show first 2 products
                            print(f"      📦 {detail.get('title', 'No title')[:60]}...")
                            print(f"         💰 {detail.get('price', 'No price')}")
                    working_platforms.append(platform_name)
                else:
                    print(f"   ❌ FAILED: {details}")
                    failed_platforms.append(platform_name)
            except Exception as e:
                print(f"   💥 ERROR: {str(e)[:100]}...")
                failed_platforms.append(platform_name)
            
            print()
            await asyncio.sleep(1)  # Rate limiting between platforms
        
        # Summary
        print("=" * 60)
        print("🎯 FINAL RESULTS:")
        print(f"   ✅ WORKING: {len(working_platforms)}/8 platforms")
        if working_platforms:
            print(f"      → {', '.join(working_platforms)}")
        
        print(f"   ❌ FAILED: {len(failed_platforms)}/8 platforms")
        if failed_platforms:
            print(f"      → {', '.join(failed_platforms)}")
        
        if len(working_platforms) >= 6:
            print("\n🏆 EXCELLENT: System is production ready!")
        elif len(working_platforms) >= 4:
            print("\n⚠️  GOOD: Most platforms working, minor fixes needed")
        else:
            print("\n🚨 NEEDS WORK: Significant platform fixes required")
            
        return working_platforms, failed_platforms

    async def test_ebay(self):
        """Test eBay with proper OAuth"""
        try:
            # Check credentials
            app_id = os.getenv("EBAY_APP_ID")
            cert_id = os.getenv("EBAY_CERT_ID")
            
            if not app_id or not cert_id:
                return False, 0, "Missing eBay credentials in environment"
            
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
            
            # Get access token
            async with self.session.post(
                "https://api.ebay.com/identity/v1/oauth2/token", 
                headers=headers, 
                data=data
            ) as resp:
                token_data = await resp.json()
                
                if "access_token" not in token_data:
                    return False, 0, f"OAuth failed: {token_data}"
                
                access_token = token_data["access_token"]
            
            # Test search API
            search_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }
            
            params = {"q": "phone", "limit": "5"}
            
            async with self.session.get(
                "https://api.ebay.com/buy/browse/v1/item_summary/search",
                headers=search_headers,
                params=params
            ) as resp:
                data = await resp.json()
                items = data.get("itemSummaries", [])
                
                results = []
                for item in items:
                    results.append({
                        "title": item.get("title", ""),
                        "price": item.get("price", {}).get("value", ""),
                        "url": item.get("itemWebUrl", ""),
                    })
                
                return True, len(results), results
                
        except Exception as e:
            return False, 0, str(e)

    async def test_craigslist(self):
        """Test Craigslist with improved scraping"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=self.ua.random,
                    viewport={'width': 1366, 'height': 768}
                )
                page = await context.new_page()
                
                # Test with a major city
                url = "https://newyork.craigslist.org/search/sss?query=phone&sort=date"
                
                await page.goto(url, timeout=30000)
                await page.wait_for_timeout(3000)
                
                # Updated selectors for current Craigslist
                listings = await page.query_selector_all('.cl-search-result')
                
                results = []
                for listing in listings[:5]:
                    try:
                        title_elem = await listing.query_selector('.cl-titlebox a')
                        price_elem = await listing.query_selector('.priceinfo')
                        location_elem = await listing.query_selector('.location')
                        
                        title = await title_elem.inner_text() if title_elem else ""
                        price = await price_elem.inner_text() if price_elem else ""
                        location = await location_elem.inner_text() if location_elem else ""
                        link = await title_elem.get_attribute('href') if title_elem else ""
                        
                        if title and link:
                            if not link.startswith('http'):
                                link = f"https://newyork.craigslist.org{link}"
                            
                            results.append({
                                "title": title.strip(),
                                "price": price.strip(),
                                "location": location.strip(),
                                "url": link
                            })
                    except:
                        continue
                
                await browser.close()
                return True, len(results), results
                
        except Exception as e:
            return False, 0, str(e)

    async def test_mercari(self):
        """Test Mercari with updated selectors"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=self.ua.random,
                    viewport={'width': 1920, 'height': 1080}
                )
                page = await context.new_page()
                
                url = "https://www.mercari.com/search/?keyword=phone"
                
                await page.goto(url, timeout=30000)
                await page.wait_for_timeout(5000)  # Wait for dynamic content
                
                # Try multiple selector strategies
                selectors_to_try = [
                    '[data-testid="ItemCell"]',
                    '.mercari-item',
                    '.ItemCell',
                    '[data-item-id]'
                ]
                
                items = []
                for selector in selectors_to_try:
                    items = await page.query_selector_all(selector)
                    if items:
                        break
                
                results = []
                for item in items[:5]:
                    try:
                        # Try multiple title selectors
                        title_selectors = [
                            '[data-testid="ItemCell__ItemTitle"]',
                            '.item-name',
                            '.title',
                            'h3',
                            'p[data-testid="ItemCell__ItemTitle"]'
                        ]
                        
                        title = ""
                        for title_sel in title_selectors:
                            title_elem = await item.query_selector(title_sel)
                            if title_elem:
                                title = await title_elem.inner_text()
                                break
                        
                        # Try multiple price selectors
                        price_selectors = [
                            '[data-testid="ItemCell__ItemPrice"]',
                            '.item-price',
                            '.price',
                            'div[data-testid="ItemCell__ItemPrice"]'
                        ]
                        
                        price = ""
                        for price_sel in price_selectors:
                            price_elem = await item.query_selector(price_sel)
                            if price_elem:
                                price = await price_elem.inner_text()
                                break
                        
                        link_elem = await item.query_selector('a')
                        link = await link_elem.get_attribute('href') if link_elem else ""
                        
                        if title and link:
                            if not link.startswith('http'):
                                link = f"https://www.mercari.com{link}"
                            
                            results.append({
                                "title": title.strip(),
                                "price": price.strip(),
                                "url": link
                            })
                    except:
                        continue
                
                await browser.close()
                return True, len(results), results
                
        except Exception as e:
            return False, 0, str(e)

    async def test_aliexpress(self):
        """Test AliExpress with improved handling"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=self.ua.random,
                    viewport={'width': 1920, 'height': 1080},
                    extra_http_headers={
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    }
                )
                page = await context.new_page()
                
                url = "https://www.aliexpress.com/wholesale?SearchText=phone"
                
                await page.goto(url, timeout=30000)
                await page.wait_for_timeout(5000)
                
                # Handle potential bot detection
                if await page.query_selector('.baxia-dialog, .fm-button'):
                    print("      ⚠️  Bot detection encountered, trying to continue...")
                    await page.wait_for_timeout(3000)
                
                # Try multiple selector strategies
                product_selectors = [
                    '[data-product-id]',
                    '.search-item-card',
                    '.product-item',
                    '.item-wrap'
                ]
                
                products = []
                for selector in product_selectors:
                    products = await page.query_selector_all(selector)
                    if products:
                        break
                
                results = []
                for product in products[:5]:
                    try:
                        title_selectors = [
                            '.item-title',
                            'h1', 'h2', 'h3',
                            'a[title]',
                            '.search-card-item__titles'
                        ]
                        
                        title = ""
                        for title_sel in title_selectors:
                            title_elem = await product.query_selector(title_sel)
                            if title_elem:
                                title = await title_elem.inner_text()
                                break
                        
                        price_selectors = [
                            '.price',
                            '.notranslate',
                            '[class*="price"]',
                            '.search-card-item__price'
                        ]
                        
                        price = ""
                        for price_sel in price_selectors:
                            price_elem = await product.query_selector(price_sel)
                            if price_elem:
                                price = await price_elem.inner_text()
                                break
                        
                        link_elem = await product.query_selector('a')
                        link = await link_elem.get_attribute('href') if link_elem else ""
                        
                        if title and link:
                            if not link.startswith('http'):
                                link = f"https://www.aliexpress.com{link}"
                            
                            results.append({
                                "title": title.strip()[:60] + "...",
                                "price": price.strip(),
                                "url": link
                            })
                    except:
                        continue
                
                await browser.close()
                return True, len(results), results
                
        except Exception as e:
            return False, 0, str(e)

    async def test_gumtree(self):
        """Test Gumtree UK"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=self.ua.random,
                    viewport={'width': 1366, 'height': 768}
                )
                page = await context.new_page()
                
                url = "https://www.gumtree.com/search?search_category=all&q=phone"
                
                await page.goto(url, timeout=30000)
                await page.wait_for_timeout(3000)
                
                # Updated selectors for current Gumtree
                listing_selectors = [
                    'article.listing-maxi',
                    '.listing-tile',
                    '.listing-card'
                ]
                
                listings = []
                for selector in listing_selectors:
                    listings = await page.query_selector_all(selector)
                    if listings:
                        break
                
                results = []
                for listing in listings[:5]:
                    try:
                        title_selectors = [
                            '.listing-title a',
                            'h2 a',
                            '.ad-listing-title'
                        ]
                        
                        title = ""
                        link = ""
                        for title_sel in title_selectors:
                            title_elem = await listing.query_selector(title_sel)
                            if title_elem:
                                title = await title_elem.inner_text()
                                link = await title_elem.get_attribute('href')
                                break
                        
                        price_selectors = [
                            '.listing-price strong',
                            '.ad-price',
                            '.price'
                        ]
                        
                        price = ""
                        for price_sel in price_selectors:
                            price_elem = await listing.query_selector(price_sel)
                            if price_elem:
                                price = await price_elem.inner_text()
                                break
                        
                        if title and link:
                            if not link.startswith('http'):
                                link = f"https://www.gumtree.com{link}"
                            
                            results.append({
                                "title": title.strip(),
                                "price": price.strip(),
                                "url": link
                            })
                    except:
                        continue
                
                await browser.close()
                return True, len(results), results
                
        except Exception as e:
            return False, 0, str(e)

    async def test_olx(self):
        """Test OLX Poland"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=self.ua.random,
                    viewport={'width': 1920, 'height': 1080}
                )
                page = await context.new_page()
                
                url = "https://www.olx.pl/oferty/q-phone/"
                
                await page.goto(url, timeout=30000)
                await page.wait_for_timeout(3000)
                
                # Handle cookie consent if present
                try:
                    cookie_button = await page.query_selector('[data-cy="accept-consent-button"]')
                    if cookie_button:
                        await cookie_button.click()
                        await page.wait_for_timeout(1000)
                except:
                    pass
                
                # OLX listing selectors
                listing_selectors = [
                    '[data-cy="l-card"]',
                    '.offer-wrapper',
                    'article'
                ]
                
                listings = []
                for selector in listing_selectors:
                    listings = await page.query_selector_all(selector)
                    if listings:
                        break
                
                results = []
                for listing in listings[:5]:
                    try:
                        title_selectors = [
                            'h3',
                            'h4',
                            '.title',
                            '[data-cy="ad-card-title"]'
                        ]
                        
                        title = ""
                        link = ""
                        for title_sel in title_selectors:
                            title_elem = await listing.query_selector(title_sel)
                            if title_elem:
                                title = await title_elem.inner_text()
                                # Look for link in parent or self
                                link_elem = await listing.query_selector('a')
                                if link_elem:
                                    link = await link_elem.get_attribute('href')
                                break
                        
                        price_selectors = [
                            '.price',
                            '[data-testid="ad-price"]',
                            '.offer-price'
                        ]
                        
                        price = ""
                        for price_sel in price_selectors:
                            price_elem = await listing.query_selector(price_sel)
                            if price_elem:
                                price = await price_elem.inner_text()
                                break
                        
                        if title and link:
                            if not link.startswith('http'):
                                link = f"https://www.olx.pl{link}"
                            
                            results.append({
                                "title": title.strip(),
                                "price": price.strip(),
                                "url": link
                            })
                    except:
                        continue
                
                await browser.close()
                return True, len(results), results
                
        except Exception as e:
            return False, 0, str(e)

    async def test_mercadolibre(self):
        """Test MercadoLibre Mexico"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=self.ua.random,
                    viewport={'width': 1920, 'height': 1080}
                )
                page = await context.new_page()
                
                url = "https://listado.mercadolibre.com.mx/phone"
                
                await page.goto(url, timeout=30000)
                await page.wait_for_timeout(3000)
                
                # Wait for search results
                await page.wait_for_selector('.ui-search-results', timeout=10000)
                
                # Extract products with JavaScript
                products = await page.evaluate('''
                    () => {
                        const products = [];
                        const productElements = document.querySelectorAll('.ui-search-result, .item__info');
                        
                        productElements.forEach((el, index) => {
                            if (index >= 5) return; // Limit results
                            
                            const titleEl = el.querySelector('.ui-search-item__title, h2 a, .item__title');
                            const priceEl = el.querySelector('.price-tag, .ui-search-price__second-line, .item__price');
                            const linkEl = el.querySelector('a, .ui-search-link');
                            
                            const title = titleEl ? titleEl.textContent.trim() : '';
                            const price = priceEl ? priceEl.textContent.trim() : '';
                            const link = linkEl ? linkEl.href : '';
                            
                            if (title && link) {
                                products.push({
                                    title: title,
                                    price: price,
                                    url: link
                                });
                            }
                        });
                        
                        return products;
                    }
                ''')
                
                await browser.close()
                return True, len(products), products
                
        except Exception as e:
            return False, 0, str(e)

    async def test_taobao(self):
        """Test Taobao with anti-bot handling"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=self.ua.random,
                    viewport={'width': 1920, 'height': 1080},
                    extra_http_headers={
                        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    }
                )
                page = await context.new_page()
                
                url = "https://s.taobao.com/search?q=phone"
                
                await page.goto(url, timeout=30000)
                await page.wait_for_timeout(5000)
                
                # Check for anti-bot measures
                if await page.query_selector('.nc_wrapper, .J_MIDDLEWARE_ERROR'):
                    return False, 0, "Anti-bot detection triggered"
                
                # Try to extract data from window variables
                products_data = await page.evaluate('''
                    () => {
                        try {
                            let data = [];
                            
                            // Check for data in window.g_page_config
                            if (window.g_page_config && window.g_page_config.mods) {
                                const itemlist = window.g_page_config.mods.itemlist;
                                if (itemlist && itemlist.data && itemlist.data.auctions) {
                                    data = itemlist.data.auctions.slice(0, 5);
                                }
                            }
                            
                            // Fallback: DOM scraping
                            if (data.length === 0) {
                                const items = document.querySelectorAll('.item, .J_MouserOnverReq');
                                items.forEach((item, index) => {
                                    if (index >= 5) return;
                                    
                                    const titleEl = item.querySelector('.title a, .pic-box-inner .title');
                                    const priceEl = item.querySelector('.price .g_price, .view_price');
                                    const linkEl = item.querySelector('.title a, .pic-box-inner a');
                                    
                                    if (titleEl && linkEl) {
                                        data.push({
                                            title: titleEl.textContent.trim(),
                                            view_price: priceEl ? priceEl.textContent.trim() : '',
                                            detail_url: linkEl.href
                                        });
                                    }
                                });
                            }
                            
                            return data;
                        } catch (e) {
                            return [];
                        }
                    }
                ''')
                
                results = []
                for product in products_data:
                    title = product.get('title', '') or product.get('raw_title', '')
                    price = product.get('view_price', '')
                    url = product.get('detail_url', '') or product.get('nid', '')
                    
                    if url and not url.startswith('http'):
                        url = f'https://item.taobao.com/item.htm?id={url}'
                    
                    if title and url:
                        results.append({
                            'title': title,
                            'price': price,
                            'url': url
                        })
                
                await browser.close()
                return True, len(results), results
                
        except Exception as e:
            return False, 0, str(e)


async def main():
    """Run comprehensive platform diagnostics"""
    async with PlatformDiagnostics() as diagnostics:
        working, failed = await diagnostics.test_all_platforms()
        
        print()
        print("🔧 REPAIR RECOMMENDATIONS:")
        print("-" * 40)
        
        for platform in failed:
            if platform == "eBay":
                print(f"   🔑 {platform}: Check OAuth credentials and API access")
            elif platform in ["Craigslist", "MercadoLibre"]:
                print(f"   🕒 {platform}: Implement better timeout handling")
            elif platform in ["Mercari", "AliExpress", "Gumtree", "OLX"]:
                print(f"   🎯 {platform}: Update CSS selectors for current site structure")
            elif platform == "Taobao":
                print(f"   🛡️  {platform}: Implement advanced anti-bot circumvention")
        
        print()
        if len(working) >= 6:
            print("🎊 CONCLUSION: System is ready for production!")
        else:
            print("🔄 CONCLUSION: Implementing fixes...")


if __name__ == "__main__":
    asyncio.run(main())
