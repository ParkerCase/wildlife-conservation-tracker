#!/usr/bin/env python3
"""
WildGuard AI - AliExpress Real Data Scanner
Production-ready AliExpress scraper for wildlife trafficking detection
"""

import asyncio
import aiohttp
import json
import re
import logging
from typing import Dict, List
from urllib.parse import quote, urlencode
from datetime import datetime
import random
from fake_useragent import UserAgent
import time

class AliExpressScanner:
    """
    Real AliExpress scanner that works with actual data
    """
    
    def __init__(self):
        self.ua = UserAgent()
        self.session = None
        self.base_url = "https://www.aliexpress.com"
        self.search_url = "https://www.aliexpress.com/af/search"
        
        # Rate limiting
        self.last_request_time = 0
        self.min_delay = 2.0  # Minimum 2 seconds between requests
        
        # Headers to appear legitimate
        self.base_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5,zh-CN;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        
        # Chinese translations for wildlife terms
        self.chinese_wildlife_terms = {
            'ivory': ['象牙', '象牙制品', '象牙雕刻', '象牙手镯', '象牙饰品'],
            'tiger': ['虎骨', '虎皮', '虎牙', '虎爪', '老虎'],
            'rhino': ['犀牛角', '犀角', '犀牛角粉', '犀角粉'],
            'pangolin': ['穿山甲', '穿山甲鳞片', '穿山甲甲片'],
            'bear': ['熊胆', '熊胆粉', '熊掌', '黑熊胆'],
            'leopard': ['豹皮', '豹骨', '花豹', '金钱豹'],
            'turtle': ['龟板', '龟甲', '海龟壳', '玳瑁'],
            'coral': ['红珊瑚', '珊瑚', '珊瑚饰品', '血珊瑚'],
            'medicine': ['中药材', '传统药材', '名贵药材', '野生药材'],
            'traditional': ['传统工艺', '手工制作', '古法制作', '祖传秘方']
        }
        
    async def __aenter__(self):
        """Async context manager entry"""
        timeout = aiohttp.ClientTimeout(total=30)
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
        
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers={'User-Agent': self.ua.random}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def _rate_limit(self):
        """Enforce rate limiting to avoid being blocked"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_delay:
            sleep_time = self.min_delay - time_since_last
            await asyncio.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _get_search_headers(self):
        """Get headers for search requests"""
        headers = self.base_headers.copy()
        headers['User-Agent'] = self.ua.random
        headers['Referer'] = 'https://www.aliexpress.com/'
        return headers
    
    async def search_wildlife_terms(self, keywords: List[str]) -> List[Dict]:
        """
        Search AliExpress for wildlife-related terms
        """
        results = []
        
        # Combine English and Chinese terms
        search_terms = keywords.copy()
        
        # Add Chinese translations for common wildlife terms
        for keyword in keywords[:5]:  # Limit to avoid too many requests
            for eng_term, chinese_terms in self.chinese_wildlife_terms.items():
                if eng_term in keyword.lower():
                    search_terms.extend(chinese_terms[:2])  # Add top 2 Chinese terms
        
        for term in search_terms[:15]:  # Limit total searches
            try:
                await self._rate_limit()
                search_results = await self._search_single_term(term)
                results.extend(search_results)
                
                # Random delay between searches
                await asyncio.sleep(random.uniform(1.5, 3.0))
                
            except Exception as e:
                logging.warning(f"AliExpress search error for '{term}': {e}")
                continue
        
        return results
    
    async def _search_single_term(self, search_term: str) -> List[Dict]:
        """Search for a single term on AliExpress"""
        
        # URL encode the search term
        encoded_term = quote(search_term.strip())
        
        # Build search URL
        params = {
            'SearchText': search_term,
            'catId': '0',
            'initiative_id': 'SB_20220101',
            'page': '1'
        }
        
        search_url = f"https://www.aliexpress.com/wholesale"
        
        headers = self._get_search_headers()
        
        try:
            async with self.session.get(
                search_url,
                params=params,
                headers=headers,
                allow_redirects=True
            ) as response:
                
                if response.status != 200:
                    logging.warning(f"AliExpress returned status {response.status} for term: {search_term}")
                    return []
                
                html_content = await response.text()
                
                # Parse the HTML for product listings
                products = self._parse_search_results(html_content, search_term)
                
                logging.info(f"AliExpress found {len(products)} products for '{search_term}'")
                return products
                
        except Exception as e:
            logging.error(f"Error searching AliExpress for '{search_term}': {e}")
            return []
    
    def _parse_search_results(self, html_content: str, search_term: str) -> List[Dict]:
        """Parse HTML search results from AliExpress"""
        
        products = []
        
        try:
            # Look for JSON data in the HTML (AliExpress embeds data)
            json_pattern = r'window\.runParams\s*=\s*(\{.*?\});'
            json_match = re.search(json_pattern, html_content, re.DOTALL)
            
            if json_match:
                try:
                    data = json.loads(json_match.group(1))
                    # Extract product data from the JSON structure
                    products.extend(self._extract_products_from_json(data, search_term))
                except json.JSONDecodeError:
                    pass
            
            # Fallback: Parse HTML directly for product listings
            if not products:
                products = self._parse_html_products(html_content, search_term)
            
        except Exception as e:
            logging.warning(f"Error parsing AliExpress results: {e}")
        
        return products[:20]  # Limit to top 20 results
    
    def _extract_products_from_json(self, data: Dict, search_term: str) -> List[Dict]:
        """Extract product data from embedded JSON"""
        products = []
        
        try:
            # AliExpress structure may vary, look for common patterns
            if 'mods' in data:
                for mod in data.get('mods', {}).values():
                    if isinstance(mod, dict) and 'resultList' in mod:
                        for item in mod['resultList']:
                            product = self._format_product_data(item, search_term, 'json')
                            if product:
                                products.append(product)
            
            # Alternative structure
            if 'data' in data and 'itemList' in data.get('data', {}):
                for item in data['data']['itemList']:
                    product = self._format_product_data(item, search_term, 'json')
                    if product:
                        products.append(product)
                        
        except Exception as e:
            logging.debug(f"JSON extraction error: {e}")
        
        return products
    
    def _parse_html_products(self, html_content: str, search_term: str) -> List[Dict]:
        """Parse products directly from HTML"""
        products = []
        
        try:
            # Look for product containers in HTML
            # AliExpress uses various selectors, try multiple patterns
            patterns = [
                r'<div[^>]*class="[^"]*item[^"]*"[^>]*>.*?</div>',
                r'<div[^>]*data-spm-anchor-id[^>]*>.*?</div>',
                r'<a[^>]*href="[^"]*item[^"]*\.html[^"]*"[^>]*>.*?</a>'
            ]
            
            for pattern in patterns:
                matches = re.finditer(pattern, html_content, re.DOTALL | re.IGNORECASE)
                
                for match in list(matches)[:10]:  # Limit matches to avoid too much processing
                    product_html = match.group(0)
                    product = self._extract_product_from_html(product_html, search_term)
                    if product:
                        products.append(product)
                
                if products:  # If we found products with this pattern, stop trying others
                    break
            
        except Exception as e:
            logging.debug(f"HTML parsing error: {e}")
        
        return products
    
    def _extract_product_from_html(self, product_html: str, search_term: str) -> Dict:
        """Extract product data from HTML snippet"""
        
        try:
            # Extract title
            title_patterns = [
                r'title="([^"]+)"',
                r'alt="([^"]+)"',
                r'<h[1-6][^>]*>([^<]+)</h[1-6]>',
                r'class="[^"]*title[^"]*"[^>]*>([^<]+)<'
            ]
            
            title = ""
            for pattern in title_patterns:
                title_match = re.search(pattern, product_html, re.IGNORECASE)
                if title_match:
                    title = title_match.group(1).strip()
                    break
            
            # Extract price
            price_patterns = [
                r'US \$([0-9.,]+)',
                r'\$([0-9.,]+)',
                r'price[^>]*>.*?\$([0-9.,]+)',
                r'(\d+\.\d+)'
            ]
            
            price = ""
            for pattern in price_patterns:
                price_match = re.search(pattern, product_html, re.IGNORECASE)
                if price_match:
                    price = f"${price_match.group(1)}"
                    break
            
            # Extract URL
            url_patterns = [
                r'href="([^"]*item[^"]*\.html[^"]*)"',
                r'href="([^"]*aliexpress\.com[^"]*)"'
            ]
            
            url = ""
            for pattern in url_patterns:
                url_match = re.search(pattern, product_html, re.IGNORECASE)
                if url_match:
                    url = url_match.group(1)
                    if not url.startswith('http'):
                        url = f"https:{url}" if url.startswith('//') else f"https://www.aliexpress.com{url}"
                    break
            
            # Only return if we have at least title and URL
            if title and url:
                return {
                    'title': title,
                    'price': price,
                    'url': url,
                    'platform': 'aliexpress',
                    'search_term': search_term,
                    'scan_time': datetime.now().isoformat(),
                    'item_id': self._extract_item_id(url)
                }
            
        except Exception as e:
            logging.debug(f"Product extraction error: {e}")
        
        return None
    
    def _format_product_data(self, item: Dict, search_term: str, source: str) -> Dict:
        """Format product data from JSON structure"""
        
        try:
            # Try different possible field names for title
            title = (
                item.get('title') or 
                item.get('productTitle') or 
                item.get('subject') or 
                item.get('name') or 
                ""
            )
            
            # Try different possible field names for price
            price_data = (
                item.get('price') or 
                item.get('salePrice') or 
                item.get('minPrice') or 
                {}
            )
            
            if isinstance(price_data, dict):
                price = f"${price_data.get('value', price_data.get('min', ''))}"
            else:
                price = str(price_data) if price_data else ""
            
            # Try different possible field names for URL
            url = (
                item.get('productDetailUrl') or
                item.get('itemUrl') or
                item.get('url') or
                item.get('link') or
                ""
            )
            
            # Clean up URL
            if url and not url.startswith('http'):
                if url.startswith('//'):
                    url = f"https:{url}"
                else:
                    url = f"https://www.aliexpress.com{url}"
            
            # Item ID
            item_id = (
                item.get('productId') or
                item.get('itemId') or
                self._extract_item_id(url)
            )
            
            if title and url:
                return {
                    'title': title,
                    'price': price,
                    'url': url,
                    'platform': 'aliexpress',
                    'search_term': search_term,
                    'scan_time': datetime.now().isoformat(),
                    'item_id': str(item_id),
                    'source': source
                }
            
        except Exception as e:
            logging.debug(f"Product formatting error: {e}")
        
        return None
    
    def _extract_item_id(self, url: str) -> str:
        """Extract item ID from AliExpress URL"""
        
        try:
            # AliExpress URLs typically contain item IDs
            patterns = [
                r'item/([0-9]+)\.html',
                r'i/([0-9]+)\.html',
                r'productId=([0-9]+)',
                r'/([0-9]+)\.html'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(1)
            
            # Fallback: use hash of URL
            return str(abs(hash(url)) % 1000000)
            
        except:
            return str(random.randint(100000, 999999))


async def test_aliexpress_scanner():
    """Test the AliExpress scanner with real searches"""
    
    print("🛒 TESTING ALIEXPRESS REAL DATA SCANNER")
    print("=" * 80)
    
    test_keywords = [
        'ivory carving', 'elephant ivory', 'traditional medicine',
        'tiger bone', 'rhino horn', 'coral jewelry',
        'antique carving', 'natural remedy'
    ]
    
    async with AliExpressScanner() as scanner:
        print(f"🔍 Searching AliExpress for {len(test_keywords)} terms...")
        
        results = await scanner.search_wildlife_terms(test_keywords)
        
        print(f"\n📊 ALIEXPRESS SCAN RESULTS:")
        print(f"   Total Results Found: {len(results)}")
        
        if results:
            print(f"\n🎯 SAMPLE RESULTS:")
            for i, result in enumerate(results[:5], 1):
                print(f"   {i}. {result['title'][:60]}...")
                print(f"      Price: {result['price']}")
                print(f"      Search Term: {result['search_term']}")
                print(f"      URL: {result['url'][:80]}...")
                print()
            
            print(f"✅ SUCCESS: AliExpress scanner returned {len(results)} real listings")
            return results
        else:
            print(f"❌ No results found - may need to adjust parsing logic")
            return []


if __name__ == "__main__":
    # Test the scanner
    results = asyncio.run(test_aliexpress_scanner())
    
    if results:
        print(f"\n🎉 ALIEXPRESS INTEGRATION: WORKING")
        print(f"   Real data returned: {len(results)} listings")
        print(f"   Ready for integration with main scanner")
    else:
        print(f"\n🔧 ALIEXPRESS INTEGRATION: NEEDS ADJUSTMENT")
        print(f"   Check parsing logic or anti-bot measures")
