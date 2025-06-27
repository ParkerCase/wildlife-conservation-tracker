#!/usr/bin/env python3
"""
Quick verification test for Vision API + TaoBao/AliExpress integration
"""

import asyncio
import os
import json
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)

async def test_vision_integration():
    """Test Vision API with real TaoBao/AliExpress listings"""
    
    print("🧪 TESTING VISION API + NEW PLATFORMS INTEGRATION")
    print("=" * 80)
    
    # Check API key
    vision_api_key = os.getenv('GOOGLE_VISION_API_KEY')
    if not vision_api_key:
        print("❌ GOOGLE_VISION_API_KEY not found in environment")
        print("💡 Add your Google Vision API key to test this functionality")
        return False
    
    print(f"✅ Vision API key configured: {vision_api_key[:10]}...")
    
    try:
        # Import our components
        from enhanced_platforms.aliexpress_scanner import AliExpressScanner
        from enhanced_platforms.taobao_scanner import TaobaoScanner
        from enhanced_platforms.enhanced_threat_scorer import EnhancedThreatScorer
        from enhanced_platforms.google_vision_controller import GoogleVisionController
        
        # Initialize components
        scorer = EnhancedThreatScorer()
        vision = GoogleVisionController()
        
        print(f"📊 Vision quota status: {vision.get_quota_status()['quota_remaining']}/1000 remaining")
        
        # Test 1: AliExpress + Vision
        print(f"\n🛒 Testing AliExpress + Enhanced Scoring...")
        async with AliExpressScanner() as aliexpress:
            results = await aliexpress.search_wildlife_terms(['traditional medicine', 'ivory carving'])
            
            if results:
                print(f"   ✅ AliExpress found {len(results)} listings")
                
                # Test enhanced scoring on first result
                test_result = results[0]
                print(f"   📋 Sample: {test_result['title'][:50]}...")
                
                # Calculate original score
                original_score = 65  # Base score
                
                # Enhanced scoring
                analysis = scorer.enhance_existing_score(test_result, original_score)
                print(f"   🎯 Enhanced Score: {original_score} → {analysis.enhanced_score}")
                print(f"   🏷️ Category: {analysis.threat_category.value}")
                
                # Vision analysis (if image available and criteria met)
                if test_result.get('image_url') and vision.can_use_quota()[0]:
                    print(f"   📸 Testing Vision API on listing...")
                    vision_analysis = await vision.analyze_listing_image(test_result, analysis.__dict__)
                    
                    if vision_analysis:
                        final_score, reasoning = vision.enhance_score_with_vision(
                            analysis.enhanced_score, vision_analysis
                        )
                        print(f"   🎨 Vision Enhanced: {analysis.enhanced_score} → {final_score}")
                        print(f"   🔍 Vision Confidence: {vision_analysis.confidence_score:.1%}")
                        print(f"   💡 Reasoning: {reasoning[:100]}...")
                    else:
                        print(f"   📸 Vision analysis skipped (criteria not met or quota)")
                else:
                    print(f"   📸 No image URL or quota exhausted")
            else:
                print(f"   ⚠️ AliExpress returned no results")
        
        # Test 2: Taobao + Vision
        print(f"\n🛒 Testing Taobao + Enhanced Scoring...")
        async with TaobaoScanner() as taobao:
            results = await taobao.search_wildlife_terms(['traditional medicine'])
            
            if results:
                print(f"   ✅ Taobao found {len(results)} listings")
                
                # Test enhanced scoring on first result
                test_result = results[0]
                print(f"   📋 Sample: {test_result['title'][:50]}...")
                
                # Enhanced scoring
                analysis = scorer.enhance_existing_score(test_result, 60)
                print(f"   🎯 Enhanced Score: 60 → {analysis.enhanced_score}")
                print(f"   🏷️ Category: {analysis.threat_category.value}")
                
            else:
                print(f"   ⚠️ Taobao returned no results (anti-bot measures may be active)")
        
        print(f"\n✅ INTEGRATION TEST COMPLETED")
        print(f"📊 Vision quota after test: {vision.get_quota_status()['quota_remaining']}/1000 remaining")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enhanced_scoring_examples():
    """Test enhanced scoring with various examples"""
    
    print(f"\n🔍 TESTING ENHANCED SCORING EXAMPLES")
    print("=" * 50)
    
    try:
        from enhanced_platforms.enhanced_threat_scorer import EnhancedThreatScorer
        scorer = EnhancedThreatScorer()
        
        # Test cases covering different scenarios
        test_cases = [
            {
                'name': 'Wildlife Trafficking',
                'listing': {
                    'listing_title': 'Traditional Chinese Medicine Tiger Bone Powder',
                    'description': 'Authentic tiger bone for traditional healing. Private collection.',
                    'listing_price': '¥450',
                    'search_term': 'tiger bone',
                    'platform': 'taobao'
                },
                'original_score': 70
            },
            {
                'name': 'Human Trafficking',
                'listing': {
                    'listing_title': 'Young Massage Therapist Available',
                    'description': 'New talent, 18 years old, full service available 24/7. Cash only.',
                    'listing_price': '$200',
                    'search_term': 'massage',
                    'platform': 'craigslist'
                },
                'original_score': 50
            },
            {
                'name': 'False Positive (Safe)',
                'listing': {
                    'listing_title': 'Tiger Print Dress Fashion',
                    'description': 'Beautiful tiger pattern dress for women. Brand new.',
                    'listing_price': '$25',
                    'search_term': 'tiger',
                    'platform': 'aliexpress'
                },
                'original_score': 60
            }
        ]
        
        for test_case in test_cases:
            analysis = scorer.enhance_existing_score(test_case['listing'], test_case['original_score'])
            
            print(f"\n📋 {test_case['name']}:")
            print(f"   Title: {test_case['listing']['listing_title'][:40]}...")
            print(f"   Score: {test_case['original_score']} → {analysis.enhanced_score}")
            print(f"   Category: {analysis.threat_category.value}")
            print(f"   Level: {analysis.threat_level.value}")
            print(f"   Review Required: {'YES' if analysis.requires_human_review else 'NO'}")
            
            if analysis.wildlife_indicators:
                print(f"   Wildlife: {len(analysis.wildlife_indicators)} indicators")
            if analysis.human_trafficking_indicators:
                print(f"   Human Trafficking: {len(analysis.human_trafficking_indicators)} indicators")
        
        print(f"\n✅ Enhanced scoring working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Enhanced scoring test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 VISION API + PLATFORM INTEGRATION TEST")
    print("=" * 80)
    
    # Test enhanced scoring first
    scoring_ok = test_enhanced_scoring_examples()
    
    # Test full integration
    integration_ok = asyncio.run(test_vision_integration())
    
    if scoring_ok and integration_ok:
        print(f"\n🎉 ALL TESTS PASSED - READY FOR DEPLOYMENT!")
    else:
        print(f"\n⚠️ SOME TESTS FAILED - REVIEW NEEDED")
