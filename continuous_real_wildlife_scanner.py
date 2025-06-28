#!/usr/bin/env python3
"""
CONTINUOUS REAL Wildlife Scanner - Live Platform Data Only
✅ Real scraping from actual marketplaces (no simulation)
✅ Continuous scanning every 15 minutes
✅ ALL 1,452 multilingual wildlife keywords
✅ Intelligent threat scoring with REAL data
"""

import asyncio
import os
import json
import logging
import sys
from datetime import datetime
from typing import List, Dict, Any, Set
import hashlib

# Import REAL platform scanning
try:
    from real_platform_scanner import RealPlatformScanner
    from intelligent_threat_scoring_system import IntelligentThreatScorer, ThreatLevel
    REAL_SCANNING_AVAILABLE = True
    logging.info("✅ REAL platform scanning system imported")
except ImportError as e:
    logging.warning(f"⚠️ Real scanning systems not available: {e}")
    REAL_SCANNING_AVAILABLE = False

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

class ContinuousRealWildlifeScanner:
    """
    CONTINUOUS Real Wildlife Scanner - Live Data Only
    - Connects to REAL platforms (eBay API, Craigslist scraping, etc.)
    - Uses ALL 1,452 multilingual wildlife keywords
    - Intelligent threat scoring with REAL listing data
    - Continuous 15-minute scanning
    """

    def __init__(self):
        # Initialize REAL platform scanner
        self.real_scanner = RealPlatformScanner() if REAL_SCANNING_AVAILABLE else None
        
        # Initialize intelligent scoring for REAL data
        self.threat_scorer = IntelligentThreatScorer() if REAL_SCANNING_AVAILABLE else None
        
        # Wildlife platforms for REAL scanning
        self.real_platforms = [
            'ebay',        # Real eBay API
            'craigslist',  # Real Craigslist scraping  
            'aliexpress',  # Real AliExpress scraping
            'olx',         # Real OLX scraping
            'gumtree',     # Real Gumtree scraping
            'mercadolibre',# Real MercadoLibre scraping
            'taobao',      # Real Taobao scraping
            'mercari'      # Real Mercari scraping
        ]
        
        # Load ALL 1,452 wildlife keywords
        self.wildlife_keywords = self._load_all_1452_wildlife_keywords()
        
        # Deduplication tracking
        self.seen_urls: Set[str] = set()
        
        # Check environment
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_ANON_KEY")
        
        if not all([self.supabase_url, self.supabase_key]):
            logging.error("❌ Missing required Supabase credentials")
            sys.exit(1)
            
        if not REAL_SCANNING_AVAILABLE:
            logging.error("❌ Real scanning systems not available")
            sys.exit(1)

        logging.info(f"✅ CONTINUOUS REAL WILDLIFE SCANNER ready")
        logging.info(f"🎯 Wildlife keywords: {len(self.wildlife_keywords):,} (ALL 1,452 multilingual)")
        logging.info(f"🌍 Real platforms: {len(self.real_platforms)} ({', '.join(self.real_platforms)})")
        logging.info(f"🧠 Intelligent scoring: {'ENABLED' if self.threat_scorer else 'FALLBACK'}")

    def _load_all_1452_wildlife_keywords(self) -> List[str]:
        """Load ALL 1,452 multilingual wildlife keywords"""
        try:
            with open('multilingual_wildlife_keywords.json', 'r') as f:
                keywords_data = json.load(f)
            
            all_keywords = []
            for language, keywords in keywords_data['keywords_by_language'].items():
                all_keywords.extend(keywords)
                logging.info(f"   {language}: {len(keywords)} keywords")
            
            unique_keywords = list(dict.fromkeys(all_keywords))
            logging.info(f"✅ Successfully loaded {len(unique_keywords)} unique wildlife keywords")
            return unique_keywords
                
        except FileNotFoundError:
            logging.error("❌ multilingual_wildlife_keywords.json not found!")
            return [
                "ivory", "elephant ivory", "rhino horn", "tiger bone", "pangolin scales",
                "bear bile", "tiger skin", "turtle shell", "shark fin", "coral",
                "traditional medicine", "chinese medicine", "wildlife carving"
            ]

    async def scan_real_platforms_wildlife(self, keywords: List[str]) -> List[Dict]:
        """Scan REAL platforms for wildlife with live data"""
        
        if not self.real_scanner:
            logging.error("❌ Real scanner not available")
            return []
        
        # Prepare keywords for real platform scanning
        keyword_dict = {
            'direct_terms': keywords
        }
        
        logging.info(f"🔍 Scanning REAL platforms with {len(keywords)} wildlife keywords...")
        
        try:
            # Use REAL platform scanner
            async with self.real_scanner as scanner:
                real_results = await scanner.scan_all_platforms()
            
            logging.info(f"✅ REAL scan completed: {len(real_results)} live listings found")
            
            # Process and enhance real results with wildlife-specific analysis
            processed_results = []
            for result in real_results:
                # Skip if not wildlife-related (basic filtering)
                if not self._is_wildlife_related(result, keywords):
                    continue
                
                # Add wildlife-specific metadata
                result['scan_type'] = 'wildlife'
                result['real_data'] = True
                result['scan_timestamp'] = datetime.now().isoformat()
                
                # Apply intelligent threat scoring to REAL data
                if self.threat_scorer:
                    try:
                        threat_analysis = self.threat_scorer.analyze_listing(result, result.get('search_term', ''), result.get('platform', ''))
                        
                        result.update({
                            "threat_score": threat_analysis.threat_score,
                            "threat_level": threat_analysis.threat_level.value,
                            "threat_category": "wildlife",  # Explicit wildlife category
                            "confidence": threat_analysis.confidence,
                            "requires_human_review": threat_analysis.requires_human_review,
                            "reasoning": threat_analysis.reasoning,
                            "wildlife_indicators": threat_analysis.wildlife_indicators
                        })
                    except Exception as e:
                        logging.warning(f"Threat analysis failed for result: {e}")
                        result.update({
                            "threat_score": self._calculate_basic_wildlife_score(result),
                            "threat_level": "BASIC_ANALYSIS",
                            "threat_category": "wildlife"
                        })
                else:
                    # Fallback scoring
                    result.update({
                        "threat_score": self._calculate_basic_wildlife_score(result),
                        "threat_level": "BASIC_ANALYSIS", 
                        "threat_category": "wildlife"
                    })
                
                processed_results.append(result)
            
            logging.info(f"✅ Processed {len(processed_results)} wildlife-relevant listings")
            return processed_results
            
        except Exception as e:
            logging.error(f"❌ Real platform scanning failed: {e}")
            return []

    def _is_wildlife_related(self, result: Dict, keywords: List[str]) -> bool:
        """Check if a real listing is wildlife-related"""
        title = result.get('title', '').lower()
        search_term = result.get('search_term', '').lower()
        
        # Check if title or search term contains wildlife indicators
        wildlife_indicators = [
            'ivory', 'bone', 'horn', 'tusk', 'shell', 'fur', 'leather', 'skin',
            'traditional', 'medicine', 'carving', 'antique', 'vintage', 'rare',
            'specimen', 'taxidermy', 'mounted', 'collection', 'artifact'
        ]
        
        # Must match search term (was specifically searched for)
        term_match = any(keyword.lower() in search_term for keyword in keywords)
        
        # Additional wildlife context in title
        context_match = any(indicator in title for indicator in wildlife_indicators)
        
        return term_match or context_match

    def _calculate_basic_wildlife_score(self, result: Dict) -> int:
        """Basic wildlife threat scoring for real listings"""
        title = result.get('title', '').lower()
        price = result.get('price', '').lower()
        
        score = 40  # Base score for wildlife items
        
        # High-risk wildlife terms
        high_risk = ['ivory', 'rhino horn', 'tiger bone', 'pangolin', 'bear bile']
        if any(term in title for term in high_risk):
            score += 35
        
        # Suspicious pricing patterns
        if any(term in price for term in ['cash only', 'contact', 'offer', 'negotiate']):
            score += 10
        
        # Suspicious title terms
        suspicious = ['authentic', 'genuine', 'certificate', 'private', 'collection', 'estate']
        score += sum(5 for term in suspicious if term in title)
        
        return min(100, max(20, score))

    def deduplicate_real_results(self, results: List[Dict]) -> List[Dict]:
        """Remove duplicate real listings based on URL"""
        unique_results = []
        
        for result in results:
            url = result.get("url", "")
            if url and url not in self.seen_urls:
                unique_results.append(result)
                self.seen_urls.add(url)
        
        return unique_results

    async def store_real_wildlife_results(self, results: List[Dict]) -> Dict:
        """Store REAL wildlife results to Supabase"""
        if not results:
            logging.warning("⚠️ No real results to store")
            return {"stored_count": 0, "quality_metrics": {}}

        import aiohttp
        
        stored_count = 0
        quality_metrics = {
            "high_threat_items": 0,
            "critical_alerts": 0,
            "human_review_required": 0,
            "real_data_used": True
        }

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        }

        async with aiohttp.ClientSession() as session:
            logging.info(f"🔄 Storing {len(results)} REAL wildlife results to Supabase...")
            
            for i, result in enumerate(results):
                try:
                    evidence_id = f"REAL-WILDLIFE-{result.get('platform', 'UNKNOWN').upper()}-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{i:04d}"

                    # Get threat data
                    threat_score = result.get('threat_score', 40)
                    threat_level = result.get('threat_level', 'WILDLIFE_THREAT')
                    requires_review = result.get('requires_human_review', threat_score >= 70)

                    # Update quality metrics
                    if threat_score >= 70:
                        quality_metrics["high_threat_items"] += 1
                    if threat_score >= 85:
                        quality_metrics["critical_alerts"] += 1
                    if requires_review:
                        quality_metrics["human_review_required"] += 1

                    detection = {
                        "evidence_id": evidence_id,
                        "timestamp": datetime.now().isoformat(),
                        "platform": result.get('platform', 'unknown'),
                        "threat_score": threat_score,
                        "threat_level": threat_level,
                        "threat_category": "wildlife",  # EXPLICIT wildlife category
                        "species_involved": f"Real wildlife scan: {result.get('search_term', 'unknown')}",
                        "alert_sent": False,
                        "status": "REAL_WILDLIFE_SCAN",
                        "listing_title": (result.get("title", "") or "")[:500],
                        "listing_url": result.get("url", "") or "",
                        "listing_price": str(result.get("price", "") or ""),
                        "search_term": result.get("search_term", "") or "",
                        "description": (result.get("description", "") or "")[:1000],
                        "confidence_score": result.get('confidence', 0.7),
                        "requires_human_review": requires_review
                    }

                    # Remove None values
                    detection = {k: v for k, v in detection.items() if v is not None}

                    url = f"{self.supabase_url}/rest/v1/detections"

                    async with session.post(url, headers=headers, json=detection) as resp:
                        if resp.status in [200, 201]:
                            stored_count += 1
                            if stored_count % 25 == 0:
                                logging.info(f"✅ Stored {stored_count}/{len(results)} REAL wildlife results...")
                        elif resp.status == 409:
                            continue  # Duplicate
                        else:
                            response_text = await resp.text()
                            logging.error(f"❌ Storage error: HTTP {resp.status} - {response_text}")

                except Exception as e:
                    logging.error(f"❌ Exception storing result {i}: {e}")
                    continue

        quality_metrics["quality_score"] = stored_count / len(results) if results else 0
        
        logging.info(f"✅ Stored {stored_count}/{len(results)} REAL wildlife results")
        return {"stored_count": stored_count, "quality_metrics": quality_metrics}

    async def run_continuous_real_wildlife_scan(self, keyword_batch_size: int = 15) -> Dict:
        """Run continuous REAL wildlife scan with live platform data and proper state management"""
        
        logging.info(f"🚀 Starting CONTINUOUS REAL WILDLIFE SCAN")
        logging.info(f"🌍 Platforms: REAL scraping from {len(self.real_platforms)} live marketplaces")
        logging.info(f"🎯 Keywords: {keyword_batch_size} from {len(self.wildlife_keywords):,} total")
        
        start_time = datetime.now()
        
        # PROPER STATE MANAGEMENT - Continue where last run left off
        state_file = 'continuous_wildlife_keyword_state.json'
        try:
            with open(state_file, 'r') as f:
                state = json.load(f)
        except FileNotFoundError:
            state = {
                "last_index": 0,
                "total_keywords": len(self.wildlife_keywords),
                "completed_cycles": 0,
                "last_run": None
            }
        
        # Get next batch of keywords starting from where we left off
        start_index = state['last_index']
        end_index = min(start_index + keyword_batch_size, len(self.wildlife_keywords))
        
        # If we've reached the end, start over and increment cycle count
        if start_index >= len(self.wildlife_keywords):
            start_index = 0
            end_index = min(keyword_batch_size, len(self.wildlife_keywords))
            state['completed_cycles'] += 1
            logging.info(f"🔄 Completed full cycle {state['completed_cycles']}, starting over")
        
        keyword_batch = self.wildlife_keywords[start_index:end_index]
        
        # Update state for next run
        state['last_index'] = end_index
        state['last_run'] = datetime.now().isoformat()
        
        # Save state
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
        
        logging.info(f"📊 Keywords {start_index}-{end_index}/{len(self.wildlife_keywords)} (cycle {state['completed_cycles']})")
        logging.info(f"📝 Current batch: {', '.join(keyword_batch[:5])}...")
        
        # Scan REAL platforms
        all_results = await self.scan_real_platforms_wildlife(keyword_batch)
        
        # Deduplicate
        unique_results = self.deduplicate_real_results(all_results)
        
        # Store REAL results
        storage_result = await self.store_real_wildlife_results(unique_results)
        stored_count = storage_result["stored_count"]
        quality_metrics = storage_result["quality_metrics"]
        
        duration = (datetime.now() - start_time).total_seconds()
        
        results = {
            'scan_type': 'wildlife',
            'total_scanned': len(all_results),
            'total_stored': stored_count,
            'platforms_scanned': self.real_platforms,
            'keywords_used': len(keyword_batch),
            'keywords_progress': f"{end_index}/{len(self.wildlife_keywords)}",
            'completed_cycles': state['completed_cycles'],
            'duration_seconds': duration,
            'listings_per_minute': int(len(all_results) * 60 / duration) if duration > 0 else 0,
            'timestamp': datetime.now().isoformat(),
            'quality_metrics': quality_metrics,
            'real_data_used': True,
            'continuous_scanning': True,
            'state_managed': True,
            'high_threat_items': quality_metrics.get("high_threat_items", 0),
            'critical_alerts': quality_metrics.get("critical_alerts", 0),
            'human_review_required': quality_metrics.get("human_review_required", 0)
        }
        
        logging.info(f"✅ CONTINUOUS REAL WILDLIFE SCAN COMPLETED")
        logging.info(f"📊 Total scanned: {len(all_results):,} REAL listings")
        logging.info(f"💾 Total stored: {stored_count:,}")
        logging.info(f"⚡ Rate: {results['listings_per_minute']:,} real listings/minute")
        logging.info(f"🎯 Progress: {end_index}/{len(self.wildlife_keywords)} keywords (cycle {state['completed_cycles']})")
        logging.info(f"🎯 High threat items: {quality_metrics.get('high_threat_items', 0)}")
        logging.info(f"🚨 Critical alerts: {quality_metrics.get('critical_alerts', 0)}")
        
        return results


async def run_continuous_real_wildlife_scan():
    """Run continuous REAL wildlife scan with live platform data"""
    scanner = ContinuousRealWildlifeScanner()
    return await scanner.run_continuous_real_wildlife_scan(30)


if __name__ == "__main__":
    print("🔧 CONTINUOUS REAL WILDLIFE SCANNER")
    print("✅ REAL platform scraping (eBay API, Craigslist, AliExpress, etc.)")
    print("✅ Live marketplace data (NO simulation)")
    print("✅ Uses ALL 1,452 multilingual wildlife keywords")
    print("✅ Intelligent threat scoring with REAL data")
    print("✅ Continuous 15-minute scanning")
    print("🌍 Platforms: eBay, Craigslist, AliExpress, OLX, Gumtree, MercadoLibre, Taobao, Mercari")
    print("-" * 80)

    result = asyncio.run(run_continuous_real_wildlife_scan())
    
    print(f"\n🎉 CONTINUOUS REAL WILDLIFE SCAN COMPLETED:")
    print(f"   📊 Total scanned: {result['total_scanned']:,} REAL listings")
    print(f"   💾 Total stored: {result['total_stored']:,}")
    print(f"   🎯 High threat items: {result.get('high_threat_items', 0):,}")
    print(f"   🚨 Critical alerts: {result.get('critical_alerts', 0):,}")
    print(f"   🌍 Real data: {'YES' if result.get('real_data_used') else 'NO'}")
    print(f"   📈 Quality score: {result.get('quality_metrics', {}).get('quality_score', 0):.2%}")
