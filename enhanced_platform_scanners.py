#!/usr/bin/env python3
"""
Enhanced Platform Scanners - Bulletproof versions with anti-bot measures
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
import base64
from fake_useragent import UserAgent
import random
import time
from dotenv import load_dotenv

load_dotenv('/Users/parkercase/conservation-bot/backend/.env')

class EnhancedEbayScanner:
    """Enhanced eBay scanner with proper OAuth and retry logic"""
    
    def __init__(self):
        self.app_id = os.getenv("EBAY_APP_ID")
        self.cert_id = os.getenv("EBAY_CERT_ID")
        self.oauth_token = None
        self.token_expiry = None
        self.token_endpoint = "https://api.ebay.com/identity/v1/oauth2/token"
        self.api_endpoint = "https://api.ebay.com/buy/browse/v1/item_summary/search"
        self.max_retries = 3

    async def get_access_token(self, session):
        """Enhanced OAuth with better error handling"""
        if (self.oauth_token and self.token_expiry and 
            datetime.utcnow() < self.token_expiry):
            return self.oauth_token

        if not self.app_id or not self.cert_id:
            raise ValueError("eBay credentials missing - check EBAY_APP_ID and EBAY_CERT_ID")

        credentials = f"{self.app_id}:{self.cert_id}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        
        data = {
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope",
        }

        for attempt in range(self.max_retries):
            try:
                async with session.post(self.token_endpoint, headers=headers, data=data) as resp:
                    token_data = await resp.json()
                    
                    if resp.status == 200 and "access_token" in token_data:
                        self.oauth_token = token_data["access_token"]
                        expires_in = int(token_data.get("expires_in", 7200))
                        self.token_expiry = datetime.utcnow() + timedelta(seconds=expires_in - 60)
                        logging.info("eBay OAuth successful")
                        return self.oauth_token
                    else:
                        error_msg = token_data.get("error_description", "Unknown OAuth error")
                        logging.warning(f"eBay OAuth attempt {attempt + 1} failed: {error_msg}")
                        
                        if attempt < self.max_retries - 1:
                            await asyncio.sleep(2 ** attempt)  # Exponential backoff
                            
            except Exception as e:
                logging.warning(f"eBay OAuth attempt {attempt + 1} exception: {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)

        raise RuntimeError("eBay OAuth failed after all retries")

    async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
        """Enhanced scan with retry logic and rate limiting"""
        results = []
        search_terms = keywords["direct_terms"][:5]  # Limit to respect API limits
        
        try:
            token = await self.get_access_token(session)
        except Exception as e:
            logging.error(f"eBay OAuth failed: {e}")
            return []

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "WildGuard-Conservation-Bot/1.0"
        }

        for term in search_terms:
            params = {"q": term, "limit": "10"}  # Increased limit
            
            for attempt in range(self.max_retries):
                try:
                    async with session.get(self.api_endpoint, headers=headers, params=params) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            items = data.get("itemSummaries", [])
                            
                            for item in items:
                                results.append({
                                    "title": item.get("title", ""),
                                    "price": item.get("price", {}).get("value", ""),
                                    "url": item.get("itemWebUrl", ""),
                                    "search_term": term,
                                    "image": item.get("image", {}).get("imageUrl", ""),
                                    "location": item.get("itemLocation", {}).get("postalCode", ""),
                                    "platform": "ebay"
                                })
                            
                            logging.info(f"eBay: Found {len(items)} items for '{term}'")
                            break  # Success, exit retry loop
                            
                        elif resp.status == 429:  # Rate limited
                            logging.warning(f"eBay rate limited, waiting...")
                            await asyncio.sleep(60)  # Wait 1 minute
                            
                        else:
                            logging.warning(f"eBay API error {resp.status} for {term}")
                            break  # Don't retry non-rate-limit errors
                            
                except Exception as e:
                    logging.warning(f"eBay scan attempt {attempt + 1} failed for {term}: {e}")
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(2 ** attempt)

            # Rate limiting between terms
            await asyncio.sleep(1)

        return results


class EnhancedCraigslistScanner:
    """Enhanced Craigslist scanner with anti-bot measures"""
    
    def __init__(self):
        self.priority_cities = [
            "newyork", "losangeles", "chicago", "miami", "houston", 
            "seattle", "boston", "atlanta", "denver", "portland"
        ]
        self.ua = UserAgent()
        self.max_retries = 2

    async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
        """Enhanced scan with browser rotation and stealth measures"""
        results = []
        search_terms = keywords["direct_terms"][:2]  # Limit to avoid blocks
        
        async with async_playwright() as p:
            # Random browser choice
            browser_type = random.choice([p.chromium, p.firefox])
            
            browser = await browser_type.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu'
                ]
            )
            
            for city in self.priority_cities[:3]:  # Limit cities to avoid detection
                for term in search_terms:
                    url = f"https://{city}.craigslist.org/search/sss?query={term}&sort=date"
                    
                    # Create new context for each search (fresh fingerprint)
                    context = await browser.new_context(
                        user_agent=self.ua.random,
                        viewport=random.choice([
                            {"width": 1366, "height": 768},
                            {"width": 1920, "height": 1080},
                            {"width": 1536, "height": 864},
                        ]),
                        extra_http_headers={
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                            "Accept-Language": "en-US,en;q=0.5",
                            "Accept-Encoding": "gzip, deflate",
                            "Connection": "keep-alive",
                            "Upgrade-Insecure-Requests": "1",
                        }
                    )
                    
                    page = await context.new_page()
                    
                    try:
                        await page.goto(url, timeout=20000, wait_until='domcontentloaded')
                        
                        # Human-like behavior
                        await page.wait_for_timeout(random.randint(2000, 4000))
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight/2)")
                        await page.wait_for_timeout(random.randint(1000, 2000))
                        
                        # Extract listings
                        items = await page.query_selector_all(".cl-search-result")
                        
                        for item in items[:3]:  # Limit per city/term
                            try:
                                title_elem = await item.query_selector("a.cl-app-anchor")
                                price_elem = await item.query_selector(".priceinfo")
                                location_elem = await item.query_selector(".location")
                                
                                title = await title_elem.inner_text() if title_elem else ""
                                price = await price_elem.inner_text() if price_elem else ""
                                location = await location_elem.inner_text() if location_elem else ""
                                link = await title_elem.get_attribute("href") if title_elem else ""
                                
                                if link and link.startswith("/"):
                                    link = f"https://{city}.craigslist.org{link}"
                                
                                if title and link:
                                    results.append({
                                        "title": title.strip(),
                                        "price": price.strip(),
                                        "location": location.strip(),
                                        "url": link,
                                        "search_term": term,
                                        "city": city,
                                        "platform": "craigslist"
                                    })
                            except:
                                continue
                        
                        logging.info(f"Craigslist {city}: Found {len(items[:3])} items for '{term}'")
                        
                    except Exception as e:
                        logging.warning(f"Craigslist {city} error for {term}: {e}")
                    
                    finally:
                        await page.close()
                        await context.close()
                    
                    # Random delay between requests
                    await asyncio.sleep(random.uniform(3, 7))
            
            await browser.close()
        
        return results


class EnhancedAliExpressScanner:
    """Enhanced AliExpress scanner with advanced anti-bot measures"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.search_url = "https://www.aliexpress.us/w/wholesale"
        
    async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
        """Enhanced scan with stealth measures for AliExpress"""
        results = []
        search_terms = keywords["direct_terms"][:2]
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ]
            )
            
            context = await browser.new_context(
                user_agent=self.ua.random,
                viewport={'width': 1920, 'height': 1080},
                extra_http_headers={
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                }
            )
            
            page = await context.new_page()
            
            # Set additional properties to avoid detection
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
            """)
            
            for term in search_terms:
                url = f"{self.search_url}?SearchText={term}&SortType=default"
                
                try:
                    await page.goto(url, timeout=30000, wait_until='networkidle')
                    
                    # Human-like waiting and scrolling
                    await page.wait_for_timeout(random.randint(3000, 6000))
                    
                    # Check for bot detection
                    if await page.query_selector('.baxia-dialog, .nc_wrapper'):
                        logging.warning(f"AliExpress bot detection for {term}")
                        continue
                    
                    # Wait for products and scroll to load more
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight/3)")
                    await page.wait_for_timeout(2000)
                    
                    # Extract products with JavaScript evaluation
                    products = await page.evaluate('''
                        () => {
                            const products = [];
                            const selectors = [
                                '.search-item-card-wrapper-gallery',
                                '.product-item',
                                '[data-item-id]',
                                '.item'
                            ];
                            
                            let elements = [];
                            for (const selector of selectors) {
                                elements = document.querySelectorAll(selector);
                                if (elements.length > 0) break;
                            }
                            
                            elements.forEach((el, index) => {
                                if (index >= 5) return;
                                
                                const titleSelectors = ['h1', 'h3', 'a[title]', '.item-title'];
                                const priceSelectors = ['.price', '.notranslate', '[class*="price"]'];
                                const linkSelectors = ['a'];
                                const imageSelectors = ['img'];
                                
                                let title = '', price = '', link = '', image = '';
                                
                                for (const sel of titleSelectors) {
                                    const elem = el.querySelector(sel);
                                    if (elem && elem.textContent.trim()) {
                                        title = elem.textContent.trim();
                                        break;
                                    }
                                }
                                
                                for (const sel of priceSelectors) {
                                    const elem = el.querySelector(sel);
                                    if (elem && elem.textContent.trim()) {
                                        price = elem.textContent.trim();
                                        break;
                                    }
                                }
                                
                                for (const sel of linkSelectors) {
                                    const elem = el.querySelector(sel);
                                    if (elem && elem.href) {
                                        link = elem.href;
                                        break;
                                    }
                                }
                                
                                for (const sel of imageSelectors) {
                                    const elem = el.querySelector(sel);
                                    if (elem && elem.src) {
                                        image = elem.src;
                                        break;
                                    }
                                }
                                
                                if (title && link) {
                                    products.push({
                                        title: title,
                                        price: price,
                                        url: link.startsWith('http') ? link : 'https://www.aliexpress.com' + link,
                                        image: image
                                    });
                                }
                            });
                            
                            return products;
                        }
                    ''')
                    
                    for product in products:
                        product['search_term'] = term
                        product['platform'] = 'aliexpress'
                        results.append(product)
                    
                    logging.info(f"AliExpress: Found {len(products)} products for '{term}'")
                    
                    # Rate limiting
                    await asyncio.sleep(random.uniform(4, 8))
                    
                except Exception as e:
                    logging.warning(f"AliExpress error for {term}: {e}")
            
            await browser.close()
        
        return results


class ProductionPlatformScanner:
    """Production-ready platform scanner with all enhancements"""
    
    def __init__(self):
        self.platforms = {
            "ebay": EnhancedEbayScanner(),
            "craigslist": EnhancedCraigslistScanner(),
            "aliexpress": EnhancedAliExpressScanner(),
            # Add other enhanced scanners here
        }
        self.session = None

    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=60)
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=3)
        self.session = aiohttp.ClientSession(timeout=timeout, connector=connector)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def scan_platform_safely(self, platform_name: str, platform_scanner, keywords: Dict) -> List[Dict]:
        """Scan a platform with comprehensive error handling and retries"""
        max_attempts = 2
        
        for attempt in range(max_attempts):
            try:
                logging.info(f"Scanning {platform_name} (attempt {attempt + 1})...")
                
                # Set timeout based on platform
                if platform_name in ['taobao', 'aliexpress']:
                    timeout = 60
                elif platform_name in ['craigslist', 'gumtree']:
                    timeout = 45
                else:
                    timeout = 30
                
                results = await asyncio.wait_for(
                    platform_scanner.scan(keywords, self.session),
                    timeout=timeout
                )
                
                if results:
                    logging.info(f"{platform_name}: Success - {len(results)} results")
                    return results
                else:
                    logging.warning(f"{platform_name}: No results found")
                    
            except asyncio.TimeoutError:
                logging.warning(f"{platform_name}: Timeout on attempt {attempt + 1}")
                if attempt < max_attempts - 1:
                    await asyncio.sleep(5)  # Wait before retry
                    
            except Exception as e:
                logging.error(f"{platform_name}: Error on attempt {attempt + 1}: {e}")
                if attempt < max_attempts - 1:
                    await asyncio.sleep(3)
        
        logging.error(f"{platform_name}: Failed after all attempts")
        return []

    async def scan_all_platforms_robust(self, keywords: Dict) -> Dict[str, List[Dict]]:
        """Scan all platforms with robust error handling"""
        results = {}
        
        # Run platforms in parallel with limited concurrency
        semaphore = asyncio.Semaphore(3)  # Max 3 platforms at once
        
        async def scan_with_semaphore(platform_name, platform_scanner):
            async with semaphore:
                return await self.scan_platform_safely(platform_name, platform_scanner, keywords)
        
        tasks = [
            scan_with_semaphore(name, scanner) 
            for name, scanner in self.platforms.items()
        ]
        
        platform_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for (platform_name, _), result in zip(self.platforms.items(), platform_results):
            if isinstance(result, Exception):
                logging.error(f"{platform_name}: Exception - {result}")
                results[platform_name] = []
            else:
                results[platform_name] = result
        
        return results


# Test the enhanced scanners
async def test_enhanced_platforms():
    """Test the enhanced platform scanners"""
    print("🧪 TESTING ENHANCED PLATFORM SCANNERS")
    print("=" * 50)
    
    keywords = {'direct_terms': ['antique', 'carved']}
    
    async with ProductionPlatformScanner() as scanner:
        results = await scanner.scan_all_platforms_robust(keywords)
        
        total_results = 0
        working_platforms = []
        
        for platform_name, platform_results in results.items():
            count = len(platform_results)
            total_results += count
            
            if count > 0:
                working_platforms.append((platform_name, count))
                print(f"✅ {platform_name.upper()}: {count} results")
                
                # Show samples
                for i, result in enumerate(platform_results[:2], 1):
                    title = result.get('title', 'No title')[:40]
                    price = result.get('price', 'No price')
                    print(f"   {i}. {title}... - {price}")
            else:
                print(f"❌ {platform_name.upper()}: No results")
        
        print(f"\n📊 ENHANCED SCANNER RESULTS:")
        print(f"   ✅ Working platforms: {len(working_platforms)}")
        print(f"   📊 Total results: {total_results}")
        
        return len(working_platforms), total_results

if __name__ == "__main__":
    asyncio.run(test_enhanced_platforms())
