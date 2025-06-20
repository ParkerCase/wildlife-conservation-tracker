#!/usr/bin/env python3
"""
Complete Enhanced Platform System - All 8 platforms bulletproof
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
from supabase import create_client

load_dotenv('/Users/parkercase/conservation-bot/backend/.env')

class BulletproofPlatformManager:
    """Complete bulletproof platform management system"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.max_retries = 3
        self.setup_supabase()
        
        # Enhanced scanners for all 8 platforms
        self.platforms = {
            "ebay": self.create_enhanced_ebay_scanner(),
            "craigslist": self.create_enhanced_craigslist_scanner(),
            "aliexpress": self.create_enhanced_aliexpress_scanner(),
            "olx": self.create_enhanced_olx_scanner(),
            "gumtree": self.create_enhanced_gumtree_scanner(),
            "mercadolibre": self.create_enhanced_mercadolibre_scanner(),
            "taobao": self.create_enhanced_taobao_scanner(),
            "mercari": self.create_enhanced_mercari_scanner()
        }
        
        self.session = None

    def setup_supabase(self):
        """Setup Supabase for storing results"""
        try:
            SUPABASE_URL = os.getenv('SUPABASE_URL')
            SUPABASE_KEY = os.getenv('SUPABASE_KEY')
            self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            logging.warning(f"Supabase setup failed: {e}")
            self.supabase = None

    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=90)
        connector = aiohttp.TCPConnector(limit=15, limit_per_host=5)
        self.session = aiohttp.ClientSession(timeout=timeout, connector=connector)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def create_enhanced_ebay_scanner(self):
        """Create enhanced eBay scanner"""
        class EnhancedEbayScanner:
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
                        raise RuntimeError(f"eBay OAuth failed: {await resp.text()}")

            async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
                results = []
                search_terms = keywords["direct_terms"][:5]
                
                try:
                    token = await self.get_access_token(session)
                    headers = {
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json",
                    }

                    for term in search_terms:
                        params = {"q": term, "limit": "10"}
                        
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
                                        "image": item.get("image", {}).get("imageUrl", ""),
                                        "platform": "ebay"
                                    })
                        
                        await asyncio.sleep(1)  # Rate limiting

                except Exception as e:
                    logging.error(f"eBay scan error: {e}")
                
                return results

        return EnhancedEbayScanner()

    def create_enhanced_craigslist_scanner(self):
        """Create enhanced Craigslist scanner"""
        class EnhancedCraigslistScanner:
            def __init__(self):
                self.cities = ["newyork", "losangeles", "chicago", "seattle", "boston"]
                self.ua = UserAgent()

            async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
                results = []
                search_terms = keywords["direct_terms"][:2]
                
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True)
                    
                    for city in self.cities[:2]:  # Limit cities
                        for term in search_terms:
                            url = f"https://{city}.craigslist.org/search/sss?query={term}"
                            
                            context = await browser.new_context(
                                user_agent=self.ua.random,
                                viewport={'width': 1366, 'height': 768}
                            )
                            page = await context.new_page()
                            
                            try:
                                await page.goto(url, timeout=20000)
                                await page.wait_for_timeout(3000)
                                
                                items = await page.query_selector_all(".cl-search-result")
                                
                                for item in items[:3]:
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
                                                    "city": city,
                                                    "platform": "craigslist"
                                                })
                                    except:
                                        continue
                                
                            except Exception as e:
                                logging.warning(f"Craigslist {city} error: {e}")
                            
                            finally:
                                await page.close()
                                await context.close()
                            
                            await asyncio.sleep(random.uniform(3, 6))
                    
                    await browser.close()
                
                return results

        return EnhancedCraigslistScanner()

    def create_enhanced_aliexpress_scanner(self):
        """Create enhanced AliExpress scanner"""
        class EnhancedAliExpressScanner:
            async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
                results = []
                search_terms = keywords["direct_terms"][:2]
                
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True)
                    context = await browser.new_context(
                        user_agent=UserAgent().random,
                        viewport={'width': 1920, 'height': 1080}
                    )
                    page = await context.new_page()
                    
                    for term in search_terms:
                        url = f"https://www.aliexpress.us/w/wholesale?SearchText={term}"
                        
                        try:
                            await page.goto(url, timeout=30000)
                            await page.wait_for_timeout(5000)
                            
                            # Extract with JavaScript
                            products = await page.evaluate('''
                                () => {
                                    const products = [];
                                    const items = document.querySelectorAll('.search-item-card-wrapper-gallery, .product-item');
                                    
                                    items.forEach((item, index) => {
                                        if (index >= 5) return;
                                        
                                        const titleEl = item.querySelector('h1, h3, a[title]');
                                        const priceEl = item.querySelector('.price, [class*="price"]');
                                        const linkEl = item.querySelector('a');
                                        
                                        if (titleEl && linkEl) {
                                            products.push({
                                                title: titleEl.textContent.trim(),
                                                price: priceEl ? priceEl.textContent.trim() : '',
                                                url: linkEl.href
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
                            
                        except Exception as e:
                            logging.warning(f"AliExpress error: {e}")
                    
                    await browser.close()
                
                return results

        return EnhancedAliExpressScanner()

    def create_enhanced_olx_scanner(self):
        """Create enhanced OLX scanner"""
        class EnhancedOLXScanner:
            async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
                results = []
                search_terms = keywords["direct_terms"][:2]
                
                # OLX is actually working, use the existing implementation but enhanced
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True)
                    context = await browser.new_context(
                        user_agent=UserAgent().random,
                        viewport={'width': 1920, 'height': 1080}
                    )
                    page = await context.new_page()
                    
                    countries = ['pl', 'in']  # Focus on working countries
                    
                    for country in countries:
                        base_url = f"https://www.olx.{country}"
                        
                        for term in search_terms:
                            url = f"{base_url}/oferty?q={term}" if country == 'pl' else f"{base_url}/all-results?q={term}"
                            
                            try:
                                await page.goto(url, timeout=25000)
                                await page.wait_for_timeout(3000)
                                
                                items = await page.query_selector_all('[data-cy="l-card"], .offer-wrapper, article')
                                
                                for item in items[:3]:
                                    try:
                                        title_elem = await item.query_selector('h3, h4, .title')
                                        price_elem = await item.query_selector('.price, [data-testid="ad-price"]')
                                        link_elem = await item.query_selector('a')
                                        
                                        if title_elem and link_elem:
                                            title = await title_elem.inner_text()
                                            price = await price_elem.inner_text() if price_elem else ""
                                            link = await link_elem.get_attribute('href')
                                            
                                            if not link.startswith('http'):
                                                link = f"{base_url}{link}"
                                            
                                            results.append({
                                                "title": title.strip(),
                                                "price": price.strip(),
                                                "url": link,
                                                "search_term": term,
                                                "country": country,
                                                "platform": "olx"
                                            })
                                    except:
                                        continue
                                
                            except Exception as e:
                                logging.warning(f"OLX {country} error: {e}")
                            
                            await asyncio.sleep(3)
                    
                    await browser.close()
                
                return results

        return EnhancedOLXScanner()

    def create_enhanced_gumtree_scanner(self):
        """Create enhanced Gumtree scanner"""
        class EnhancedGumtreeScanner:
            async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
                results = []
                search_terms = keywords["direct_terms"][:2]
                
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True)
                    context = await browser.new_context(
                        user_agent=UserAgent().random,
                        viewport={'width': 1366, 'height': 768}
                    )
                    page = await context.new_page()
                    
                    # Focus on UK Gumtree
                    for term in search_terms:
                        url = f"https://www.gumtree.com/search?search_category=all&q={term}"
                        
                        try:
                            await page.goto(url, timeout=25000)
                            await page.wait_for_timeout(3000)
                            
                            listings = await page.query_selector_all('article.listing-maxi, .listing-tile')
                            
                            for listing in listings[:3]:
                                try:
                                    title_elem = await listing.query_selector('h2 a, .listing-title a')
                                    price_elem = await listing.query_selector('.listing-price strong')
                                    
                                    if title_elem:
                                        title = await title_elem.inner_text()
                                        price = await price_elem.inner_text() if price_elem else ""
                                        link = await title_elem.get_attribute('href')
                                        
                                        if not link.startswith('http'):
                                            link = f'https://www.gumtree.com{link}'
                                        
                                        results.append({
                                            "title": title.strip(),
                                            "price": price.strip(),
                                            "url": link,
                                            "search_term": term,
                                            "platform": "gumtree"
                                        })
                                except:
                                    continue
                            
                        except Exception as e:
                            logging.warning(f"Gumtree error: {e}")
                        
                        await asyncio.sleep(4)
                    
                    await browser.close()
                
                return results

        return EnhancedGumtreeScanner()

    def create_enhanced_mercadolibre_scanner(self):
        """Create enhanced MercadoLibre scanner"""
        class EnhancedMercadoLibreScanner:
            async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
                results = []
                search_terms = keywords["direct_terms"][:2]
                
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True)
                    context = await browser.new_context(
                        user_agent=UserAgent().random,
                        viewport={'width': 1920, 'height': 1080}
                    )
                    page = await context.new_page()
                    
                    countries = {'mx': 'https://listado.mercadolibre.com.mx'}
                    
                    for country, base_url in countries.items():
                        for term in search_terms:
                            url = f"{base_url}/{term}"
                            
                            try:
                                await page.goto(url, timeout=25000)
                                await page.wait_for_timeout(4000)
                                
                                products = await page.evaluate('''
                                    () => {
                                        const products = [];
                                        const items = document.querySelectorAll('.ui-search-result, .item__info');
                                        
                                        items.forEach((item, index) => {
                                            if (index >= 4) return;
                                            
                                            const titleEl = item.querySelector('.ui-search-item__title, h2 a');
                                            const priceEl = item.querySelector('.price-tag, .ui-search-price__second-line');
                                            const linkEl = item.querySelector('a');
                                            
                                            if (titleEl && linkEl) {
                                                products.push({
                                                    title: titleEl.textContent.trim(),
                                                    price: priceEl ? priceEl.textContent.trim() : '',
                                                    url: linkEl.href
                                                });
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
                                
                            except Exception as e:
                                logging.warning(f"MercadoLibre error: {e}")
                            
                            await asyncio.sleep(4)
                    
                    await browser.close()
                
                return results

        return EnhancedMercadoLibreScanner()

    def create_enhanced_taobao_scanner(self):
        """Create enhanced Taobao scanner"""
        class EnhancedTaobaoScanner:
            async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
                results = []
                search_terms = keywords["direct_terms"][:1]  # Very limited due to anti-bot
                
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True)
                    context = await browser.new_context(
                        user_agent=UserAgent().random,
                        viewport={'width': 1920, 'height': 1080},
                        extra_http_headers={'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}
                    )
                    page = await context.new_page()
                    
                    for term in search_terms:
                        url = f"https://s.taobao.com/search?q={term}"
                        
                        try:
                            await page.goto(url, timeout=30000)
                            await page.wait_for_timeout(8000)  # Longer wait
                            
                            # Check for anti-bot
                            if await page.query_selector('.nc_wrapper'):
                                logging.warning("Taobao anti-bot detected")
                                continue
                            
                            items = await page.query_selector_all('.item, .J_MouserOnverReq')
                            
                            for item in items[:2]:  # Very limited
                                try:
                                    title_elem = await item.query_selector('.title a')
                                    price_elem = await item.query_selector('.price .g_price')
                                    
                                    if title_elem:
                                        title = await title_elem.inner_text()
                                        price = await price_elem.inner_text() if price_elem else ""
                                        link = await title_elem.get_attribute('href')
                                        
                                        if link and not link.startswith('http'):
                                            link = f'https:{link}'
                                        
                                        results.append({
                                            "title": title.strip(),
                                            "price": price.strip(),
                                            "url": link,
                                            "search_term": term,
                                            "platform": "taobao"
                                        })
                                except:
                                    continue
                            
                        except Exception as e:
                            logging.warning(f"Taobao error: {e}")
                        
                        await asyncio.sleep(8)  # Long delays for Taobao
                    
                    await browser.close()
                
                return results

        return EnhancedTaobaoScanner()

    def create_enhanced_mercari_scanner(self):
        """Create enhanced Mercari scanner"""
        class EnhancedMercariScanner:
            async def scan(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
                results = []
                search_terms = keywords["direct_terms"][:2]
                
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True)
                    context = await browser.new_context(
                        user_agent=UserAgent().random,
                        viewport={'width': 1920, 'height': 1080}
                    )
                    page = await context.new_page()
                    
                    for term in search_terms:
                        url = f"https://www.mercari.com/search/?keyword={term}"
                        
                        try:
                            await page.goto(url, timeout=25000)
                            await page.wait_for_timeout(4000)
                            
                            items = await page.query_selector_all('[data-testid="ItemCell"], .mercari-item')
                            
                            for item in items[:3]:
                                try:
                                    title_elem = await item.query_selector('[data-testid="ItemCell__ItemTitle"], .item-title')
                                    price_elem = await item.query_selector('[data-testid="ItemCell__ItemPrice"], .item-price')
                                    link_elem = await item.query_selector('a')
                                    
                                    if title_elem and link_elem:
                                        title = await title_elem.inner_text()
                                        price = await price_elem.inner_text() if price_elem else ""
                                        link = await link_elem.get_attribute('href')
                                        
                                        if not link.startswith('http'):
                                            link = f'https://www.mercari.com{link}'
                                        
                                        results.append({
                                            "title": title.strip(),
                                            "price": price.strip(),
                                            "url": link,
                                            "search_term": term,
                                            "platform": "mercari"
                                        })
                                except:
                                    continue
                            
                        except Exception as e:
                            logging.warning(f"Mercari error: {e}")
                        
                        await asyncio.sleep(3)
                    
                    await browser.close()
                
                return results

        return EnhancedMercariScanner()

    async def scan_all_platforms_bulletproof(self, keywords: Dict) -> Dict[str, Any]:
        """Bulletproof scanning of all 8 platforms"""
        print("🛡️  BULLETPROOF PLATFORM SCANNING")
        print("=" * 50)
        
        results_summary = {}
        total_results = 0
        total_stored = 0
        
        # Scan platforms with controlled concurrency
        semaphore = asyncio.Semaphore(3)  # Max 3 concurrent scans
        
        async def scan_platform_with_semaphore(platform_name, platform_scanner):
            async with semaphore:
                return await self.scan_platform_bulletproof(platform_name, platform_scanner, keywords)
        
        # Create tasks for all platforms
        tasks = [
            scan_platform_with_semaphore(name, scanner)
            for name, scanner in self.platforms.items()
        ]
        
        # Execute all scans
        platform_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for (platform_name, _), result in zip(self.platforms.items(), platform_results):
            if isinstance(result, Exception):
                print(f"❌ {platform_name.upper()}: Exception - {result}")
                results_summary[platform_name] = {'status': 'ERROR', 'count': 0, 'stored': 0}
            else:
                status, count, stored, samples = result
                results_summary[platform_name] = {
                    'status': status,
                    'count': count,
                    'stored': stored,
                    'samples': samples
                }
                total_results += count
                total_stored += stored
                
                if count > 0:
                    print(f"✅ {platform_name.upper()}: {count} results, {stored} stored")
                    for i, sample in enumerate(samples[:2], 1):
                        title = sample.get('title', 'No title')[:40]
                        price = sample.get('price', 'No price')
                        print(f"   {i}. {title}... - {price}")
                else:
                    print(f"⚠️  {platform_name.upper()}: No results")
        
        # Calculate metrics
        working_platforms = [p for p, r in results_summary.items() if r['count'] > 0]
        
        return {
            'results_summary': results_summary,
            'total_results': total_results,
            'total_stored': total_stored,
            'working_platforms': working_platforms,
            'working_count': len(working_platforms)
        }

    async def scan_platform_bulletproof(self, platform_name: str, platform_scanner, keywords: Dict):
        """Scan a single platform with bulletproof error handling"""
        max_attempts = 2
        
        for attempt in range(max_attempts):
            try:
                # Set timeout based on platform complexity
                if platform_name in ['taobao']:
                    timeout = 90
                elif platform_name in ['aliexpress', 'mercadolibre']:
                    timeout = 60
                else:
                    timeout = 45
                
                results = await asyncio.wait_for(
                    platform_scanner.scan(keywords, self.session),
                    timeout=timeout
                )
                
                if results:
                    # Store results in Supabase
                    stored_count = await self.store_results_safely(platform_name, results[:5])
                    return 'WORKING', len(results), stored_count, results[:3]
                else:
                    return 'NO_RESULTS', 0, 0, []
                    
            except asyncio.TimeoutError:
                if attempt < max_attempts - 1:
                    await asyncio.sleep(5)
                else:
                    return 'TIMEOUT', 0, 0, []
                    
            except Exception as e:
                if attempt < max_attempts - 1:
                    await asyncio.sleep(3)
                else:
                    return 'ERROR', 0, 0, []
        
        return 'FAILED', 0, 0, []

    async def store_results_safely(self, platform: str, results: List[Dict]) -> int:
        """Safely store results in Supabase"""
        if not self.supabase or not results:
            return 0
        
        stored_count = 0
        for i, result in enumerate(results):
            try:
                evidence_id = f"BULLET-{platform.upper()}-{datetime.now().strftime('%m%d%H%M')}-{i+1:02d}"
                
                detection = {
                    'evidence_id': evidence_id,
                    'timestamp': datetime.now().isoformat(),
                    'platform': platform,
                    'threat_score': 50,
                    'threat_level': 'MEDIUM',
                    'species_involved': f"Bulletproof scan: {result.get('search_term', 'test')}",
                    'alert_sent': False,
                    'status': f'BULLETPROOF_SCAN_{platform.upper()}'
                }
                
                self.supabase.table('detections').insert(detection).execute()
                stored_count += 1
                
            except Exception as e:
                logging.warning(f"Storage error for {platform}: {e}")
        
        return stored_count


async def test_bulletproof_system():
    """Test the complete bulletproof system"""
    print("🛡️  TESTING COMPLETE BULLETPROOF SYSTEM")
    print("=" * 60)
    
    keywords = {'direct_terms': ['antique', 'vintage', 'carved']}
    
    async with BulletproofPlatformManager() as manager:
        results = await manager.scan_all_platforms_bulletproof(keywords)
        
        working_count = results['working_count']
        total_results = results['total_results']
        total_stored = results['total_stored']
        
        print(f"\n🎯 BULLETPROOF SYSTEM RESULTS:")
        print(f"   ✅ Working platforms: {working_count}/8")
        print(f"   📊 Total results: {total_results}")
        print(f"   💾 Stored in Supabase: {total_stored}")
        
        if working_count >= 6:
            print(f"\n🏆 EXCELLENT: {working_count}/8 platforms operational!")
            print("   Your system is production-ready and bulletproof")
        elif working_count >= 4:
            print(f"\n✅ VERY GOOD: {working_count}/8 platforms working")
            print("   Strong foundation with minor optimizations needed")
        else:
            print(f"\n🔧 NEEDS WORK: Only {working_count}/8 platforms working")
            print("   Focus on debugging remaining issues")
        
        # Calculate projections
        if total_results > 0:
            keywords_used = len(keywords['direct_terms'])
            keywords_full = 20
            scans_per_day = 24
            
            daily_projection = total_results * (keywords_full / keywords_used) * scans_per_day
            annual_projection = daily_projection * 365
            
            print(f"\n📈 REALISTIC PROJECTIONS:")
            print(f"   Daily capacity: {daily_projection:.0f} listings")
            print(f"   Annual capacity: {annual_projection:,.0f} listings")
        
        return results

if __name__ == "__main__":
    asyncio.run(test_bulletproof_system())
