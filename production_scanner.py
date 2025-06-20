#!/usr/bin/env python3
"""
WildGuard AI - FINAL FIXED Scanner
Correctly handles auto-incrementing ID column
"""

import asyncio
import aiohttp
import os
import base64
import json
import logging
import sys
from datetime import datetime
from typing import List, Dict, Any
import traceback

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

class FinalFixedScanner:
    """Final scanner with correct ID handling"""
    
    def __init__(self):
        self.session = None
        self.total_results = 0
        self.total_stored = 0
        
        # Check environment
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        self.ebay_app_id = os.getenv('EBAY_APP_ID')
        self.ebay_cert_id = os.getenv('EBAY_CERT_ID')
        
        if not all([self.supabase_url, self.supabase_key, self.ebay_app_id, self.ebay_cert_id]):
            logging.error("❌ Missing required environment variables")
            sys.exit(1)
        
        logging.info("✅ Final fixed scanner initialized")

    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=180)
        self.session = aiohttp.ClientSession(timeout=timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def run_final_scan(self) -> Dict[str, Any]:
        """Run final scan with correct schema"""
        scan_id = f"FINAL-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        start_time = datetime.now()
        
        logging.info(f"🚀 Starting FINAL FIXED scan {scan_id}")
        
        try:
            # Test with small sample first
            ebay_results = await self.scan_ebay_sample()
            
            if ebay_results:
                logging.info(f"🔍 Testing storage with {len(ebay_results)} sample results...")
                stored = await self.store_results_final(ebay_results)
                
                self.total_results = len(ebay_results)
                self.total_stored = stored
                
                logging.info(f"✅ Sample test: {len(ebay_results)} results, {stored} stored")
                
                if stored > 0:
                    logging.info("🎉 Schema FINALLY fixed! Storage working correctly.")
                    
                    # Scale up gradually
                    logging.info("🚀 Running larger scan...")
                    larger_results = await self.scan_ebay_larger()
                    
                    if larger_results:
                        larger_stored = await self.store_results_final(larger_results)
                        self.total_results += len(larger_results)
                        self.total_stored += larger_stored
                        
                        logging.info(f"✅ Larger scan: {len(larger_results)} results, {larger_stored} stored")
                        
                        # If that works, do an even bigger scan
                        if larger_stored > 0:
                            logging.info("🚀 Running full scan...")
                            full_results = await self.scan_ebay_full()
                            
                            if full_results:
                                full_stored = await self.store_results_final(full_results)
                                self.total_results += len(full_results)
                                self.total_stored += full_stored
                                
                                logging.info(f"✅ Full scan: {len(full_results)} results, {full_stored} stored")
                else:
                    logging.error("❌ Storage still failing")
            
            duration = (datetime.now() - start_time).total_seconds()
            
            result = {
                'scan_id': scan_id,
                'timestamp': start_time.isoformat(),
                'duration_seconds': duration,
                'total_results': self.total_results,
                'total_stored': self.total_stored,
                'success_rate': (self.total_stored / self.total_results * 100) if self.total_results > 0 else 0,
                'hourly_projection': int(self.total_results * 3600 / duration) if duration > 0 else 0,
                'daily_projection': int(self.total_results * 24),
                'status': 'SUCCESS' if self.total_stored > 0 else 'FAILED'
            }
            
            logging.info(f"🎯 FINAL SCAN SUMMARY:")
            logging.info(f"   Results: {self.total_results:,}, Stored: {self.total_stored:,}")
            logging.info(f"   Success Rate: {result['success_rate']:.1f}%")
            logging.info(f"   Hourly Projection: {result['hourly_projection']:,}")
            logging.info(f"   Daily Projection: {result['daily_projection']:,}")
            
            return result
            
        except Exception as e:
            logging.error(f"💥 Final scan failed: {e}")
            logging.error(traceback.format_exc())
            raise

    async def scan_ebay_sample(self) -> List[Dict]:
        """Small eBay sample for testing"""
        results = []
        
        try:
            # Get OAuth token
            credentials = f"{self.ebay_app_id}:{self.ebay_cert_id}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers_auth = {
                "Authorization": f"Basic {encoded_credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            
            data = {
                "grant_type": "client_credentials",
                "scope": "https://api.ebay.com/oauth/api_scope",
            }

            async with self.session.post(
                "https://api.ebay.com/identity/v1/oauth2/token", 
                headers=headers_auth, 
                data=data
            ) as resp:
                if resp.status == 200:
                    token_data = await resp.json()
                    oauth_token = token_data["access_token"]
                    
                    headers = {
                        "Authorization": f"Bearer {oauth_token}",
                        "Content-Type": "application/json",
                    }
                    
                    # Small sample search
                    params = {"q": "antique", "limit": "5"}
                    
                    async with self.session.get(
                        "https://api.ebay.com/buy/browse/v1/item_summary/search",
                        headers=headers, 
                        params=params
                    ) as search_resp:
                        if search_resp.status == 200:
                            data = await search_resp.json()
                            items = data.get("itemSummaries", [])
                            
                            for item in items:
                                results.append({
                                    "title": item.get("title", ""),
                                    "price": str(item.get("price", {}).get("value", "")),
                                    "url": item.get("itemWebUrl", ""),
                                    "search_term": "antique",
                                    "platform": "ebay"
                                })
                            
                            logging.info(f"✅ eBay sample: {len(results)} results")
                        else:
                            logging.error(f"❌ eBay search failed: {search_resp.status}")
                else:
                    logging.error(f"❌ eBay auth failed: {resp.status}")
                    
        except Exception as e:
            logging.error(f"❌ eBay sample error: {e}")
            
        return results

    async def scan_ebay_larger(self) -> List[Dict]:
        """Medium eBay scan"""
        results = []
        
        try:
            # Get OAuth token
            credentials = f"{self.ebay_app_id}:{self.ebay_cert_id}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers_auth = {
                "Authorization": f"Basic {encoded_credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            
            data = {
                "grant_type": "client_credentials",
                "scope": "https://api.ebay.com/oauth/api_scope",
            }

            async with self.session.post(
                "https://api.ebay.com/identity/v1/oauth2/token", 
                headers=headers_auth, 
                data=data
            ) as resp:
                if resp.status == 200:
                    token_data = await resp.json()
                    oauth_token = token_data["access_token"]
                    
                    headers = {
                        "Authorization": f"Bearer {oauth_token}",
                        "Content-Type": "application/json",
                    }
                    
                    # Medium searches
                    keywords = ['antique', 'vintage', 'collectible']
                    
                    for keyword in keywords:
                        params = {"q": keyword, "limit": "20"}
                        
                        async with self.session.get(
                            "https://api.ebay.com/buy/browse/v1/item_summary/search",
                            headers=headers, 
                            params=params
                        ) as search_resp:
                            if search_resp.status == 200:
                                data = await search_resp.json()
                                items = data.get("itemSummaries", [])
                                
                                for item in items:
                                    results.append({
                                        "title": item.get("title", ""),
                                        "price": str(item.get("price", {}).get("value", "")),
                                        "url": item.get("itemWebUrl", ""),
                                        "search_term": keyword,
                                        "platform": "ebay"
                                    })
                                
                                await asyncio.sleep(0.5)
                            else:
                                logging.warning(f"eBay search failed for {keyword}: {search_resp.status}")
                    
                    logging.info(f"✅ eBay medium scan: {len(results)} results")
                else:
                    logging.error(f"❌ eBay auth failed: {resp.status}")
                    
        except Exception as e:
            logging.error(f"❌ eBay medium scan error: {e}")
            
        return results

    async def scan_ebay_full(self) -> List[Dict]:
        """Full eBay scan"""
        results = []
        
        try:
            # Get OAuth token
            credentials = f"{self.ebay_app_id}:{self.ebay_cert_id}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers_auth = {
                "Authorization": f"Basic {encoded_credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            
            data = {
                "grant_type": "client_credentials",
                "scope": "https://api.ebay.com/oauth/api_scope",
            }

            async with self.session.post(
                "https://api.ebay.com/identity/v1/oauth2/token", 
                headers=headers_auth, 
                data=data
            ) as resp:
                if resp.status == 200:
                    token_data = await resp.json()
                    oauth_token = token_data["access_token"]
                    
                    headers = {
                        "Authorization": f"Bearer {oauth_token}",
                        "Content-Type": "application/json",
                    }
                    
                    # Full searches
                    keywords = ['antique', 'vintage', 'collectible', 'art', 'jewelry', 'carved', 'tribal', 'cultural']
                    categories = ["", "20081", "550"]  # All, Antiques, Art
                    
                    for keyword in keywords:
                        for category in categories:
                            params = {"q": keyword, "limit": "100"}
                            if category:
                                params["category_ids"] = category
                            
                            async with self.session.get(
                                "https://api.ebay.com/buy/browse/v1/item_summary/search",
                                headers=headers, 
                                params=params
                            ) as search_resp:
                                if search_resp.status == 200:
                                    data = await search_resp.json()
                                    items = data.get("itemSummaries", [])
                                    
                                    for item in items:
                                        results.append({
                                            "title": item.get("title", ""),
                                            "price": str(item.get("price", {}).get("value", "")),
                                            "url": item.get("itemWebUrl", ""),
                                            "search_term": keyword,
                                            "platform": "ebay",
                                            "category": category or "all"
                                        })
                                    
                                    await asyncio.sleep(0.2)
                                else:
                                    logging.warning(f"eBay search failed for {keyword}/{category}: {search_resp.status}")
                    
                    logging.info(f"✅ eBay full scan: {len(results)} results")
                else:
                    logging.error(f"❌ eBay auth failed: {resp.status}")
                    
        except Exception as e:
            logging.error(f"❌ eBay full scan error: {e}")
            
        return results

    async def store_results_final(self, results: List[Dict]) -> int:
        """Store results with CORRECT ID handling"""
        if not results:
            return 0
        
        stored_count = 0
        
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        
        for i, result in enumerate(results):
            try:
                # Create unique evidence_id (but NOT id - that's auto-generated)
                evidence_id = f"FINAL-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{i+1:04d}"
                
                # Build detection record - DO NOT INCLUDE 'id' since it's auto-incrementing
                detection = {
                    'evidence_id': evidence_id,  # This is the string identifier we control
                    'timestamp': datetime.now().isoformat(),
                    'platform': result.get('platform', 'ebay'),
                    'threat_score': 50,
                    'threat_level': 'UNRATED',
                    'species_involved': f"Scan: {result.get('search_term', 'unknown')}",
                    'alert_sent': False,
                    'status': 'FINAL_GITHUB_ACTIONS'
                }
                
                # Add optional fields if we have them in the table structure
                title = result.get('title', '')[:500] if result.get('title') else ''
                if title:
                    detection['listing_title'] = title
                
                url = result.get('url', '') if result.get('url') else ''
                if url:
                    detection['listing_url'] = url
                    
                price = str(result.get('price', '')) if result.get('price') else ''
                if price:
                    detection['listing_price'] = price
                    
                search_term = result.get('search_term', '') if result.get('search_term') else ''
                if search_term:
                    detection['search_term'] = search_term
                
                # Remove any None values
                detection = {k: v for k, v in detection.items() if v is not None}
                
                if i < 3:  # Log first few attempts
                    logging.info(f"🔍 Storing item {i+1}: {list(detection.keys())}")
                
                url = f"{self.supabase_url}/rest/v1/detections"
                
                async with self.session.post(url, headers=headers, json=detection) as resp:
                    if resp.status in [200, 201]:
                        stored_count += 1
                        if stored_count <= 3:
                            logging.info(f"✅ Successfully stored item {i+1}")
                    else:
                        error_text = await resp.text()
                        if i < 3:  # Only log first few errors
                            logging.error(f"❌ Storage failed for item {i+1}: {resp.status} - {error_text}")
                        
                        # If still getting errors after several attempts, stop
                        if i > 3 and stored_count == 0:
                            logging.error("❌ Still getting errors - stopping")
                            break
                            
            except Exception as e:
                if i < 3:
                    logging.error(f"❌ Error storing result {i+1}: {e}")
                continue
        
        logging.info(f"💾 Stored {stored_count}/{len(results)} results ({(stored_count/len(results)*100):.1f}% success)")
        return stored_count


async def run_final_scan():
    """Run the final fixed scan"""
    try:
        async with FinalFixedScanner() as scanner:
            result = await scanner.run_final_scan()
            
            print("\n" + "="*80)
            print("🎯 FINAL FIXED SCAN SUMMARY")
            print("="*80)
            print(f"Scan ID: {result['scan_id']}")
            print(f"Total Results: {result['total_results']:,}")
            print(f"Total Stored: {result['total_stored']:,}")
            print(f"Success Rate: {result.get('success_rate', 0):.1f}%")
            print(f"Hourly Projection: {result.get('hourly_projection', 0):,}")
            print(f"Daily Projection: {result.get('daily_projection', 0):,}")
            print(f"Status: {result['status']}")
            
            if result.get('success_rate', 0) > 90:
                print("\n🎉 SUCCESS! Schema fully fixed and ready to scale!")
            elif result.get('total_stored', 0) > 0:
                print("\n⚠️ Partial success - needs minor adjustments")
            else:
                print("\n❌ Still needs fixing")
            
            if result['status'] == 'FAILED':
                sys.exit(1)
                
            return result
            
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        logging.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    print("🔧 WildGuard AI - FINAL FIXED Scanner")
    print("🎯 Correctly handling auto-incrementing ID column")
    print("-" * 80)
    
    asyncio.run(run_final_scan())
