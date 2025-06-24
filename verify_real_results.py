#!/usr/bin/env python3
"""
WildGuard AI - Real Platform Results Verification
Tests Facebook and Gumtree to verify they return actual, real listings
"""

import asyncio
import aiohttp
import os
import sys
from datetime import datetime
from playwright.async_api import async_playwright
from fake_useragent import UserAgent
import json
import re

# Set environment variables
os.environ['SUPABASE_URL'] = 'https://hgnefrvllutcagdutcaa.supabase.co'
os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhnbmVmcnZsbHV0Y2FnZHV0Y2FhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkzMjU4NzcsImV4cCI6MjA2NDkwMTg3N30.ftaP4Xa1vTXumTlcPy0OwdG1s-4JSYz10-ENiWB_QZ0'

class RealResultsVerification:
    """Verify platforms return real, actual listings - not mock data"""
    
    def __init__(self):
        self.ua = UserAgent()
        
    async def verify_facebook_marketplace_real(self):
        """Verify Facebook Marketplace returns real listings"""
        print("🔵 VERIFYING FACEBOOK MARKETPLACE - REAL RESULTS")
        print("-" * 55)
        
        real_results = []
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )
                
                context = await browser.new_context(
                    user_agent=self.ua.random,
                    viewport={'width': 1366, 'height': 768}
                )
                
                page = await context.new_page()
                
                # Test with a common search term that should have real results
                search_term = "antique"
                url = f"https://www.facebook.com/marketplace/search/?query={search_term}"
                
                print(f"🔍 Searching Facebook for: '{search_term}'")
                print(f"🌐 URL: {url}")
                
                await page.goto(url, timeout=30000)
                await page.wait_for_timeout(5000)  # Wait for content to load
                
                # Take screenshot for verification
                await page.screenshot(path='/tmp/facebook_marketplace_test.png')
                print("📸 Screenshot saved: /tmp/facebook_marketplace_test.png")
                
                # Check page title and content
                title = await page.title()
                print(f"📄 Page title: {title}")
                
                if "marketplace" in title.lower():
                    print("✅ Successfully reached Facebook Marketplace")
                else:
                    print("❌ May not have reached marketplace correctly")
                
                # Look for marketplace items with multiple selectors
                item_selectors = [
                    '[data-testid="marketplace-item"]',
                    'div[role="main"] a[href*="/marketplace/item/"]',
                    'a[href*="marketplace/item"]',
                    '[data-testid="marketplace-product-item"]'
                ]
                
                found_items = False
                for selector in item_selectors:
                    try:
                        items = await page.query_selector_all(selector)
                        if items:
                            print(f"✅ Found {len(items)} items with selector: {selector}")
                            found_items = True
                            
                            # Extract details from first few items
                            for i, item in enumerate(items[:3]):
                                try:
                                    # Get text content
                                    text_content = await item.inner_text()
                                    link = await item.get_attribute('href')
                                    
                                    if link and len(text_content.strip()) > 10:
                                        # This looks like a real listing
                                        real_results.append({
                                            'title': text_content.strip()[:100],
                                            'url': link if link.startswith('http') else f"https://www.facebook.com{link}",
                                            'platform': 'facebook_marketplace',
                                            'search_term': search_term,
                                            'verified_real': True
                                        })
                                        
                                        print(f"   📋 Item {i+1}: {text_content.strip()[:50]}...")
                                        print(f"   🔗 URL: {link[:50]}...")
                                        
                                except Exception as e:
                                    print(f"   ⚠️  Error processing item {i+1}: {e}")
                            break
                    except Exception as e:
                        print(f"⚠️  Selector {selector} failed: {e}")
                
                if not found_items:
                    print("❌ No marketplace items found - may be blocked or page structure changed")
                    
                    # Check for any error messages or blocks
                    page_content = await page.content()
                    if "blocked" in page_content.lower() or "robot" in page_content.lower():
                        print("🚫 Detected potential blocking")
                    elif "marketplace" not in page_content.lower():
                        print("⚠️  Page doesn't seem to contain marketplace content")
                
                await page.close()
                await context.close()
                await browser.close()
                
        except Exception as e:
            print(f"❌ Facebook verification error: {e}")
        
        print(f"\n📊 Facebook Results: {len(real_results)} real listings verified")
        return real_results

    async def verify_gumtree_real(self):
        """Verify Gumtree returns real listings"""
        print("\n🟢 VERIFYING GUMTREE - REAL RESULTS")
        print("-" * 40)
        
        real_results = []
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent=self.ua.random)
                page = await context.new_page()
                
                # Test UK Gumtree with a common search
                search_term = "antique"
                url = f"https://www.gumtree.com/search?q={search_term}"
                
                print(f"🔍 Searching Gumtree UK for: '{search_term}'")
                print(f"🌐 URL: {url}")
                
                await page.goto(url, timeout=25000)
                await page.wait_for_timeout(4000)
                
                # Take screenshot
                await page.screenshot(path='/tmp/gumtree_test.png')
                print("📸 Screenshot saved: /tmp/gumtree_test.png")
                
                title = await page.title()
                print(f"📄 Page title: {title}")
                
                if "gumtree" in title.lower():
                    print("✅ Successfully reached Gumtree")
                else:
                    print("❌ May not have reached Gumtree correctly")
                
                # Look for Gumtree listings
                item_selectors = [
                    '.user-ad-collection-new-design',
                    '.user-ad-row',
                    '.listing-link',
                    '[data-q="ad-title"]',
                    '.listing-maxi'
                ]
                
                found_items = False
                for selector in item_selectors:
                    try:
                        items = await page.query_selector_all(selector)
                        if items:
                            print(f"✅ Found {len(items)} items with selector: {selector}")
                            found_items = True
                            
                            # Extract details from first few items
                            for i, item in enumerate(items[:3]):
                                try:
                                    # Look for title and link
                                    title_elem = await item.query_selector('h2, h3, .user-ad-title, [data-q="ad-title"] a')
                                    link_elem = await item.query_selector('a')
                                    
                                    if title_elem and link_elem:
                                        title = await title_elem.inner_text()
                                        link = await link_elem.get_attribute('href')
                                        
                                        if title and link and len(title.strip()) > 5:
                                            if not link.startswith('http'):
                                                link = f"https://www.gumtree.com{link}"
                                            
                                            real_results.append({
                                                'title': title.strip(),
                                                'url': link,
                                                'platform': 'gumtree',
                                                'search_term': search_term,
                                                'verified_real': True
                                            })
                                            
                                            print(f"   📋 Item {i+1}: {title.strip()[:50]}...")
                                            print(f"   🔗 URL: {link[:50]}...")
                                            
                                except Exception as e:
                                    print(f"   ⚠️  Error processing item {i+1}: {e}")
                            break
                    except Exception as e:
                        print(f"⚠️  Selector {selector} failed: {e}")
                
                if not found_items:
                    print("❌ No Gumtree items found")
                    
                    # Check page content for clues
                    page_content = await page.content()
                    if "no results" in page_content.lower():
                        print("ℹ️  Search returned no results")
                    elif "blocked" in page_content.lower():
                        print("🚫 Potential blocking detected")
                
                await page.close()
                await context.close()
                await browser.close()
                
        except Exception as e:
            print(f"❌ Gumtree verification error: {e}")
        
        print(f"\n📊 Gumtree Results: {len(real_results)} real listings verified")
        return real_results

    async def verify_avito_real(self):
        """Verify Avito returns real listings (our star performer)"""
        print("\n🔴 VERIFYING AVITO - REAL RESULTS")
        print("-" * 35)
        
        real_results = []
        
        try:
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
                    'Accept-Language': 'ru,en-US;q=0.7,en;q=0.3'
                }
                
                search_term = "antique"
                url = f"https://www.avito.ru/rossiya?q={search_term}"
                
                print(f"🔍 Searching Avito Russia for: '{search_term}'")
                print(f"🌐 URL: {url}")
                
                async with session.get(url, headers=headers) as resp:
                    print(f"📡 HTTP Status: {resp.status}")
                    
                    if resp.status == 200:
                        html = await resp.text()
                        
                        # Save HTML for inspection
                        with open('/tmp/avito_test.html', 'w', encoding='utf-8') as f:
                            f.write(html[:10000])  # First 10k chars
                        print("📄 HTML sample saved: /tmp/avito_test.html")
                        
                        # Check if we got real Avito content
                        if "avito" in html.lower() and "item" in html.lower():
                            print("✅ Successfully reached Avito with item content")
                            
                            # Count potential items in HTML
                            item_markers = html.count('data-marker="item"')
                            print(f"📊 Found {item_markers} potential items in HTML")
                            
                            if item_markers > 0:
                                print("✅ Avito contains real item data")
                                # Create a sample result to show it's working
                                real_results.append({
                                    'title': f"Avito search results for {search_term}",
                                    'url': url,
                                    'platform': 'avito',
                                    'search_term': search_term,
                                    'verified_real': True,
                                    'items_found': item_markers
                                })
                            else:
                                print("⚠️  No item markers found")
                        else:
                            print("❌ Unexpected content returned")
                    else:
                        print(f"❌ HTTP error: {resp.status}")
                        
        except Exception as e:
            print(f"❌ Avito verification error: {e}")
        
        print(f"\n📊 Avito Results: {len(real_results)} real search verified")
        return real_results

    async def run_verification(self):
        """Run complete verification of all platforms"""
        print("🔍 REAL PLATFORM RESULTS VERIFICATION")
        print("=" * 60)
        print("🎯 Goal: Verify platforms return actual listings, not mock data")
        print()
        
        all_results = []
        
        # Test each platform
        facebook_results = await self.verify_facebook_marketplace_real()
        gumtree_results = await self.verify_gumtree_real()
        avito_results = await self.verify_avito_real()
        
        all_results.extend(facebook_results)
        all_results.extend(gumtree_results)
        all_results.extend(avito_results)
        
        # Summary
        print(f"\n📊 VERIFICATION SUMMARY")
        print("=" * 30)
        print(f"🔵 Facebook Marketplace: {len(facebook_results)} real results")
        print(f"🟢 Gumtree UK: {len(gumtree_results)} real results")
        print(f"🔴 Avito Russia: {len(avito_results)} real searches")
        print(f"🎯 Total verified: {len(all_results)} real results")
        
        # Verdict
        working_platforms = sum([
            len(facebook_results) > 0,
            len(gumtree_results) > 0,
            len(avito_results) > 0
        ])
        
        print(f"\n🎯 VERIFICATION VERDICT:")
        print(f"✅ Working platforms: {working_platforms}/3")
        
        if working_platforms >= 2:
            print("🎉 PLATFORMS VERIFIED - Returning real results!")
        elif working_platforms == 1:
            print("⚠️  Some platforms working - May need adjustments")
        else:
            print("❌ Platforms need debugging")
        
        # Save verification results
        with open('/tmp/real_results_verification.json', 'w') as f:
            json.dump(all_results, f, indent=2, default=str)
        print(f"\n💾 Verification results saved: /tmp/real_results_verification.json")
        
        return all_results

async def main():
    """Run real results verification"""
    verifier = RealResultsVerification()
    await verifier.run_verification()

if __name__ == "__main__":
    asyncio.run(main())
