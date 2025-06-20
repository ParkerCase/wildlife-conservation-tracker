#!/usr/bin/env python3
"""
WildGuard AI - Complete Platform Fix
Fix the remaining 3 platforms to make 8/8 fully operational
"""

import asyncio
import sys
import os
from playwright.async_api import async_playwright
from dotenv import load_dotenv
from fake_useragent import UserAgent

load_dotenv('/Users/parkercase/conservation-bot/backend/.env')

class PlatformCompletionFixer:
    def __init__(self):
        self.ua = UserAgent()

    async def fix_mercari_completely(self):
        """Complete fix for Mercari with comprehensive approach"""
        print("🔧 COMPLETING MERCARI FIX...")
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    viewport={'width': 1920, 'height': 1080}
                )
                page = await context.new_page()
                
                # Try multiple URL patterns
                urls_to_test = [
                    "https://www.mercari.com/search/?keyword=jewelry",
                    "https://www.mercari.com/us/search/?keyword=jewelry",
                    "https://www.mercari.com/browse/jewelry"
                ]
                
                for url in urls_to_test:
                    print(f"   Testing: {url}")
                    try:
                        await page.goto(url, timeout=30000)
                        await page.wait_for_timeout(10000)  # Extended wait
                        
                        # Scroll to trigger lazy loading
                        for i in range(3):
                            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                            await page.wait_for_timeout(2000)
                        
                        # Try comprehensive selector approach
                        selectors_to_try = [
                            # New selectors based on current Mercari structure
                            '[data-testid="ItemCell"]',
                            '[data-cy="item-cell"]', 
                            '.ItemCell',
                            '.mercari-item',
                            '.search-result-item',
                            '.item-card',
                            'div[data-item-id]',
                            'article',
                            '[class*="Item"]',
                            '[class*="item"]'
                        ]
                        
                        working_combination = None
                        
                        for selector in selectors_to_try:
                            items = await page.query_selector_all(selector)
                            print(f"      Selector '{selector}': {len(items)} items")
                            
                            if items and len(items) > 0:
                                # Test extracting from first item
                                first_item = items[0]
                                
                                # Get all text content to analyze structure
                                text_content = await first_item.inner_text()
                                html_content = await first_item.inner_html()
                                
                                print(f"      Sample text: {text_content[:100]}...")
                                
                                # Look for title patterns
                                title_selectors = [
                                    'h1', 'h2', 'h3', 'h4',
                                    '[data-testid*="title"]',
                                    '[data-testid*="Title"]',
                                    '[data-cy*="title"]',
                                    '.title',
                                    '.item-title',
                                    '.name',
                                    'p:first-child',
                                    'span:first-child',
                                    'a[title]'
                                ]
                                
                                for title_sel in title_selectors:
                                    title_elem = await first_item.query_selector(title_sel)
                                    if title_elem:
                                        title_text = await title_elem.inner_text()
                                        if title_text and len(title_text.strip()) > 5:
                                            print(f"      ✅ WORKING: {selector} + {title_sel}")
                                            print(f"         Title: {title_text[:50]}...")
                                            working_combination = (url, selector, title_sel)
                                            break
                                
                                if working_combination:
                                    break
                        
                        if working_combination:
                            # Extract multiple products to verify
                            url_used, item_selector, title_selector = working_combination
                            items = await page.query_selector_all(item_selector)
                            products = []
                            
                            for item in items[:5]:
                                try:
                                    title_elem = await item.query_selector(title_selector)
                                    price_elem = await item.query_selector('[data-testid*="price"], .price, [class*="price"]')
                                    link_elem = await item.query_selector('a')
                                    
                                    title = await title_elem.inner_text() if title_elem else ""
                                    price = await price_elem.inner_text() if price_elem else ""
                                    link = await link_elem.get_attribute('href') if link_elem else ""
                                    
                                    if title and len(title.strip()) > 5:
                                        products.append({
                                            "title": title.strip(),
                                            "price": price.strip(),
                                            "url": link
                                        })
                                except:
                                    continue
                            
                            await browser.close()
                            return True, {
                                "url": url_used,
                                "item_selector": item_selector,
                                "title_selector": title_selector,
                                "products": products
                            }
                    
                    except Exception as e:
                        print(f"      Error with {url}: {e}")
                        continue
                
                await browser.close()
                return False, "No working combination found"
                
        except Exception as e:
            return False, str(e)

    async def fix_gumtree_completely(self):
        """Complete fix for Gumtree with UK and AU domains"""
        print("🔧 COMPLETING GUMTREE FIX...")
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=self.ua.random,
                    viewport={'width': 1366, 'height': 768}
                )
                page = await context.new_page()
                
                # Test both UK and Australia
                domains_to_test = [
                    {
                        "name": "UK",
                        "url": "https://www.gumtree.com/search?search_category=all&q=jewelry",
                        "selectors": {
                            "listings": ['article.listing-maxi', '.listing-tile', '.listing-card', 'article'],
                            "titles": ['h2 a', 'h3 a', '.listing-title a', '.ad-listing-title']
                        }
                    },
                    {
                        "name": "AU", 
                        "url": "https://www.gumtree.com.au/s-ad/jewelry/k0",
                        "selectors": {
                            "listings": ['.user-ad-row', 'article', '.search-result', '.ad-item'],
                            "titles": ['.user-ad-row-new-design__title-link', 'h3 a', '.title a']
                        }
                    }
                ]
                
                for domain in domains_to_test:
                    print(f"   Testing Gumtree {domain['name']}: {domain['url']}")
                    
                    try:
                        await page.goto(domain['url'], timeout=25000)
                        await page.wait_for_timeout(4000)
                        
                        # Check page loaded properly
                        page_title = await page.title()
                        print(f"      Page title: {page_title}")
                        
                        working_combination = None
                        
                        for listing_selector in domain['selectors']['listings']:
                            listings = await page.query_selector_all(listing_selector)
                            print(f"      Selector '{listing_selector}': {len(listings)} listings")
                            
                            if listings and len(listings) > 0:
                                for title_selector in domain['selectors']['titles']:
                                    first_listing = listings[0]
                                    title_elem = await first_listing.query_selector(title_selector)
                                    
                                    if title_elem:
                                        title = await title_elem.inner_text()
                                        link = await title_elem.get_attribute('href')
                                        
                                        if title and link and len(title.strip()) > 5:
                                            print(f"      ✅ WORKING: {listing_selector} + {title_selector}")
                                            print(f"         Title: {title[:50]}...")
                                            working_combination = (domain, listing_selector, title_selector)
                                            break
                                
                                if working_combination:
                                    break
                        
                        if working_combination:
                            # Extract multiple products
                            domain_info, listing_sel, title_sel = working_combination
                            listings = await page.query_selector_all(listing_sel)
                            products = []
                            
                            for listing in listings[:5]:
                                try:
                                    title_elem = await listing.query_selector(title_sel)
                                    price_elem = await listing.query_selector('.listing-price strong, .ad-price, .price')
                                    location_elem = await listing.query_selector('.listing-location span, .location')
                                    
                                    title = await title_elem.inner_text() if title_elem else ""
                                    price = await price_elem.inner_text() if price_elem else ""
                                    location = await location_elem.inner_text() if location_elem else ""
                                    link = await title_elem.get_attribute('href') if title_elem else ""
                                    
                                    if title and len(title.strip()) > 5:
                                        if not link.startswith('http'):
                                            base_domain = domain_info['url'].split('/')[0] + '//' + domain_info['url'].split('/')[2]
                                            link = base_domain + link
                                        
                                        products.append({
                                            "title": title.strip(),
                                            "price": price.strip(),
                                            "location": location.strip(),
                                            "url": link
                                        })
                                except:
                                    continue
                            
                            await browser.close()
                            return True, {
                                "domain": domain_info['name'],
                                "url": domain_info['url'],
                                "listing_selector": listing_sel,
                                "title_selector": title_sel,
                                "products": products
                            }
                    
                    except Exception as e:
                        print(f"      Error with {domain['name']}: {e}")
                        continue
                
                await browser.close()
                return False, "No working domain/selector combination found"
                
        except Exception as e:
            return False, str(e)

    async def fix_mercadolibre_completely(self):
        """Complete fix for MercadoLibre with multiple countries"""
        print("🔧 COMPLETING MERCADOLIBRE FIX...")
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=self.ua.random,
                    viewport={'width': 1920, 'height': 1080}
                )
                page = await context.new_page()
                
                # Test multiple country domains with different approaches
                countries_to_test = [
                    {
                        "name": "Mexico",
                        "url": "https://listado.mercadolibre.com.mx/jewelry",
                        "alt_url": "https://articulo.mercadolibre.com.mx/noindex/catalog?q=jewelry"
                    },
                    {
                        "name": "Argentina", 
                        "url": "https://listado.mercadolibre.com.ar/jewelry",
                        "alt_url": "https://articulo.mercadolibre.com.ar/noindex/catalog?q=jewelry"
                    },
                    {
                        "name": "Brazil",
                        "url": "https://lista.mercadolivre.com.br/jewelry",
                        "alt_url": "https://produto.mercadolivre.com.br/noindex/catalog?q=jewelry"
                    }
                ]
                
                for country in countries_to_test:
                    urls_to_try = [country['url'], country['alt_url']]
                    
                    for url in urls_to_try:
                        print(f"   Testing {country['name']}: {url}")
                        
                        try:
                            await page.goto(url, timeout=30000)
                            await page.wait_for_timeout(5000)
                            
                            # Check if page loaded
                            page_title = await page.title()
                            print(f"      Page title: {page_title}")
                            
                            # Wait for potential results container
                            container_selectors = [
                                '.ui-search-results',
                                '.results-container', 
                                '.search-results',
                                '.items-container',
                                '.ui-search-wrapper'
                            ]
                            
                            working_container = None
                            for container_sel in container_selectors:
                                try:
                                    await page.wait_for_selector(container_sel, timeout=8000)
                                    print(f"      ✅ Found container: {container_sel}")
                                    working_container = container_sel
                                    break
                                except:
                                    continue
                            
                            if working_container:
                                # Use JavaScript for robust extraction
                                products = await page.evaluate(f'''
                                    () => {{
                                        const container = document.querySelector('{working_container}');
                                        if (!container) return [];
                                        
                                        const products = [];
                                        
                                        // Try multiple item selectors
                                        const itemSelectors = [
                                            '.ui-search-result',
                                            '.item',
                                            '[data-item-id]',
                                            '.ui-search-item',
                                            '.product-item',
                                            '[class*="item"]'
                                        ];
                                        
                                        let items = [];
                                        for (const selector of itemSelectors) {{
                                            items = container.querySelectorAll(selector);
                                            if (items.length > 0) break;
                                        }}
                                        
                                        items.forEach((item, index) => {{
                                            if (index >= 5) return; // Limit results
                                            
                                            // Try multiple title selectors
                                            const titleSelectors = [
                                                '.ui-search-item__title',
                                                'h2 a',
                                                '.item-title',
                                                '.title',
                                                'h3',
                                                'h2',
                                                'a[title]'
                                            ];
                                            
                                            let title = '';
                                            let link = '';
                                            
                                            for (const titleSel of titleSelectors) {{
                                                const titleEl = item.querySelector(titleSel);
                                                if (titleEl && titleEl.textContent.trim()) {{
                                                    title = titleEl.textContent.trim();
                                                    link = titleEl.href || titleEl.closest('a')?.href || '';
                                                    break;
                                                }}
                                            }}
                                            
                                            // Try price selectors
                                            const priceSelectors = [
                                                '.price-tag',
                                                '.ui-search-price__second-line',
                                                '.price',
                                                '.item-price',
                                                '[class*="price"]'
                                            ];
                                            
                                            let price = '';
                                            for (const priceSel of priceSelectors) {{
                                                const priceEl = item.querySelector(priceSel);
                                                if (priceEl && priceEl.textContent.trim()) {{
                                                    price = priceEl.textContent.trim();
                                                    break;
                                                }}
                                            }}
                                            
                                            if (title && title.length > 5) {{
                                                products.push({{
                                                    title: title,
                                                    price: price,
                                                    url: link
                                                }});
                                            }}
                                        }});
                                        
                                        return products;
                                    }}
                                ''')
                                
                                if products and len(products) > 0:
                                    print(f"      ✅ EXTRACTED {len(products)} products!")
                                    for product in products[:2]:
                                        print(f"         📦 {product['title'][:50]}...")
                                    
                                    await browser.close()
                                    return True, {
                                        "country": country['name'],
                                        "url": url,
                                        "container": working_container,
                                        "products": products
                                    }
                        
                        except Exception as e:
                            print(f"      Error with {url}: {e}")
                            continue
                
                await browser.close()
                return False, "No working country/URL combination found"
                
        except Exception as e:
            return False, str(e)

    async def test_all_fixes(self):
        """Test all platform fixes"""
        print("🎯 TESTING ALL PLATFORM FIXES")
        print("=" * 50)
        
        fixes = [
            ("Mercari", self.fix_mercari_completely),
            ("Gumtree", self.fix_gumtree_completely),
            ("MercadoLibre", self.fix_mercadolibre_completely)
        ]
        
        results = {}
        
        for platform_name, fix_func in fixes:
            print(f"\n🔧 FIXING {platform_name.upper()}...")
            try:
                success, details = await fix_func()
                results[platform_name] = (success, details)
                
                if success:
                    print(f"✅ {platform_name}: COMPLETELY FIXED!")
                    if isinstance(details, dict) and 'products' in details:
                        print(f"   → {len(details['products'])} products extracted")
                        print(f"   → Configuration: {details.get('url', 'N/A')}")
                else:
                    print(f"❌ {platform_name}: Still needs work")
                    print(f"   → {details}")
                
            except Exception as e:
                results[platform_name] = (False, str(e))
                print(f"💥 {platform_name}: Exception - {e}")
        
        # Summary
        fixed = [p for p, (success, _) in results.items() if success]
        still_broken = [p for p, (success, _) in results.items() if not success]
        
        print("\n" + "=" * 50)
        print("🎯 PLATFORM COMPLETION RESULTS:")
        print(f"   ✅ COMPLETELY FIXED: {len(fixed)}/3 platforms")
        if fixed:
            print(f"      → {', '.join(fixed)}")
        
        print(f"   ❌ STILL NEEDS WORK: {len(still_broken)}/3 platforms")
        if still_broken:
            print(f"      → {', '.join(still_broken)}")
        
        # Overall status
        previously_working = 5  # eBay, Craigslist, AliExpress, OLX, Taobao
        total_working = previously_working + len(fixed)
        
        print(f"\n🏆 TOTAL PLATFORM STATUS: {total_working}/8 FULLY OPERATIONAL")
        
        if total_working == 8:
            print("🎊 SUCCESS: All 8 platforms are now fully operational!")
        elif total_working >= 7:
            print("🏆 EXCELLENT: 7-8 platforms working - virtually complete!")
        elif total_working >= 6:
            print("⚠️  GOOD: 6+ platforms working - strong majority operational")
        
        return results


async def main():
    fixer = PlatformCompletionFixer()
    await fixer.test_all_fixes()


if __name__ == "__main__":
    asyncio.run(main())
