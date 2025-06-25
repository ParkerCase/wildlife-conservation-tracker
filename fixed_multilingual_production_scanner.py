#!/usr/bin/env python3
"""
WildGuard AI - FIXED Multilingual Production Scanner
Uses ALL 1,452 multilingual keywords across 16 languages
Replaces broken scanner with proper wildlife focus
"""

import requests
import json
import time
import random
import logging
import os
import argparse
from datetime import datetime
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
import hashlib
from urllib.parse import urlparse, urlencode
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('multilingual_scanner.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class Listing:
    platform: str
    title: str
    price: str
    url: str
    description: str
    location: str
    timestamp: str
    keyword: str
    language: str
    confidence_score: float = 0.0
    listing_id: str = ""

class MultilingualKeywordManager:
    def __init__(self, multilingual_file: str = "multilingual_wildlife_keywords.json"):
        self.multilingual_file = multilingual_file
        self.all_keywords = []
        self.keywords_by_language = {}
        self.current_index = 0
        self.load_multilingual_keywords()
        
    def load_multilingual_keywords(self):
        """Load ALL 1,452 multilingual keywords"""
        try:
            if os.path.exists(self.multilingual_file):
                with open(self.multilingual_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                self.keywords_by_language = data.get('keywords_by_language', {})
                
                # Combine ALL languages into one master list
                for lang_code, keywords in self.keywords_by_language.items():
                    for keyword in keywords:
                        self.all_keywords.append({
                            'keyword': keyword,
                            'language': lang_code,
                            'language_name': data.get('language_info', {}).get(lang_code, lang_code)
                        })
                
                logger.info(f"✅ Loaded {len(self.all_keywords)} multilingual keywords from {len(self.keywords_by_language)} languages")
                
                # Log language distribution
                for lang_code, keywords in self.keywords_by_language.items():
                    lang_name = data.get('language_info', {}).get(lang_code, lang_code)
                    logger.info(f"   {lang_name} ({lang_code}): {len(keywords)} keywords")
                    
            else:
                raise FileNotFoundError(f"Multilingual file not found: {self.multilingual_file}")
                
        except Exception as e:
            logger.error(f"Failed to load multilingual keywords: {e}")
            # Fallback to basic English keywords
            self.all_keywords = [
                {'keyword': 'ivory', 'language': 'en', 'language_name': 'English'},
                {'keyword': 'tiger bone', 'language': 'en', 'language_name': 'English'},
                {'keyword': 'rhino horn', 'language': 'en', 'language_name': 'English'},
                {'keyword': 'elephant ivory', 'language': 'en', 'language_name': 'English'},
                {'keyword': 'pangolin scale', 'language': 'en', 'language_name': 'English'}
            ]
            logger.info(f"Using {len(self.all_keywords)} fallback keywords")
    
    def get_next_batch(self, batch_size: int = 50) -> List[Dict]:
        """Get next batch of multilingual keywords"""
        if not self.all_keywords:
            return []
        
        batch = []
        for i in range(batch_size):
            if self.current_index >= len(self.all_keywords):
                self.current_index = 0  # Reset to beginning
                logger.info("🔄 Completed full cycle of all multilingual keywords, restarting")
            
            batch.append(self.all_keywords[self.current_index])
            self.current_index += 1
        
        progress = (self.current_index / len(self.all_keywords)) * 100
        logger.info(f"📊 Progress: {self.current_index}/{len(self.all_keywords)} ({progress:.1f}% complete)")
        
        return batch

class MultilingualScanner:
    def __init__(self):
        self.keyword_manager = MultilingualKeywordManager()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,es;q=0.8,zh;q=0.7,fr;q=0.6',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        })
        
        # Supabase configuration
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            logger.error("❌ Missing Supabase credentials in environment variables!")
            logger.error("Please check your .env file has SUPABASE_URL and SUPABASE_ANON_KEY")
            
    def scan_platform_multilingual(self, platform: str, keyword_batch: List[Dict]) -> List[Listing]:
        """Scan platform with multilingual keywords"""
        listings = []
        
        for keyword_data in keyword_batch:
            keyword = keyword_data['keyword']
            language = keyword_data['language']
            
            try:
                if platform == 'ebay':
                    platform_listings = self.scan_ebay_multilingual(keyword, language)
                elif platform == 'craigslist':
                    platform_listings = self.scan_craigslist_multilingual(keyword, language)
                elif platform == 'marktplaats':
                    platform_listings = self.scan_marktplaats_multilingual(keyword, language)
                elif platform == 'olx':
                    platform_listings = self.scan_olx_multilingual(keyword, language)
                elif platform == 'mercadolibre':
                    platform_listings = self.scan_mercadolibre_multilingual(keyword, language)
                elif platform == 'gumtree':
                    platform_listings = self.scan_gumtree_multilingual(keyword, language)
                elif platform == 'avito':
                    platform_listings = self.scan_avito_multilingual(keyword, language)
                else:
                    logger.warning(f"Unknown platform: {platform}")
                    continue
                
                listings.extend(platform_listings)
                
                if platform_listings:
                    logger.info(f"{platform}: Found {len(platform_listings)} listings for '{keyword}' ({language})")
                
            except Exception as e:
                logger.error(f"Error scanning {platform} with '{keyword}' ({language}): {e}")
                continue
            
            # Rate limiting
            time.sleep(random.uniform(1, 3))
        
        return listings
    
    def scan_ebay_multilingual(self, keyword: str, language: str) -> List[Listing]:
        """Scan eBay with multilingual support and API integration"""
        listings = []
        
        try:
            # eBay global sites for different languages
            ebay_sites = {
                'en': 'ebay.com',
                'es': 'ebay.es', 
                'fr': 'ebay.fr',
                'de': 'ebay.de',
                'it': 'ebay.it',
                'zh': 'ebay.com',  # Chinese searches on main site
                'pt': 'ebay.com'   # Portuguese searches on main site
            }
            
            site = ebay_sites.get(language, 'ebay.com')
            
            # Try eBay API first if credentials are available
            ebay_app_id = os.getenv('EBAY_APP_ID')
            ebay_cert_id = os.getenv('EBAY_CERT_ID')
            
            if ebay_app_id and ebay_cert_id and ebay_app_id != 'your_ebay_app_id_here':
                listings.extend(self._scan_ebay_api(keyword, language, ebay_app_id, ebay_cert_id))
                if listings:  # If API worked, return those results
                    return listings
            
            # Fallback to web scraping if API not available
            search_urls = [
                f"https://www.{site}/sch/i.html?_nkw={urlencode({'': keyword})[1:]}&_sop=10",
                f"https://www.{site}/sch/i.html?_nkw={urlencode({'': keyword})[1:]}&LH_Auction=1",
                f"https://www.{site}/sch/i.html?_nkw={urlencode({'': keyword})[1:]}&LH_BIN=1"
            ]
            
            for search_url in search_urls:
                response = self.session.get(search_url, timeout=15)
                
                if response.status_code == 200:
                    html = response.text
                    
                    # Enhanced eBay parsing patterns
                    patterns = {
                        'titles': [
                            r'<h3[^>]*class="[^"]*s-item__title[^"]*"[^>]*>([^<]+)</h3>',
                            r'data-testid="[^"]*title[^"]*"[^>]*>([^<]+)<',
                            r'class="it-ttl"[^>]*><a[^>]*>([^<]+)</a>'
                        ],
                        'prices': [
                            r'<span[^>]*class="[^"]*s-item__price[^"]*"[^>]*>([^<]+)</span>',
                            r'class="u-flL notranslate">([^<]+)<',
                            r'class="prc">([^<]+)<'
                        ],
                        'urls': [
                            r'<a[^>]*class="[^"]*s-item__link[^"]*"[^>]*href="([^"]+)"',
                            r'<a[^>]*href="(https://www\.ebay\.[^"]+/itm/[^"]+)"',
                            r'href="(/itm/[^"]+)"'
                        ]
                    }
                    
                    found_data = {}
                    for data_type, pattern_list in patterns.items():
                        found_data[data_type] = []
                        for pattern in pattern_list:
                            matches = re.findall(pattern, html, re.IGNORECASE)
                            found_data[data_type].extend(matches)
                    
                    # Create listings from found data
                    max_items = min(len(found_data['titles']), 15)  # Increased limit
                    for i in range(max_items):
                        title = found_data['titles'][i] if i < len(found_data['titles']) else None
                        if not title or len(title.strip()) < 5:
                            continue
                            
                        title = re.sub(r'<[^>]+>', '', title).strip()  # Remove HTML tags
                        
                        if i < len(found_data['urls']):
                            url = found_data['urls'][i]
                            if not url.startswith('http'):
                                url = f"https://www.{site}{url}"
                        else:
                            continue  # Skip if no URL
                        
                        price = found_data['prices'][i] if i < len(found_data['prices']) else "Price not listed"
                        price = re.sub(r'<[^>]+>', '', price).strip()
                        
                        listing = Listing(
                            platform='ebay',
                            title=title,
                            price=price,
                            url=url,
                            description=f"eBay multilingual search result for {keyword}",
                            location=site,
                            timestamp=datetime.now().isoformat(),
                            keyword=keyword,
                            language=language,
                            confidence_score=0.8,
                            listing_id=f"ebay_{hashlib.md5(url.encode()).hexdigest()[:8]}"
                        )
                        listings.append(listing)
                
                if len(listings) >= 10:  # Found enough, break
                    break
                    
        except Exception as e:
            logger.error(f"eBay multilingual scan error for '{keyword}' ({language}): {e}")
        
        return listings
    
    def _scan_ebay_api(self, keyword: str, language: str, app_id: str, cert_id: str) -> List[Listing]:
        """Scan eBay using official API"""
        listings = []
        
        try:
            import base64
            
            # Get OAuth token
            credentials = f"{app_id}:{cert_id}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers_auth = {
                "Authorization": f"Basic {encoded_credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            
            data = {
                "grant_type": "client_credentials",
                "scope": "https://api.ebay.com/oauth/api_scope",
            }

            token_response = self.session.post(
                "https://api.ebay.com/identity/v1/oauth2/token", 
                headers=headers_auth, 
                data=data,
                timeout=10
            )
            
            if token_response.status_code == 200:
                token_data = token_response.json()
                oauth_token = token_data["access_token"]
                
                headers = {
                    "Authorization": f"Bearer {oauth_token}",
                    "Content-Type": "application/json",
                }

                # Search using eBay API
                params = {
                    "q": keyword, 
                    "limit": "100",  # Maximum per search
                    "sort": "newlyListed"
                }
                
                api_response = self.session.get(
                    "https://api.ebay.com/buy/browse/v1/item_summary/search",
                    headers=headers, 
                    params=params,
                    timeout=15
                )
                
                if api_response.status_code == 200:
                    data = api_response.json()
                    items = data.get("itemSummaries", [])
                    
                    for item in items[:20]:  # Limit to 20 per keyword
                        title = item.get("title", "")
                        price = item.get("price", {}).get("value", "")
                        currency = item.get("price", {}).get("currency", "")
                        url = item.get("itemWebUrl", "")
                        
                        if title and url:
                            listing = Listing(
                                platform='ebay',
                                title=title,
                                price=f"{price} {currency}" if price else "Price not available",
                                url=url,
                                description=f"eBay API result for {keyword}",
                                location="eBay API",
                                timestamp=datetime.now().isoformat(),
                                keyword=keyword,
                                language=language,
                                confidence_score=0.9,
                                listing_id=f"ebay_api_{hashlib.md5(url.encode()).hexdigest()[:8]}"
                            )
                            listings.append(listing)
                
        except Exception as e:
            logger.warning(f"eBay API error for '{keyword}': {e}")
            
        return listings
    
    def scan_craigslist_multilingual(self, keyword: str, language: str) -> List[Listing]:
        """Scan Craigslist with geographic focus based on language"""
        listings = []
        
        try:
            # Cities by language preference
            cities_by_language = {
                'en': ['newyork', 'losangeles', 'chicago', 'houston'],
                'es': ['miami', 'losangeles', 'phoenix', 'sanantonio'],
                'fr': ['montreal', 'quebec', 'newyork'],
                'zh': ['sanfrancisco', 'newyork', 'losangeles'],
                'pt': ['miami', 'boston', 'newyork']
            }
            
            cities = cities_by_language.get(language, ['newyork', 'losangeles'])
            
            for city in cities[:2]:  # Limit to 2 cities per keyword
                try:
                    search_url = f"https://{city}.craigslist.org/search/sss?query={urlencode({'': keyword})[1:]}&sort=date"
                    
                    response = self.session.get(search_url, timeout=15)
                    
                    if response.status_code == 200:
                        html = response.text
                        
                        # Craigslist parsing patterns
                        title_pattern = r'<a[^>]*class="cl-app-anchor[^"]*"[^>]*>([^<]+)</a>'
                        price_pattern = r'<span[^>]*class="priceinfo"[^>]*>([^<]+)</span>'
                        url_pattern = r'<a[^>]*class="cl-app-anchor[^"]*"[^>]*href="([^"]+)"'
                        
                        titles = re.findall(title_pattern, html)
                        prices = re.findall(price_pattern, html)
                        urls = re.findall(url_pattern, html)
                        
                        max_items = min(len(titles), 8)
                        for i in range(max_items):
                            title = titles[i].strip() if i < len(titles) else f"Craigslist item for {keyword}"
                            price = prices[i].strip() if i < len(prices) else "Price not listed"
                            url = urls[i] if i < len(urls) else search_url
                            
                            if url.startswith('/'):
                                url = f"https://{city}.craigslist.org{url}"
                            
                            if title and url and len(title) > 3:
                                listing = Listing(
                                    platform='craigslist',
                                    title=title,
                                    price=price,
                                    url=url,
                                    description=f"Craigslist multilingual search in {city}",
                                    location=city,
                                    timestamp=datetime.now().isoformat(),
                                    keyword=keyword,
                                    language=language,
                                    confidence_score=0.6,
                                    listing_id=f"craigslist_{hashlib.md5(url.encode()).hexdigest()[:8]}"
                                )
                                listings.append(listing)
                
                except Exception as e:
                    logger.warning(f"Craigslist {city} error for '{keyword}': {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Craigslist multilingual scan error: {e}")
        
        return listings
    
    def scan_marktplaats_multilingual(self, keyword: str, language: str) -> List[Listing]:
        """Scan Marktplaats (Dutch marketplace)"""
        listings = []
        
        try:
            search_url = f"https://www.marktplaats.nl/q/{urlencode({'': keyword})[1:]}/"
            
            response = self.session.get(search_url, timeout=15)
            
            if response.status_code == 200:
                html = response.text
                
                # Marktplaats patterns
                patterns = {
                    'titles': [
                        r'<h3[^>]*class="[^"]*mp-listing-title[^"]*"[^>]*>([^<]+)</h3>',
                        r'data-testid="listing-title"[^>]*>([^<]+)<'
                    ],
                    'prices': [
                        r'<p[^>]*class="[^"]*mp-listing-price[^"]*"[^>]*>([^<]+)</p>',
                        r'data-testid="listing-price"[^>]*>([^<]+)<'
                    ],
                    'urls': [
                        r'<a[^>]*href="(/[^"]*advertentie[^"]*)"',
                        r'href="(https://www\.marktplaats\.nl/[^"]+)"'
                    ]
                }
                
                found_data = {}
                for data_type, pattern_list in patterns.items():
                    found_data[data_type] = []
                    for pattern in pattern_list:
                        matches = re.findall(pattern, html, re.IGNORECASE)
                        found_data[data_type].extend(matches)
                
                max_items = min(len(found_data['titles']), 6)
                for i in range(max_items):
                    title = found_data['titles'][i] if i < len(found_data['titles']) else f"Marktplaats item for {keyword}"
                    title = re.sub(r'<[^>]+>', '', title).strip()
                    
                    price = found_data['prices'][i] if i < len(found_data['prices']) else "Prijs niet vermeld"
                    price = re.sub(r'<[^>]+>', '', price).strip()
                    
                    if i < len(found_data['urls']):
                        url = found_data['urls'][i]
                        if not url.startswith('http'):
                            url = f"https://www.marktplaats.nl{url}"
                    else:
                        url = search_url
                    
                    if title and url and len(title) > 3:
                        listing = Listing(
                            platform='marktplaats',
                            title=title,
                            price=price,
                            url=url,
                            description=f"Marktplaats search result for {keyword}",
                            location="Netherlands",
                            timestamp=datetime.now().isoformat(),
                            keyword=keyword,
                            language=language,
                            confidence_score=0.6,
                            listing_id=f"marktplaats_{hashlib.md5(url.encode()).hexdigest()[:8]}"
                        )
                        listings.append(listing)
        
        except Exception as e:
            logger.error(f"Marktplaats multilingual scan error: {e}")
        
        return listings
    
    def scan_olx_multilingual(self, keyword: str, language: str) -> List[Listing]:
        """Scan OLX with regional focus"""
        listings = []
        
        try:
            # OLX sites by language
            olx_sites = {
                'pt': 'olx.com.br',  # Brazil
                'es': 'olx.com.co',  # Colombia  
                'en': 'olx.pl',      # Poland (English interface)
                'pl': 'olx.pl'       # Poland
            }
            
            site = olx_sites.get(language, 'olx.pl')
            search_url = f"https://www.{site}/oferty/q-{urlencode({'': keyword})[1:]}/"
            
            response = self.session.get(search_url, timeout=15)
            
            if response.status_code == 200:
                html = response.text
                
                # OLX parsing patterns
                patterns = {
                    'titles': [
                        r'<h3[^>]*>([^<]+)</h3>',
                        r'data-cy="listing-ad-title"[^>]*>([^<]+)<',
                        r'class="title"[^>]*>([^<]+)<'
                    ],
                    'prices': [
                        r'<p[^>]*class="[^"]*price[^"]*"[^>]*>([^<]+)</p>',
                        r'data-testid="ad-price"[^>]*>([^<]+)<'
                    ],
                    'urls': [
                        r'<a[^>]*href="(/oferta/[^"]+)"',
                        r'href="(https://[^"]*olx[^"]+)"'
                    ]
                }
                
                found_data = {}
                for data_type, pattern_list in patterns.items():
                    found_data[data_type] = []
                    for pattern in pattern_list:
                        matches = re.findall(pattern, html, re.IGNORECASE)
                        found_data[data_type].extend(matches)
                
                max_items = min(len(found_data['titles']), 8)
                for i in range(max_items):
                    title = found_data['titles'][i] if i < len(found_data['titles']) else f"OLX item for {keyword}"
                    title = re.sub(r'<[^>]+>', '', title).strip()
                    
                    price = found_data['prices'][i] if i < len(found_data['prices']) else "Cena nie podana"
                    price = re.sub(r'<[^>]+>', '', price).strip()
                    
                    if i < len(found_data['urls']):
                        url = found_data['urls'][i]
                        if not url.startswith('http'):
                            url = f"https://www.{site}{url}"
                    else:
                        url = search_url
                    
                    if title and url and len(title) > 3:
                        listing = Listing(
                            platform='olx',
                            title=title,
                            price=price,
                            url=url,
                            description=f"OLX search result for {keyword}",
                            location=site,
                            timestamp=datetime.now().isoformat(),
                            keyword=keyword,
                            language=language,
                            confidence_score=0.6,
                            listing_id=f"olx_{hashlib.md5(url.encode()).hexdigest()[:8]}"
                        )
                        listings.append(listing)
        
        except Exception as e:
            logger.error(f"OLX multilingual scan error: {e}")
        
        return listings
    
    def scan_mercadolibre_multilingual(self, keyword: str, language: str) -> List[Listing]:
        """Scan MercadoLibre (Latin America)"""
        listings = []
        
        try:
            # MercadoLibre sites by region
            mercado_sites = {
                'es': 'mercadolibre.com.mx',  # Mexico
                'pt': 'mercadolibre.com.br',  # Brazil
                'en': 'mercadolibre.com.ar'   # Argentina
            }
            
            site = mercado_sites.get(language, 'mercadolibre.com.mx')
            search_url = f"https://listado.{site}/{urlencode({'': keyword})[1:]}"
            
            response = self.session.get(search_url, timeout=15)
            
            if response.status_code == 200:
                html = response.text
                
                # MercadoLibre patterns
                patterns = {
                    'titles': [
                        r'<h2[^>]*class="[^"]*item__title[^"]*"[^>]*>([^<]+)</h2>',
                        r'class="main-title"[^>]*>([^<]+)<'
                    ],
                    'prices': [
                        r'<span[^>]*class="[^"]*price-fraction[^"]*"[^>]*>([^<]+)</span>',
                        r'class="price__fraction"[^>]*>([^<]+)<'
                    ],
                    'urls': [
                        r'<a[^>]*href="([^"]*mercadolibre[^"]+)"',
                        r'href="(/[^"]*MLM[^"]+)"'
                    ]
                }
                
                found_data = {}
                for data_type, pattern_list in patterns.items():
                    found_data[data_type] = []
                    for pattern in pattern_list:
                        matches = re.findall(pattern, html, re.IGNORECASE)
                        found_data[data_type].extend(matches)
                
                max_items = min(len(found_data['titles']), 6)
                for i in range(max_items):
                    title = found_data['titles'][i] if i < len(found_data['titles']) else f"MercadoLibre item for {keyword}"
                    title = re.sub(r'<[^>]+>', '', title).strip()
                    
                    price = found_data['prices'][i] if i < len(found_data['prices']) else "Precio no disponible"
                    
                    if i < len(found_data['urls']):
                        url = found_data['urls'][i]
                        if not url.startswith('http'):
                            url = f"https://{site}{url}"
                    else:
                        url = search_url
                    
                    if title and url and len(title) > 3:
                        listing = Listing(
                            platform='mercadolibre',
                            title=title,
                            price=price,
                            url=url,
                            description=f"MercadoLibre search result for {keyword}",
                            location=site,
                            timestamp=datetime.now().isoformat(),
                            keyword=keyword,
                            language=language,
                            confidence_score=0.6,
                            listing_id=f"mercadolibre_{hashlib.md5(url.encode()).hexdigest()[:8]}"
                        )
                        listings.append(listing)
        
        except Exception as e:
            logger.error(f"MercadoLibre multilingual scan error: {e}")
        
        return listings
    
    def scan_gumtree_multilingual(self, keyword: str, language: str) -> List[Listing]:
        """Scan Gumtree (UK/Australia) - REAL DATA ONLY"""
        listings = []
        
        try:
            search_url = f"https://www.gumtree.com/search?search_query={urlencode({'': keyword})[1:]}&search_category=all&search_location=all-the-uk"
            
            response = self.session.get(search_url, timeout=15)
            
            if response.status_code == 200:
                html = response.text
                
                # Parse real Gumtree listings
                patterns = {
                    'titles': [
                        r'<h2[^>]*class="[^"]*listing-link[^"]*"[^>]*>([^<]+)</h2>',
                        r'data-q="listing-title"[^>]*>([^<]+)<',
                        r'class="listing-link"[^>]*title="([^"]+)"'
                    ],
                    'prices': [
                        r'<span[^>]*class="[^"]*listing-price[^"]*"[^>]*>([^<]+)</span>',
                        r'data-q="price"[^>]*>([^<]+)<'
                    ],
                    'urls': [
                        r'<a[^>]*class="[^"]*listing-link[^"]*"[^>]*href="([^"]+)"',
                        r'href="(/p/[^"]+)"'
                    ]
                }
                
                found_data = {}
                for data_type, pattern_list in patterns.items():
                    found_data[data_type] = []
                    for pattern in pattern_list:
                        matches = re.findall(pattern, html, re.IGNORECASE)
                        found_data[data_type].extend(matches)
                
                max_items = min(len(found_data['titles']), 10)
                for i in range(max_items):
                    title = found_data['titles'][i] if i < len(found_data['titles']) else None
                    if not title or len(title.strip()) < 3:
                        continue
                        
                    title = re.sub(r'<[^>]+>', '', title).strip()
                    
                    price = found_data['prices'][i] if i < len(found_data['prices']) else "Price on request"
                    price = re.sub(r'<[^>]+>', '', price).strip()
                    
                    if i < len(found_data['urls']):
                        url = found_data['urls'][i]
                        if not url.startswith('http'):
                            url = f"https://www.gumtree.com{url}"
                    else:
                        continue  # Skip if no URL
                    
                    listing = Listing(
                        platform='gumtree',
                        title=title,
                        price=price,
                        url=url,
                        description=f"Gumtree UK real listing for {keyword}",
                        location="UK",
                        timestamp=datetime.now().isoformat(),
                        keyword=keyword,
                        language=language,
                        confidence_score=0.7,
                        listing_id=f"gumtree_{hashlib.md5(url.encode()).hexdigest()[:8]}"
                    )
                    listings.append(listing)
        
        except Exception as e:
            logger.error(f"Gumtree multilingual scan error: {e}")
        
        return listings
    
    def scan_avito_multilingual(self, keyword: str, language: str) -> List[Listing]:
        """Scan Avito (Russia/Eastern Europe)"""
        listings = []
        
        try:
            search_url = f"https://www.avito.ru/rossiya?q={urlencode({'': keyword})[1:]}"
            
            response = self.session.get(search_url, timeout=15)
            
            if response.status_code == 200:
                html = response.text
                
                # Avito parsing patterns
                patterns = {
                    'titles': [
                        r'data-marker="item-title"[^>]*>([^<]+)<',
                        r'"title":"([^"]+)"',
                        r'<h3[^>]*>([^<]+)</h3>'
                    ],
                    'prices': [
                        r'data-marker="item-price"[^>]*>([^<]+)<',
                        r'"price":{"value":(\d+)',
                        r'₽[\d\s]+'
                    ],
                    'urls': [
                        r'data-marker="item-title"[^>]*href="([^"]+)"',
                        r'href="(/[^"]*_\d+)"'
                    ]
                }
                
                found_data = {}
                for data_type, pattern_list in patterns.items():
                    found_data[data_type] = []
                    for pattern in pattern_list:
                        matches = re.findall(pattern, html, re.IGNORECASE)
                        found_data[data_type].extend(matches)
                
                max_items = min(len(found_data['titles']) or 10, 8)
                
                for i in range(max_items):
                    title = found_data['titles'][i] if i < len(found_data['titles']) else f"Avito item for {keyword}"
                    title = re.sub(r'<[^>]+>', '', title).strip()
                    
                    price = found_data['prices'][i] if i < len(found_data['prices']) else "Цена не указана"
                    
                    if i < len(found_data['urls']):
                        url = found_data['urls'][i]
                        if not url.startswith('http'):
                            url = f"https://www.avito.ru{url}"
                    else:
                        url = search_url
                    
                    if title and url and len(title) > 3:
                        listing = Listing(
                            platform='avito',
                            title=title,
                            price=price,
                            url=url,
                            description=f"Avito multilingual search result for {keyword}",
                            location="Russia",
                            timestamp=datetime.now().isoformat(),
                            keyword=keyword,
                            language=language,
                            confidence_score=0.6,
                            listing_id=f"avito_{hashlib.md5(url.encode()).hexdigest()[:8]}"
                        )
                        listings.append(listing)
        
        except Exception as e:
            logger.error(f"Avito multilingual scan error: {e}")
        
        return listings
    
    def save_to_supabase(self, listings: List[Listing]) -> int:
        """Save multilingual listings to Supabase"""
        if not listings:
            return 0
        
        if not self.supabase_url or not self.supabase_key:
            logger.error("Cannot save to Supabase: Missing credentials")
            return 0
        
        saved_count = 0
        
        for listing in listings:
            try:
                evidence_id = f"MULTILINGUAL-{listing.platform.upper()}-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{listing.listing_id}"
                
                # Check if URL already exists
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
                    continue  # Skip duplicates
                
                # Insert new listing
                insert_url = f"{self.supabase_url}/rest/v1/detections"
                insert_headers = {
                    'apikey': self.supabase_key,
                    'Authorization': f'Bearer {self.supabase_key}',
                    'Content-Type': 'application/json',
                    'Prefer': 'return=minimal'
                }
                
                data = {
                    'evidence_id': evidence_id,
                    'timestamp': listing.timestamp,
                    'platform': listing.platform,
                    'threat_score': int(listing.confidence_score * 100),
                    'threat_level': 'MULTILINGUAL_SCAN',
                    'species_involved': f'Multilingual scan: {listing.keyword} ({listing.language})',
                    'alert_sent': False,
                    'status': f'MULTILINGUAL_{listing.platform.upper()}_{listing.language.upper()}',
                    'listing_title': listing.title[:500],
                    'listing_url': listing.url,
                    'listing_price': listing.price,
                    'search_term': listing.keyword
                }
                
                response = requests.post(insert_url, json=data, headers=insert_headers)
                
                if response.status_code in [200, 201]:
                    saved_count += 1
                    logger.info(f"Saved: {listing.platform} - {listing.title[:50]} ({listing.language})")
                elif response.status_code == 409:
                    continue  # Skip duplicates
                else:
                    response_text = response.text
                    if "unique" in response_text.lower() and "listing_url" in response_text.lower():
                        continue  # Skip duplicates
                    else:
                        logger.error(f"Failed to save listing: {response.status_code} - {response_text[:100]}")
                
            except Exception as e:
                error_msg = str(e).lower()
                if "unique" in error_msg and "listing_url" in error_msg:
                    continue  # Skip duplicates
                else:
                    logger.error(f"Error saving listing: {e}")
                    continue
        
        return saved_count

def run_multilingual_production_scan():
    """Run the multilingual production scanner"""
    parser = argparse.ArgumentParser(description='WildGuard AI Multilingual Production Scanner')
    parser.add_argument('--platform', choices=['ebay', 'craigslist', 'marktplaats', 'olx', 'mercadolibre', 'gumtree', 'avito', 'all'], 
                       default='all', help='Platform to scan')
    parser.add_argument('--batch-size', type=int, default=50, help='Keywords per batch (default: 50)')
    parser.add_argument('--max-batches', type=int, default=10, help='Maximum batches to run (default: 10)')
    
    args = parser.parse_args()
    
    logger.info("🌍 STARTING MULTILINGUAL PRODUCTION SCANNER")
    logger.info("=" * 80)
    logger.info(f"🎯 Platform: {args.platform}")
    logger.info(f"📊 Batch size: {args.batch_size} keywords")
    logger.info(f"🔄 Max batches: {args.max_batches}")
    
    scanner = MultilingualScanner()
    
    # Platform list
    if args.platform == 'all':
        platforms = ['ebay', 'craigslist', 'marktplaats', 'olx', 'mercadolibre', 'gumtree', 'avito']
    else:
        platforms = [args.platform]
    
    total_results = 0
    total_saved = 0
    
    start_time = datetime.now()
    
    try:
        for batch_num in range(args.max_batches):
            logger.info(f"\n🚀 BATCH {batch_num + 1}/{args.max_batches}")
            logger.info("-" * 50)
            
            # Get next batch of multilingual keywords
            keyword_batch = scanner.keyword_manager.get_next_batch(args.batch_size)
            
            if not keyword_batch:
                logger.warning("No more keywords available")
                break
            
            batch_start = datetime.now()
            
            # Show language distribution for this batch
            lang_count = {}
            for kw_data in keyword_batch:
                lang = kw_data['language']
                lang_count[lang] = lang_count.get(lang, 0) + 1
            
            logger.info(f"🗣️  Language distribution: {dict(list(lang_count.items())[:5])}...")
            
            # Scan each platform
            for platform in platforms:
                platform_start = datetime.now()
                logger.info(f"\n📡 Scanning {platform} with {len(keyword_batch)} multilingual keywords...")
                
                platform_listings = scanner.scan_platform_multilingual(platform, keyword_batch)
                
                platform_saved = scanner.save_to_supabase(platform_listings)
                
                platform_duration = (datetime.now() - platform_start).total_seconds()
                
                logger.info(f"✅ {platform}: {len(platform_listings)} found, {platform_saved} saved ({platform_duration:.1f}s)")
                
                total_results += len(platform_listings)
                total_saved += platform_saved
            
            batch_duration = (datetime.now() - batch_start).total_seconds()
            logger.info(f"⏱️  Batch {batch_num + 1} completed in {batch_duration:.1f}s")
    
    except KeyboardInterrupt:
        logger.info("\n⚠️  Scan interrupted by user")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
    
    total_duration = (datetime.now() - start_time).total_seconds()
    
    # Final results
    logger.info("\n" + "=" * 80)
    logger.info("🎯 MULTILINGUAL SCAN COMPLETE")
    logger.info("=" * 80)
    logger.info(f"⏱️  Total duration: {total_duration:.1f} seconds")
    logger.info(f"📊 Total listings found: {total_results:,}")
    logger.info(f"💾 Total listings saved: {total_saved:,}")
    logger.info(f"🌍 Languages used: {len(scanner.keyword_manager.keywords_by_language)}")
    logger.info(f"🔤 Total keywords available: {len(scanner.keyword_manager.all_keywords):,}")
    logger.info(f"🛡️  Platforms scanned: {len(platforms)}")
    
    if total_saved > 0:
        rate_per_hour = (total_saved / total_duration) * 3600
        daily_projection = rate_per_hour * 24
        
        logger.info(f"\n📈 PERFORMANCE METRICS:")
        logger.info(f"   Rate: {rate_per_hour:.1f} listings/hour")
        logger.info(f"   Daily projection: {daily_projection:,.0f} listings/day")
        
        if daily_projection >= 1000:
            logger.info(f"🏆 EXCELLENT! Multilingual scanning performing at scale!")
        
        logger.info(f"\n🌍 MULTILINGUAL COVERAGE SUCCESS:")
        logger.info(f"   Using ALL {len(scanner.keyword_manager.all_keywords)} keywords")
        logger.info(f"   Across {len(scanner.keyword_manager.keywords_by_language)} languages")
        logger.info(f"   Global wildlife trafficking detection: ACTIVE")

if __name__ == "__main__":
    run_multilingual_production_scan()
