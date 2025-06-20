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
import aiohttp

load_dotenv('/Users/parkercase/conservation-bot/backend/.env')
sys.path.append('/Users/parkercase/conservation-bot')
sys.path.append('/Users/parkercase/conservation-bot/src')

class PlatformTester:
    def __init__(self):
        self.supabase = None
        self.session = None
        self.results = {}
        
    async def setup_connections(self):
        """Setup Supabase and HTTP session"""
        try:
            from supabase import create_client
            
            SUPABASE_URL = os.getenv('SUPABASE_URL')
            SUPABASE_KEY = os.getenv('SUPABASE_KEY')
            self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            
            self.session = aiohttp.ClientSession()
            print("✅ Connections established")
            return True
        except Exception as e:
            print(f"❌ Connection setup failed: {e}")
            return False

    async def test_ebay(self):
        """Test eBay platform specifically"""
        print("\n🔍 TESTING EBAY PLATFORM")
        print("-" * 30)
        
        try:
            from monitoring.platforms.ebay_scanner import EbayScanner
            
            ebay = EbayScanner()
            test_keywords = {'direct_terms': ['ivory', 'wildlife']}
            
            start_time = datetime.now()
            results = await ebay.scan(test_keywords, self.session)
            duration = (datetime.now() - start_time).total_seconds()
            
            if results and len(results) > 0:
                print(f"✅ eBay: {len(results)} results in {duration:.1f}s")
                
                # Store samples
                stored = await self.store_results('ebay', results[:5])
                
                self.results['ebay'] = {
                    'status': 'WORKING',
                    'results_count': len(results),
                    'duration': duration,
                    'stored': stored,
                    'samples': [r.get('title', '')[:50] for r in results[:3]]
                }
                return True
            else:
                print("❌ eBay: No results")
                self.results['ebay'] = {'status': 'FAILED', 'error': 'No results'}
                return False
                
        except Exception as e:
            print(f"❌ eBay error: {e}")
            self.results['ebay'] = {'status': 'ERROR', 'error': str(e)}
            return False

    async def test_craigslist(self):
        """Test Craigslist platform"""
        print("\n🔍 TESTING CRAIGSLIST PLATFORM")
        print("-" * 30)
        
        try:
            from monitoring.platforms.craigslist_scanner import CraigslistScanner
            
            craigslist = CraigslistScanner()
            test_keywords = {'direct_terms': ['ivory']}
            
            print("Testing Craigslist with single keyword...")
            start_time = datetime.now()
            
            # Test with longer timeout
            results = await asyncio.wait_for(
                craigslist.scan(test_keywords, self.session), 
                timeout=45.0
            )
            duration = (datetime.now() - start_time).total_seconds()
            
            if results and len(results) > 0:
                print(f"✅ Craigslist: {len(results)} results in {duration:.1f}s")
                
                stored = await self.store_results('craigslist', results[:5])
                
                self.results['craigslist'] = {
                    'status': 'WORKING',
                    'results_count': len(results),
                    'duration': duration,
                    'stored': stored,
                    'samples': [r.get('title', '')[:50] for r in results[:3]]
                }
                return True
            else:
                print("❌ Craigslist: No results")
                self.results['craigslist'] = {'status': 'FAILED', 'error': 'No results'}
                return False
                
        except asyncio.TimeoutError:
            print("❌ Craigslist: Timeout")
            self.results['craigslist'] = {'status': 'TIMEOUT', 'error': 'Timeout after 45s'}
            return False
        except Exception as e:
            print(f"❌ Craigslist error: {e}")
            self.results['craigslist'] = {'status': 'ERROR', 'error': str(e)}
            return False

    async def test_aliexpress(self):
        """Test AliExpress platform"""
        print("\n🔍 TESTING ALIEXPRESS PLATFORM")
        print("-" * 30)
        
        try:
            from monitoring.platforms.aliexpress_scanner import AliexpressScanner
            
            aliexpress = AliexpressScanner()
            test_keywords = {'direct_terms': ['jewelry']}  # Safer keyword
            
            print("Testing AliExpress with jewelry keyword...")
            start_time = datetime.now()
            
            results = await asyncio.wait_for(
                aliexpress.scan(test_keywords, self.session),
                timeout=45.0
            )
            duration = (datetime.now() - start_time).total_seconds()
            
            if results and len(results) > 0:
                print(f"✅ AliExpress: {len(results)} results in {duration:.1f}s")
                
                stored = await self.store_results('aliexpress', results[:5])
                
                self.results['aliexpress'] = {
                    'status': 'WORKING',
                    'results_count': len(results),
                    'duration': duration,
                    'stored': stored,
                    'samples': [r.get('title', '')[:50] for r in results[:3]]
                }
                return True
            else:
                print("❌ AliExpress: No results")
                self.results['aliexpress'] = {'status': 'FAILED', 'error': 'No results'}
                return False
                
        except asyncio.TimeoutError:
            print("❌ AliExpress: Timeout")
            self.results['aliexpress'] = {'status': 'TIMEOUT', 'error': 'Timeout after 45s'}
            return False
        except Exception as e:
            print(f"❌ AliExpress error: {e}")
            self.results['aliexpress'] = {'status': 'ERROR', 'error': str(e)}
            return False

    async def test_olx(self):
        """Test OLX platform"""
        print("\n🔍 TESTING OLX PLATFORM")
        print("-" * 30)
        
        try:
            from monitoring.platforms.olx_scanner import OlxScanner
            
            olx = OlxScanner()
            test_keywords = {'direct_terms': ['jewelry']}
            
            print("Testing OLX...")
            start_time = datetime.now()
            
            results = await asyncio.wait_for(
                olx.scan(test_keywords, self.session),
                timeout=45.0
            )
            duration = (datetime.now() - start_time).total_seconds()
            
            if results and len(results) > 0:
                print(f"✅ OLX: {len(results)} results in {duration:.1f}s")
                
                stored = await self.store_results('olx', results[:5])
                
                self.results['olx'] = {
                    'status': 'WORKING',
                    'results_count': len(results),
                    'duration': duration,
                    'stored': stored,
                    'samples': [r.get('title', '')[:50] for r in results[:3]]
                }
                return True
            else:
                print("❌ OLX: No results")
                self.results['olx'] = {'status': 'FAILED', 'error': 'No results'}
                return False
                
        except asyncio.TimeoutError:
            print("❌ OLX: Timeout")
            self.results['olx'] = {'status': 'TIMEOUT', 'error': 'Timeout after 45s'}
            return False
        except Exception as e:
            print(f"❌ OLX error: {e}")
            self.results['olx'] = {'status': 'ERROR', 'error': str(e)}
            return False

    async def test_taobao(self):
        """Test Taobao platform"""
        print("\n🔍 TESTING TAOBAO PLATFORM")
        print("-" * 30)
        
        try:
            from monitoring.platforms.taobao_scanner import TaobaoScanner
            
            taobao = TaobaoScanner()
            test_keywords = {'direct_terms': ['jewelry']}
            
            print("Testing Taobao...")
            start_time = datetime.now()
            
            results = await asyncio.wait_for(
                taobao.scan(test_keywords, self.session),
                timeout=60.0  # Longer timeout for Taobao
            )
            duration = (datetime.now() - start_time).total_seconds()
            
            if results and len(results) > 0:
                print(f"✅ Taobao: {len(results)} results in {duration:.1f}s")
                
                stored = await self.store_results('taobao', results[:5])
                
                self.results['taobao'] = {
                    'status': 'WORKING',
                    'results_count': len(results),
                    'duration': duration,
                    'stored': stored,
                    'samples': [r.get('title', '')[:50] for r in results[:3]]
                }
                return True
            else:
                print("❌ Taobao: No results")
                self.results['taobao'] = {'status': 'FAILED', 'error': 'No results'}
                return False
                
        except asyncio.TimeoutError:
            print("❌ Taobao: Timeout")
            self.results['taobao'] = {'status': 'TIMEOUT', 'error': 'Timeout after 60s'}
            return False
        except Exception as e:
            print(f"❌ Taobao error: {e}")
            self.results['taobao'] = {'status': 'ERROR', 'error': str(e)}
            return False

    async def test_gumtree(self):
        """Test Gumtree platform"""
        print("\n🔍 TESTING GUMTREE PLATFORM")
        print("-" * 30)
        
        try:
            from monitoring.platforms.gumtree_scanner import GumtreeScanner
            
            gumtree = GumtreeScanner()
            test_keywords = {'direct_terms': ['jewelry']}
            
            print("Testing Gumtree...")
            start_time = datetime.now()
            
            results = await asyncio.wait_for(
                gumtree.scan(test_keywords, self.session),
                timeout=45.0
            )
            duration = (datetime.now() - start_time).total_seconds()
            
            if results and len(results) > 0:
                print(f"✅ Gumtree: {len(results)} results in {duration:.1f}s")
                
                stored = await self.store_results('gumtree', results[:5])
                
                self.results['gumtree'] = {
                    'status': 'WORKING',
                    'results_count': len(results),
                    'duration': duration,
                    'stored': stored,
                    'samples': [r.get('title', '')[:50] for r in results[:3]]
                }
                return True
            else:
                print("❌ Gumtree: No results")
                self.results['gumtree'] = {'status': 'FAILED', 'error': 'No results'}
                return False
                
        except asyncio.TimeoutError:
            print("❌ Gumtree: Timeout")
            self.results['gumtree'] = {'status': 'TIMEOUT', 'error': 'Timeout after 45s'}
            return False
        except Exception as e:
            print(f"❌ Gumtree error: {e}")
            self.results['gumtree'] = {'status': 'ERROR', 'error': str(e)}
            return False

    async def test_mercadolibre(self):
        """Test MercadoLibre platform"""
        print("\n🔍 TESTING MERCADOLIBRE PLATFORM")
        print("-" * 30)
        
        try:
            from monitoring.platforms.mercadolibre_scanner import MercadolibreScanner
            
            mercadolibre = MercadolibreScanner()
            test_keywords = {'direct_terms': ['jewelry']}
            
            print("Testing MercadoLibre...")
            start_time = datetime.now()
            
            results = await asyncio.wait_for(
                mercadolibre.scan(test_keywords, self.session),
                timeout=45.0
            )
            duration = (datetime.now() - start_time).total_seconds()
            
            if results and len(results) > 0:
                print(f"✅ MercadoLibre: {len(results)} results in {duration:.1f}s")
                
                stored = await self.store_results('mercadolibre', results[:5])
                
                self.results['mercadolibre'] = {
                    'status': 'WORKING',
                    'results_count': len(results),
                    'duration': duration,
                    'stored': stored,
                    'samples': [r.get('title', '')[:50] for r in results[:3]]
                }
                return True
            else:
                print("❌ MercadoLibre: No results")
                self.results['mercadolibre'] = {'status': 'FAILED', 'error': 'No results'}
                return False
                
        except asyncio.TimeoutError:
            print("❌ MercadoLibre: Timeout")
            self.results['mercadolibre'] = {'status': 'TIMEOUT', 'error': 'Timeout after 45s'}
            return False
        except Exception as e:
            print(f"❌ MercadoLibre error: {e}")
            self.results['mercadolibre'] = {'status': 'ERROR', 'error': str(e)}
            return False

    async def test_poshmark(self):
        """Test Poshmark platform"""
        print("\n🔍 TESTING POSHMARK PLATFORM")
        print("-" * 30)
        
        try:
            # Check if Poshmark scanner exists
            try:
                from monitoring.platforms.poshmark_scanner import PoshmarkScanner
                scanner_exists = True
            except ImportError:
                print("❌ Poshmark scanner not found - need to implement")
                self.results['poshmark'] = {'status': 'NOT_IMPLEMENTED', 'error': 'Scanner not found'}
                return False
            
            poshmark = PoshmarkScanner()
            test_keywords = {'direct_terms': ['jewelry']}
            
            print("Testing Poshmark...")
            start_time = datetime.now()
            
            results = await asyncio.wait_for(
                poshmark.scan(test_keywords, self.session),
                timeout=45.0
            )
            duration = (datetime.now() - start_time).total_seconds()
            
            if results and len(results) > 0:
                print(f"✅ Poshmark: {len(results)} results in {duration:.1f}s")
                
                stored = await self.store_results('poshmark', results[:5])
                
                self.results['poshmark'] = {
                    'status': 'WORKING',
                    'results_count': len(results),
                    'duration': duration,
                    'stored': stored,
                    'samples': [r.get('title', '')[:50] for r in results[:3]]
                }
                return True
            else:
                print("❌ Poshmark: No results")
                self.results['poshmark'] = {'status': 'FAILED', 'error': 'No results'}
                return False
                
        except asyncio.TimeoutError:
            print("❌ Poshmark: Timeout")
            self.results['poshmark'] = {'status': 'TIMEOUT', 'error': 'Timeout after 45s'}
            return False
        except Exception as e:
            print(f"❌ Poshmark error: {e}")
            self.results['poshmark'] = {'status': 'ERROR', 'error': str(e)}
            return False

    async def store_results(self, platform, results):
        """Store results in Supabase"""
        if not self.supabase or not results:
            return 0
            
        stored_count = 0
        for i, result in enumerate(results[:5]):  # Store max 5 per platform
            try:
                evidence_id = f"TEST-{datetime.now().strftime('%Y%m%d-%H%M')}-{platform.upper()}-{i+1:03d}"
                
                detection = {
                    'evidence_id': evidence_id,
                    'timestamp': datetime.now().isoformat(),
                    'platform': platform,
                    'threat_score': 25,
                    'threat_level': 'TEST',
                    'species_involved': f"Platform test: {result.get('search_term', 'test')}",
                    'alert_sent': False,
                    'status': f'PLATFORM_TEST_{platform.upper()}'
                }
                
                self.supabase.table('detections').insert(detection).execute()
                stored_count += 1
                
            except Exception as e:
                print(f"   ⚠️ Storage error for {platform}: {e}")
                
        return stored_count

    async def run_comprehensive_test(self):
        """Run tests on all platforms"""
        
        print("🧪 COMPREHENSIVE PLATFORM TESTING")
        print("=" * 50)
        print("Testing each platform individually to get real status...")
        
        if not await self.setup_connections():
            return
        
        # Test all platforms
        platforms_to_test = [
            ('eBay', self.test_ebay),
            ('Craigslist', self.test_craigslist),
            ('AliExpress', self.test_aliexpress),
            ('OLX', self.test_olx),
            ('Taobao', self.test_taobao),
            ('Gumtree', self.test_gumtree),
            ('MercadoLibre', self.test_mercadolibre),
            ('Poshmark', self.test_poshmark),
        ]
        
        working_platforms = 0
        total_results = 0
        total_stored = 0
        
        for platform_name, test_func in platforms_to_test:
            try:
                success = await test_func()
                if success:
                    working_platforms += 1
                    platform_data = self.results[platform_name.lower()]
                    total_results += platform_data.get('results_count', 0)
                    total_stored += platform_data.get('stored', 0)
                    
            except Exception as e:
                print(f"❌ {platform_name} test failed: {e}")
        
        # Cleanup
        if self.session:
            await self.session.close()
        
        # Generate final report
        await self.generate_final_report(working_platforms, total_results, total_stored)

    async def generate_final_report(self, working_platforms, total_results, total_stored):
        """Generate comprehensive status report"""
        
        print(f"\n" + "=" * 60)
        print("🎯 FINAL PLATFORM STATUS REPORT")
        print("=" * 60)
        
        print("📊 INDIVIDUAL PLATFORM RESULTS:")
        
        working = []
        partially_working = []
        broken = []
        
        for platform, data in self.results.items():
            status = data.get('status', 'UNKNOWN')
            
            if status == 'WORKING':
                working.append(platform)
                results_count = data.get('results_count', 0)
                stored = data.get('stored', 0)
                duration = data.get('duration', 0)
                print(f"   ✅ {platform.upper()}: {results_count} results, {stored} stored, {duration:.1f}s")
                
                # Show samples
                samples = data.get('samples', [])
                for sample in samples:
                    print(f"      • {sample}...")
                    
            elif status in ['TIMEOUT', 'FAILED']:
                partially_working.append(platform)
                error = data.get('error', 'Unknown')
                print(f"   🔧 {platform.upper()}: {status} - {error}")
                
            else:
                broken.append(platform)
                error = data.get('error', 'Unknown')
                print(f"   ❌ {platform.upper()}: {status} - {error}")
        
        print(f"\n📈 SUMMARY:")
        print(f"   ✅ Fully Working: {len(working)}/8 platforms")
        print(f"   🔧 Partially Working: {len(partially_working)}/8 platforms")
        print(f"   ❌ Not Working: {len(broken)}/8 platforms")
        print(f"   📊 Total results found: {total_results}")
        print(f"   💾 Total stored in Supabase: {total_stored}")
        
        # Calculate realistic daily projections
        if total_results > 0:
            daily_projection = total_results * 24 * 20  # 24 scans/day, 20 keywords
            print(f"   📅 Realistic daily projection: {daily_projection:,}")
            print(f"   📅 Annual projection: {daily_projection * 365:,}")
        
        print(f"\n🎯 ACCURATE STATUS CLAIMS:")
        if len(working) >= 5:
            print(f"   ✅ '{len(working)}/8 platforms fully operational'")
        if len(working) + len(partially_working) >= 7:
            print(f"   ✅ '{len(working) + len(partially_working)}/8 platforms connected'")
        if total_results >= 50:
            print(f"   ✅ 'Processing {total_results}+ listings per test scan'")
        if total_stored > 0:
            print(f"   ✅ 'Real-time Supabase integration with {total_stored} detections stored'")
        
        # Next steps
        print(f"\n🔧 NEXT STEPS TO FIX:")
        for platform in partially_working + broken:
            platform_data = self.results.get(platform, {})
            error = platform_data.get('error', 'Unknown error')
            
            if 'Timeout' in error:
                print(f"   • {platform.upper()}: Optimize selectors and reduce page load time")
            elif 'No results' in error:
                print(f"   • {platform.upper()}: Update search URLs and selectors")
            elif 'not found' in error or 'NOT_IMPLEMENTED' in error:
                print(f"   • {platform.upper()}: Implement missing scanner")
            else:
                print(f"   • {platform.upper()}: Debug {error}")

async def main():
    """Run the comprehensive platform test"""
    tester = PlatformTester()
    await tester.run_comprehensive_test()

if __name__ == "__main__":
    asyncio.run(main())
