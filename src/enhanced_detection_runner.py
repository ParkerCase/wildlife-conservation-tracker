#!/usr/bin/env python3
"""
WildGuard AI - Enhanced Production Detection Runner
Integrates quality filtering with existing platform scanners
Target: 100-200k quality detections daily with <20% UNRATED
"""

import asyncio
import aiohttp
import os
import json
import logging
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any, Set
import traceback
import time
import random
import hashlib
from pathlib import Path

# Import existing components
from comprehensive_endangered_keywords import (
    ALL_ENDANGERED_SPECIES_KEYWORDS, 
    TIER_1_CRITICAL_SPECIES,
    TIER_2_HIGH_PRIORITY_SPECIES
)

# Import quality filter
sys.path.append('/Users/parkercase/conservation-bot/src')
from quality_filters import WildlifeQualityFilter

# Import existing scanner
from final_production_scanner import FinalProductionScanner

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/tmp/enhanced_wildguard.log')
    ]
)

class EnhancedWildlifeDetectionRunner:
    """Enhanced detection runner with quality filtering and optimized performance"""
    
    def __init__(self):
        self.quality_filter = WildlifeQualityFilter()
        self.scanner = FinalProductionScanner()
        
        # Performance tracking
        self.session_stats = {
            'total_scanned': 0,
            'total_accepted': 0,
            'total_rejected': 0,
            'total_stored': 0,
            'start_time': datetime.now(),
            'by_platform': {},
            'by_threat_level': {
                'CRITICAL': 0,
                'HIGH': 0,
                'MEDIUM': 0,
                'LOW': 0,
                'UNRATED': 0
            },
            'rejection_reasons': {}
        }
        
        # URL deduplication
        self.seen_urls: Set[str] = set()
        self.load_url_cache()
        
        # Keyword management with better rotation (OPTIMIZED)
        self.keyword_batch_size = int(os.getenv('BATCH_SIZE', '100'))  # Doubled from 50
        self.current_keyword_index = 0
        self.multilingual_keywords = self.load_multilingual_keywords()
        
        # Historical backfill settings
        self.enable_historical = os.getenv('ENABLE_HISTORICAL_BACKFILL', 'true').lower() == 'true'
        self.historical_days = int(os.getenv('HISTORICAL_DAYS', '60'))
        
        # Platform performance weights (OPTIMIZED for 150-200K daily)
        self.platform_weights = {
            'avito': 5,      # 130K+ daily (STAR PERFORMER - increased)
            'ebay': 3,       # 40K+ daily (increased)
            'marktplaats': 3, # 35K+ daily (increased)
            'craigslist': 2,  # 35K+ daily (increased)
            'olx': 2,        # 25K+ daily (increased)
            'mercadolibre': 2, # 35K+ daily (increased)
            'facebook_marketplace': 1, # 1.4K+ daily (rate limited)
            'gumtree': 1     # 10K+ daily
        }
        
        # Environment validation
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        if not all([self.supabase_url, self.supabase_key]):
            logging.error("❌ Missing required environment variables")
            raise ValueError("SUPABASE_URL and SUPABASE_KEY are required")
        
        logging.info("🚀 Enhanced WildGuard Detection Runner Initialized")
        logging.info(f"🎯 Target: 100-200k quality detections daily")
        logging.info(f"🔍 Quality Filter: Active (targeting <15% UNRATED)")
        logging.info(f"📊 Keywords: {len(self.multilingual_keywords):,} multilingual")
        logging.info(f"🎯 Batch Size: {self.keyword_batch_size} keywords per cycle")
        logging.info(f"📅 Historical Backfill: {'ENABLED' if self.enable_historical else 'DISABLED'} ({self.historical_days} days)")
        if self.enable_historical:
            logging.info(f"📅 Historical Strategy: Every 5th cycle scans {self.historical_days}+ day old listings")
        
        # Print quality filter stats
        filter_stats = self.quality_filter.get_filter_stats()
        logging.info(f"🛡️ Filter Rules: {filter_stats['total_reject_terms']} reject terms, {filter_stats['total_wildlife_terms']} wildlife terms")
        
        # URL deduplication with enhanced checking
        self.url_hashes = set()  # Track URL hashes for faster duplicate checking

    def load_multilingual_keywords(self) -> List[str]:
        """Load multilingual keywords with smart prioritization"""
        try:
            # Load from existing multilingual file
            keywords_file = Path('/Users/parkercase/conservation-bot/multilingual_wildlife_keywords.json')
            if keywords_file.exists():
                with open(keywords_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                all_keywords = []
                for lang, keywords in data['keywords_by_language'].items():
                    all_keywords.extend(keywords)
                
                # Remove duplicates and shuffle
                all_keywords = list(set(all_keywords))
                random.shuffle(all_keywords)
                
                logging.info(f"✅ Loaded {len(all_keywords):,} multilingual keywords")
                return all_keywords
            
        except Exception as e:
            logging.warning(f"Could not load multilingual keywords: {e}")
        
        # Fallback to comprehensive keywords
        keywords = list(set(ALL_ENDANGERED_SPECIES_KEYWORDS))
        random.shuffle(keywords)
        logging.info(f"🔄 Using fallback keywords: {len(keywords):,}")
        return keywords

    def load_url_cache(self):
        """Load URL cache for deduplication"""
        try:
            cache_file = Path('/tmp/enhanced_wildguard_urls.json')
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    self.seen_urls = set(data.get('seen_urls', []))
                    logging.info(f"📁 Loaded {len(self.seen_urls):,} URLs from cache")
        except Exception as e:
            logging.warning(f"Cache load error: {e}")
            self.seen_urls = set()

    def save_url_cache(self):
        """Save URL cache with rotation"""
        try:
            # Keep cache manageable
            if len(self.seen_urls) > 150000:
                self.seen_urls = set(list(self.seen_urls)[-100000:])
            
            cache_file = Path('/tmp/enhanced_wildguard_urls.json')
            data = {'seen_urls': list(self.seen_urls), 'updated': datetime.now().isoformat()}
            with open(cache_file, 'w') as f:
                json.dump(data, f)
            
            logging.debug(f"💾 Saved {len(self.seen_urls):,} URLs to cache")
        except Exception as e:
            logging.warning(f"Cache save error: {e}")

    def get_next_keyword_batch(self) -> List[str]:
        """Get next batch of keywords with smart rotation (OPTIMIZED)"""
        # Enhanced prioritization for better performance
        if self.current_keyword_index % 3 == 0:
            available_keywords = TIER_1_CRITICAL_SPECIES
            batch_name = "Critical Species"
        elif self.current_keyword_index % 2 == 0:
            available_keywords = TIER_2_HIGH_PRIORITY_SPECIES
            batch_name = "High Priority"
        else:
            available_keywords = self.multilingual_keywords
            batch_name = "Multilingual"
        
        # Get batch
        start_idx = (self.current_keyword_index * self.keyword_batch_size) % len(available_keywords)
        end_idx = min(start_idx + self.keyword_batch_size, len(available_keywords))
        
        if end_idx - start_idx < self.keyword_batch_size and len(available_keywords) > self.keyword_batch_size:
            # Wrap around if needed
            batch = available_keywords[start_idx:] + available_keywords[:self.keyword_batch_size - (end_idx - start_idx)]
        else:
            batch = available_keywords[start_idx:end_idx]
        
        self.current_keyword_index += 1
        
        logging.info(f"🔑 Keyword batch {self.current_keyword_index}: {len(batch)} {batch_name} keywords")
        return batch

    def get_next_platform(self) -> str:
        """Get next platform with weighted selection"""
        # Create weighted list
        weighted_platforms = []
        for platform, weight in self.platform_weights.items():
            weighted_platforms.extend([platform] * weight)
        
        # Random selection from weighted list
        platform = random.choice(weighted_platforms)
        
        # Initialize platform stats if needed
        if platform not in self.session_stats['by_platform']:
            self.session_stats['by_platform'][platform] = {
                'scanned': 0, 'accepted': 0, 'rejected': 0, 'stored': 0
            }
        
        return platform

    async def process_platform_results(self, platform: str, raw_results: List[Dict], keywords: List[str], historical_mode: bool = False) -> int:
        """Process results through quality filter and store high-quality ones (ENHANCED with duplicate prevention)"""
        if not raw_results:
            return 0
        
        platform_stats = self.session_stats['by_platform'][platform]
        accepted_results = []
        
        for result in raw_results:
            self.session_stats['total_scanned'] += 1
            platform_stats['scanned'] += 1
            
            # Enhanced duplicate prevention
            url = result.get('url', '')
            if url in self.seen_urls:
                continue
            
            # Additional hash-based duplicate checking for performance
            url_hash = hashlib.md5(url.encode()).hexdigest()[:16]
            if url_hash in self.url_hashes:
                continue
            self.url_hashes.add(url_hash)
            
            # Apply quality filter
            quality_assessment = self.quality_filter.assess_quality(result)
            
            if quality_assessment['shouldInclude']:
                # Accept high-quality result
                self.session_stats['total_accepted'] += 1
                platform_stats['accepted'] += 1
                
                # Track threat level
                threat_level = quality_assessment['threatLevel']
                self.session_stats['by_threat_level'][threat_level] += 1
                
                # Enhance result with quality data and historical flag
                enhanced_result = {
                    **result,
                    'quality_score': quality_assessment['qualityScore'],
                    'threat_level': threat_level,
                    'confidence': quality_assessment['confidence'],
                    'platform': platform,
                    'keywords_used': keywords[:5],  # First 5 keywords for reference
                    'scan_timestamp': datetime.now().isoformat(),
                    'historical_scan': historical_mode,
                    'backfill_days': self.historical_days if historical_mode else 0
                }
                
                accepted_results.append(enhanced_result)
                self.seen_urls.add(url)
                
                logging.debug(f"✅ {platform}: {result.get('title', '')[:50]}... ({threat_level}, {quality_assessment['qualityScore']:.1%})")
            
            else:
                # Reject low-quality result
                self.session_stats['total_rejected'] += 1
                platform_stats['rejected'] += 1
                
                # Track rejection reason
                reason = quality_assessment.get('reason', 'Unknown')
                self.session_stats['rejection_reasons'][reason] = self.session_stats['rejection_reasons'].get(reason, 0) + 1
                
                logging.debug(f"❌ {platform}: {result.get('title', '')[:50]}... (Rejected: {reason})")
        
        # Store accepted results
        stored_count = await self.store_results(accepted_results)
        self.session_stats['total_stored'] += stored_count
        platform_stats['stored'] += stored_count
        
        logging.info(f"📊 {platform}{'[HIST]' if historical_mode else ''}: {len(raw_results)} scanned → {len(accepted_results)} accepted → {stored_count} stored")
        
        return stored_count

    async def store_results(self, results: List[Dict]) -> int:
        """Store quality results in Supabase"""
        if not results:
            return 0
        
        stored_count = 0
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        
        async with aiohttp.ClientSession() as session:
            for result in results:
                try:
                    # Create detection record
                    evidence_id = f"ENHANCED-{result['platform'].upper()}-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{result.get('item_id', 'unknown')}"
                    
                    detection = {
                        'evidence_id': evidence_id,
                        'timestamp': datetime.now().isoformat(),
                        'platform': result['platform'],
                        'threat_score': int(result['quality_score'] * 100),
                        'threat_level': result['threat_level'],
                        'species_involved': f"Keywords: {', '.join(result.get('keywords_used', []))}",
                        'alert_sent': result['threat_level'] in ['CRITICAL', 'HIGH'],
                        'status': f'ENHANCED_PRODUCTION_{result["platform"].upper()}' + ('_HISTORICAL' if result.get('historical_scan') else ''),
                        'listing_title': (result.get('title', '') or '')[:500],
                        'listing_url': result.get('url', '') or '',
                        'listing_price': str(result.get('price', '') or ''),
                        'search_term': result.get('search_term', '') or '',
                        'confidence_score': int(result['confidence'] * 100),
                        'quality_score': result['quality_score'],
                        'enhanced_scan': True
                    }
                    
                    url = f"{self.supabase_url}/rest/v1/detections"
                    
                    async with session.post(url, headers=headers, json=detection) as resp:
                        if resp.status in [200, 201]:
                            stored_count += 1
                        elif resp.status == 409:
                            # Duplicate - skip silently
                            continue
                        else:
                            response_text = await resp.text()
                            if 'duplicate' not in response_text.lower():
                                logging.warning(f"Storage error {resp.status}: {response_text[:100]}")
                
                except Exception as e:
                    if 'duplicate' not in str(e).lower():
                        logging.warning(f"Storage error: {e}")
                    continue
        
        return stored_count

    async def run_historical_backfill(self, platform: str, keywords: List[str]) -> int:
        """Run historical backfill scan for older listings (2+ months)"""
        if not self.enable_historical:
            logging.debug(f"Historical backfill disabled for {platform}")
            return 0
            
        logging.info(f"🕰️ Running historical backfill for {platform} ({self.historical_days} days back)")
        
        try:
            # Scan platform with historical mode enabled
            historical_results = await self.scanner.scan_platform_with_keywords(
                platform, keywords, historical_mode=True
            )
            
            # Process historical results with historical flag
            stored_count = await self.process_platform_results(
                platform, historical_results, keywords, historical_mode=True
            )
            
            logging.info(f"📚 Historical backfill {platform}: {stored_count} stored")
            return stored_count
            
        except Exception as e:
            logging.error(f"Historical backfill error for {platform}: {e}")
            return 0

    async def run_enhanced_scan_cycle(self, duration_hours: float = 3.0) -> Dict[str, Any]:
        """Run enhanced scanning cycle with quality filtering"""
        logging.info(f"🚀 Starting enhanced scan cycle ({duration_hours} hours)")
        
        end_time = datetime.now() + timedelta(hours=duration_hours)
        cycle_count = 0
        
        # Initialize scanner session
        async with self.scanner:
            while datetime.now() < end_time:
                cycle_count += 1
                cycle_start = datetime.now()
                
                # Get next platform and keywords
                platform = self.get_next_platform()
                keywords = self.get_next_keyword_batch()
                
                logging.info(f"🔄 Cycle {cycle_count}: {platform} with {len(keywords)} keywords")
                
                try:
                    # Primary scan - current listings
                    raw_results = await self.scanner.scan_platform_with_keywords(platform, keywords)
                    stored_count = await self.process_platform_results(platform, raw_results, keywords)
                    
                    # Historical backfill scan (every 5th cycle to avoid overload)
                    if cycle_count % 5 == 0 and self.enable_historical:
                        historical_count = await self.run_historical_backfill(platform, keywords)
                        stored_count += historical_count
                    
                    # Calculate performance metrics
                    cycle_duration = (datetime.now() - cycle_start).total_seconds()
                    total_runtime = (datetime.now() - self.session_stats['start_time']).total_seconds()
                    
                    if total_runtime > 0:
                        hourly_rate = int(self.session_stats['total_stored'] * 3600 / total_runtime)
                        daily_projection = hourly_rate * 24
                        acceptance_rate = (self.session_stats['total_accepted'] / max(1, self.session_stats['total_scanned'])) * 100
                        
                        logging.info(f"📈 Performance: {hourly_rate:,}/hr → {daily_projection:,}/day (Accept: {acceptance_rate:.1f}%)")
                        
                        # Performance status
                        if daily_projection >= 150000:
                            logging.info("🎉 EXCEEDING TARGET!")
                        elif daily_projection >= 100000:
                            logging.info("✅ Meeting target")
                        else:
                            logging.info("⚠️ Below target")
                    
                    # Optimized adaptive delays for higher performance
                    if platform == 'avito':
                        delay = 20  # REDUCED - Even shorter for star performer
                    elif platform == 'facebook_marketplace':
                        delay = 90  # MAINTAIN - Keep safe for rate limits
                    elif platform in ['ebay', 'marktplaats', 'craigslist']:
                        delay = 25  # REDUCED - Faster for high performers
                    else:
                        delay = 35  # REDUCED - Faster standard delay
                    
                    logging.info(f"⏳ Waiting {delay}s...")
                    await asyncio.sleep(delay)
                    
                    # Save cache periodically
                    if cycle_count % 10 == 0:
                        self.save_url_cache()
                
                except Exception as e:
                    logging.error(f"Cycle {cycle_count} error: {e}")
                    await asyncio.sleep(60)  # Error recovery delay
        
        # Final stats
        total_runtime = (datetime.now() - self.session_stats['start_time']).total_seconds()
        final_stats = self.calculate_final_stats(total_runtime)
        
        # Save final cache
        self.save_url_cache()
        
        return final_stats

    def calculate_final_stats(self, runtime_seconds: float) -> Dict[str, Any]:
        """Calculate comprehensive final statistics"""
        stats = {
            'session_summary': {
                'runtime_hours': round(runtime_seconds / 3600, 2),
                'total_scanned': self.session_stats['total_scanned'],
                'total_accepted': self.session_stats['total_accepted'],
                'total_rejected': self.session_stats['total_rejected'],
                'total_stored': self.session_stats['total_stored'],
                'acceptance_rate': round((self.session_stats['total_accepted'] / max(1, self.session_stats['total_scanned'])) * 100, 1),
                'storage_success_rate': round((self.session_stats['total_stored'] / max(1, self.session_stats['total_accepted'])) * 100, 1)
            },
            'performance_metrics': {
                'hourly_rate': int(self.session_stats['total_stored'] * 3600 / max(1, runtime_seconds)),
                'daily_projection': int(self.session_stats['total_stored'] * 24 * 3600 / max(1, runtime_seconds)),
                'weekly_projection': int(self.session_stats['total_stored'] * 7 * 24 * 3600 / max(1, runtime_seconds)),
                'monthly_projection': int(self.session_stats['total_stored'] * 30 * 24 * 3600 / max(1, runtime_seconds))
            },
            'threat_distribution': self.session_stats['by_threat_level'],
            'platform_performance': self.session_stats['by_platform'],
            'top_rejection_reasons': dict(sorted(self.session_stats['rejection_reasons'].items(), key=lambda x: x[1], reverse=True)[:10]),
            'quality_metrics': {
                'unrated_percentage': round((self.session_stats['by_threat_level']['UNRATED'] / max(1, self.session_stats['total_scanned'])) * 100, 1),
                'high_threat_percentage': round(((self.session_stats['by_threat_level']['CRITICAL'] + self.session_stats['by_threat_level']['HIGH']) / max(1, self.session_stats['total_accepted'])) * 100, 1)
            }
        }
        
        return stats

    def print_final_report(self, stats: Dict[str, Any]):
        """Print comprehensive final report"""
        print("\n" + "="*80)
        print("🎯 ENHANCED WILDGUARD DETECTION RUNNER - FINAL REPORT")
        print("="*80)
        
        # Session Summary
        summary = stats['session_summary']
        print(f"\n📊 SESSION SUMMARY:")
        print(f"   Runtime: {summary['runtime_hours']} hours")
        print(f"   Scanned: {summary['total_scanned']:,} listings")
        print(f"   Accepted: {summary['total_accepted']:,} ({summary['acceptance_rate']}%)")
        print(f"   Rejected: {summary['total_rejected']:,}")
        print(f"   Stored: {summary['total_stored']:,} ({summary['storage_success_rate']}% success)")
        
        # Performance Metrics
        perf = stats['performance_metrics']
        print(f"\n🚀 PERFORMANCE METRICS:")
        print(f"   Hourly Rate: {perf['hourly_rate']:,} detections/hour")
        print(f"   Daily Projection: {perf['daily_projection']:,} detections/day")
        print(f"   Weekly Projection: {perf['weekly_projection']:,} detections/week")
        print(f"   Monthly Projection: {perf['monthly_projection']:,} detections/month")
        
        # Target Assessment
        daily_proj = perf['daily_projection']
        if daily_proj >= 200000:
            print(f"   🎉 STATUS: EXCEEDING TARGET! ({daily_proj:,} ≥ 200k)")
        elif daily_proj >= 100000:
            print(f"   ✅ STATUS: MEETING TARGET ({daily_proj:,} ≥ 100k)")
        else:
            print(f"   ⚠️ STATUS: BELOW TARGET ({daily_proj:,} < 100k)")
        
        # Threat Distribution
        threat = stats['threat_distribution']
        print(f"\n🔍 THREAT LEVEL DISTRIBUTION:")
        for level, count in threat.items():
            percentage = (count / max(1, summary['total_scanned'])) * 100
            print(f"   {level}: {count:,} ({percentage:.1f}%)")
        
        # Quality Assessment
        quality = stats['quality_metrics']
        print(f"\n🛡️ QUALITY ASSESSMENT:")
        print(f"   UNRATED Rate: {quality['unrated_percentage']}% (Target: <20%)")
        print(f"   High Threat Rate: {quality['high_threat_percentage']}% of accepted")
        
        if quality['unrated_percentage'] < 20:
            print(f"   ✅ QUALITY TARGET MET!")
        else:
            print(f"   ⚠️ QUALITY TARGET MISSED")
        
        # Platform Performance
        print(f"\n🌍 PLATFORM PERFORMANCE:")
        for platform, stats_data in stats['platform_performance'].items():
            if stats_data['scanned'] > 0:
                accept_rate = (stats_data['accepted'] / stats_data['scanned']) * 100
                print(f"   {platform}: {stats_data['stored']:,} stored ({accept_rate:.1f}% accept rate)")
        
        # Top Rejection Reasons
        if stats['top_rejection_reasons']:
            print(f"\n❌ TOP REJECTION REASONS:")
            for reason, count in list(stats['top_rejection_reasons'].items())[:5]:
                print(f"   {reason}: {count:,}")
        
        print("\n" + "="*80)

# Main execution
async def run_enhanced_detection():
    """Main entry point for enhanced detection"""
    try:
        # Get duration from environment or default to 3 hours
        duration = float(os.getenv('SCAN_DURATION', '3'))
        
        # Initialize and run
        runner = EnhancedWildlifeDetectionRunner()
        
        print(f"🚀 Starting Enhanced WildGuard Detection Runner")
        print(f"⏰ Duration: {duration} hours")
        print(f"🎯 Target: 100-200k quality detections daily")
        print(f"🔍 Quality filtering: Active (targeting <20% UNRATED)")
        print("-" * 80)
        
        # Run the enhanced scan
        final_stats = await runner.run_enhanced_scan_cycle(duration)
        
        # Print final report
        runner.print_final_report(final_stats)
        
        # Save detailed stats
        stats_file = f"/tmp/enhanced_scan_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(stats_file, 'w') as f:
            json.dump(final_stats, f, indent=2, default=str)
        
        print(f"💾 Detailed stats saved to: {stats_file}")
        
        return final_stats
        
    except Exception as e:
        logging.error(f"Critical error: {e}")
        logging.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    asyncio.run(run_enhanced_detection())
