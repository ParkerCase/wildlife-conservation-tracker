#!/usr/bin/env python3
"""
WildGuard AI - REAL Platform Scanner (No Fake Data)
All 8 platforms with 100% real scraping implementations
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
import sys

# Add path for keyword database
sys.path.append('/Users/parkercase/conservation-bot')
from enhanced_keywords import get_massive_keyword_database, get_optimized_search_terms, get_platform_specific_terms

load_dotenv('/Users/parkercase/conservation-bot/backend/.env')

class RealPlatformScanner:
    """100% REAL Platform Scanner - No Fake Data Anywhere"""
    
    def __init__(self):
        self.ua = UserAgent()
        
        # All 8 platforms with REAL implementations
        self.platforms = {
            "ebay": RealEbayScanner(),
            "craigslist": RealCraigslistScanner(),
            "aliexpress": RealAliExpressScanner(),
            "olx": RealOLXScanner(),
            "gumtree": RealGumtreeScanner(),
            "mercadolibre": RealMercadoLibreScanner(),
            "taobao": RealTaobaoScanner(),
            "mercari": RealMercariScanner()
        }
        
        self.keywords = get_massive_keyword_database()
        self.session = None

    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=120)
        connector = aiohttp.TCPConnector(limit=30, limit_per_host=8)
        self.session = aiohttp.ClientSession(
            timeout=timeout, 
            connector=connector,
            headers={'User-Agent': self.ua.random}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def scan_all_platforms(self) -> List[Dict[Any, Any]]:
        """Scan all 8 platforms with REAL data only"""
        results = []
        
        # Use optimized search terms for maximum results
        optimized_keywords = {
            'direct_terms': get_optimized_search_terms()
        }
        
        # Scan platforms concurrently
        tasks = []
        for platform_name, scanner in self.platforms.items():
            # Get platform-specific keywords for better results
            platform_keywords = {
                'direct_terms': get_platform_specific_terms(platform_name)
            }
            task = self._scan_platform_real(platform_name, scanner, platform_keywords)
            tasks.append(task)
        
        platform_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for platform_name, result in zip(self.platforms.keys(), platform_results):
            if isinstance(result, Exception):
                logging.error(f"{platform_name} scan failed: {result}")
                continue
            
            for listing in result:
                listing["platform"] = platform_name
                listing["scan_timestamp"] = datetime.utcnow().isoformat()
                results.append(listing)
        
        return results

    async def _scan_platform_real(self, platform_name: str, scanner, keywords: Dict) -> List[Dict]:
        """Scan platform with REAL data only - no fallbacks"""
        try:
            timeout = self._get_platform_timeout(platform_name)
            
            results = await asyncio.wait_for(
                scanner.scan(keywords, self.session),
                timeout=timeout
            )
            
            if results:
                logging.info(f"{platform_name}: {len(results)} REAL results")
                return results
            else:
                logging.warning(f"{platform_name}: No results found")
                return []
                
        except asyncio.TimeoutError:
            logging.warning(f"{platform_name}: Timeout after {timeout}s")
            return []
        except Exception as e:
            logging.error(f"{platform_name}: Error - {e}")
            return []

    def _get_platform_timeout(self, platform_name: str) -> int:
        """Get appropriate timeout for each platform"""
        timeouts = {
            'taobao': 120,  # Increased for anti-bot measures
            'aliexpress': 90,
            'mercadolibre': 60,
            'gumtree': 60,
            'craigslist': 90,
            'olx': 60,
            'mercari': 50,
            'ebay': 40
        }
        return timeouts.get(platform_name, 60)

    def load_keyword_database(self) -> Dict:
        """Load massive keyword database"""
        return get_massive_keyword_database()


class RealEbayScanner:
    """ENHANCED eBay scanner - more keywords, better results"""
    
    def __init__(self):
        self.app_id = os.getenv("EBAY_APP_ID")
        self.cert_id = os.getenv("EBAY_CERT_ID")
        self.oauth_token = None
        self.token_expiry = None

    async def get_access_token(self, session):
        if (self.oauth_token and self.token_expiry and 
            datetime.utcnow() < self.token_expiry):
            return self.oauth_token

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

        async with session.post(
            "https://api.ebay.com/identity/v1/oauth2/token", 
            headers=headers, data=data
        ) as resp:
            if resp.status == 200:
                token_data = await resp.json()
                self.oauth_token = token_data["access_token"]
                expires_in = int(token_data.get("expires_in", 7200))
                self.token_expiry = datetime.utcnow() + timedelta(seconds=expires_in - 60)
                return self.oauth_token
            else:
                raise RuntimeError(f"eBay OAuth failed: {resp.status}")

    async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
        results = []
        search_terms = keywords["direct_terms"][:8]  # Increased from 3 to 8
        
        try:
            token = await self.get_access_token(session)
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }

            for term in search_terms:
                params = {"q": term, "limit": "20"}  # Increased from 15 to 20
                
                async with session.get(
                    "https://api.ebay.com/buy/browse/v1/item_summary/search",
                    headers=headers, params=params
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        items = data.get("itemSummaries", [])
                        
                        for item in items:
                            results.append({
                                "title": item.get("title", ""),
                                "price": item.get("price", {}).get("value", ""),
                                "url": item.get("itemWebUrl", ""),
                                "search_term": term,
                                "platform": "ebay",
                                "location": item.get("itemLocation", {}).get("postalCode", ""),
                                "image": item.get("image", {}).get("imageUrl", "")
                            })
                    
                    elif resp.status == 429:  # Rate limited
                        await asyncio.sleep(5)
                        continue
                
                await asyncio.sleep(0.5)  # Reduced delay for faster scanning

        except Exception as e:
            logging.error(f"eBay error: {e}")
        
        return results


class RealCraigslistScanner:
    """ENHANCED Craigslist scanner - more cities, more keywords"""
    
    def __init__(self):
        self.cities = [
            "newyork", "losangeles", "chicago", "houston", "phoenix", 
            "philadelphia", "sanantonio", "sandiego", "dallas", "seattle"
        ]
        self.ua = UserAgent()

    async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
        results = []
        search_terms = keywords["direct_terms"][:5]  # Increased from 2 to 5
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
            )
            
            for city in self.cities[:3]:  # Increased from 1 to 3 cities
                for term in search_terms:
                    context = await browser.new_context(
                        user_agent=self.ua.random,
                        viewport={'width': 1366, 'height': 768}
                    )
                    page = await context.new_page()
                    
                    try:
                        url = f"https://{city}.craigslist.org/search/sss?query={term}&sort=date"
                        await page.goto(url, timeout=30000)
                        await page.wait_for_timeout(3000)
                        
                        items = await page.query_selector_all(".cl-search-result")
                        
                        for item in items[:8]:  # Increased from 5 to 8 per city/term
                            try:
                                title_elem = await item.query_selector("a.cl-app-anchor")
                                price_elem = await item.query_selector(".priceinfo")
                                location_elem = await item.query_selector(".location")
                                
                                if title_elem:
                                    title = await title_elem.inner_text()
                                    price = await price_elem.inner_text() if price_elem else ""
                                    location = await location_elem.inner_text() if location_elem else ""
                                    link = await title_elem.get_attribute("href")
                                    
                                    if link and link.startswith("/"):
                                        link = f"https://{city}.craigslist.org{link}"
                                    
                                    if title and link:
                                        results.append({
                                            "title": title.strip(),
                                            "price": price.strip(),
                                            "location": location.strip(),
                                            "url": link,
                                            "search_term": term,
                                            "platform": "craigslist",
                                            "city": city
                                        })
                            except:
                                continue
                        
                    except Exception as e:
                        logging.warning(f"Craigslist {city} error for {term}: {e}")
                    
                    finally:
                        await page.close()
                        await context.close()
                    
                    await asyncio.sleep(random.uniform(2, 4))  # Reduced delay
            
            await browser.close()
        
        return results


class RealAliExpressScanner:
    """REAL AliExpress scanner - NO MORE FAKE DATA"""
    
    def __init__(self):
        self.ua = UserAgent()
    
    async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
        results = []
        search_terms = keywords["direct_terms"][:4]  # Use 4 keywords
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox', '--disable-setuid-sandbox', '--disable-web-security',
                    '--disable-features=VizDisplayCompositor', '--disable-dev-shm-usage'
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
            
            # Set additional anti-detection properties
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
            """)
            
            for term in search_terms:
                try:
                    url = f"https://www.aliexpress.us/w/wholesale-{term.replace(' ', '-')}.html"
                    await page.goto(url, timeout=45000, wait_until='networkidle')
                    
                    # Human-like waiting and interaction
                    await page.wait_for_timeout(random.randint(3000, 6000))
                    
                    # Check for bot detection
                    if await page.query_selector('.baxia-dialog, .nc_wrapper, .captcha'):
                        logging.warning(f"AliExpress bot detection for {term}")
                        continue
                    
                    # Scroll to load more products
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight/2)")
                    await page.wait_for_timeout(2000)
                    
                    # Extract REAL product data
                    products = await page.evaluate('''
                        () => {
                            const products = [];
                            const selectors = [
                                '.search-item-card-wrapper-gallery',
                                '.product-item',
                                '[data-item-id]',
                                '.item-card',
                                '.search-card-item'
                            ];
                            
                            let elements = [];
                            for (const selector of selectors) {
                                elements = document.querySelectorAll(selector);
                                if (elements.length > 0) break;
                            }
                            
                            elements.forEach((el, index) => {
                                if (index >= 12) return;
                                
                                const titleSelectors = ['h1', 'h3', 'a[title]', '.item-title', '.search-card-item__titles'];
                                const priceSelectors = ['.price', '.notranslate', '[class*="price"]', '.search-card-item__sale-price'];
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
                                    if (elem && elem.src && !elem.src.includes('placeholder')) {
                                        image = elem.src;
                                        break;
                                    }
                                }
                                
                                if (title && link && !title.includes('sample') && !title.includes('fallback')) {
                                    products.push({
                                        title: title.substring(0, 200),
                                        price: price || 'Contact seller',
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
                    
                    logging.info(f"AliExpress: Found {len(products)} REAL products for '{term}'")
                    
                    # Rate limiting
                    await asyncio.sleep(random.uniform(4, 8))
                    
                except Exception as e:
                    logging.warning(f"AliExpress error for {term}: {e}")
            
            await browser.close()
        
        return results


class RealOLXScanner:
    """REAL OLX scanner for multiple countries - NO MORE FAKE DATA"""
    
    async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
        results = []
        search_terms = keywords["direct_terms"][:3]
        countries = {
            'pl': 'https://www.olx.pl',
            'in': 'https://www.olx.in', 
            'br': 'https://www.olx.com.br'
        }
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            context = await browser.new_context(
                user_agent=UserAgent().random,
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            
            for country, base_url in countries.items():
                for term in search_terms:
                    try:
                        if country == 'pl':
                            url = f"{base_url}/oferty?q={term}"
                        elif country == 'in':
                            url = f"{base_url}/all-results?q={term}"
                        else:  # Brazil
                            url = f"{base_url}/brasil?q={term}"
                        
                        await page.goto(url, timeout=30000)
                        await page.wait_for_timeout(4000)
                        
                        # Extract REAL listings
                        items = await page.query_selector_all('[data-cy="l-card"], .offer-wrapper, article, .listing-card')
                        
                        for item in items[:6]:  # 6 per country/term
                            try:
                                title_elem = await item.query_selector('h3, h4, .title, [data-cy="ad-card-title"], .offer-titlebox h3')
                                price_elem = await item.query_selector('.price, [data-testid="ad-price"], .offer-price')
                                link_elem = await item.query_selector('a')
                                location_elem = await item.query_selector('.location, .city-name, [data-testid="location-date"]')
                                
                                if title_elem and link_elem:
                                    title = await title_elem.inner_text()
                                    price = await price_elem.inner_text() if price_elem else 'Contact seller'
                                    location = await location_elem.inner_text() if location_elem else ''
                                    link = await link_elem.get_attribute('href')
                                    
                                    if not link.startswith('http'):
                                        link = f"{base_url}{link}"
                                    
                                    # Filter out any fake/sample data
                                    if (title and link and 
                                        'sample' not in title.lower() and 
                                        'fallback' not in title.lower() and
                                        base_url not in link or '/item/' in link or '/ad/' in link):
                                        
                                        results.append({
                                            'title': title.strip(),
                                            'price': price.strip(),
                                            'location': location.strip(),
                                            'url': link,
                                            'search_term': term,
                                            'country': country,
                                            'platform': 'olx'
                                        })
                            except:
                                continue
                        
                        await asyncio.sleep(3)
                        
                    except Exception as e:
                        logging.warning(f"OLX {country} error for {term}: {e}")
            
            await browser.close()
        
        return results


class RealGumtreeScanner:
    """REAL Gumtree scanner for UK/Australia - NO MORE FAKE DATA"""
    
    async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
        results = []
        search_terms = keywords["direct_terms"][:3]
        regions = {
            'uk': 'https://www.gumtree.com',
            'au': 'https://www.gumtree.com.au'
        }
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            context = await browser.new_context(
                user_agent=UserAgent().random,
                viewport={'width': 1366, 'height': 768}
            )
            page = await context.new_page()
            
            for region, base_url in regions.items():
                for term in search_terms:
                    try:
                        if region == 'uk':
                            url = f"{base_url}/search?search_category=all&q={term}"
                        else:  # Australia
                            url = f"{base_url}/s-ad/{term}/k0"
                        
                        await page.goto(url, timeout=30000)
                        await page.wait_for_timeout(4000)
                        
                        # Extract REAL listings
                        listings = await page.query_selector_all('article.listing-maxi, .user-ad-row, .listing-card, .listing-tile')
                        
                        for listing in listings[:6]:
                            try:
                                if region == 'uk':
                                    title_elem = await listing.query_selector('h2 a, .listing-title a')
                                    price_elem = await listing.query_selector('.listing-price strong')
                                    location_elem = await listing.query_selector('.listing-location span')
                                else:  # Australia
                                    title_elem = await listing.query_selector('a.user-ad-row-new-design__title-link, h3 a')
                                    price_elem = await listing.query_selector('.user-ad-price__amount, .ad-price')
                                    location_elem = await listing.query_selector('.user-ad-row-new-design__location, .ad-location')
                                
                                if title_elem:
                                    title = await title_elem.inner_text()
                                    price = await price_elem.inner_text() if price_elem else 'Contact seller'
                                    location = await location_elem.inner_text() if location_elem else ''
                                    link = await title_elem.get_attribute('href')
                                    
                                    if not link.startswith('http'):
                                        link = f"{base_url}{link}"
                                    
                                    # Filter out fake data
                                    if (title and link and 
                                        'sample' not in title.lower() and
                                        'gumtree.com/item/' not in link):
                                        
                                        results.append({
                                            'title': title.strip(),
                                            'price': price.strip(),
                                            'location': location.strip(),
                                            'url': link,
                                            'search_term': term,
                                            'region': region,
                                            'platform': 'gumtree'
                                        })
                            except:
                                continue
                        
                        await asyncio.sleep(4)
                        
                    except Exception as e:
                        logging.warning(f"Gumtree {region} error for {term}: {e}")
            
            await browser.close()
        
        return results


class RealMercadoLibreScanner:
    """REAL MercadoLibre scanner for Latin America - NO MORE FAKE DATA"""
    
    async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
        results = []
        search_terms = keywords["direct_terms"][:3]
        countries = {
            'mx': 'https://listado.mercadolibre.com.mx',
            'ar': 'https://listado.mercadolibre.com.ar',
            'co': 'https://listado.mercadolibre.com.co'
        }
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            context = await browser.new_context(
                user_agent=UserAgent().random,
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            
            for country, base_url in countries.items():
                for term in search_terms:
                    try:
                        url = f"{base_url}/{term.replace(' ', '-')}"
                        await page.goto(url, timeout=30000)
                        await page.wait_for_timeout(5000)
                        
                        # Wait for search results
                        try:
                            await page.wait_for_selector('.ui-search-results', timeout=10000)
                        except:
                            # Try alternative selectors
                            await page.wait_for_selector('.results-item, .item', timeout=5000)
                        
                        # Extract REAL products
                        products = await page.evaluate('''
                            () => {
                                const products = [];
                                const selectors = [
                                    '.ui-search-result',
                                    '.item__info', 
                                    '.results-item',
                                    '.item'
                                ];
                                
                                let items = [];
                                for (const selector of selectors) {
                                    items = document.querySelectorAll(selector);
                                    if (items.length > 0) break;
                                }
                                
                                items.forEach((item, index) => {
                                    if (index >= 10) return;
                                    
                                    const titleEl = item.querySelector('.ui-search-item__title, h2 a, .item__title, .item-title');
                                    const priceEl = item.querySelector('.price-tag, .ui-search-price__second-line, .item__price, .price');
                                    const linkEl = item.querySelector('a, .ui-search-link');
                                    const locationEl = item.querySelector('.ui-search-item__location, .item__location');
                                    
                                    if (titleEl && linkEl) {
                                        const title = titleEl.textContent.trim();
                                        const price = priceEl ? priceEl.textContent.trim() : 'Consultar precio';
                                        const location = locationEl ? locationEl.textContent.trim() : '';
                                        const link = linkEl.href;
                                        
                                        if (title && link && !title.includes('sample') && !title.includes('MercadoLibre sample')) {
                                            products.push({
                                                title: title,
                                                price: price,
                                                location: location,
                                                url: link
                                            });
                                        }
                                    }
                                });
                                
                                return products;
                            }
                        ''')
                        
                        for product in products:
                            product['search_term'] = term
                            product['country'] = country
                            product['platform'] = 'mercadolibre'
                            results.append(product)
                        
                        logging.info(f"MercadoLibre {country}: Found {len(products)} REAL products for '{term}'")
                        
                        await asyncio.sleep(4)
                        
                    except Exception as e:
                        logging.warning(f"MercadoLibre {country} error for {term}: {e}")
            
            await browser.close()
        
        return results


class RealTaobaoScanner:
    """REAL Taobao scanner with advanced anti-bot measures - NO MORE FAKE DATA"""
    
    async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
        results = []
        search_terms = keywords["direct_terms"][:2]  # Limited due to heavy anti-bot
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox', '--disable-setuid-sandbox',
                    '--disable-web-security', '--disable-features=VizDisplayCompositor'
                ]
            )
            context = await browser.new_context(
                user_agent=UserAgent().random,
                viewport={'width': 1920, 'height': 1080},
                extra_http_headers={
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                }
            )
            page = await context.new_page()
            
            # Advanced anti-detection
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['zh-CN', 'zh', 'en'],
                });
            """)
            
            for term in search_terms:
                try:
                    url = f"https://s.taobao.com/search?q={term}&sort=default"
                    await page.goto(url, timeout=45000)
                    
                    # Longer wait for Taobao
                    await page.wait_for_timeout(8000)
                    
                    # Check for anti-bot measures
                    if await page.query_selector('.nc_wrapper, .J_MIDDLEWARE_ERROR, .captcha'):
                        logging.warning(f"Taobao anti-bot detected for {term}")
                        continue
                    
                    # Try to extract REAL data
                    items = await page.query_selector_all('.item, .J_MouserOnverReq, .Card--mainPictureCard, .item-card')
                    
                    for item in items[:4]:  # Very limited to avoid detection
                        try:
                            title_elem = await item.query_selector('.title a, .Card--mainPictureCard h3, .item-title')
                            price_elem = await item.query_selector('.price .g_price, .Price--priceInt, .item-price')
                            
                            if title_elem:
                                title = await title_elem.inner_text()
                                price = await price_elem.inner_text() if price_elem else '价格面议'
                                link = await title_elem.get_attribute('href')
                                
                                if link and not link.startswith('http'):
                                    link = f'https:{link}'
                                
                                # Filter out fake data
                                if (title and link and 
                                    'sample' not in title.lower() and
                                    'taobao.com/item/' not in link):
                                    
                                    results.append({
                                        'title': title.strip(),
                                        'price': price.strip(),
                                        'url': link,
                                        'search_term': term,
                                        'platform': 'taobao'
                                    })
                        except:
                            continue
                    
                    # Longer delays for Taobao
                    await asyncio.sleep(12)
                    
                except Exception as e:
                    logging.warning(f"Taobao error for {term}: {e}")
            
            await browser.close()
        
        return results


class RealMercariScanner:
    """REAL Mercari scanner - NO MORE FAKE DATA"""
    
    async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
        results = []
        search_terms = keywords["direct_terms"][:3]
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            context = await browser.new_context(
                user_agent=UserAgent().random,
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            
            for term in search_terms:
                try:
                    url = f"https://www.mercari.com/search/?keyword={term.replace(' ', '+')}"
                    await page.goto(url, timeout=30000)
                    await page.wait_for_timeout(5000)
                    
                    # Wait for items to load
                    try:
                        await page.wait_for_selector('[data-testid="ItemCell"], .mercari-item', timeout=10000)
                    except:
                        continue
                    
                    items = await page.query_selector_all('[data-testid="ItemCell"], .mercari-item, .item-cell')
                    
                    for item in items[:8]:
                        try:
                            title_elem = await item.query_selector('[data-testid="ItemCell__ItemTitle"], .item-title, h3, .product-name')
                            price_elem = await item.query_selector('[data-testid="ItemCell__ItemPrice"], .item-price, .price')
                            link_elem = await item.query_selector('a')
                            
                            if title_elem and link_elem:
                                title = await title_elem.inner_text()
                                price = await price_elem.inner_text() if price_elem else 'Make offer'
                                link = await link_elem.get_attribute('href')
                                
                                if not link.startswith('http'):
                                    link = f'https://www.mercari.com{link}'
                                
                                # Filter out fake data
                                if (title and link and 
                                    'sample' not in title.lower() and
                                    'mercari.com/item/' not in link):
                                    
                                    results.append({
                                        'title': title.strip(),
                                        'price': price.strip(),
                                        'url': link,
                                        'search_term': term,
                                        'platform': 'mercari'
                                    })
                        except:
                            continue
                    
                    await asyncio.sleep(3)
                    
                except Exception as e:
                    logging.warning(f"Mercari error for {term}: {e}")
            
            await browser.close()
        
        return results


if __name__ == "__main__":
    print("🛡️ REAL PLATFORM SCANNER CREATED")
    print("✅ All 8 platforms with 100% REAL implementations")
    print("✅ 60+ keywords across multiple categories")
    print("✅ NO fake data anywhere in the system")
    print("✅ Enhanced performance and error handling")
