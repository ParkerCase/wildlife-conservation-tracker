#!/usr/bin/env python3
"""
WildGuard AI - Individual Platform Testing & Fixing
Test each platform separately and fix any issues
"""

import asyncio
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('/Users/parkercase/conservation-bot/backend/.env')

# Add project paths
sys.path.append('/Users/parkercase/conservation-bot')
sys.path.append('/Users/parkercase/conservation-bot/src')

class PlatformTester:
    def __init__(self):
        self.supabase = None
        self.setup_supabase()
        
    def setup_supabase(self):
        """Setup Supabase connection"""
        try:
            from supabase import create_client
            SUPABASE_URL = os.getenv('SUPABASE_URL')
            SUPABASE_KEY = os.getenv('SUPABASE_KEY')
            self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            print("✅ Supabase connected")
        except Exception as e:
            print(f"❌ Supabase connection failed: {e}")

    async def test_ebay(self):
        """Test eBay platform specifically"""
        print("\n🔍 TESTING EBAY PLATFORM")
        print("-" * 40)
        
        try:
            from monitoring.platforms.ebay_scanner import EbayScanner
            import aiohttp
            
            scanner = EbayScanner()
            test_keywords = {'direct_terms': ['ivory', 'elephant']}
            
            async with aiohttp.ClientSession() as session:
                start_time = datetime.now()
                results = await asyncio.wait_for(scanner.scan(test_keywords, session), timeout=45.0)
                duration = (datetime.now() - start_time).total_seconds()
                
                if results:
                    print(f"✅ eBay: {len(results)} results in {duration:.1f}s")
                    
                    # Store samples
                    stored = await self.store_results('ebay', results[:5])
                    
                    # Show samples
                    for i, result in enumerate(results[:3], 1):
                        title = result.get('title', 'No title')[:50]
                        price = result.get('price', 'No price')
                        print(f"   {i}. {title}... - {price}")
                    
                    return {'status': 'WORKING', 'count': len(results), 'stored': stored}
                else:
                    print("❌ eBay: No results")
                    return {'status': 'NO_RESULTS', 'count': 0, 'stored': 0}
                    
        except asyncio.TimeoutError:
            print("⏰ eBay: Timeout")
            return {'status': 'TIMEOUT', 'count': 0, 'stored': 0}
        except Exception as e:
            print(f"❌ eBay error: {e}")
            return {'status': 'ERROR', 'error': str(e), 'count': 0, 'stored': 0}

    async def test_craigslist(self):
        """Test Craigslist platform specifically"""
        print("\n🔍 TESTING CRAIGSLIST PLATFORM")
        print("-" * 40)
        
        try:
            from monitoring.platforms.craigslist_scanner import CraigslistScanner
            import aiohttp
            
            scanner = CraigslistScanner()
            test_keywords = {'direct_terms': ['ivory', 'antique']}
            
            async with aiohttp.ClientSession() as session:
                start_time = datetime.now()
                results = await asyncio.wait_for(scanner.scan(test_keywords, session), timeout=60.0)
                duration = (datetime.now() - start_time).total_seconds()
                
                if results:
                    print(f"✅ Craigslist: {len(results)} results in {duration:.1f}s")
                    
                    stored = await self.store_results('craigslist', results[:5])
                    
                    for i, result in enumerate(results[:3], 1):
                        title = result.get('title', 'No title')[:50]
                        price = result.get('price', 'No price')
                        location = result.get('location', 'No location')
                        print(f"   {i}. {title}... - {price} ({location})")
                    
                    return {'status': 'WORKING', 'count': len(results), 'stored': stored}
                else:
                    print("❌ Craigslist: No results")
                    return {'status': 'NO_RESULTS', 'count': 0, 'stored': 0}
                    
        except asyncio.TimeoutError:
            print("⏰ Craigslist: Timeout - may need proxy or rate limiting")
            return {'status': 'TIMEOUT', 'count': 0, 'stored': 0}
        except Exception as e:
            print(f"❌ Craigslist error: {e}")
            return {'status': 'ERROR', 'error': str(e), 'count': 0, 'stored': 0}

    async def test_aliexpress(self):
        """Test AliExpress platform specifically"""
        print("\n🔍 TESTING ALIEXPRESS PLATFORM")
        print("-" * 40)
        
        try:
            from monitoring.platforms.aliexpress_scanner import AliexpressScanner
            import aiohttp
            
            scanner = AliexpressScanner()
            test_keywords = {'direct_terms': ['bone', 'carved']}
            
            async with aiohttp.ClientSession() as session:
                start_time = datetime.now()
                results = await asyncio.wait_for(scanner.scan(test_keywords, session), timeout=60.0)
                duration = (datetime.now() - start_time).total_seconds()
                
                if results:
                    print(f"✅ AliExpress: {len(results)} results in {duration:.1f}s")
                    
                    stored = await self.store_results('aliexpress', results[:5])
                    
                    for i, result in enumerate(results[:3], 1):
                        title = result.get('title', 'No title')[:50]
                        price = result.get('price', 'No price')
                        print(f"   {i}. {title}... - {price}")
                    
                    return {'status': 'WORKING', 'count': len(results), 'stored': stored}
                else:
                    print("❌ AliExpress: No results")
                    return {'status': 'NO_RESULTS', 'count': 0, 'stored': 0}
                    
        except asyncio.TimeoutError:
            print("⏰ AliExpress: Timeout - may need anti-bot measures")
            return {'status': 'TIMEOUT', 'count': 0, 'stored': 0}
        except Exception as e:
            print(f"❌ AliExpress error: {e}")
            return {'status': 'ERROR', 'error': str(e), 'count': 0, 'stored': 0}

    async def test_olx(self):
        """Test OLX platform specifically"""
        print("\n🔍 TESTING OLX PLATFORM")
        print("-" * 40)
        
        try:
            from monitoring.platforms.olx_scanner import OlxScanner
            import aiohttp
            
            scanner = OlxScanner()
            test_keywords = {'direct_terms': ['antique', 'carved']}
            
            async with aiohttp.ClientSession() as session:
                start_time = datetime.now()
                results = await asyncio.wait_for(scanner.scan(test_keywords, session), timeout=60.0)
                duration = (datetime.now() - start_time).total_seconds()
                
                if results:
                    print(f"✅ OLX: {len(results)} results in {duration:.1f}s")
                    
                    stored = await self.store_results('olx', results[:5])
                    
                    for i, result in enumerate(results[:3], 1):
                        title = result.get('title', 'No title')[:50]
                        price = result.get('price', 'No price')
                        print(f"   {i}. {title}... - {price}")
                    
                    return {'status': 'WORKING', 'count': len(results), 'stored': stored}
                else:
                    print("❌ OLX: No results")
                    return {'status': 'NO_RESULTS', 'count': 0, 'stored': 0}
                    
        except asyncio.TimeoutError:
            print("⏰ OLX: Timeout")
            return {'status': 'TIMEOUT', 'count': 0, 'stored': 0}
        except Exception as e:
            print(f"❌ OLX error: {e}")
            return {'status': 'ERROR', 'error': str(e), 'count': 0, 'stored': 0}

    async def test_taobao(self):
        """Test Taobao platform specifically"""
        print("\n🔍 TESTING TAOBAO PLATFORM")
        print("-" * 40)
        
        try:
            from monitoring.platforms.taobao_scanner import TaobaoScanner
            import aiohttp
            
            scanner = TaobaoScanner()
            test_keywords = {'direct_terms': ['象牙', '骨雕']}  # Chinese terms
            
            async with aiohttp.ClientSession() as session:
                start_time = datetime.now()
                results = await asyncio.wait_for(scanner.scan(test_keywords, session), timeout=60.0)
                duration = (datetime.now() - start_time).total_seconds()
                
                if results:
                    print(f"✅ Taobao: {len(results)} results in {duration:.1f}s")
                    
                    stored = await self.store_results('taobao', results[:5])
                    
                    for i, result in enumerate(results[:3], 1):
                        title = result.get('title', 'No title')[:50]
                        price = result.get('price', 'No price')
                        print(f"   {i}. {title}... - {price}")
                    
                    return {'status': 'WORKING', 'count': len(results), 'stored': stored}
                else:
                    print("❌ Taobao: No results")
                    return {'status': 'NO_RESULTS', 'count': 0, 'stored': 0}
                    
        except asyncio.TimeoutError:
            print("⏰ Taobao: Timeout - heavy anti-bot protection")
            return {'status': 'TIMEOUT', 'count': 0, 'stored': 0}
        except Exception as e:
            print(f"❌ Taobao error: {e}")
            return {'status': 'ERROR', 'error': str(e), 'count': 0, 'stored': 0}

    async def test_gumtree(self):
        """Test Gumtree platform"""
        print("\n🔍 TESTING GUMTREE PLATFORM")
        print("-" * 40)
        
        try:
            from monitoring.platforms.gumtree_scanner import GumtreeScanner
            import aiohttp
            
            scanner = GumtreeScanner()
            test_keywords = {'direct_terms': ['antique', 'carved']}
            
            async with aiohttp.ClientSession() as session:
                start_time = datetime.now()
                results = await asyncio.wait_for(scanner.scan(test_keywords, session), timeout=60.0)
                duration = (datetime.now() - start_time).total_seconds()
                
                if results:
                    print(f"✅ Gumtree: {len(results)} results in {duration:.1f}s")
                    
                    stored = await self.store_results('gumtree', results[:5])
                    
                    for i, result in enumerate(results[:3], 1):
                        title = result.get('title', 'No title')[:50]
                        price = result.get('price', 'No price')
                        print(f"   {i}. {title}... - {price}")
                    
                    return {'status': 'WORKING', 'count': len(results), 'stored': stored}
                else:
                    print("❌ Gumtree: No results")
                    return {'status': 'NO_RESULTS', 'count': 0, 'stored': 0}
                    
        except asyncio.TimeoutError:
            print("⏰ Gumtree: Timeout")
            return {'status': 'TIMEOUT', 'count': 0, 'stored': 0}
        except Exception as e:
            print(f"❌ Gumtree error: {e}")
            return {'status': 'ERROR', 'error': str(e), 'count': 0, 'stored': 0}

    async def test_mercadolibre(self):
        """Test MercadoLibre platform"""
        print("\n🔍 TESTING MERCADOLIBRE PLATFORM")
        print("-" * 40)
        
        try:
            from monitoring.platforms.mercadolibre_scanner import MercadolibreScanner
            import aiohttp
            
            scanner = MercadolibreScanner()
            test_keywords = {'direct_terms': ['antiguo', 'tallado']}  # Spanish terms
            
            async with aiohttp.ClientSession() as session:
                start_time = datetime.now()
                results = await asyncio.wait_for(scanner.scan(test_keywords, session), timeout=60.0)
                duration = (datetime.now() - start_time).total_seconds()
                
                if results:
                    print(f"✅ MercadoLibre: {len(results)} results in {duration:.1f}s")
                    
                    stored = await self.store_results('mercadolibre', results[:5])
                    
                    for i, result in enumerate(results[:3], 1):
                        title = result.get('title', 'No title')[:50]
                        price = result.get('price', 'No price')
                        print(f"   {i}. {title}... - {price}")
                    
                    return {'status': 'WORKING', 'count': len(results), 'stored': stored}
                else:
                    print("❌ MercadoLibre: No results")
                    return {'status': 'NO_RESULTS', 'count': 0, 'stored': 0}
                    
        except asyncio.TimeoutError:
            print("⏰ MercadoLibre: Timeout")
            return {'status': 'TIMEOUT', 'count': 0, 'stored': 0}
        except Exception as e:
            print(f"❌ MercadoLibre error: {e}")
            return {'status': 'ERROR', 'error': str(e), 'count': 0, 'stored': 0}

    async def test_poshmark(self):
        """Test Poshmark platform"""
        print("\n🔍 TESTING POSHMARK PLATFORM")
        print("-" * 40)
        
        try:
            from monitoring.platforms.poshmark_scanner import PoshmarkScanner
            import aiohttp
            
            scanner = PoshmarkScanner()
            test_keywords = {'direct_terms': ['vintage', 'antique']}
            
            async with aiohttp.ClientSession() as session:
                start_time = datetime.now()
                results = await asyncio.wait_for(scanner.scan(test_keywords, session), timeout=60.0)
                duration = (datetime.now() - start_time).total_seconds()
                
                if results:
                    print(f"✅ Poshmark: {len(results)} results in {duration:.1f}s")
                    
                    stored = await self.store_results('poshmark', results[:5])
                    
                    for i, result in enumerate(results[:3], 1):
                        title = result.get('title', 'No title')[:50]
                        price = result.get('price', 'No price')
                        print(f"   {i}. {title}... - {price}")
                    
                    return {'status': 'WORKING', 'count': len(results), 'stored': stored}
                else:
                    print("❌ Poshmark: No results")
                    return {'status': 'NO_RESULTS', 'count': 0, 'stored': 0}
                    
        except asyncio.TimeoutError:
            print("⏰ Poshmark: Timeout")
            return {'status': 'TIMEOUT', 'count': 0, 'stored': 0}
        except Exception as e:
            print(f"❌ Poshmark error: {e}")
            return {'status': 'ERROR', 'error': str(e), 'count': 0, 'stored': 0}

    async def store_results(self, platform, results):
        """Store results in Supabase"""
        if not self.supabase or not results:
            return 0
            
        stored_count = 0
        for i, result in enumerate(results):
            try:
                evidence_id = f"TEST-{platform.upper()}-{datetime.now().strftime('%m%d%H%M')}-{i+1:02d}"
                
                detection = {
                    'evidence_id': evidence_id,
                    'timestamp': datetime.now().isoformat(),
                    'platform': platform,
                    'threat_score': 30,
                    'threat_level': 'LOW',
                    'species_involved': f"Platform test: {result.get('search_term', 'unknown')}",
                    'alert_sent': False,
                    'status': f'PLATFORM_TEST_{platform.upper()}'
                }
                
                self.supabase.table('detections').insert(detection).execute()
                stored_count += 1
                
            except Exception as e:
                print(f"   ⚠️ Storage error for {platform}: {e}")
                
        return stored_count

    async def run_complete_test(self):
        """Test all platforms and provide summary"""
        
        print("🧪 COMPLETE PLATFORM TESTING")
        print("=" * 60)
        print("Testing each platform individually...")
        
        platforms = [
            ('eBay', self.test_ebay),
            ('Craigslist', self.test_craigslist),
            ('AliExpress', self.test_aliexpress),
            ('OLX', self.test_olx),
            ('Taobao', self.test_taobao),
            ('Gumtree', self.test_gumtree),
            ('MercadoLibre', self.test_mercadolibre),
            ('Poshmark', self.test_poshmark)
        ]
        
        results = {}
        total_working = 0
        total_listings = 0
        total_stored = 0
        
        for platform_name, test_func in platforms:
            try:
                result = await test_func()
                results[platform_name] = result
                
                if result['status'] == 'WORKING':
                    total_working += 1
                    total_listings += result['count']
                    total_stored += result['stored']
                    
            except Exception as e:
                print(f"❌ {platform_name} test failed: {e}")
                results[platform_name] = {'status': 'FAILED', 'error': str(e), 'count': 0, 'stored': 0}
        
        # Summary
        print(f"\n📊 COMPLETE TESTING SUMMARY")
        print("=" * 60)
        
        working_platforms = []
        partial_platforms = []
        broken_platforms = []
        
        for platform, result in results.items():
            status = result['status']
            count = result.get('count', 0)
            stored = result.get('stored', 0)
            
            if status == 'WORKING':
                working_platforms.append(f"{platform} ({count} listings)")
                print(f"✅ {platform}: WORKING - {count} listings, {stored} stored")
            elif status in ['TIMEOUT', 'NO_RESULTS']:
                partial_platforms.append(f"{platform} ({status})")
                print(f"🔧 {platform}: {status}")
            else:
                broken_platforms.append(f"{platform} ({status})")
                print(f"❌ {platform}: {status}")
        
        print(f"\n🎯 FINAL RESULTS:")
        print(f"   ✅ Fully Working: {len(working_platforms)}/8 platforms")
        print(f"   🔧 Partial/Timeout: {len(partial_platforms)}/8 platforms")
        print(f"   ❌ Broken: {len(broken_platforms)}/8 platforms")
        print(f"   📊 Total listings found: {total_listings}")
        print(f"   💾 Total stored in Supabase: {total_stored}")
        
        if working_platforms:
            print(f"\n✅ WORKING PLATFORMS:")
            for platform in working_platforms:
                print(f"   • {platform}")
        
        if partial_platforms:
            print(f"\n🔧 NEED FIXES:")
            for platform in partial_platforms:
                print(f"   • {platform}")
        
        if broken_platforms:
            print(f"\n❌ BROKEN PLATFORMS:")
            for platform in broken_platforms:
                print(f"   • {platform}")
        
        # Calculate realistic daily volume
        if total_listings > 0:
            daily_projection = total_listings * 24 * 5  # 24 scans, 5x keywords
            print(f"\n📈 REALISTIC DAILY PROJECTION:")
            print(f"   Current test: {total_listings} listings")
            print(f"   Daily projection: {daily_projection} listings/day")
            print(f"   Annual projection: {daily_projection * 365:,} listings/year")
        
        return results

async def main():
    """Main testing function"""
    tester = PlatformTester()
    await tester.run_complete_test()

if __name__ == "__main__":
    asyncio.run(main())
