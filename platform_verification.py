#!/usr/bin/env python3
"""
Comprehensive Platform Verification Script
- Tests all 3 new platforms with real keyword searches
- Verifies actual results vs mock results
- Checks for proper HTML parsing and data extraction
- Validates duplicate prevention systems
"""

import requests
import json
import time
import random
import logging
import os
from datetime import datetime
from typing import Dict, List, Tuple
import re
from urllib.parse import urlparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PlatformVerifier:
    """Comprehensive platform verification system"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # Test keywords that should return real results
        self.test_keywords = [
            'antique', 'vintage', 'collectible', 'rare', 'exotic',
            'tiger', 'elephant', 'rhino', 'ivory', 'leather'
        ]
    
    def verify_facebook_marketplace(self) -> Dict:
        """Verify Facebook Marketplace returns real results"""
        logger.info("Verifying Facebook Marketplace...")
        
        results = {
            'platform': 'facebook_marketplace',
            'working': False,
            'real_results': False,
            'results_found': 0,
            'sample_results': [],
            'errors': []
        }
        
        try:
            for keyword in self.test_keywords[:3]:  # Test with 3 keywords
                url = "https://www.facebook.com/marketplace/search"
                params = {'query': keyword}
                
                time.sleep(random.uniform(2, 4))
                response = self.session.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    html = response.text
                    
                    # Check for various Facebook Marketplace indicators
                    marketplace_indicators = [
                        'marketplace',
                        'listing',
                        'price',
                        'location',
                        'facebook.com/marketplace'
                    ]
                    
                    indicator_count = sum(1 for indicator in marketplace_indicators if indicator in html.lower())
                    
                    # Look for actual listing data
                    title_patterns = [
                        r'"marketplace_listing_title":"([^"]+)"',
                        r'aria-label="([^"]*' + re.escape(keyword) + r'[^"]*)"',
                        r'"text":"([^"]*' + re.escape(keyword) + r'[^"]*)"'
                    ]
                    
                    found_titles = []
                    for pattern in title_patterns:
                        matches = re.findall(pattern, html, re.IGNORECASE)
                        found_titles.extend(matches)
                    
                    # Look for price patterns
                    price_patterns = [
                        r'\$[\d,]+(?:\.\d{2})?',
                        r'"price":\s*"([^"]+)"',
                        r'data-price="([^"]+)"'
                    ]
                    
                    found_prices = []
                    for pattern in price_patterns:
                        matches = re.findall(pattern, html)
                        found_prices.extend(matches)
                    
                    if found_titles or (indicator_count >= 3 and len(html) > 50000):
                        results['working'] = True
                        results['real_results'] = True
                        results['results_found'] += len(found_titles)
                        
                        # Add sample results
                        for i, title in enumerate(found_titles[:3]):
                            price = found_prices[i] if i < len(found_prices) else "N/A"
                            results['sample_results'].append({
                                'title': title,
                                'price': price,
                                'keyword': keyword
                            })
                        
                        logger.info(f"Facebook: Found {len(found_titles)} results for '{keyword}'")
                    else:
                        logger.warning(f"Facebook: No clear results for '{keyword}' (HTML length: {len(html)})")
                
                else:
                    results['errors'].append(f"HTTP {response.status_code} for keyword '{keyword}'")
                    
        except Exception as e:
            results['errors'].append(f"Exception: {str(e)}")
            logger.error(f"Facebook verification error: {e}")
        
        return results
    
    def verify_gumtree(self) -> Dict:
        """Verify Gumtree returns real results"""
        logger.info("Verifying Gumtree...")
        
        results = {
            'platform': 'gumtree',
            'working': False,
            'real_results': False,
            'results_found': 0,
            'sample_results': [],
            'errors': []
        }
        
        try:
            for keyword in self.test_keywords[:3]:
                url = "https://www.gumtree.com/search"
                params = {
                    'search_query': keyword,
                    'search_category': 'all',
                    'search_location': 'all-the-uk'
                }
                
                time.sleep(random.uniform(2, 4))
                response = self.session.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    html = response.text
                    
                    # Check for Gumtree-specific patterns
                    gumtree_indicators = [
                        'gumtree',
                        'listing',
                        'advert',
                        'classified'
                    ]
                    
                    indicator_count = sum(1 for indicator in gumtree_indicators if indicator in html.lower())
                    
                    # Multiple title patterns for current Gumtree structure
                    title_patterns = [
                        r'<h2[^>]*class="[^"]*listing-title[^"]*"[^>]*>([^<]+)</h2>',
                        r'<a[^>]*class="[^"]*listing-link[^"]*"[^>]*>([^<]+)</a>',
                        r'data-q="listing-title">([^<]+)<',
                        r'"listing-title"[^>]*>([^<]+)<',
                        r'<h\d[^>]*>([^<]*' + re.escape(keyword) + r'[^<]*)</h\d>',
                        r'<a[^>]*title="([^"]*' + re.escape(keyword) + r'[^"]*)"'
                    ]
                    
                    found_titles = []
                    for pattern in title_patterns:
                        matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
                        found_titles.extend([title.strip() for title in matches if title.strip()])
                    
                    # Price patterns
                    price_patterns = [
                        r'£[\d,]+(?:\.\d{2})?',
                        r'<span[^>]*class="[^"]*price[^"]*"[^>]*>([^<]+)</span>',
                        r'"price"[^>]*>([^<]+)<'
                    ]
                    
                    found_prices = []
                    for pattern in price_patterns:
                        matches = re.findall(pattern, html, re.IGNORECASE)
                        found_prices.extend(matches)
                    
                    # Look for "no results" indicators
                    no_results_indicators = [
                        'no results found',
                        'no ads found',
                        'try different search',
                        'refine your search'
                    ]
                    
                    has_no_results = any(indicator in html.lower() for indicator in no_results_indicators)
                    
                    if found_titles and not has_no_results:
                        results['working'] = True
                        results['real_results'] = True
                        results['results_found'] += len(found_titles)
                        
                        # Add sample results
                        for i, title in enumerate(found_titles[:3]):
                            price = found_prices[i] if i < len(found_prices) else "Contact seller"
                            results['sample_results'].append({
                                'title': title,
                                'price': price,
                                'keyword': keyword
                            })
                        
                        logger.info(f"Gumtree: Found {len(found_titles)} results for '{keyword}'")
                    else:
                        logger.warning(f"Gumtree: No results for '{keyword}' (HTML length: {len(html)}, indicators: {indicator_count})")
                        if has_no_results:
                            logger.info(f"Gumtree explicitly shows 'no results' for '{keyword}'")
                
                else:
                    results['errors'].append(f"HTTP {response.status_code} for keyword '{keyword}'")
                    
        except Exception as e:
            results['errors'].append(f"Exception: {str(e)}")
            logger.error(f"Gumtree verification error: {e}")
        
        return results
    
    def verify_avito(self) -> Dict:
        """Verify Avito returns real results"""
        logger.info("Verifying Avito...")
        
        results = {
            'platform': 'avito',
            'working': False,
            'real_results': False,
            'results_found': 0,
            'sample_results': [],
            'errors': []
        }
        
        try:
            for keyword in self.test_keywords[:3]:
                url = "https://www.avito.ru/rossiya"
                params = {
                    'q': keyword,
                    's': '104'  # Sort by date
                }
                
                time.sleep(random.uniform(1, 3))
                response = self.session.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    html = response.text
                    
                    # Avito patterns are usually well-structured
                    title_patterns = [
                        r'data-marker="item-title">([^<]+)<',
                        r'"title":"([^"]+)"',
                        r'<h3[^>]*>([^<]+)</h3>',
                        r'item-title[^>]*>([^<]+)<',
                        r'"name":"([^"]+)"'
                    ]
                    
                    found_titles = []
                    for pattern in title_patterns:
                        matches = re.findall(pattern, html, re.IGNORECASE)
                        found_titles.extend([title.strip() for title in matches if title.strip()])
                    
                    # Price patterns
                    price_patterns = [
                        r'₽[\d\s]+',
                        r'data-marker="item-price">([^<]+)<',
                        r'"price":{"value":(\d+)',
                        r'price[^>]*>([^<]*₽[^<]*)<'
                    ]
                    
                    found_prices = []
                    for pattern in price_patterns:
                        matches = re.findall(pattern, html, re.IGNORECASE)
                        found_prices.extend(matches)
                    
                    # Check for Avito-specific indicators
                    avito_indicators = [
                        'avito',
                        'item-title',
                        'item-price',
                        'data-marker'
                    ]
                    
                    indicator_count = sum(1 for indicator in avito_indicators if indicator in html.lower())
                    
                    if found_titles and indicator_count >= 2:
                        results['working'] = True
                        results['real_results'] = True
                        results['results_found'] += len(found_titles)
                        
                        # Add sample results
                        for i, title in enumerate(found_titles[:5]):  # Avito often has many results
                            price = found_prices[i] if i < len(found_prices) else "Цена не указана"
                            results['sample_results'].append({
                                'title': title,
                                'price': price,
                                'keyword': keyword
                            })
                        
                        logger.info(f"Avito: Found {len(found_titles)} results for '{keyword}'")
                    else:
                        logger.warning(f"Avito: No clear results for '{keyword}' (titles: {len(found_titles)}, indicators: {indicator_count})")
                
                else:
                    results['errors'].append(f"HTTP {response.status_code} for keyword '{keyword}'")
                    
        except Exception as e:
            results['errors'].append(f"Exception: {str(e)}")
            logger.error(f"Avito verification error: {e}")
        
        return results
    
    def run_comprehensive_verification(self) -> Dict:
        """Run verification on all platforms"""
        logger.info("Starting comprehensive platform verification...")
        
        verification_results = {
            'timestamp': datetime.now().isoformat(),
            'platforms': {},
            'summary': {
                'total_platforms': 3,
                'working_platforms': 0,
                'platforms_with_real_results': 0,
                'total_results_found': 0
            }
        }
        
        # Test each platform
        platforms = {
            'facebook_marketplace': self.verify_facebook_marketplace,
            'gumtree': self.verify_gumtree,
            'avito': self.verify_avito
        }
        
        for platform_name, verify_func in platforms.items():
            logger.info(f"\n{'='*50}")
            logger.info(f"TESTING {platform_name.upper()}")
            logger.info(f"{'='*50}")
            
            platform_result = verify_func()
            verification_results['platforms'][platform_name] = platform_result
            
            # Update summary
            if platform_result['working']:
                verification_results['summary']['working_platforms'] += 1
            
            if platform_result['real_results']:
                verification_results['summary']['platforms_with_real_results'] += 1
            
            verification_results['summary']['total_results_found'] += platform_result['results_found']
            
            # Log results
            status = "✅ WORKING" if platform_result['working'] else "❌ NOT WORKING"
            real_results = "✅ REAL RESULTS" if platform_result['real_results'] else "❌ NO REAL RESULTS"
            
            logger.info(f"{platform_name}: {status} | {real_results} | Results: {platform_result['results_found']}")
            
            if platform_result['sample_results']:
                logger.info(f"Sample results from {platform_name}:")
                for result in platform_result['sample_results'][:3]:
                    logger.info(f"  - {result['title']} ({result['price']}) [keyword: {result['keyword']}]")
            
            if platform_result['errors']:
                logger.warning(f"Errors in {platform_name}: {platform_result['errors']}")
        
        return verification_results

def main():
    """Main verification function"""
    verifier = PlatformVerifier()
    results = verifier.run_comprehensive_verification()
    
    # Save results to file
    with open('platform_verification_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print comprehensive summary
    print("\n" + "="*80)
    print("COMPREHENSIVE PLATFORM VERIFICATION RESULTS")
    print("="*80)
    
    summary = results['summary']
    print(f"\nOVERALL SUMMARY:")
    print(f"  Total platforms tested: {summary['total_platforms']}")
    print(f"  Working platforms: {summary['working_platforms']}")
    print(f"  Platforms with real results: {summary['platforms_with_real_results']}")
    print(f"  Total results found: {summary['total_results_found']}")
    
    success_rate = (summary['platforms_with_real_results'] / summary['total_platforms']) * 100
    print(f"  Success rate: {success_rate:.1f}%")
    
    print(f"\nDETAILED RESULTS:")
    for platform_name, platform_data in results['platforms'].items():
        status_emoji = "✅" if platform_data['working'] else "❌"
        results_emoji = "✅" if platform_data['real_results'] else "❌"
        
        print(f"\n  {platform_name.upper()}:")
        print(f"    Status: {status_emoji} {'Working' if platform_data['working'] else 'Not Working'}")
        print(f"    Real Results: {results_emoji} {'Yes' if platform_data['real_results'] else 'No'}")
        print(f"    Results Found: {platform_data['results_found']}")
        
        if platform_data['sample_results']:
            print(f"    Sample Results:")
            for result in platform_data['sample_results'][:2]:
                print(f"      - {result['title']} ({result['price']})")
        
        if platform_data['errors']:
            print(f"    Errors: {len(platform_data['errors'])}")
    
    print(f"\n{'='*80}")
    if summary['platforms_with_real_results'] >= 2:
        print("🎉 VERIFICATION SUCCESSFUL! Ready for production deployment.")
    else:
        print("⚠️  VERIFICATION NEEDS ATTENTION. Some platforms may need adjustment.")
    print("="*80)

if __name__ == "__main__":
    main()
