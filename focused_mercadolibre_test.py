#!/usr/bin/env python3
"""
Focused MercadoLibre Test - Latin America's Largest Marketplace
"""

import asyncio
from playwright.async_api import async_playwright
from fake_useragent import UserAgent
import logging

class FocusedMercadoLibreTest:
    """Focused test specifically for MercadoLibre"""
    
    def __init__(self):
        self.ua = UserAgent()

    async def test_mercadolibre_focused(self):
        """Focused MercadoLibre test with web scraping"""
        print("🎯 FOCUSED MERCADOLIBRE TEST")
        print("=" * 50)
        
        results = []
        keywords = ['antique', 'vintage']
        countries = [
            ('mercadolibre.com.mx', 'Mexico'),
            ('mercadolibre.com.ar', 'Argentina')
        ]
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            
            for domain, country in countries:
                print(f"\n🔍 Testing {country} ({domain})...")
                
                for keyword in keywords:
                    context = await browser.new_context(
                        user_agent=self.ua.random,
                        viewport={'width': 1920, 'height': 1080},
                        locale='es-MX' if 'mx' in domain else 'es-AR'
                    )
                    page = await context.new_page()
                    
                    try:
                        # Try the search URL format
                        url = f"https://listado.{domain}/{keyword}"
                        
                        await page.goto(url, timeout=20000)
                        await page.wait_for_timeout(4000)
                        
                        # Multiple selector strategies for MercadoLibre
                        selectors_to_try = [
                            '.ui-search-result',
                            '.ui-search-results__item',
                            '[data-testid="result"]',
                            '.item-results',
                            '.item'
                        ]
                        
                        items = []
                        for selector in selectors_to_try:
                            try:
                                items = await page.query_selector_all(selector)
                                if items:
                                    print(f"   Found items with selector: {selector}")
                                    break
                            except:
                                continue
                        
                        if not items:
                            # Try to see what's on the page
                            page_title = await page.title()
                            print(f"   Page title: {page_title}")
                            
                            # Check for common elements
                            has_search = await page.query_selector('input[placeholder*="Buscar"], input[name*="search"], .nav-search')
                            if has_search:
                                print(f"   ✅ Search functionality detected")
                            
                            # Look for any product-like elements
                            possible_items = await page.query_selector_all('article, .card, [data-item], [data-id]')
                            if possible_items:
                                print(f"   Found {len(possible_items)} possible product containers")
                                items = possible_items[:10]  # Limit for testing
                        
                        for item in items[:15]:
                            try:
                                # Multiple title strategies
                                title_selectors = [
                                    '.ui-search-item__title',
                                    'h2 a',
                                    'h3 a', 
                                    '.item-title',
                                    '[data-testid="item-title"]',
                                    'a[title]'
                                ]
                                
                                title = None
                                for title_sel in title_selectors:
                                    try:
                                        title_elem = await item.query_selector(title_sel)
                                        if title_elem:
                                            title = await title_elem.inner_text()
                                            if title and len(title.strip()) > 3:
                                                break
                                    except:
                                        continue
                                
                                # Multiple price strategies
                                price_selectors = [
                                    '.ui-search-price__second-line',
                                    '.price',
                                    '.item-price',
                                    '[data-testid="price"]',
                                    '.price-tag'
                                ]
                                
                                price = ""
                                for price_sel in price_selectors:
                                    try:
                                        price_elem = await item.query_selector(price_sel)
                                        if price_elem:
                                            price = await price_elem.inner_text()
                                            if price:
                                                break
                                    except:
                                        continue
                                
                                # Get link
                                link = ""
                                try:
                                    link_elem = await item.query_selector('a')
                                    if link_elem:
                                        link = await link_elem.get_attribute('href')
                                        if link and not link.startswith('http'):
                                            link = f"https://{domain}{link}"
                                except:
                                    pass
                                
                                if title and len(title.strip()) > 3:
                                    results.append({
                                        'title': title.strip(),
                                        'price': price.strip(),
                                        'url': link,
                                        'search_term': keyword,
                                        'platform': 'mercadolibre',
                                        'country': country
                                    })
                                    
                            except Exception as e:
                                continue
                        
                        found_count = len([r for r in results if r.get('country') == country and r.get('search_term') == keyword])
                        print(f"   {keyword}: {found_count} results")
                        
                    except Exception as e:
                        print(f"   ❌ Error with {keyword}: {str(e)[:40]}")
                    
                    finally:
                        await page.close()
                        await context.close()
                    
                    await asyncio.sleep(3)
            
            await browser.close()
        
        return results

async def run_focused_mercadolibre_test():
    """Run focused MercadoLibre test"""
    
    tester = FocusedMercadoLibreTest()
    results = await tester.test_mercadolibre_focused()
    
    print(f"\n🎯 MERCADOLIBRE FOCUSED TEST RESULTS:")
    print(f"   📊 Total results: {len(results)}")
    
    if results:
        print(f"\n✅ SUCCESS! MercadoLibre is working:")
        
        # Group by country
        by_country = {}
        for result in results:
            country = result.get('country', 'Unknown')
            if country not in by_country:
                by_country[country] = []
            by_country[country].append(result)
        
        for country, country_results in by_country.items():
            print(f"\n   🇲🇽 {country}: {len(country_results)} results")
            for i, result in enumerate(country_results[:3], 1):
                title = result.get('title', 'No title')[:40]
                price = result.get('price', 'No price')
                print(f"     {i}. {title}... - {price}")
        
        # Estimate daily capacity
        results_per_test = len(results)
        estimated_daily = results_per_test * 50  # Conservative scaling
        
        print(f"\n🚀 MERCADOLIBRE IMPACT:")
        print(f"   Results per test: {results_per_test}")
        print(f"   Estimated daily: {estimated_daily:,}")
        print(f"   📈 This would boost total to: {202200 + estimated_daily:,} daily")
        
        return True, estimated_daily
    else:
        print("\n❌ MercadoLibre test failed - needs more development")
        return False, 0

if __name__ == "__main__":
    asyncio.run(run_focused_mercadolibre_test())
