#!/usr/bin/env python3
"""
Individual Platform Scanner Tests
Test each of the 5 new platforms separately to verify they work
"""

import asyncio
import aiohttp
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from fake_useragent import UserAgent
import logging

# Load environment variables from the correct path
load_dotenv()

# Set up basic logging
logging.basicConfig(level=logging.INFO)

class PlatformTester:
    def __init__(self):
        self.ua = UserAgent()
        self.test_keywords = ['ivory', 'antique', 'carved', 'vintage', 'bone']
        
    async def test_facebook_marketplace(self, session):
        """Test Facebook Marketplace"""
        print("🔵 Testing Facebook Marketplace...")
        
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent=self.ua.random)
                page = await context.new_page()
                
                try:
                    # Test with a simple search
                    url = "https://www.facebook.com/marketplace/search/?query=antique"
                    await page.goto(url, timeout=20000)
                    await page.wait_for_timeout(3000)
                    
                    # Check if we can access the page
                    title = await page.title()
                    if "marketplace" in title.lower() or "facebook" in title.lower():
                        print("   ✅ Facebook Marketplace: Accessible")
                        return True
                    else:
                        print(f"   ⚠️  Facebook Marketplace: Unexpected page - {title}")
                        return False
                        
                except Exception as e:
                    print(f"   ❌ Facebook Marketplace error: {e}")
                    return False
                finally:
                    await page.close()
                    await context.close()
                    await browser.close()
                    
        except Exception as e:
            print(f"   ❌ Facebook Marketplace setup error: {e}")
            return False

    async def test_alibaba(self, session):
        """Test Alibaba"""
        print("🟠 Testing Alibaba...")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            url = "https://www.alibaba.com/trade/search?SearchText=antique"
            
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    if "alibaba" in html.lower() and ("product" in html.lower() or "offer" in html.lower()):
                        print("   ✅ Alibaba: Working")
                        return True
                    else:
                        print("   ⚠️  Alibaba: Unexpected response")
                        return False
                else:
                    print(f"   ❌ Alibaba: HTTP {resp.status}")
                    return False
                    
        except Exception as e:
            print(f"   ❌ Alibaba error: {e}")
            return False

    async def test_gumtree(self, session):
        """Test Gumtree"""
        print("🟢 Testing Gumtree...")
        
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent=self.ua.random)
                page = await context.new_page()
                
                try:
                    # Test UK Gumtree
                    url = "https://www.gumtree.com/search?search_category=all&q=antique"
                    await page.goto(url, timeout=20000)
                    await page.wait_for_timeout(3000)
                    
                    title = await page.title()
                    if "gumtree" in title.lower():
                        print("   ✅ Gumtree: Working")
                        return True
                    else:
                        print(f"   ⚠️  Gumtree: Unexpected page - {title}")
                        return False
                        
                except Exception as e:
                    print(f"   ❌ Gumtree error: {e}")
                    return False
                finally:
                    await page.close()
                    await context.close()
                    await browser.close()
                    
        except Exception as e:
            print(f"   ❌ Gumtree setup error: {e}")
            return False

    async def test_avito(self, session):
        """Test Avito"""
        print("🔴 Testing Avito...")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
                'Accept-Language': 'ru,en-US;q=0.7,en;q=0.3'
            }
            
            url = "https://www.avito.ru/rossiya?q=antique"
            
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    if "avito" in html.lower():
                        print("   ✅ Avito: Working")
                        return True
                    else:
                        print("   ⚠️  Avito: Unexpected response")
                        return False
                else:
                    print(f"   ❌ Avito: HTTP {resp.status}")
                    return False
                    
        except Exception as e:
            print(f"   ❌ Avito error: {e}")
            return False

    async def test_bonanza(self, session):
        """Test Bonanza"""
        print("🟡 Testing Bonanza...")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            url = "https://www.bonanza.com/items/search?q%5Bkeywords_search%5D=antique"
            
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    if "bonanza" in html.lower() and ("item" in html.lower() or "product" in html.lower()):
                        print("   ✅ Bonanza: Working")
                        return True
                    else:
                        print("   ⚠️  Bonanza: Unexpected response")
                        return False
                else:
                    print(f"   ❌ Bonanza: HTTP {resp.status}")
                    return False
                    
        except Exception as e:
            print(f"   ❌ Bonanza error: {e}")
            return False

    async def run_all_tests(self):
        """Test all 5 new platforms"""
        print("🧪 Testing All 5 New Platform Scanners")
        print("=" * 50)
        
        results = {}
        
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            
            # Test each platform
            tests = [
                ('Facebook Marketplace', self.test_facebook_marketplace(session)),
                ('Alibaba', self.test_alibaba(session)),
                ('Gumtree', self.test_gumtree(session)),
                ('Avito', self.test_avito(session)),
                ('Bonanza', self.test_bonanza(session))
            ]
            
            for platform_name, test_coro in tests:
                try:
                    result = await test_coro
                    results[platform_name] = result
                except Exception as e:
                    print(f"   ❌ {platform_name}: Critical error - {e}")
                    results[platform_name] = False
                
                await asyncio.sleep(2)  # Brief pause between tests
        
        # Summary
        print(f"\n📊 PLATFORM TEST RESULTS")
        print("=" * 30)
        
        working_count = sum(results.values())
        total_count = len(results)
        
        for platform, status in results.items():
            status_icon = "✅" if status else "❌"
            print(f"{status_icon} {platform}")
        
        print(f"\n🎯 Working Platforms: {working_count}/{total_count}")
        
        if working_count >= 3:
            print("🎉 Sufficient platforms working for production!")
        else:
            print("⚠️  Need more working platforms for optimal coverage")
        
        return results

async def main():
    """Main test runner"""
    tester = PlatformTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
