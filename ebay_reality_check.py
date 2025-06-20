#!/usr/bin/env python3
"""
Reality Check - Verify actual eBay API usage and limits
"""

import asyncio
import aiohttp
import os
import base64
from dotenv import load_dotenv

load_dotenv('/Users/parkercase/conservation-bot/backend/.env')

class EbayRealityCheck:
    """Check actual eBay API limits and realistic numbers"""
    
    def __init__(self):
        self.app_id = os.getenv("EBAY_APP_ID")
        self.cert_id = os.getenv("EBAY_CERT_ID")
        self.api_calls_made = 0
        self.total_results = 0
        
    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=60)
        self.session = aiohttp.ClientSession(timeout=timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def test_real_limits(self):
        """Test actual eBay API limits and realistic numbers"""
        print("🔍 EBAY API REALITY CHECK")
        print("=" * 60)
        
        try:
            # Get OAuth token
            credentials = f"{self.app_id}:{self.cert_id}"
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
                headers=headers_auth, data=data
            ) as resp:
                if resp.status == 200:
                    token_data = await resp.json()
                    oauth_token = token_data["access_token"]
                    
                    headers = {
                        "Authorization": f"Bearer {oauth_token}",
                        "Content-Type": "application/json",
                    }

                    print("✅ OAuth token obtained")
                    
                    # Test realistic searches
                    test_keywords = ['antique', 'vintage', 'carved']
                    test_categories = ["", "20081"]  # All items, Antiques
                    
                    print(f"\n🧪 Testing {len(test_keywords)} keywords × {len(test_categories)} categories")
                    print(f"📊 Expected API calls: {len(test_keywords) * len(test_categories)}")
                    
                    for keyword in test_keywords:
                        for category in test_categories:
                            result = await self.single_api_call(headers, keyword, category)
                            
                            if result:
                                self.api_calls_made += 1
                                self.total_results += len(result)
                                print(f"   {keyword} + {category or 'all'}: {len(result)} results")
                            else:
                                print(f"   {keyword} + {category or 'all'}: FAILED")
                    
                    print(f"\n📊 REALITY CHECK RESULTS:")
                    print(f"   API calls made: {self.api_calls_made}")
                    print(f"   Total results: {self.total_results}")
                    print(f"   Average results per call: {self.total_results / max(self.api_calls_made, 1):.1f}")
                    
                    # Calculate realistic daily limits
                    print(f"\n🚨 REALISTIC DAILY LIMITS:")
                    
                    # eBay free tier limits (estimated)
                    daily_call_limit = 5000  # Typical free tier limit
                    calls_per_hour = daily_call_limit / 24
                    
                    print(f"   Estimated daily API limit: {daily_call_limit:,}")
                    print(f"   Calls per hour: {calls_per_hour:.0f}")
                    
                    if self.api_calls_made > 0:
                        avg_results = self.total_results / self.api_calls_made
                        realistic_hourly = calls_per_hour * avg_results
                        realistic_daily = realistic_hourly * 24
                        
                        print(f"   Realistic results per hour: {realistic_hourly:,.0f}")
                        print(f"   Realistic results per day: {realistic_daily:,.0f}")
                        
                        if realistic_daily >= 100000:
                            print(f"   🎉 100K+ daily: ACHIEVABLE within API limits")
                        else:
                            print(f"   ⚠️  100K+ daily: Would require {100000 / realistic_daily:.1f}x more API calls")
                    
                else:
                    print("❌ OAuth failed")
                    
        except Exception as e:
            print(f"❌ Error: {e}")

    async def single_api_call(self, headers, keyword, category):
        """Make a single API call and return results"""
        try:
            params = {"q": keyword, "limit": "200"}
            if category:
                params["category_ids"] = category
            
            async with self.session.get(
                "https://api.ebay.com/buy/browse/v1/item_summary/search",
                headers=headers, params=params
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    items = data.get("itemSummaries", [])
                    return items
                else:
                    print(f"      API call failed: {resp.status}")
                    return None
        except Exception as e:
            print(f"      API error: {e}")
            return None

async def run_reality_check():
    """Run the reality check"""
    async with EbayRealityCheck() as checker:
        await checker.test_real_limits()

if __name__ == "__main__":
    asyncio.run(run_reality_check())
