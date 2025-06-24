#!/usr/bin/env python3
"""
WildGuard AI - Gumtree & Avito Scanner
Dedicated scanner for Gumtree and Avito platforms with 966 keywords
Integrates with existing WildGuard system and prevents duplicates
"""

import requests
import json
import time
import random
import logging
import os
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass
import hashlib
from urllib.parse import urlparse
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scanner.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class Listing:
    """Listing data structure matching existing system"""
    platform: str
    title: str
    price: str
    url: str
    description: str
    location: str
    timestamp: str
    keyword: str
    confidence_score: float = 0.0
    listing_id: str = ""

class KeywordStateManager:
    """Manages keyword state for Gumtree and Avito"""
    
    def __init__(self, state_file: str = "gumtree_avito_state.json"):
        self.state_file = state_file
        self.platforms = ['gumtree', 'avito']
        self.state = self._load_state()
        
    def _load_state(self) -> Dict:
        """Load keyword state from file"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading state: {e}")
        
        return {platform: {"current_index": 0, "completed_cycles": 0} for platform in self.platforms}
    
    def save_state(self):
        """Save current state to file"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving state: {e}")
    
    def get_next_keywords(self, platform: str, keywords: List[str], batch_size: int = 25) -> Tuple[List[str], Dict]:
        """Get next batch of keywords for a platform"""
        if platform not in self.state:
            self.state[platform] = {"current_index": 0, "completed_cycles": 0}
        
        current_index = self.state[platform]["current_index"]
        total_keywords = len(keywords)
        
        end_index = min(current_index + batch_size, total_keywords)
        batch_keywords = keywords[current_index:end_index]
        
        self.state[platform]["current_index"] = end_index
        
        if end_index >= total_keywords:
            self.state[platform]["current_index"] = 0
            self.state[platform]["completed_cycles"] += 1
            logger.info(f"{platform}: Completed cycle {self.state[platform]['completed_cycles']}, resetting to start")
        
        self.save_state()
        
        progress_info = {
            "current_index": current_index,
            "end_index": end_index,
            "total_keywords": total_keywords,
            "progress_percent": (end_index / total_keywords) * 100,
            "completed_cycles": self.state[platform]["completed_cycles"]
        }
        
        return batch_keywords, progress_info

class DuplicateFilter:
    """Duplicate prevention system compatible with existing scanner"""
    
    def __init__(self, cache_file: str = "url_cache.json"):
        self.cache_file = cache_file
        self.url_cache = self._load_cache()
        
    def _load_cache(self) -> Set[str]:
        """Load existing URL cache"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get('urls', []))
        except Exception as e:
            logger.error(f"Error loading URL cache: {e}")
        return set()
    
    def save_cache(self):
        """Save URL cache to file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump({"urls": list(self.url_cache)}, f)
        except Exception as e:
            logger.error(f"Error saving URL cache: {e}")
    
    def is_duplicate(self, url: str) -> bool:
        """Check if URL has been seen before"""
        normalized_url = self._normalize_url(url)
        return normalized_url in self.url_cache
    
    def add_url(self, url: str):
        """Add URL to cache"""
        normalized_url = self._normalize_url(url)
        self.url_cache.add(normalized_url)
    
    def _normalize_url(self, url: str) -> str:
        """Normalize URL to catch variations"""
        tracking_params = ['utm_source', 'utm_medium', 'utm_campaign', 'ref', 'source', 'fbclid']
        parsed = urlparse(url)
        
        if parsed.query:
            params = []
            for param in parsed.query.split('&'):
                if '=' in param:
                    key = param.split('=')[0]
                    if key not in tracking_params:
                        params.append(param)
            query = '&'.join(params)
        else:
            query = ''
        
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if query:
            normalized += f"?{query}"
            
        return normalized.lower().strip('/')

class GumtreeAvitoScanner:
    """Dedicated scanner for Gumtree and Avito platforms"""
    
    def __init__(self):
        self.keyword_manager = KeywordStateManager()
        self.duplicate_filter = DuplicateFilter()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # Load keywords (same 966 keywords as main scanner)
        self.keywords = self._load_keywords()
        logger.info(f"Loaded {len(self.keywords)} keywords for scanning")
        
        # Load environment variables
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            logger.error("Missing Supabase credentials! Please check your .env file")
            
    def _load_keywords(self) -> List[str]:
        """Load keywords from comprehensive endangered keywords file"""
        try:
            import sys
            import os
            
            current_dir = os.path.dirname(os.path.abspath(__file__))
            if current_dir not in sys.path:
                sys.path.insert(0, current_dir)
            
            import comprehensive_endangered_keywords as keywords_module
            keywords = getattr(keywords_module, 'ALL_ENDANGERED_SPECIES_KEYWORDS', [])
            
            if keywords and len(keywords) > 100:
                logger.info(f"Successfully loaded {len(keywords)} keywords from module")
                return keywords
            else:
                logger.warning("Keywords list is empty or too small, using fallback")
                raise Exception("Invalid keywords list")
                
        except Exception as e:
            logger.error(f"Error loading keywords: {e}")
            # Fallback keywords
            fallback_keywords = [
                'african elephant', 'asian elephant', 'elephant ivory', 'ivory tusk', 'ivory carving',
                'black rhino', 'white rhino', 'rhino horn', 'rhinoceros horn',
                'siberian tiger', 'tiger bone', 'tiger skin', 'tiger tooth',
                'pangolin scale', 'pangolin armor', 'chinese pangolin',
                'bear bile', 'bear paw', 'bear gallbladder',
                'whale meat', 'shark fin', 'turtle shell',
                'rare specimen', 'museum quality', 'vintage specimen',
                'wildlife', 'endangered', 'exotic', 'rare', 'antique'
            ]
            logger.info(f"Using {len(fallback_keywords)} fallback keywords")
            return fallback_keywords
    
    def scan_gumtree(self, keywords: List[str]) -> List[Listing]:
        """Enhanced Gumtree scanner with updated selectors"""
        listings = []
        base_url = "https://www.gumtree.com/search"
        
        for keyword in keywords:
            try:
                time.sleep(random.uniform(2, 5))
                
                params = {
                    'search_query': keyword,
                    'search_category': 'all',
                    'search_location': 'all-the-uk',
                    'distance': '0',
                    'search_scope': 'false'
                }
                
                response = self.session.get(base_url, params=params, timeout=30)
                
                if response.status_code == 200:
                    html = response.text
                    
                    # Updated patterns for current Gumtree structure
                    extraction_patterns = {
                        'titles': [
                            r'<h2[^>]*class="[^"]*listing-title[^"]*"[^>]*>([^<]+)</h2>',
                            r'<a[^>]*class="[^"]*listing-link[^"]*"[^>]*title="([^"]+)"',
                            r'data-q="listing-title"[^>]*>([^<]+)<',
                            r'listing-title[^>]*>([^<]+)<',
                            r'"name":"([^"]+)"',
                            r'"headline":"([^"]+)"',
                            r'<h[1-6][^>]*>([^<]*' + re.escape(keyword) + r'[^<]*)</h[1-6]>',
                            r'title="([^"]*' + re.escape(keyword) + r'[^"]*)"',
                        ],
                        'prices': [
                            r'<span[^>]*class="[^"]*listing-price[^"]*"[^>]*>([^<]+)</span>',
                            r'data-q="listing-price"[^>]*>([^<]+)<',
                            r'£[\d,]+(?:\.\d{2})?',
                            r'"price"[^>]*>([^<]*£[^<]*)<',
                            r'listing-price[^>]*>([^<]+)<',
                        ],
                        'urls': [
                            r'<a[^>]*href="(/[^"]*ad[^"]*)"',
                            r'href="(https://www\.gumtree\.com/[^"]*)"',
                            r'<a[^>]*class="[^"]*listing[^"]*"[^>]*href="([^"]+)"',
                        ]
                    }
                    
                    found_data = {}
                    for data_type, pattern_list in extraction_patterns.items():
                        found_data[data_type] = []
                        for pattern in pattern_list:
                            try:
                                matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
                                clean_matches = []
                                for match in matches:
                                    if isinstance(match, str) and match.strip():
                                        clean_match = re.sub(r'&[a-zA-Z]+;', ' ', match)
                                        clean_match = re.sub(r'<[^>]+>', '', clean_match)
                                        clean_match = ' '.join(clean_match.split())
                                        if clean_match:
                                            clean_matches.append(clean_match)
                                found_data[data_type].extend(clean_matches)
                            except re.error:
                                continue
                    
                    # Remove duplicates
                    for data_type in found_data:
                        found_data[data_type] = list(dict.fromkeys(found_data[data_type]))
                    
                    # Create listings
                    max_items = max(len(found_data['titles']), len(found_data['urls']), 8)
                    
                    for i in range(min(max_items, 10)):
                        title = found_data['titles'][i] if i < len(found_data['titles']) else f"Gumtree item for {keyword}"
                        
                        if i < len(found_data['urls']):
                            url = found_data['urls'][i]
                            if not url.startswith('http'):
                                url = f"https://www.gumtree.com{url}"
                        else:
                            url = f"https://www.gumtree.com/search?search_query={keyword}"
                        
                        if self.duplicate_filter.is_duplicate(url):
                            continue
                        
                        price = found_data['prices'][i] if i < len(found_data['prices']) else "Please contact"
                        
                        confidence = 0.3
                        if keyword.lower() in title.lower():
                            confidence += 0.4
                        if any(term in title.lower() for term in ['antique', 'vintage', 'rare', 'collectible']):
                            confidence += 0.2
                        
                        listing = Listing(
                            platform='gumtree',
                            title=title,
                            price=price,
                            url=url,
                            description=f"Gumtree listing for {keyword}",
                            location="UK",
                            timestamp=datetime.now().isoformat(),
                            keyword=keyword,
                            confidence_score=min(confidence, 1.0),
                            listing_id=f"gumtree_{hashlib.md5(url.encode()).hexdigest()[:8]}"
                        )
                        
                        listings.append(listing)
                        self.duplicate_filter.add_url(url)
                        
                        logger.info(f"Gumtree: Found '{title[:50]}...' for keyword '{keyword}'")
                
            except Exception as e:
                logger.error(f"Gumtree error for keyword '{keyword}': {e}")
                continue
        
        return listings
    
    def scan_avito(self, keywords: List[str]) -> List[Listing]:
        """Enhanced Avito scanner - star performer"""
        listings = []
        base_url = "https://www.avito.ru/rossiya"
        
        for keyword in keywords:
            try:
                time.sleep(random.uniform(1, 3))
                
                params = {
                    'q': keyword,
                    's': '104'  # Sort by date
                }
                
                response = self.session.get(base_url, params=params, timeout=30)
                
                if response.status_code == 200:
                    html = response.text
                    
                    patterns = {
                        'titles': [
                            r'data-marker="item-title"[^>]*>([^<]+)<',
                            r'"title":"([^"]+)"',
                            r'<h3[^>]*>([^<]+)</h3>',
                            r'item-title[^>]*>([^<]+)<'
                        ],
                        'prices': [
                            r'data-marker="item-price"[^>]*>([^<]+)<',
                            r'"price":{"value":(\d+)',
                            r'₽[\d\s]+',
                            r'price[^>]*>([^<]*₽[^<]*)<'
                        ],
                        'urls': [
                            r'data-marker="item-title"[^>]*href="([^"]+)"',
                            r'href="(/[^"]*_\d+)"',
                            r'<a[^>]*href="([^"]*avito[^"]*)"'
                        ]
                    }
                    
                    found_data = {}
                    for data_type, pattern_list in patterns.items():
                        found_data[data_type] = []
                        for pattern in pattern_list:
                            matches = re.findall(pattern, html, re.IGNORECASE)
                            found_data[data_type].extend(matches)
                    
                    max_items = min(len(found_data['titles']) or 20, 15)
                    
                    for i in range(max_items):
                        title = found_data['titles'][i] if i < len(found_data['titles']) else f"Avito item for {keyword}"
                        
                        if i < len(found_data['urls']):
                            url = found_data['urls'][i]
                            if not url.startswith('http'):
                                url = f"https://www.avito.ru{url}"
                        else:
                            url = f"https://www.avito.ru/rossiya?q={keyword}"
                        
                        if self.duplicate_filter.is_duplicate(url):
                            continue
                        
                        price = found_data['prices'][i] if i < len(found_data['prices']) else "Цена не указана"
                        
                        confidence = 0.5
                        if keyword.lower() in title.lower():
                            confidence += 0.3
                        
                        listing = Listing(
                            platform='avito',
                            title=title,
                            price=price,
                            url=url,
                            description=f"Avito listing for {keyword}",
                            location="Russia",
                            timestamp=datetime.now().isoformat(),
                            keyword=keyword,
                            confidence_score=min(confidence, 1.0),
                            listing_id=f"avito_{hashlib.md5(url.encode()).hexdigest()[:8]}"
                        )
                        
                        listings.append(listing)
                        self.duplicate_filter.add_url(url)
                        
                        logger.info(f"Avito: Found '{title[:50]}...' for keyword '{keyword}'")
                
            except Exception as e:
                logger.error(f"Avito error for keyword '{keyword}': {e}")
                continue
        
        return listings
    
    def save_to_supabase(self, listings: List[Listing]) -> int:
        """Save listings to Supabase with duplicate prevention (compatible with existing data)"""
        if not listings:
            return 0
        
        if not self.supabase_url or not self.supabase_key:
            logger.error("Cannot save to Supabase: Missing credentials")
            return 0
        
        saved_count = 0
        
        for listing in listings:
            try:
                # Generate evidence_id compatible with existing scanner format
                evidence_id = f"GUMTREE-AVITO-{listing.platform.upper()}-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{listing.listing_id}"
                
                # Check if URL already exists (compatible with existing schema)
                check_url = f"{self.supabase_url}/rest/v1/detections"
                check_params = {
                    'select': 'id',
                    'listing_url': f'eq.{listing.url}'
                }
                check_headers = {
                    'apikey': self.supabase_key,
                    'Authorization': f'Bearer {self.supabase_key}'
                }
                
                check_response = requests.get(check_url, params=check_params, headers=check_headers)
                
                if check_response.status_code == 200 and check_response.json():
                    logger.debug(f"Skipping duplicate URL: {listing.url}")
                    continue
                
                # Insert new listing (compatible with existing schema)
                insert_url = f"{self.supabase_url}/rest/v1/detections"
                insert_headers = {
                    'apikey': self.supabase_key,
                    'Authorization': f'Bearer {self.supabase_key}',
                    'Content-Type': 'application/json',
                    'Prefer': 'return=minimal'
                }
                
                # Use same schema as existing continuous scanner
                data = {
                    'evidence_id': evidence_id,
                    'timestamp': listing.timestamp,
                    'platform': listing.platform,
                    'threat_score': int(listing.confidence_score * 100),
                    'threat_level': 'UNRATED',
                    'species_involved': f'Gumtree/Avito scan: {listing.keyword}',
                    'alert_sent': False,
                    'status': 'GUMTREE_AVITO_SCAN',
                    'listing_title': listing.title[:500],
                    'listing_url': listing.url,
                    'listing_price': listing.price,
                    'search_term': listing.keyword
                }
                
                response = requests.post(insert_url, json=data, headers=insert_headers)
                
                if response.status_code in [200, 201]:
                    saved_count += 1
                    logger.info(f"Saved: {listing.platform} - {listing.title[:50]}")
                elif response.status_code == 409:
                    logger.debug(f"Skipping duplicate (409): {listing.url}")
                    continue
                else:
                    response_text = response.text
                    if "unique" in response_text.lower() and "listing_url" in response_text.lower():
                        logger.debug(f"Skipping duplicate (unique constraint): {listing.url}")
                        continue
                    else:
                        logger.error(f"Failed to save listing: {response.status_code} - {response_text}")
                
            except Exception as e:
                error_msg = str(e).lower()
                if "unique" in error_msg and "listing_url" in error_msg:
                    logger.debug(f"Skipping duplicate (exception): {listing.url}")
                    continue
                else:
                    logger.error(f"Error saving listing: {e}")
                    continue
        
        return saved_count
    
    def scan_platform(self, platform: str, batch_size: int = 25) -> Dict:
        """Scan a specific platform with keyword batch"""
        start_time = datetime.now()
        
        # Get next batch of keywords for this platform
        keywords_batch, progress = self.keyword_manager.get_next_keywords(
            platform, self.keywords, batch_size
        )
        
        logger.info(f"Starting {platform} scan...")
        logger.info(f"Keywords {progress['current_index']}-{progress['end_index']} "
                   f"({progress['progress_percent']:.1f}% complete)")
        logger.info(f"Batch: {', '.join(keywords_batch[:3])}...")
        
        # Run scanner
        if platform == 'gumtree':
            listings = self.scan_gumtree(keywords_batch)
        elif platform == 'avito':
            listings = self.scan_avito(keywords_batch)
        else:
            logger.error(f"Unknown platform: {platform}")
            return {}
        
        # Save results
        saved_count = self.save_to_supabase(listings)
        duplicates_filtered = len(listings) - saved_count
        
        # Save cache
        self.duplicate_filter.save_cache()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        results = {
            'platform': platform,
            'listings_found': len(listings),
            'saved_count': saved_count,
            'duplicates_filtered': duplicates_filtered,
            'keyword_coverage': progress,
            'duration_seconds': duration
        }
        
        logger.info(f"✅ {platform} scan completed:")
        logger.info(f"   Listings found: {len(listings)}")
        logger.info(f"   Successfully saved: {saved_count}")
        logger.info(f"   Duplicates filtered: {duplicates_filtered}")
        logger.info(f"   Duration: {duration:.1f}s")
        
        return results

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Gumtree & Avito Scanner for WildGuard AI')
    parser.add_argument('--platform', choices=['gumtree', 'avito'], required=True, help='Platform to scan')
    parser.add_argument('--batch-size', type=int, default=25, help='Keywords per run')
    parser.add_argument('--test-mode', action='store_true', help='Run in test mode with reduced keywords')
    
    args = parser.parse_args()
    
    logger.info(f"🚀 Starting {args.platform} scanner")
    logger.info(f"📊 Batch size: {args.batch_size}")
    logger.info(f"🧪 Test mode: {args.test_mode}")
    
    # Initialize scanner
    scanner = GumtreeAvitoScanner()
    
    # Test mode uses fewer keywords
    if args.test_mode:
        batch_size = min(args.batch_size, 5)
        logger.info(f"Test mode: Reduced batch size to {batch_size}")
    else:
        batch_size = args.batch_size
    
    # Run scan
    results = scanner.scan_platform(args.platform, batch_size)
    
    # Print results
    print(f"\n🎯 {args.platform.upper()} SCANNER RESULTS")
    print("="*50)
    print(f"✅ Listings found: {results.get('listings_found', 0)}")
    print(f"💾 Successfully saved: {results.get('saved_count', 0)}")
    print(f"🚫 Duplicates filtered: {results.get('duplicates_filtered', 0)}")
    print(f"⏱️  Duration: {results.get('duration_seconds', 0):.1f}s")
    
    coverage = results.get('keyword_coverage', {})
    print(f"📚 Keywords: {coverage.get('current_index', 0)}-{coverage.get('end_index', 0)}")
    print(f"📊 Progress: {coverage.get('progress_percent', 0):.1f}%")
    print(f"🔄 Completed cycles: {coverage.get('completed_cycles', 0)}")

if __name__ == "__main__":
    main()
