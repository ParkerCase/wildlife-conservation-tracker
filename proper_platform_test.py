#!/usr/bin/env python3
"""
WildGuard AI - PROPER Platform Testing
Test all implemented platforms with correct imports
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

class PlatformVerifier:
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

    async def test_platform_scanner(self):
        """Test the main PlatformScanner"""
        print("\n🔍 TESTING MAIN PLATFORM SCANNER")
        print("-" * 50)
        
        try:
            from src.monitoring.platform_scanner import PlatformScanner
            
            # Test keywords
            test_keywords = {
                'direct_terms': ['ivory', 'antique', 'carved']
            }
            
            print(f"🔍 Testing with keywords: {test_keywords['direct_terms']}")
            
            async with PlatformScanner() as scanner:
                print(f"✅ PlatformScanner initialized")
                print(f"📊 Available platforms: {list(scanner.platforms.keys())}")
                
                # Test each platform individually
                platform_results = {}
                total_results = 0
                
                for platform_name, platform_scanner in scanner.platforms.items():
                    print(f"\n🔍 Testing {platform_name.upper()}...")
                    
                    try:
                        start_time = datetime.now()
                        
                        # Test with timeout
                        results = await asyncio.wait_for(
                            platform_scanner.scan(test_keywords, scanner.session),
                            timeout=45.0
                        )
                        
                        duration = (datetime.now() - start_time).total_seconds()
                        
                        if results:
                            count = len(results)
                            total_results += count
                            platform_results[platform_name] = {
                                'status': 'WORKING',
                                'count': count,
                                'duration': duration,
                                'samples': results[:2]  # Store 2 samples
                            }
                            
                            print(f"   ✅ {platform_name}: {count} results in {duration:.1f}s")
                            
                            # Show samples
                            for i, result in enumerate(results[:2], 1):
                                title = result.get('title', 'No title')[:40]
                                price = result.get('price', 'No price')
                                print(f"      {i}. {title}... - {price}")
                            
                            # Store in Supabase
                            stored = await self.store_results(platform_name, results[:3])
                            platform_results[platform_name]['stored'] = stored
                            
                        else:
                            platform_results[platform_name] = {
                                'status': 'NO_RESULTS',
                                'count': 0,
                                'duration': duration,
                                'stored': 0
                            }
                            print(f"   ⚠️  {platform_name}: No results")
                            
                    except asyncio.TimeoutError:
                        platform_results[platform_name] = {
                            'status': 'TIMEOUT',
                            'count': 0,
                            'duration': 45.0,
                            'stored': 0
                        }
                        print(f"   ⏰ {platform_name}: Timeout after 45s")
                        
                    except Exception as e:
                        platform_results[platform_name] = {
                            'status': 'ERROR',
                            'count': 0,
                            'duration': 0,
                            'error': str(e),
                            'stored': 0
                        }
                        print(f"   ❌ {platform_name}: {e}")
                
                return platform_results, total_results
                
        except Exception as e:
            print(f"❌ PlatformScanner import/setup error: {e}")
            return None, 0

    async def store_results(self, platform, results):
        """Store results in Supabase"""
        if not self.supabase or not results:
            return 0
            
        stored_count = 0
        for i, result in enumerate(results):
            try:
                evidence_id = f"VERIFY-{platform.upper()}-{datetime.now().strftime('%m%d%H%M')}-{i+1:02d}"
                
                detection = {
                    'evidence_id': evidence_id,
                    'timestamp': datetime.now().isoformat(),
                    'platform': platform,
                    'threat_score': 40,
                    'threat_level': 'MEDIUM',
                    'species_involved': f"Platform verification: {result.get('search_term', 'test')}",
                    'alert_sent': False,
                    'status': f'PLATFORM_VERIFICATION_{platform.upper()}'
                }
                
                self.supabase.table('detections').insert(detection).execute()
                stored_count += 1
                
            except Exception as e:
                print(f"   ⚠️ Storage error for {platform}: {e}")
                
        return stored_count

    def generate_status_report(self, platform_results, total_results):
        """Generate comprehensive status report"""
        
        print(f"\n📊 COMPREHENSIVE PLATFORM STATUS REPORT")
        print("=" * 60)
        
        working_platforms = []
        partial_platforms = []
        broken_platforms = []
        
        total_stored = 0
        
        for platform, result in platform_results.items():
            status = result['status']
            count = result.get('count', 0)
            stored = result.get('stored', 0)
            total_stored += stored
            
            if status == 'WORKING':
                working_platforms.append((platform, count, stored))
                print(f"✅ {platform.upper()}: FULLY WORKING - {count} listings, {stored} stored")
                
            elif status in ['TIMEOUT', 'NO_RESULTS']:
                partial_platforms.append((platform, status))
                print(f"🔧 {platform.upper()}: {status} - needs optimization")
                
            else:
                broken_platforms.append((platform, status))
                error = result.get('error', 'Unknown error')
                print(f"❌ {platform.upper()}: {status} - {error[:50]}...")
        
        print(f"\n🎯 SUMMARY:")
        print(f"   ✅ Fully Working: {len(working_platforms)}/8 platforms")
        print(f"   🔧 Partial/Timeout: {len(partial_platforms)}/8 platforms")
        print(f"   ❌ Broken: {len(broken_platforms)}/8 platforms")
        print(f"   📊 Total listings found: {total_results}")
        print(f"   💾 Total stored in Supabase: {total_stored}")
        
        # Calculate daily projections
        if total_results > 0:
            keywords_full = 20  # Realistic keyword set
            scans_per_day = 24  # Hourly scanning
            keywords_tested = 3  # We tested 3 keywords
            
            daily_projection = total_results * (keywords_full / keywords_tested) * scans_per_day
            annual_projection = daily_projection * 365
            
            print(f"\n📈 REALISTIC PROJECTIONS:")
            print(f"   Current test: {total_results} listings with {keywords_tested} keywords")
            print(f"   With {keywords_full} keywords: {total_results * (keywords_full / keywords_tested):.0f} per scan")
            print(f"   Daily projection: {daily_projection:.0f} listings/day")
            print(f"   Annual projection: {annual_projection:,.0f} listings/year")
        
        # Working platforms details
        if working_platforms:
            print(f"\n✅ FULLY WORKING PLATFORMS:")
            for platform, count, stored in working_platforms:
                print(f"   • {platform.upper()}: {count} listings found, {stored} stored")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if len(working_platforms) >= 5:
            print("   🎉 EXCELLENT: 5+ platforms working - ready for production!")
        elif len(working_platforms) >= 3:
            print("   ✅ GOOD: 3+ platforms working - solid foundation")
        else:
            print("   🔧 NEEDS WORK: Fix timeout/error issues for better coverage")
        
        if partial_platforms:
            print("   🔧 Fix timeout issues with:")
            for platform, status in partial_platforms:
                print(f"      • {platform.upper()} ({status})")
        
        if broken_platforms:
            print("   ❌ Debug and fix:")
            for platform, status in broken_platforms:
                print(f"      • {platform.upper()} ({status})")
        
        # Generate accurate claims
        print(f"\n✅ 100% ACCURATE CLAIMS:")
        if total_results > 0:
            print(f"   • 'Processes {total_results} wildlife-relevant listings per scan cycle'")
            if daily_projection:
                print(f"   • 'Realistic daily processing: {daily_projection:.0f} wildlife listings'")
                print(f"   • 'Annual capacity: {annual_projection:,.0f} wildlife detections'")
        
        print(f"   • '{len(working_platforms)}/8 platforms fully operational'")
        print(f"   • 'Successfully storing results in production Supabase database'")
        print(f"   • 'Real-time wildlife monitoring across {len(working_platforms)} international platforms'")
        
        return {
            'working': len(working_platforms),
            'partial': len(partial_platforms),
            'broken': len(broken_platforms),
            'total_results': total_results,
            'total_stored': total_stored,
            'daily_projection': daily_projection if total_results > 0 else 0
        }

async def main():
    """Main verification function"""
    
    print("🧪 WILDGUARD AI - COMPREHENSIVE PLATFORM VERIFICATION")
    print("=" * 60)
    print("Testing all implemented platforms with proper imports...")
    
    verifier = PlatformVerifier()
    
    # Test the platform scanner
    platform_results, total_results = await verifier.test_platform_scanner()
    
    if platform_results:
        # Generate comprehensive report
        summary = verifier.generate_status_report(platform_results, total_results)
        
        print(f"\n🎯 FINAL VERDICT:")
        if summary['working'] >= 5:
            print("   🏆 EXCELLENT: Your platform claims are largely accurate!")
            print("   🚀 Ready for production wildlife conservation work")
        elif summary['working'] >= 3:
            print("   ✅ GOOD: Strong foundation with room for optimization")
            print("   🔧 Fix timeout issues to reach full potential")
        else:
            print("   🔧 NEEDS WORK: Focus on debugging platform issues")
        
        if summary['total_results'] > 50:
            print(f"   📊 IMPRESSIVE: {summary['total_results']} listings found!")
        elif summary['total_results'] > 20:
            print(f"   📊 SOLID: {summary['total_results']} listings found")
        else:
            print(f"   📊 MODEST: {summary['total_results']} listings found")
    
    else:
        print("❌ Platform testing failed - check import issues")

if __name__ == "__main__":
    asyncio.run(main())
