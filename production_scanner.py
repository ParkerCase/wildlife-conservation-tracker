#!/usr/bin/env python3
"""
WildGuard AI - Simplified Production Scanner
Designed for GitHub Actions reliability
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

# Simple logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

class SimpleProductionScanner:
    """Simplified production scanner for GitHub Actions"""
    
    def __init__(self):
        self.session = None
        self.results = []
        
        # Check environment variables
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        self.ebay_app_id = os.getenv('EBAY_APP_ID')
        self.ebay_cert_id = os.getenv('EBAY_CERT_ID')
        
        if not all([self.supabase_url, self.supabase_key, self.ebay_app_id, self.ebay_cert_id]):
            logging.error("❌ Missing required environment variables")
            sys.exit(1)
        
        logging.info("✅ Environment variables loaded")

    async def __aenter__(self):
        """Async context manager entry"""
        timeout = aiohttp.ClientTimeout(total=60)
        self.session = aiohttp.ClientSession(timeout=timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    async def run_simple_scan(self) -> Dict[str, Any]:
        """Run a simplified production scan"""
        scan_id = f"SIMPLE-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        logging.info(f"🚀 Starting simplified scan {scan_id}")
        
        try:
            # Test eBay API connection
            ebay_results = await self.test_ebay_simple()
            
            # Test Supabase connection
            supabase_test = await self.test_supabase_simple()
            
            total_results = len(ebay_results)
            
            # Store a few sample results
            stored_count = 0
            if supabase_test and ebay_results:
                stored_count = await self.store_sample_results(ebay_results[:5])
            
            result = {
                'scan_id': scan_id,
                'timestamp': datetime.now().isoformat(),
                'total_results': total_results,
                'stored_results': stored_count,
                'ebay_status': 'SUCCESS' if ebay_results else 'FAILED',
                'supabase_status': 'SUCCESS' if supabase_test else 'FAILED',
                'status': 'SUCCESS' if total_results > 0 else 'PARTIAL'
            }
            
            logging.info(f"🎉 Scan completed: {total_results} results, {stored_count} stored")
            return result
            
        except Exception as e:
            logging.error(f"💥 Scan failed: {e}")
            logging.error(traceback.format_exc())
            return {
                'scan_id': scan_id,
                'status': 'FAILED',
                'error': str(e)
            }

    async def test_ebay_simple(self) -> List[Dict]:
        """Simple eBay API test"""
        results = []
        
        try:
            logging.info("🔍 Testing eBay API...")
            
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
                    
                    logging.info("✅ eBay OAuth successful")
                    
                    # Simple search
                    headers = {
                        "Authorization": f"Bearer {oauth_token}",
                        "Content-Type": "application/json",
                    }
                    
                    params = {"q": "antique", "limit": "20"}
                    
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
                                    "price": item.get("price", {}).get("value", ""),
                                    "url": item.get("itemWebUrl", ""),
                                    "platform": "ebay",
                                    "search_term": "antique"
                                })
                            
                            logging.info(f"✅ eBay: {len(results)} results")
                        else:
                            logging.error(f"❌ eBay search failed: {search_resp.status}")
                else:
                    logging.error(f"❌ eBay auth failed: {resp.status}")
                    
        except Exception as e:
            logging.error(f"❌ eBay test error: {e}")
            
        return results

    async def test_supabase_simple(self) -> bool:
        """Simple Supabase connection test"""
        try:
            logging.info("🔍 Testing Supabase connection...")
            
            headers = {
                "apikey": self.supabase_key,
                "Authorization": f"Bearer {self.supabase_key}",
                "Content-Type": "application/json"
            }
            
            # Test with a simple query
            url = f"{self.supabase_url}/rest/v1/detections?select=id&limit=1"
            
            async with self.session.get(url, headers=headers) as resp:
                if resp.status in [200, 404]:  # 404 is OK if table doesn't exist yet
                    logging.info("✅ Supabase connection successful")
                    return True
                else:
                    logging.error(f"❌ Supabase test failed: {resp.status}")
                    return False
                    
        except Exception as e:
            logging.error(f"❌ Supabase test error: {e}")
            return False

    async def store_sample_results(self, results: List[Dict]) -> int:
        """Store sample results in Supabase"""
        stored_count = 0
        
        try:
            headers = {
                "apikey": self.supabase_key,
                "Authorization": f"Bearer {self.supabase_key}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal"
            }
            
            for i, result in enumerate(results):
                try:
                    evidence_id = f"GITHUB-SIMPLE-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{i+1:03d}"
                    
                    detection = {
                        'evidence_id': evidence_id,
                        'timestamp': datetime.now().isoformat(),
                        'platform': 'ebay',
                        'threat_score': 50,
                        'threat_level': 'GITHUB_TEST',
                        'species_involved': f"Test scan: {result.get('search_term', 'antique')}",
                        'alert_sent': False,
                        'status': 'GITHUB_ACTIONS_TEST',
                        'listing_title': result.get('title', '')[:500],
                        'listing_price': str(result.get('price', '')),
                        'listing_url': result.get('url', ''),
                        'search_term': result.get('search_term', '')
                    }
                    
                    url = f"{self.supabase_url}/rest/v1/detections"
                    
                    async with self.session.post(url, headers=headers, json=detection) as resp:
                        if resp.status in [200, 201]:
                            stored_count += 1
                        else:
                            logging.warning(f"⚠️ Failed to store result {i+1}: {resp.status}")
                            
                except Exception as e:
                    logging.warning(f"⚠️ Error storing result {i+1}: {e}")
                    
        except Exception as e:
            logging.error(f"❌ Storage error: {e}")
            
        logging.info(f"💾 Stored {stored_count}/{len(results)} results")
        return stored_count


async def run_simple_scan():
    """Main function for GitHub Actions"""
    try:
        async with SimpleProductionScanner() as scanner:
            result = await scanner.run_simple_scan()
            
            print("\n" + "="*60)
            print("🎯 GITHUB ACTIONS SCAN SUMMARY")
            print("="*60)
            print(f"Scan ID: {result.get('scan_id', 'Unknown')}")
            print(f"Status: {result.get('status', 'Unknown')}")
            print(f"Results Found: {result.get('total_results', 0)}")
            print(f"Results Stored: {result.get('stored_results', 0)}")
            print(f"eBay Status: {result.get('ebay_status', 'Unknown')}")
            print(f"Supabase Status: {result.get('supabase_status', 'Unknown')}")
            
            if result.get('status') == 'FAILED':
                print(f"Error: {result.get('error', 'Unknown error')}")
                sys.exit(1)
            else:
                print("✅ Scan completed successfully!")
                
            return result
            
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        logging.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    print("🚀 Starting WildGuard Simple Production Scanner")
    print("Designed for GitHub Actions reliability")
    print("-" * 50)
    
    asyncio.run(run_simple_scan())
