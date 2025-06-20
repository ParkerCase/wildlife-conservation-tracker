#!/usr/bin/env python3
"""
eBay OAuth Diagnostic and Fix
Debug and fix eBay authentication issues
"""

import os
import base64
import aiohttp
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv('/Users/parkercase/conservation-bot/backend/.env')

class EbayOAuthFixer:
    def __init__(self):
        self.app_id = os.getenv("EBAY_APP_ID")
        self.cert_id = os.getenv("EBAY_CERT_ID") 
        self.dev_id = os.getenv("EBAY_DEV_ID")
        self.ru_name = os.getenv("EBAY_RU_NAME")
        
        # Different endpoints
        self.sandbox_token_url = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
        self.prod_token_url = "https://api.ebay.com/identity/v1/oauth2/token"
        
        self.sandbox_api_url = "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search"
        self.prod_api_url = "https://api.ebay.com/buy/browse/v1/item_summary/search"

    def check_credentials(self):
        """Check if all required credentials are present"""
        print("🔍 CHECKING EBAY CREDENTIALS")
        print("-" * 40)
        
        creds = {
            'EBAY_APP_ID': self.app_id,
            'EBAY_CERT_ID': self.cert_id,
            'EBAY_DEV_ID': self.dev_id,
            'EBAY_RU_NAME': self.ru_name
        }
        
        missing = []
        for name, value in creds.items():
            if value:
                print(f"✅ {name}: {value[:10]}...{value[-4:] if len(value) > 14 else value}")
            else:
                print(f"❌ {name}: MISSING")
                missing.append(name)
        
        if missing:
            print(f"\n❌ Missing credentials: {', '.join(missing)}")
            print("📋 To fix, add these to your .env file:")
            for cred in missing:
                print(f"   {cred}=your_key_here")
            return False
        
        print("✅ All credentials present")
        return True

    async def test_oauth_sandbox(self):
        """Test OAuth in sandbox environment"""
        print("\n🧪 TESTING SANDBOX OAUTH")
        print("-" * 30)
        
        credentials = f"{self.app_id}:{self.cert_id}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        
        data = {
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope",
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.sandbox_token_url, headers=headers, data=data
                ) as resp:
                    response_text = await resp.text()
                    print(f"📊 Response status: {resp.status}")
                    print(f"📋 Response: {response_text}")
                    
                    if resp.status == 200:
                        token_data = await resp.json()
                        if "access_token" in token_data:
                            print("✅ Sandbox OAuth successful!")
                            return token_data["access_token"]
                        else:
                            print("❌ No access token in response")
                            return None
                    else:
                        print(f"❌ Sandbox OAuth failed: {response_text}")
                        return None
                        
        except Exception as e:
            print(f"❌ Sandbox OAuth error: {e}")
            return None

    async def test_oauth_production(self):
        """Test OAuth in production environment"""
        print("\n🚀 TESTING PRODUCTION OAUTH")
        print("-" * 35)
        
        credentials = f"{self.app_id}:{self.cert_id}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        
        data = {
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope",
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.prod_token_url, headers=headers, data=data
                ) as resp:
                    response_text = await resp.text()
                    print(f"📊 Response status: {resp.status}")
                    print(f"📋 Response: {response_text}")
                    
                    if resp.status == 200:
                        token_data = await resp.json()
                        if "access_token" in token_data:
                            print("✅ Production OAuth successful!")
                            return token_data["access_token"]
                        else:
                            print("❌ No access token in response")
                            return None
                    else:
                        print(f"❌ Production OAuth failed: {response_text}")
                        return None
                        
        except Exception as e:
            print(f"❌ Production OAuth error: {e}")
            return None

    async def test_api_call(self, token, use_sandbox=False):
        """Test actual API call with token"""
        api_url = self.sandbox_api_url if use_sandbox else self.prod_api_url
        env_name = "SANDBOX" if use_sandbox else "PRODUCTION"
        
        print(f"\n🔍 TESTING {env_name} API CALL")
        print("-" * 40)
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        
        params = {
            "q": "test",
            "limit": "3"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    api_url, headers=headers, params=params
                ) as resp:
                    response_text = await resp.text()
                    print(f"📊 API Response status: {resp.status}")
                    
                    if resp.status == 200:
                        data = await resp.json()
                        items = data.get("itemSummaries", [])
                        print(f"✅ API call successful! Found {len(items)} items")
                        
                        if items:
                            for i, item in enumerate(items[:2], 1):
                                title = item.get("title", "No title")[:40]
                                price = item.get("price", {}).get("value", "No price")
                                print(f"   {i}. {title}... - ${price}")
                        
                        return True
                    else:
                        print(f"❌ API call failed: {response_text}")
                        return False
                        
        except Exception as e:
            print(f"❌ API call error: {e}")
            return False

    async def comprehensive_ebay_test(self):
        """Run comprehensive eBay diagnostic"""
        print("🧪 COMPREHENSIVE EBAY DIAGNOSTIC")
        print("=" * 50)
        
        # Check credentials
        if not self.check_credentials():
            return False
        
        # Test sandbox first
        sandbox_token = await self.test_oauth_sandbox()
        if sandbox_token:
            sandbox_api_works = await self.test_api_call(sandbox_token, use_sandbox=True)
        else:
            sandbox_api_works = False
        
        # Test production
        prod_token = await self.test_oauth_production()
        if prod_token:
            prod_api_works = await self.test_api_call(prod_token, use_sandbox=False)
        else:
            prod_api_works = False
        
        # Summary
        print(f"\n🎯 EBAY DIAGNOSTIC SUMMARY")
        print("-" * 30)
        print(f"✅ Credentials: Present")
        print(f"{'✅' if sandbox_token else '❌'} Sandbox OAuth: {'Working' if sandbox_token else 'Failed'}")
        print(f"{'✅' if sandbox_api_works else '❌'} Sandbox API: {'Working' if sandbox_api_works else 'Failed'}")
        print(f"{'✅' if prod_token else '❌'} Production OAuth: {'Working' if prod_token else 'Failed'}")
        print(f"{'✅' if prod_api_works else '❌'} Production API: {'Working' if prod_api_works else 'Failed'}")
        
        if prod_api_works:
            print("\n🎉 eBay is FULLY OPERATIONAL!")
            return True
        elif sandbox_api_works:
            print("\n⚠️ eBay working in sandbox only")
            print("💡 Check if production keys are approved")
            return True
        else:
            print("\n❌ eBay needs credential fixes")
            return False

async def main():
    fixer = EbayOAuthFixer()
    success = await fixer.comprehensive_ebay_test()
    
    if not success:
        print("\n🔧 EBAY FIX RECOMMENDATIONS:")
        print("1. Verify credentials in developer.ebay.com")
        print("2. Check if production keys are approved")
        print("3. Ensure OAuth scope is correct")
        print("4. Check for API usage limits")

if __name__ == "__main__":
    asyncio.run(main())
