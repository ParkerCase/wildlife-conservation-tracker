#!/usr/bin/env python3
"""
WildGuard AI - Intelligent Threat Scoring System
Replaces random scoring with sophisticated threat analysis
"""

import re
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

class ThreatLevel(Enum):
    SAFE = "SAFE"
    LOW = "LOW" 
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ThreatCategory(Enum):
    SAFE = "SAFE"
    WILDLIFE = "WILDLIFE"
    HUMAN_TRAFFICKING = "HUMAN_TRAFFICKING"
    BOTH = "BOTH"

@dataclass
class ThreatAnalysis:
    threat_score: int  # 0-100
    threat_level: ThreatLevel
    threat_category: ThreatCategory
    confidence: float  # 0.0-1.0
    reasoning: str
    wildlife_indicators: List[str]
    human_trafficking_indicators: List[str]
    false_positive_risk: float
    requires_human_review: bool

class IntelligentThreatScorer:
    """
    Sophisticated threat scoring system that analyzes listing content
    to provide accurate, non-random threat assessments
    """
    
    def __init__(self):
        # Wildlife trafficking indicators (weighted by severity)
        self.wildlife_indicators = {
            # CRITICAL (weight: 35-45)
            'critical_species': {
                'ivory': 45, 'elephant ivory': 45, 'rhino horn': 45, 'rhinoceros horn': 45,
                'tiger bone': 40, 'pangolin scale': 40, 'bear bile': 38, 'tiger skin': 42,
                'elephant tusk': 45, 'carved ivory': 42, 'rhino horn powder': 43,
                'pangolin armor': 40, 'tiger claw': 35, 'bear gallbladder': 38
            },
            
            # HIGH RISK (weight: 25-35)
            'high_risk_products': {
                'traditional medicine': 30, 'chinese medicine': 28, 'tiger wine': 35,
                'shark fin': 32, 'turtle shell': 30, 'leopard skin': 33,
                'wildlife carving': 28, 'bone carving': 25, 'horn carving': 30,
                'exotic leather': 27, 'crocodile leather': 25, 'snake skin': 25
            },
            
            # MEDIUM RISK (weight: 15-25)
            'medium_risk_items': {
                'antique carving': 20, 'tribal art': 18, 'ethnic jewelry': 15,
                'vintage specimen': 22, 'museum quality': 20, 'rare specimen': 18,
                'scientific specimen': 16, 'taxidermy': 20, 'mounted head': 22
            },
            
            # SUSPICIOUS TERMS (weight: 10-20)
            'suspicious_terms': {
                'discrete shipping': 15, 'no questions asked': 18, 'cash only': 12,
                'private collection': 10, 'inherited piece': 8, 'grandfather collection': 10,
                'estate piece': 8, 'family heirloom': 6, 'pre-ban': 15, 'pre-1975': 12
            }
        }
        
        # Human trafficking indicators (weighted by risk)
        self.human_trafficking_indicators = {
            # CRITICAL (weight: 35-50)
            'critical_services': {
                'escort service': 45, 'companion service': 40, 'massage therapy': 35,
                'full service': 48, 'outcall service': 42, 'incall service': 42,
                'private meeting': 38, 'discrete encounter': 45, '24/7 available': 35
            },
            
            # HIGH RISK (weight: 25-35)
            'high_risk_employment': {
                'no experience required': 30, 'housing provided': 32, 'visa assistance': 35,
                'cash only': 28, 'flexible hours': 25, 'immediate start': 27,
                'travel opportunities': 30, 'transportation provided': 32
            },
            
            # MEDIUM RISK (weight: 15-25)
            'medium_risk_services': {
                'entertainment work': 22, 'modeling opportunity': 20, 'hostess needed': 25,
                'personal assistant': 15, 'stress relief': 18, 'therapeutic massage': 16,
                'wellness services': 12, 'beauty services': 10
            },
            
            # LOCATION INDICATORS (weight: 10-20)
            'location_indicators': {
                'private apartment': 18, 'hotel outcall': 15, 'spa': 8,
                'massage parlor': 20, 'studio': 10, 'private residence': 15
            }
        }
        
        # FALSE POSITIVE REDUCERS (negative weights)
        self.false_positive_reducers = {
            'legitimate_business': {
                'restaurant': -15, 'hotel': -10, 'hospital': -20, 'clinic': -15,
                'university': -20, 'school': -20, 'library': -15, 'museum': -10,
                'government': -20, 'official': -15, 'licensed': -10, 'registered': -10
            },
            'legitimate_products': {
                'toy': -20, 'replica': -15, 'plastic': -15, 'synthetic': -12,
                'artificial': -15, 'imitation': -12, 'decorative': -8, 'costume': -10,
                'book': -12, 'magazine': -10, 'poster': -8, 'artwork': -5
            },
            'professional_context': {
                'veterinary': -15, 'research': -10, 'educational': -12, 'academic': -10,
                'scientific': -8, 'conservation': -20, 'rehabilitation': -15, 'sanctuary': -15
            }
        }
        
        # Language-specific adjustments
        self.language_risk_multipliers = {
            'zh': 1.2,  # Chinese - higher risk for traditional medicine
            'vi': 1.15, # Vietnamese - trafficking hub
            'th': 1.1,  # Thai - wildlife trafficking
            'en': 1.0,  # English - baseline
            'es': 1.05, # Spanish - some trafficking routes
            'fr': 1.05  # French - West Africa routes
        }

    def analyze_listing(self, listing_data: Dict, search_term: str = "", platform: str = "") -> ThreatAnalysis:
        """
        Perform comprehensive threat analysis on a listing
        """
        title = (listing_data.get('title', '') or '').lower()
        description = (listing_data.get('description', '') or '').lower()
        price = str(listing_data.get('price', '') or '')
        url = listing_data.get('url', '') or ''
        
        # Combine all text for analysis
        full_text = f"{title} {description} {search_term}".lower()
        
        # Calculate component scores
        wildlife_score, wildlife_indicators = self._calculate_wildlife_score(full_text, search_term)
        human_trafficking_score, ht_indicators = self._calculate_human_trafficking_score(full_text, search_term)
        false_positive_reduction = self._calculate_false_positive_reduction(full_text)
        
        # Apply platform-specific adjustments
        platform_multiplier = self._get_platform_multiplier(platform)
        wildlife_score = int(wildlife_score * platform_multiplier)
        human_trafficking_score = int(human_trafficking_score * platform_multiplier)
        
        # Apply false positive reduction
        wildlife_score = max(0, wildlife_score + false_positive_reduction)
        human_trafficking_score = max(0, human_trafficking_score + false_positive_reduction)
        
        # Price analysis
        price_adjustment = self._analyze_price_risk(price, wildlife_score, human_trafficking_score)
        wildlife_score += price_adjustment
        human_trafficking_score += price_adjustment
        
        # URL analysis
        url_adjustment = self._analyze_url_risk(url)
        wildlife_score += url_adjustment
        human_trafficking_score += url_adjustment
        
        # Final score calculation
        final_score = max(wildlife_score, human_trafficking_score)
        final_score = min(100, max(0, final_score))  # Clamp to 0-100
        
        # Determine threat category and level
        threat_category = self._determine_threat_category(wildlife_score, human_trafficking_score)
        threat_level = self._determine_threat_level(final_score)
        
        # Calculate confidence
        confidence = self._calculate_confidence(wildlife_score, human_trafficking_score, len(wildlife_indicators + ht_indicators))
        
        # Determine if human review is needed
        requires_review = self._requires_human_review(final_score, threat_category, confidence)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(wildlife_score, human_trafficking_score, wildlife_indicators, ht_indicators, false_positive_reduction)
        
        # Calculate false positive risk
        fp_risk = self._calculate_false_positive_risk(false_positive_reduction, confidence)
        
        return ThreatAnalysis(
            threat_score=final_score,
            threat_level=threat_level,
            threat_category=threat_category,
            confidence=confidence,
            reasoning=reasoning,
            wildlife_indicators=wildlife_indicators,
            human_trafficking_indicators=ht_indicators,
            false_positive_risk=fp_risk,
            requires_human_review=requires_review
        )

    def _calculate_wildlife_score(self, text: str, search_term: str) -> Tuple[int, List[str]]:
        """Calculate wildlife trafficking threat score"""
        score = 0
        indicators = []
        
        # Check all wildlife indicator categories
        for category, terms in self.wildlife_indicators.items():
            for term, weight in terms.items():
                if term in text:
                    score += weight
                    indicators.append(f"{term} ({category})")
        
        # Boost score if search term is high-risk
        if search_term.lower() in [term for terms in self.wildlife_indicators.values() for term in terms.keys()]:
            score += 15
            indicators.append(f"High-risk search term: {search_term}")
        
        return score, indicators

    def _calculate_human_trafficking_score(self, text: str, search_term: str) -> Tuple[int, List[str]]:
        """Calculate human trafficking threat score"""
        score = 0
        indicators = []
        
        # Check all human trafficking indicator categories
        for category, terms in self.human_trafficking_indicators.items():
            for term, weight in terms.items():
                if term in text:
                    score += weight
                    indicators.append(f"{term} ({category})")
        
        # Check for coded language patterns
        coded_patterns = [
            (r'\b(full|complete|all inclusive)\s+service\b', 25, "coded service language"),
            (r'\b(discrete|discreet|confidential)\b', 15, "discretion emphasis"),
            (r'\b24/?7\b', 12, "24/7 availability"),
            (r'\bcash\s+only\b', 10, "cash only payment")
        ]
        
        for pattern, weight, description in coded_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                score += weight
                indicators.append(description)
        
        return score, indicators

    def _calculate_false_positive_reduction(self, text: str) -> int:
        """Calculate reduction in score due to legitimate indicators"""
        reduction = 0
        
        for category, terms in self.false_positive_reducers.items():
            for term, weight in terms.items():
                if term in text:
                    reduction += weight  # These are negative weights
        
        return reduction

    def _get_platform_multiplier(self, platform: str) -> float:
        """Get platform-specific risk multiplier"""
        platform_multipliers = {
            'craigslist': 1.2,      # Higher risk platform
            'gumtree': 1.15,        # Moderate risk
            'olx': 1.1,             # Some risk
            'avito': 1.1,           # Some risk
            'ebay': 0.95,           # Lower risk (more regulated)
            'aliexpress': 1.0,      # Baseline
            'taobao': 1.1,          # Some risk for traditional medicine
            'marktplaats': 1.0,     # Baseline
            'mercadolibre': 1.05    # Slight risk
        }
        return platform_multipliers.get(platform.lower(), 1.0)

    def _analyze_price_risk(self, price_str: str, wildlife_score: int, ht_score: int) -> int:
        """Analyze price for risk indicators"""
        if not price_str:
            return 0
        
        # Extract numeric value
        price_match = re.search(r'[\d,]+\.?\d*', price_str.replace(',', ''))
        if not price_match:
            return 0
        
        try:
            price = float(price_match.group())
        except:
            return 0
        
        adjustment = 0
        
        # Very high prices for wildlife items are suspicious
        if wildlife_score > 20 and price > 1000:
            adjustment += 8
        elif wildlife_score > 30 and price > 500:
            adjustment += 5
        
        # Very low prices for expensive items might indicate desperation
        if (wildlife_score > 25 or ht_score > 25) and price < 50:
            adjustment += 6
        
        # Round numbers often used in illegal sales
        if price in [100, 200, 500, 1000, 2000, 5000]:
            adjustment += 3
        
        return adjustment

    def _analyze_url_risk(self, url: str) -> int:
        """Analyze URL for risk indicators"""
        if not url:
            return 0
        
        adjustment = 0
        url_lower = url.lower()
        
        # Suspicious URL patterns
        if any(term in url_lower for term in ['private', 'discrete', 'special', 'exclusive']):
            adjustment += 5
        
        # Multiple redirects or obfuscated URLs
        if url_lower.count('http') > 1 or len(url) > 200:
            adjustment += 3
        
        return adjustment

    def _determine_threat_category(self, wildlife_score: int, ht_score: int) -> ThreatCategory:
        """Determine the primary threat category"""
        wildlife_threshold = 25
        ht_threshold = 30
        
        if wildlife_score >= wildlife_threshold and ht_score >= ht_threshold:
            return ThreatCategory.BOTH
        elif wildlife_score >= wildlife_threshold:
            return ThreatCategory.WILDLIFE
        elif ht_score >= ht_threshold:
            return ThreatCategory.HUMAN_TRAFFICKING
        else:
            return ThreatCategory.SAFE

    def _determine_threat_level(self, score: int) -> ThreatLevel:
        """Determine threat level based on score"""
        if score >= 80:
            return ThreatLevel.CRITICAL
        elif score >= 60:
            return ThreatLevel.HIGH
        elif score >= 40:
            return ThreatLevel.MEDIUM
        elif score >= 20:
            return ThreatLevel.LOW
        else:
            return ThreatLevel.SAFE

    def _calculate_confidence(self, wildlife_score: int, ht_score: int, indicator_count: int) -> float:
        """Calculate confidence in the assessment"""
        max_score = max(wildlife_score, ht_score)
        
        # Base confidence on score and number of indicators
        base_confidence = min(0.9, max_score / 100.0)
        indicator_boost = min(0.3, indicator_count * 0.05)
        
        confidence = base_confidence + indicator_boost
        return min(1.0, max(0.1, confidence))

    def _requires_human_review(self, score: int, category: ThreatCategory, confidence: float) -> bool:
        """Determine if human review is required"""
        # Always review critical threats
        if score >= 80:
            return True
        
        # Review high-confidence medium threats
        if score >= 50 and confidence >= 0.7:
            return True
        
        # Review any human trafficking above threshold
        if category in [ThreatCategory.HUMAN_TRAFFICKING, ThreatCategory.BOTH] and score >= 45:
            return True
        
        return False

    def _generate_reasoning(self, wildlife_score: int, ht_score: int, wildlife_indicators: List[str], 
                          ht_indicators: List[str], fp_reduction: int) -> str:
        """Generate human-readable reasoning for the assessment"""
        reasons = []
        
        if wildlife_score > 0:
            reasons.append(f"Wildlife risk score: {wildlife_score} - {len(wildlife_indicators)} indicators")
        
        if ht_score > 0:
            reasons.append(f"Human trafficking risk score: {ht_score} - {len(ht_indicators)} indicators")
        
        if fp_reduction < 0:
            reasons.append(f"False positive reduction: {abs(fp_reduction)} (legitimate indicators)")
        
        if not reasons:
            reasons.append("No significant threat indicators detected")
        
        return "; ".join(reasons)

    def _calculate_false_positive_risk(self, fp_reduction: int, confidence: float) -> float:
        """Calculate the risk of this being a false positive"""
        if fp_reduction < -10:  # Strong legitimate indicators
            return min(0.8, abs(fp_reduction) / 30.0)
        elif confidence < 0.3:  # Low confidence
            return 0.6
        elif confidence > 0.8:  # High confidence
            return 0.1
        else:
            return 0.3


def test_intelligent_scoring():
    """Test the intelligent scoring system"""
    scorer = IntelligentThreatScorer()
    
    # Test cases
    test_cases = [
        {
            'title': 'Vintage ivory carving from grandfather collection',
            'description': 'Antique elephant ivory piece, museum quality',
            'price': '$500',
            'url': 'https://example.com/item123',
            'search_term': 'ivory carving',
            'platform': 'ebay'
        },
        {
            'title': 'Massage therapy services available 24/7',
            'description': 'Full service, outcall available, cash preferred',
            'price': '$200',
            'url': 'https://example.com/private123',
            'search_term': 'massage therapy',
            'platform': 'craigslist'
        },
        {
            'title': 'Holistic treatment center - licensed therapists',
            'description': 'Professional wellness services at our registered clinic',
            'price': '$80',
            'url': 'https://holistichealth.com/services',
            'search_term': 'holistic treatment',
            'platform': 'gumtree'
        },
        {
            'title': 'Plastic toy elephant for kids',
            'description': 'Decorative replica, artificial materials only',
            'price': '$15',
            'url': 'https://toystore.com/elephant',
            'search_term': 'elephant',
            'platform': 'ebay'
        }
    ]
    
    print("🧠 INTELLIGENT THREAT SCORING SYSTEM TEST")
    print("=" * 80)
    
    for i, case in enumerate(test_cases, 1):
        analysis = scorer.analyze_listing(case, case['search_term'], case['platform'])
        
        print(f"\n{i}. TEST CASE: {case['title'][:50]}...")
        print(f"   🎯 Threat Score: {analysis.threat_score}/100")
        print(f"   📊 Threat Level: {analysis.threat_level.value}")
        print(f"   🏷️  Category: {analysis.threat_category.value}")
        print(f"   🔍 Confidence: {analysis.confidence:.2%}")
        print(f"   ⚠️  False Positive Risk: {analysis.false_positive_risk:.2%}")
        print(f"   👁️  Human Review: {'YES' if analysis.requires_human_review else 'NO'}")
        print(f"   💭 Reasoning: {analysis.reasoning}")
        
        if analysis.wildlife_indicators:
            print(f"   🦏 Wildlife Indicators: {', '.join(analysis.wildlife_indicators[:3])}")
        
        if analysis.human_trafficking_indicators:
            print(f"   🚨 HT Indicators: {', '.join(analysis.human_trafficking_indicators[:3])}")
    
    print(f"\n✅ INTELLIGENT SCORING SYSTEM: READY")
    print(f"   • Replaces random scoring with sophisticated analysis")
    print(f"   • Reduces false positives with legitimate business detection")
    print(f"   • Platform-specific risk adjustments")
    print(f"   • Price and URL analysis")
    print(f"   • Confidence scoring and human review triggers")


if __name__ == "__main__":
    test_intelligent_scoring()
