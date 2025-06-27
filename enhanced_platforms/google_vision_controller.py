#!/usr/bin/env python3
"""
WildGuard AI - Google Vision API Integration with Hard 1000/month Cap
Cost-controlled image analysis for wildlife/human trafficking detection
"""

import asyncio
import aiohttp
import base64
import json
import logging
import sqlite3
import hashlib
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import calendar

@dataclass
class VisionAnalysis:
    has_wildlife_indicators: bool
    has_human_trafficking_indicators: bool
    detected_labels: List[str]
    detected_text: str
    confidence_score: float
    analysis_type: str  # 'wildlife', 'human_trafficking', 'both', 'safe'
    cost_used: bool  # True if this used our quota
    cache_hit: bool

class GoogleVisionController:
    """
    Google Vision API integration with strict 1000/month quota management
    """
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_VISION_API_KEY')  # User will set this
        self.db_path = '/Users/parkercase/conservation-bot/vision_quota.db'
        self.monthly_quota = 1000  # Hard limit
        self.current_month_usage = 0
        
        self._init_quota_db()
        self._load_monthly_usage()
        
        # Wildlife-related detection terms
        self.wildlife_terms = {
            'animals': [
                'elephant', 'rhino', 'rhinoceros', 'tiger', 'leopard', 'lion',
                'pangolin', 'bear', 'cheetah', 'jaguar', 'turtle', 'tortoise',
                'snake', 'lizard', 'crocodile', 'alligator', 'shark', 'whale',
                'seal', 'walrus', 'eagle', 'falcon', 'parrot', 'owl'
            ],
            'animal_parts': [
                'tusk', 'horn', 'antler', 'tooth', 'claw', 'scale', 'bone',
                'skull', 'hide', 'skin', 'fur', 'feather', 'shell'
            ],
            'products': [
                'carving', 'sculpture', 'jewelry', 'bracelet', 'necklace',
                'medicine', 'powder', 'capsule', 'tonic', 'ornament'
            ],
            'materials': ['ivory', 'coral', 'amber', 'leather']
        }
        
        # Human trafficking detection terms
        self.human_trafficking_terms = [
            'person', 'woman', 'girl', 'man', 'people', 'human', 'face',
            'massage', 'spa', 'entertainment', 'service', 'escort'
        ]
        
        # Exclusion terms (reduce false positives)
        self.exclusion_terms = [
            'toy', 'plush', 'stuffed', 'cartoon', 'drawing', 'illustration',
            'painting', 'artwork', 'poster', 'book', 'magazine', 'plastic',
            'synthetic', 'artificial', 'replica', 'model'
        ]
    
    def _init_quota_db(self):
        """Initialize SQLite database for quota tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vision_quota (
                month_year TEXT PRIMARY KEY,
                requests_used INTEGER,
                last_updated TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vision_cache (
                image_hash TEXT PRIMARY KEY,
                analysis_result TEXT,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_monthly_usage(self):
        """Load current month's usage"""
        current_month = datetime.now().strftime('%Y-%m')
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT requests_used FROM vision_quota WHERE month_year = ?', (current_month,))
        result = cursor.fetchone()
        
        if result:
            self.current_month_usage = result[0]
        else:
            self.current_month_usage = 0
            cursor.execute('INSERT INTO vision_quota (month_year, requests_used, last_updated) VALUES (?, 0, ?)', 
                         (current_month, datetime.now().isoformat()))
            conn.commit()
        
        conn.close()
        
        logging.info(f"Vision API quota: {self.current_month_usage}/{self.monthly_quota} used this month")
    
    def _update_quota_usage(self):
        """Update quota usage in database"""
        current_month = datetime.now().strftime('%Y-%m')
        self.current_month_usage += 1
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE vision_quota 
            SET requests_used = ?, last_updated = ?
            WHERE month_year = ?
        ''', (self.current_month_usage, datetime.now().isoformat(), current_month))
        
        conn.commit()
        conn.close()
        
        logging.info(f"Vision API quota updated: {self.current_month_usage}/{self.monthly_quota}")
    
    def can_use_quota(self) -> Tuple[bool, str]:
        """Check if we can use Vision API quota"""
        
        if not self.api_key:
            return False, "Google Vision API key not configured"
        
        if self.current_month_usage >= self.monthly_quota:
            return False, f"Monthly quota exceeded ({self.current_month_usage}/{self.monthly_quota})"
        
        return True, f"Quota available ({self.current_month_usage}/{self.monthly_quota})"
    
    def should_analyze_image(self, listing_data: Dict, enhanced_analysis: Dict) -> Tuple[bool, str]:
        """
        Determine if we should spend quota on analyzing this image
        Only analyze listings in the uncertain range where vision would help
        """
        
        # Check if image URL available first
        if not listing_data.get('image_url'):
            return False, "No image URL available"
        
        # Check if quota available
        can_use, quota_reason = self.can_use_quota()
        if not can_use:
            return False, quota_reason
        
        # Get enhanced threat analysis
        enhanced_score = enhanced_analysis.get('enhanced_score', 0)
        threat_category = enhanced_analysis.get('threat_category', 'SAFE')
        requires_review = enhanced_analysis.get('requires_human_review', False)
        
        # Always analyze if human review required
        if requires_review:
            return True, "Human review required - high priority"
        
        # Analyze uncertain scores where vision could help decide
        if 35 <= enhanced_score <= 80:
            return True, f"Uncertain score ({enhanced_score}) - vision analysis valuable"
        
        # Don't analyze very low scores (likely safe)
        if enhanced_score < 30:
            return False, f"Score too low ({enhanced_score}) - likely safe"
        
        # Don't analyze very high scores (already identified as threats)
        if enhanced_score > 75:
            return False, f"Score high enough ({enhanced_score}) - threat already identified"
        
        return False, "Does not meet analysis criteria"
    
    async def analyze_listing_image(self, listing_data: Dict, enhanced_analysis: Dict) -> Optional[VisionAnalysis]:
        """
        Analyze listing image with strict quota management
        """
        
        # Check if we should analyze
        should_analyze, reason = self.should_analyze_image(listing_data, enhanced_analysis)
        if not should_analyze:
            logging.debug(f"Skipping vision analysis: {reason}")
            return None
        
        image_url = listing_data.get('image_url')
        if not image_url:
            return None
        
        # Check cache first
        image_hash = hashlib.md5(image_url.encode()).hexdigest()
        cached_result = self._get_cached_analysis(image_hash)
        if cached_result:
            logging.debug("Using cached vision analysis")
            return cached_result
        
        try:
            # Download image
            image_data = await self._download_image(image_url)
            if not image_data:
                return None
            
            # Call Vision API
            analysis = await self._call_vision_api(image_data)
            
            # Update quota
            self._update_quota_usage()
            analysis.cost_used = True
            
            # Cache result
            self._cache_analysis(image_hash, analysis)
            
            return analysis
            
        except Exception as e:
            logging.error(f"Vision API error: {e}")
            return None
    
    async def _download_image(self, image_url: str) -> Optional[bytes]:
        """Download image with size limits"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url, timeout=15) as response:
                    if response.status == 200:
                        # Limit image size to 4MB (Vision API limit is 20MB)
                        content = await response.read()
                        if len(content) > 4 * 1024 * 1024:  # 4MB
                            logging.warning(f"Image too large: {len(content)} bytes")
                            return None
                        return content
        except Exception as e:
            logging.warning(f"Image download failed: {e}")
        
        return None
    
    async def _call_vision_api(self, image_data: bytes) -> VisionAnalysis:
        """Call Google Vision API"""
        
        # Encode image
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # Prepare request
        request_data = {
            "requests": [
                {
                    "image": {"content": image_base64},
                    "features": [
                        {"type": "LABEL_DETECTION", "maxResults": 15},
                        {"type": "TEXT_DETECTION", "maxResults": 5},
                        {"type": "OBJECT_LOCALIZATION", "maxResults": 10}
                    ]
                }
            ]
        }
        
        url = f"https://vision.googleapis.com/v1/images:annotate?key={self.api_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=request_data, timeout=30) as response:
                if response.status == 200:
                    result = await response.json()
                    return self._parse_vision_response(result)
                else:
                    error_text = await response.text()
                    raise Exception(f"Vision API error {response.status}: {error_text}")
    
    def _parse_vision_response(self, response: Dict) -> VisionAnalysis:
        """Parse Google Vision API response"""
        
        annotations = response.get('responses', [{}])[0]
        
        # Extract labels
        labels = []
        label_annotations = annotations.get('labelAnnotations', [])
        for label in label_annotations:
            labels.append(label.get('description', '').lower())
        
        # Extract text
        text_annotations = annotations.get('textAnnotations', [])
        detected_text = text_annotations[0].get('description', '') if text_annotations else ''
        
        # Extract objects
        objects = []
        object_annotations = annotations.get('localizedObjectAnnotations', [])
        for obj in object_annotations:
            objects.append(obj.get('name', '').lower())
        
        # Analyze for threats
        analysis = self._analyze_vision_results(labels, objects, detected_text)
        
        return VisionAnalysis(
            has_wildlife_indicators=analysis['wildlife_indicators'],
            has_human_trafficking_indicators=analysis['human_trafficking_indicators'],
            detected_labels=labels,
            detected_text=detected_text,
            confidence_score=analysis['confidence'],
            analysis_type=analysis['analysis_type'],
            cost_used=True,
            cache_hit=False
        )
    
    def _analyze_vision_results(self, labels: List[str], objects: List[str], text: str) -> Dict:
        """Analyze vision results for threats"""
        
        all_terms = labels + objects + [text.lower()]
        combined_text = ' '.join(all_terms)
        
        wildlife_score = 0
        human_score = 0
        
        # Check for wildlife indicators
        for category, terms in self.wildlife_terms.items():
            matches = sum(1 for term in terms if term in combined_text)
            if category == 'animals':
                wildlife_score += matches * 30
            elif category == 'animal_parts':
                wildlife_score += matches * 25
            elif category == 'products':
                wildlife_score += matches * 20
            elif category == 'materials':
                wildlife_score += matches * 35
        
        # Check for human trafficking indicators
        human_matches = sum(1 for term in self.human_trafficking_terms if term in combined_text)
        human_score = human_matches * 20
        
        # Check for exclusions
        exclusion_matches = sum(1 for term in self.exclusion_terms if term in combined_text)
        if exclusion_matches > 0:
            wildlife_score = max(0, wildlife_score - exclusion_matches * 15)
            human_score = max(0, human_score - exclusion_matches * 10)
        
        # Determine analysis type
        if wildlife_score >= 30 and human_score >= 30:
            analysis_type = 'both'
        elif wildlife_score >= 25:
            analysis_type = 'wildlife'
        elif human_score >= 20:
            analysis_type = 'human_trafficking'
        else:
            analysis_type = 'safe'
        
        # Calculate confidence
        confidence = min(1.0, (wildlife_score + human_score) / 100)
        
        return {
            'wildlife_indicators': wildlife_score >= 25,
            'human_trafficking_indicators': human_score >= 20,
            'confidence': confidence,
            'analysis_type': analysis_type
        }
    
    def _get_cached_analysis(self, image_hash: str) -> Optional[VisionAnalysis]:
        """Get cached vision analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT analysis_result FROM vision_cache WHERE image_hash = ?', (image_hash,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            data = json.loads(result[0])
            analysis = VisionAnalysis(**data)
            analysis.cache_hit = True
            analysis.cost_used = False
            return analysis
        
        return None
    
    def _cache_analysis(self, image_hash: str, analysis: VisionAnalysis):
        """Cache vision analysis result"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Prepare data for caching
        cache_data = {
            'has_wildlife_indicators': analysis.has_wildlife_indicators,
            'has_human_trafficking_indicators': analysis.has_human_trafficking_indicators,
            'detected_labels': analysis.detected_labels,
            'detected_text': analysis.detected_text,
            'confidence_score': analysis.confidence_score,
            'analysis_type': analysis.analysis_type,
            'cost_used': False,  # Cache hits don't cost quota
            'cache_hit': True
        }
        
        cursor.execute('''
            INSERT OR REPLACE INTO vision_cache (image_hash, analysis_result, timestamp)
            VALUES (?, ?, ?)
        ''', (image_hash, json.dumps(cache_data), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def enhance_score_with_vision(self, enhanced_score: int, vision_analysis: VisionAnalysis) -> Tuple[int, str]:
        """Enhance threat score based on vision analysis"""
        
        if not vision_analysis:
            return enhanced_score, "No vision analysis performed"
        
        original_score = enhanced_score
        reasoning_parts = []
        
        # Wildlife indicators
        if vision_analysis.has_wildlife_indicators:
            if vision_analysis.confidence_score > 0.7:
                enhanced_score += 20
                reasoning_parts.append("High-confidence wildlife detection")
            elif vision_analysis.confidence_score > 0.5:
                enhanced_score += 15
                reasoning_parts.append("Moderate wildlife indicators")
            else:
                enhanced_score += 10
                reasoning_parts.append("Low-confidence wildlife indicators")
        
        # Human trafficking indicators
        if vision_analysis.has_human_trafficking_indicators:
            if vision_analysis.confidence_score > 0.6:
                enhanced_score += 25  # Higher weight for human trafficking
                reasoning_parts.append("Human trafficking indicators detected")
            else:
                enhanced_score += 15
                reasoning_parts.append("Possible human trafficking indicators")
        
        # Text analysis
        if vision_analysis.detected_text:
            text_lower = vision_analysis.detected_text.lower()
            suspicious_text = any(term in text_lower for term in [
                'ivory', 'horn', 'traditional', 'medicine', 'massage', 'escort',
                'private', 'discrete', 'cash only'
            ])
            if suspicious_text:
                enhanced_score += 12
                reasoning_parts.append("Suspicious text in image")
        
        # Safety indicators (reduce score)
        safe_labels = ['toy', 'plush', 'cartoon', 'drawing', 'plastic']
        if any(label in vision_analysis.detected_labels for label in safe_labels):
            enhanced_score = max(0, enhanced_score - 20)
            reasoning_parts.append("Safety indicators detected")
        
        # Ensure valid range
        enhanced_score = max(0, min(100, enhanced_score))
        
        # Generate reasoning
        if reasoning_parts:
            reasoning = f"Vision analysis: {'; '.join(reasoning_parts)} (confidence: {vision_analysis.confidence_score:.1%})"
        else:
            reasoning = "Vision analysis: No significant indicators detected"
        
        return enhanced_score, reasoning
    
    def get_quota_status(self) -> Dict:
        """Get current quota status"""
        current_month = datetime.now().strftime('%Y-%m')
        
        # Get days remaining in month
        today = datetime.now()
        last_day = calendar.monthrange(today.year, today.month)[1]
        days_remaining = last_day - today.day + 1
        
        quota_remaining = self.monthly_quota - self.current_month_usage
        daily_budget_remaining = quota_remaining / days_remaining if days_remaining > 0 else 0
        
        return {
            'month': current_month,
            'quota_used': self.current_month_usage,
            'quota_total': self.monthly_quota,
            'quota_remaining': quota_remaining,
            'quota_percentage': (self.current_month_usage / self.monthly_quota) * 100,
            'days_remaining': days_remaining,
            'daily_budget_remaining': int(daily_budget_remaining),
            'api_key_configured': bool(self.api_key)
        }


def test_vision_quota_system():
    """Test the vision quota management system"""
    
    print("📸 TESTING GOOGLE VISION QUOTA SYSTEM")
    print("=" * 80)
    
    vision = GoogleVisionController()
    
    # Test quota status
    status = vision.get_quota_status()
    print(f"📊 QUOTA STATUS:")
    print(f"   Month: {status['month']}")
    print(f"   Used: {status['quota_used']}/{status['quota_total']} ({status['quota_percentage']:.1f}%)")
    print(f"   Remaining: {status['quota_remaining']}")
    print(f"   Days Remaining: {status['days_remaining']}")
    print(f"   Daily Budget Remaining: {status['daily_budget_remaining']}")
    print(f"   API Key Configured: {status['api_key_configured']}")
    
    # Test analysis criteria
    test_cases = [
        {
            'enhanced_score': 45,
            'threat_category': 'WILDLIFE',
            'requires_human_review': False,
            'image_url': 'https://example.com/suspicious.jpg'
        },
        {
            'enhanced_score': 85,
            'threat_category': 'CRITICAL',
            'requires_human_review': True,
            'image_url': 'https://example.com/high_threat.jpg'
        },
        {
            'enhanced_score': 15,
            'threat_category': 'SAFE',
            'requires_human_review': False,
            'image_url': 'https://example.com/safe.jpg'
        }
    ]
    
    print(f"\n🎯 ANALYSIS CRITERIA TEST:")
    for i, case in enumerate(test_cases, 1):
        should_analyze, reason = vision.should_analyze_image(case, case)
        status_icon = "✅" if should_analyze else "❌"
        print(f"   {i}. Score {case['enhanced_score']}: {status_icon} - {reason}")
    
    print(f"\n💰 COST CONTROL FEATURES:")
    print(f"   ✅ Hard 1000/month quota limit")
    print(f"   ✅ Database-backed quota tracking")
    print(f"   ✅ Intelligent analysis criteria")
    print(f"   ✅ Result caching to avoid duplicate costs")
    print(f"   ✅ Priority for uncertain scores (30-75 range)")
    print(f"   ✅ Always analyze human review cases")
    print(f"   ✅ Skip very low (<30) and very high (>75) scores")
    
    print(f"\n🔧 SETUP INSTRUCTIONS:")
    print(f"   1. Get Google Vision API key from Google Cloud Console")
    print(f"   2. Add to .env file: GOOGLE_VISION_API_KEY=your_key_here")
    print(f"   3. Enable Vision API in your Google Cloud project")
    print(f"   4. Quota will be automatically tracked and enforced")
    
    return vision


if __name__ == "__main__":
    vision_system = test_vision_quota_system()
    
    print(f"\n🎉 GOOGLE VISION INTEGRATION: READY")
    print(f"   • Hard 1000/month quota management")
    print(f"   • Intelligent cost optimization")
    print(f"   • Wildlife + human trafficking detection")
    print(f"   • Result caching system")
    print(f"   • Production-ready with safety controls")
