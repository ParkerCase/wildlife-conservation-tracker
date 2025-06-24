#!/usr/bin/env python3
"""
Quick production test of enhanced scanner
"""

import asyncio
import signal
import sys
from enhanced_continuous_scanner import EnhancedContinuousScanner

async def quick_test():
    """Run a quick 60-second test"""
    print("🚀 Quick Enhanced Scanner Test (60 seconds)")
    print("=" * 50)
    
    try:
        async with EnhancedContinuousScanner() as scanner:
            # Run just 2 cycles for testing
            for cycle in range(2):
                print(f"\n🔄 Test Cycle {cycle + 1}/2")
                
                platform = scanner.get_next_platform()
                keywords = scanner.get_next_keyword_batch(4)  # Smaller batch
                
                print(f"🔍 Testing {platform} with keywords: {', '.join(keywords)}")
                
                results = await scanner.scan_platform_with_keywords(platform, keywords)
                stored = await scanner.store_unique_results(platform, results)
                
                print(f"📊 Results: {len(results)} found, {stored} stored")
                
                if cycle < 1:  # Don't wait after last cycle
                    await asyncio.sleep(10)
            
            print(f"\n✅ Quick test completed successfully!")
            print(f"📈 Total cached URLs: {len(scanner.seen_urls):,}")
            
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    asyncio.run(quick_test())
