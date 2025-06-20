#!/usr/bin/env python3
"""
Test the platform fixes
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging
from typing import List, Dict
from playwright.async_api import async_playwright
from fake_useragent import UserAgent
import random
import json
import re

class FixedAliExpressScanner:
    """Fixed AliExpress implementation using multiple strategies"""
    
    async def scan_production(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
        results = []
        search_terms = keywords["direct_terms"][:3]  # Conservative approach
        
        # Strategy 1: Use the mobile API endpoint
        try:
            for term in search_terms:
                # Mobile AliExpress API is less protected
                mobile_url = f"https://m.aliexpress.com/search.htm?keywords={term}"
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                }
                
                async with session.get(mobile_url, headers=headers) as resp:
                    if resp.status == 200:
                        html = await resp.text()
                        
                        # Look for JSON data in script tags
                        if 'window.runParams' in html:
                            # Extract product data from JavaScript
                            json_match = re.search(r'window\.runParams\s*=\s*({.+?});', html)
                            if json_match:
                                try:
                                    data = json.loads(json_match.group(1))
                                    if 'mods' in data and 'itemList' in data['mods']:
                                        items = data['mods']['itemList']['content']
                                        
                                        for item in items[:12]:
                                            try:
                                                title = item.get('title', {}).get('displayTitle', '')
                                                price = item.get('prices', {}).get('salePrice', {}).get('formattedPrice', '')
                                                item_id = item.get('productId', '')
                                                
                                                if title and item_id:
                                                    url = f"https://www.aliexpress.com/item/{item_id}.html"
                                                    results.append({
                                                        "title": title,
                                                        "price": price,
                                                        "url": url,
                                                        "search_term": term,
                                                        "platform": "aliexpress"
                                                    })
                                            except:
                                                continue
                                except:
                                    pass
                        
                        # Fallback: Parse HTML directly
                        soup = BeautifulSoup(html, 'html.parser')
                        items = soup.find_all('div', class_=re.compile(r'item|product'))
                        
                        for item in items[:8]:
                            try:
                                title_elem = item.find(['h1', 'h2', 'h3', 'span'], string=re.compile(r'.{5,}'))
                                price_elem = item.find(string=re.compile(r'\$[\d.,]+'))
                                link_elem = item.find('a', href=True)
                                
                                if title_elem and link_elem:
                                    title = title_elem.get_text(strip=True) if hasattr(title_elem, 'get_text') else str(title_elem).strip()
                                    price = str(price_elem).strip() if price_elem else ""
                                    link = link_elem.get('href')
                                    
                                    if not link.startswith('http'):
                                        link = f"https://www.aliexpress.com{link}"
                                    
                                    if len(title) > 5:
                                        results.append({
                                            "title": title,
                                            "price": price,
                                            "url": link,
                                            "search_term": term,
                                            "platform": "aliexpress"
                                        })
                            except:
                                continue
                
                await asyncio.sleep(4)  # Longer delay for AliExpress
        
        except Exception as e:
            logging.warning(f"AliExpress error: {e}")
        
        return results


class FixedMercariScanner:
    """Fixed Mercari implementation"""
    
    async def scan_production(self, keywords: Dict, session: aiohttp.ClientSession) -> List[Dict]:
        results = []
        search_terms = keywords["direct_terms"][:3]  # Conservative
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            
            for term in search_terms:
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    viewport={'width': 1920, 'height': 1080}
                )
                page = await context.new_page()
                
                try:
                    url = f"https://www.mercari.com/search/?keyword={term.replace(' ', '%20')}"
                    
                    await page.goto(url, timeout=30000)
                    await page.wait_for_timeout(5000)
                    
                    # Wait for items to load
                    try:
                        await page.wait_for_selector('[data-testid="ItemCell"], .item, .sc-item', timeout=10000)
                    except:
                        pass  # Continue even if selector doesn't appear
                    
                    # Multiple selector strategies
                    item_selectors = [
                        '[data-testid="ItemCell"]',
                        '.sc-item',
                        '.item',
                        '.mercari-item',
                        '[data-item-id]'
                    ]
                    
                    items = []
                    for selector in item_selectors:
                        try:
                            items = await page.query_selector_all(selector)
                            if items:
                                break
                        except:
                            continue
                    
                    for item in items[:12]:
                        try:
                            # Multiple title selectors
                            title_selectors = [
                                '[data-testid="ItemName"]',
                                '.item-name',
                                '.title',
                                'h3',
                                'span[title]'
                            ]
                            
                            title_elem = None
                            for title_sel in title_selectors:
                                title_elem = await item.query_selector(title_sel)
                                if title_elem:
                                    break
                            
                            # Multiple price selectors
                            price_selectors = [
                                '[data-testid="ItemPrice"]',
                                '.item-price',
                                '.price',
                                '.cost'
                            ]
                            
                            price_elem = None
                            for price_sel in price_selectors:
                                price_elem = await item.query_selector(price_sel)
                                if price_elem:
                                    break
                            
                            # Get link
                            link_elem = await item.query_selector('a')
                            
                            if title_elem and link_elem:
                                title = await title_elem.inner_text()
                                price = await price_elem.inner_text() if price_elem else ""
                                link = await link_elem.get_attribute('href')
                                
                                if link and not link.startswith('http'):
                                    link = f"https://www.mercari.com{link}"
                                
                                if title and link and len(title.strip()) > 3:
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
                    logging.warning(f"Mercari error for {term}: {e}")
                
                finally:
                    await page.close()
                    await context.close()
                
                await asyncio.sleep(4)
            
            await browser.close()
        
        return results


# Test function to verify fixes
async def test_platform_fixes():
    """Test the fixed platform implementations"""
    
    keywords = {'direct_terms': ['antique', 'vintage', 'carved']}
    
    platforms = {
        'aliexpress': FixedAliExpressScanner(),
        'mercari': FixedMercariScanner()
    }
    
    timeout = aiohttp.ClientTimeout(total=300)
    connector = aiohttp.TCPConnector(limit=20, limit_per_host=5)
    
    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        print("🔧 TESTING PLATFORM FIXES")
        print("=" * 50)
        
        total_results = 0
        
        for platform_name, scanner in platforms.items():
            print(f"\n🔍 Testing {platform_name.upper()}...")
            
            try:
                results = await asyncio.wait_for(
                    scanner.scan_production(keywords, session),
                    timeout=120
                )
                
                count = len(results)
                total_results += count
                
                if count > 0:
                    print(f"✅ {count} results found")
                    for i, result in enumerate(results[:3], 1):
                        title = result.get('title', 'No title')[:40]
                        price = result.get('price', 'No price')
                        print(f"   {i}. {title}... - {price}")
                else:
                    print("❌ No results")
                
            except Exception as e:
                print(f"❌ Error: {str(e)[:50]}")
        
        print(f"\n🎯 TOTAL RESULTS FROM FIXED PLATFORMS: {total_results}")
        
        if total_results > 0:
            print(f"🎉 Platform fixes are working!")
            estimated_daily = (821 + total_results) * 24  # Add to current 821
            print(f"📈 New estimated daily: {estimated_daily:,} listings")
            
            if estimated_daily >= 100000:
                print(f"🏆 100K+ DAILY GOAL ACHIEVED!")
        else:
            print(f"🔧 Platform fixes need more work")


if __name__ == "__main__":
    asyncio.run(test_platform_fixes())
