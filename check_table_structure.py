#!/usr/bin/env python3
"""
Check the existing detections table structure to fix schema mismatch
"""

import asyncio
import aiohttp
import os
import json
from dotenv import load_dotenv

load_dotenv()

async def check_table_structure():
    """Check the current detections table structure"""
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Missing Supabase credentials")
        return
    
    async with aiohttp.ClientSession() as session:
        try:
            # Method 1: Get table schema via PostgREST OpenAPI
            print("🔍 Checking table structure...")
            
            headers = {
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json"
            }
            
            # Check existing data structure
            print("\n📊 CHECKING EXISTING DATA STRUCTURE:")
            url = f"{supabase_url}/rest/v1/detections?select=*&limit=1"
            
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data:
                        print("✅ Found existing data!")
                        print(f"Sample record structure:")
                        sample = data[0]
                        for key, value in sample.items():
                            print(f"  {key}: {type(value).__name__} = {str(value)[:50]}...")
                    else:
                        print("⚠️ Table exists but no data found")
                else:
                    print(f"❌ Error checking data: {resp.status}")
                    print(await resp.text())
            
            # Try to get schema info
            print("\n🔍 CHECKING TABLE SCHEMA:")
            schema_url = f"{supabase_url}/rest/v1/"
            
            async with session.options(schema_url, headers=headers) as resp:
                if resp.status == 200:
                    # Get the OpenAPI spec which includes table structure
                    spec_url = f"{supabase_url}/rest/v1/"
                    headers_spec = dict(headers)
                    headers_spec["Accept"] = "application/openapi+json"
                    
                    async with session.get(spec_url, headers=headers_spec) as spec_resp:
                        if spec_resp.status == 200:
                            spec = await spec_resp.json()
                            
                            # Look for detections table in the spec
                            if 'definitions' in spec and 'detections' in spec['definitions']:
                                print("✅ Found table schema in OpenAPI spec!")
                                table_def = spec['definitions']['detections']
                                if 'properties' in table_def:
                                    print("📋 Table columns:")
                                    for col, details in table_def['properties'].items():
                                        col_type = details.get('type', 'unknown')
                                        format_info = details.get('format', '')
                                        nullable = not details.get('nullable', True)
                                        print(f"  {col}: {col_type} {format_info} {'(required)' if nullable else '(optional)'}")
                            else:
                                print("⚠️ Could not find detections table in OpenAPI spec")
                        else:
                            print(f"❌ Could not get OpenAPI spec: {spec_resp.status}")
                else:
                    print(f"❌ Could not connect to schema endpoint: {resp.status}")
            
            # Test insert to see specific error
            print("\n🧪 TESTING INSERT TO SEE EXACT ERROR:")
            test_data = {
                'evidence_id': 'TEST-SCHEMA-CHECK-001',
                'timestamp': '2025-06-20T17:48:42.000Z',
                'platform': 'test',
                'threat_score': 50,
                'threat_level': 'TEST',
                'species_involved': 'Schema test',
                'alert_sent': False,
                'status': 'TESTING',
                'listing_title': 'Test listing',
                'listing_price': '$10',
                'listing_url': 'https://test.com',
                'search_term': 'test'
            }
            
            insert_url = f"{supabase_url}/rest/v1/detections"
            headers_insert = dict(headers)
            headers_insert["Prefer"] = "return=minimal"
            
            async with session.post(insert_url, headers=headers_insert, json=test_data) as resp:
                if resp.status in [200, 201]:
                    print("✅ Test insert successful! Schema matches.")
                else:
                    print(f"❌ Test insert failed with status {resp.status}")
                    error_text = await resp.text()
                    print(f"Error details: {error_text}")
                    
                    # Try to parse error for specific field issues
                    try:
                        error_data = json.loads(error_text)
                        if 'message' in error_data:
                            print(f"Specific error: {error_data['message']}")
                        if 'details' in error_data:
                            print(f"Details: {error_data['details']}")
                    except:
                        pass
            
        except Exception as e:
            print(f"💥 Error checking table structure: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_table_structure())
