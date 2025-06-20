#!/usr/bin/env python3
"""
WildGuard AI - Fixed Schema Scanner
Matches your ACTUAL table structure (no listing_price column)
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
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

class FixedSchemaScanner:
    """Scanner that matches your actual table structure"""
    
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
        
        logging.info("✅ Fixed schema scanner initialized")

    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=180)
        self.session = aiohttp.ClientSession(timeout=timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def discover_table_structure(self) -> List[str]:
        """Discover the actual table structure by examining existing data"""
        try:
            headers = {
                "apikey": self.supabase_key,
                "Authorization": f"Bearer {self.supabase_key}",
                "Content-Type": "application/json"
            }
            
            # Get one existing record to see the actual structure
            url = f"{self.supabase_url}/rest/v1/detections?select=*&limit=1"
            
            async with self.session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data:
                        columns = list(data[0].keys())
                        logging.info(f"✅ Discovered actual table columns: {columns}")
                        return columns
                    else:
                        logging.warning("⚠️ No existing data found")
                        return []
                else:
                    logging.error(f"❌ Could not discover table structure: {resp.status}")
                    return []
                    
        except Exception as e:
            logging.error(f"❌ Error discovering table structure: {e}")
            return []

    async def run_fixed_scan(self) -> Dict[str, Any]:
        """Run scan with discovered table structure"""
        scan_id = f"FIXED-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        start_time = datetime.now()
        
        logging.info(f"🚀 Starting FIXED SCHEMA scan {scan_id}")
        
        # Discover actual table structure first
        actual_columns = await self.discover_table_structure()
        
        if not actual_columns:
            logging.error("❌ Could not discover table structure - aborting")
            return {'status': 'FAILED', 'error': 'Could not discover table structure'}
        
        try:
            # Test eBay API with a small sample first
            ebay_results = await self.scan_ebay_sample()
            
            if ebay_results:
                logging.info(f"🔍 Testing storage with {len(ebay_results)} sample results...")
                stored = await self.store_results_fixed(ebay_results, actual_columns)
                
                self.total_results = len(ebay_results)
                self.total_stored = stored
                
                logging.info(f"✅ Sample test: {len(ebay_results)} results, {stored} stored")
                
                if stored > 0:
                    logging.info("🎉 Schema fixed! Storage working correctly.")
                    
                    # Now do a larger scan
                    logging.info("🚀 Running larger scan now that schema is fixed...")
                    larger_results = await self.scan_ebay_larger()
                    
                    if larger_results:
                        larger_stored = await self.store_results_fixed(larger_results, actual_columns)
                        self.total_results += len(larger_results)
                        self.total_stored += larger_stored
                        
                        logging.info(f"✅ Larger scan: {len(larger_results)} results, {larger_stored} stored")
                else:
                    logging.error("❌ Storage still failing even with discovered schema")
            
            duration = (datetime.now() - start_time).total_seconds()
            
            result = {
                'scan_id': scan_id,
                'timestamp': start_time.isoformat(),
                'duration_seconds': duration,
                'total_results': self.total_results,
                'total_stored': self.total_stored,
                'discovered_columns': actual_columns,
                'success_rate': (self.total_stored / self.total_results * 100) if self.total_results > 0 else 0,
                'status': 'SUCCESS' if self.total_stored > 0 else 'FAILED'
            }
            
            logging.info(f"🎯 FIXED SCHEMA SCAN SUMMARY:")
            logging.info(f"   Results: {self.total_results}, Stored: {self.total_stored}")
            logging.info(f"   Success Rate: {result['success_rate']:.1f}%")
            logging.info(f"   Table Columns: {actual_columns}")
            
            return result
            
        except Exception as e:
            logging.error(f"💥 Fixed scan failed: {e}")
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
                    params = {"q": "antique", "limit": "10"}
                    
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
        """Larger eBay scan once schema is confirmed working"""
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
                    
                    # Multiple searches for larger sample
                    keywords = ['antique', 'vintage', 'collectible', 'art', 'jewelry']
                    
                    for keyword in keywords:
                        params = {"q": keyword, "limit": "50"}
                        
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
                                
                                await asyncio.sleep(0.5)  # Rate limiting
                            else:
                                logging.warning(f"eBay search failed for {keyword}: {search_resp.status}")
                    
                    logging.info(f"✅ eBay larger scan: {len(results)} results")
                else:
                    logging.error(f"❌ eBay auth failed: {resp.status}")
                    
        except Exception as e:
            logging.error(f"❌ eBay larger scan error: {e}")
            
        return results

    async def store_results_fixed(self, results: List[Dict], actual_columns: List[str]) -> int:
        """Store results using only the columns that actually exist"""
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
                timestamp_ms = int(time.time() * 1000)
                evidence_id = f"FIXED-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{timestamp_ms}-{i+1:04d}"
                
                # Build detection record using ONLY columns that exist
                detection = {}
                
                # Map our data to actual table columns
                if 'evidence_id' in actual_columns:
                    detection['evidence_id'] = evidence_id
                if 'id' in actual_columns:
                    detection['id'] = evidence_id
                    
                if 'timestamp' in actual_columns:
                    detection['timestamp'] = datetime.now().isoformat()
                if 'created_at' in actual_columns:
                    detection['created_at'] = datetime.now().isoformat()
                    
                if 'platform' in actual_columns:
                    detection['platform'] = result.get('platform', 'ebay')
                    
                if 'threat_score' in actual_columns:
                    detection['threat_score'] = 50
                if 'score' in actual_columns:
                    detection['score'] = 50
                    
                if 'threat_level' in actual_columns:
                    detection['threat_level'] = 'UNRATED'
                if 'level' in actual_columns:
                    detection['level'] = 'UNRATED'
                    
                if 'species_involved' in actual_columns:
                    detection['species_involved'] = f"Scan: {result.get('search_term', 'unknown')}"
                if 'species' in actual_columns:
                    detection['species'] = f"Scan: {result.get('search_term', 'unknown')}"
                    
                if 'alert_sent' in actual_columns:
                    detection['alert_sent'] = False
                    
                if 'status' in actual_columns:
                    detection['status'] = 'GITHUB_ACTIONS_FIXED'
                    
                # Handle title/URL/price with various possible column names
                title = result.get('title', '')[:500]
                if 'listing_title' in actual_columns:
                    detection['listing_title'] = title
                elif 'title' in actual_columns:
                    detection['title'] = title
                elif 'name' in actual_columns:
                    detection['name'] = title
                    
                url = result.get('url', '')
                if 'listing_url' in actual_columns:
                    detection['listing_url'] = url
                elif 'url' in actual_columns:
                    detection['url'] = url
                elif 'link' in actual_columns:
                    detection['link'] = url
                    
                price = str(result.get('price', ''))
                if 'listing_price' in actual_columns:
                    detection['listing_price'] = price
                elif 'price' in actual_columns:
                    detection['price'] = price
                elif 'cost' in actual_columns:
                    detection['cost'] = price
                    
                search_term = result.get('search_term', '')
                if 'search_term' in actual_columns:
                    detection['search_term'] = search_term
                elif 'keyword' in actual_columns:
                    detection['keyword'] = search_term
                elif 'query' in actual_columns:
                    detection['query'] = search_term
                
                # Remove any None values
                detection = {k: v for k, v in detection.items() if v is not None}
                
                logging.info(f"🔍 Attempting to store: {list(detection.keys())}")
                
                url = f"{self.supabase_url}/rest/v1/detections"
                
                async with self.session.post(url, headers=headers, json=detection) as resp:
                    if resp.status in [200, 201]:
                        stored_count += 1
                        if stored_count <= 3:  # Log first few successes
                            logging.info(f"✅ Successfully stored item {i+1}")
                    else:
                        error_text = await resp.text()
                        logging.error(f"❌ Storage failed for item {i+1}: {resp.status} - {error_text}")
                        
                        # If first few items fail, log the details
                        if i < 3:
                            logging.error(f"   Attempted data: {detection}")
                            logging.error(f"   Available columns: {actual_columns}")
                        
                        # Don't continue if we're still getting schema errors
                        if i > 5 and stored_count == 0:
                            logging.error("❌ Still getting storage errors after 5 attempts - stopping")
                            break
                            
            except Exception as e:
                logging.error(f"❌ Error storing result {i+1}: {e}")
                continue
        
        logging.info(f"💾 Stored {stored_count}/{len(results)} results")
        return stored_count


async def run_fixed_scan():
    """Run the fixed schema scan"""
    try:
        async with FixedSchemaScanner() as scanner:
            result = await scanner.run_fixed_scan()
            
            print("\n" + "="*80)
            print("🎯 FIXED SCHEMA SCAN SUMMARY")
            print("="*80)
            print(f"Scan ID: {result['scan_id']}")
            print(f"Total Results: {result['total_results']:,}")
            print(f"Total Stored: {result['total_stored']:,}")
            print(f"Success Rate: {result.get('success_rate', 0):.1f}%")
            print(f"Status: {result['status']}")
            print(f"Discovered Columns: {result.get('discovered_columns', [])}")
            
            if result.get('success_rate', 0) > 80:
                print("\n🎉 Schema fixed! Ready to scale up.")
            elif result.get('total_stored', 0) > 0:
                print("\n⚠️ Partial success - may need further schema adjustments")
            else:
                print("\n❌ Schema still needs fixing")
            
            if result['status'] == 'FAILED':
                sys.exit(1)
                
            return result
            
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        logging.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    print("🔧 WildGuard AI - FIXED SCHEMA Scanner")
    print("🎯 Discovering and matching your actual table structure")
    print("-" * 80)
    
    asyncio.run(run_fixed_scan())
