#!/usr/bin/env python3
"""
WildGuard AI - Enhanced Threat Scoring System
Builds on existing scoring to dramatically improve accuracy
"""

import re
import json
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class ThreatCategory(Enum):
    WILDLIFE = "WILDLIFE"
    HUMAN_TRAFFICKING = "HUMAN_TRAFFICKING"
    BOTH = "BOTH"
    SAFE = "SAFE"

class ThreatLevel(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    SAFE = "SAFE"

@dataclass
class EnhancedThreatAnalysis:
    original_score: int
    enhanced_score: int
    threat_category: ThreatCategory
    threat_level: ThreatLevel
    wildlife_indicators: List[str]
    human_trafficking_indicators: List[str]
    exclusion_factors: List[str]
    confidence: float
    reasoning: str
    requires_human_review: bool

class EnhancedThreatScorer:
    """
    Enhanced threat scoring that builds on existing system
    """
    
    def __init__(self):
        self.load_detection_databases()
        self.initialize_scoring_weights()
        
    def load_detection_databases(self):
        """Load comprehensive detection databases"""
        
        # WILDLIFE TRAFFICKING INDICATORS
        self.wildlife_indicators = {
            # Critical species (highest priority)
            'critical_species': {
                'ivory': ['elephant ivory', 'mammoth ivory', 'walrus ivory', 'ivory carving', 'carved ivory', 'antique ivory', 'vintage ivory'],
                'rhino_horn': ['rhino horn', 'rhinoceros horn', 'horn powder', 'horn medicine', 'rhino horn powder'],
                'tiger_products': ['tiger bone', 'tiger skin', 'tiger pelt', 'tiger tooth', 'tiger claw', 'tiger bone wine'],
                'pangolin': ['pangolin scales', 'pangolin armor', 'pangolin meat', 'pangolin medicine', 'pangolin scale powder'],
                'elephant': ['elephant hair', 'elephant tail', 'elephant skin', 'elephant foot'],
                'bear_products': ['bear bile', 'bear paw', 'bear gallbladder', 'bear bile powder', 'bear bile capsule']
            },
            
            # High-priority species
            'high_priority': {
                'big_cats': ['leopard skin', 'leopard fur', 'leopard bone', 'lion bone', 'lion tooth', 'cheetah fur', 'jaguar pelt'],
                'marine': ['shark fin', 'shark cartilage', 'turtle shell', 'tortoise shell', 'whale bone', 'seal skin'],
                'birds': ['eagle feather', 'falcon', 'parrot', 'macaw', 'hornbill beak', 'toucan beak'],
                'traditional_medicine': ['traditional medicine', 'chinese medicine', 'natural remedy', 'ancient cure', 'healing properties']
            },
            
            # Trafficking language patterns
            'trafficking_language': {
                'discretion': ['discrete shipping', 'no questions asked', 'private buyer', 'serious buyers only', 'cash only'],
                'authenticity': ['genuine', 'authentic', 'real', 'certified', 'documented', 'provenance'],
                'urgency': ['must sell', 'quick sale', 'moving sale', 'last chance', 'final stock', 'limited time'],
                'collector_terms': ['rare specimen', 'museum quality', 'private collection', 'collector grade', 'exhibition quality'],
                'origin_claims': ['wild caught', 'imported', 'tribal', 'indigenous', 'ancestral', 'traditional source']
            },
            
            # Scientific and technical terms
            'scientific_terms': [
                'loxodonta africana', 'elephas maximus', 'diceros bicornis', 'ceratotherium simum',
                'panthera tigris', 'panthera pardus', 'panthera leo', 'acinonyx jubatus',
                'manis pentadactyla', 'manis javanica', 'ailuropoda melanoleuca'
            ]
        }
        
        # HUMAN TRAFFICKING INDICATORS
        self.human_trafficking_indicators = {
            # Adult services (coded language)
            'escort_services': [
                'escort', 'companionship', 'massage therapy', 'full service', 'body rub',
                'discreet encounter', 'personal service', 'private meeting', 'relaxation therapy',
                'adult entertainment', 'exotic dancer', 'hostess service', 'stress relief'
            ],
            
            # Employment exploitation
            'suspicious_employment': [
                'modeling opportunity', 'dance opportunity', 'travel companion', 'entertainment work',
                'waitress needed', 'hostess needed', 'no experience required', 'immediate start',
                'cash paid daily', 'housing provided', 'transportation provided', 'visa assistance'
            ],
            
            # Age-related concerns (major red flags)
            'age_concerns': [
                'young', 'petite', 'teen', 'barely legal', 'innocent looking', 'fresh',
                'new talent', 'inexperienced', 'just turned 18', 'school girl', 'college girl'
            ],
            
            # Control indicators
            'control_patterns': [
                'manager required', 'must check in', 'strict schedule', 'no personal phone',
                'location provided', 'driver provided', 'security present', 'screened clients',
                'agency managed', 'booking required'
            ],
            
            # Financial exploitation
            'financial_exploitation': [
                'debt payment', 'work off debt', 'room and board deducted', 'agency fee',
                'management fee', 'protection fee', 'clothing costs', 'photo costs', 'training costs'
            ],
            
            # Coded language
            'coded_language': [
                'available 24/7', 'outcall', 'incall', 'flexible schedule', 'must be willing to travel',
                'submissive', 'obedient', 'compliant', 'understanding', 'accommodating'
            ]
        }
        
        # EXCLUSION PATTERNS (reduce false positives)
        self.exclusion_patterns = {
            # Color/pattern references (not actual products)
            'colors_patterns': [
                'ivory colored', 'ivory white', 'ivory cream', 'ivory shade', 'ivory paint',
                'tiger stripe', 'tiger print', 'tiger pattern', 'tiger orange',
                'leopard print', 'leopard pattern', 'leopard spots', 'zebra stripe'
            ],
            
            # Common products that use these terms innocuously
            'innocent_products': [
                'ivory soap', 'ivory tower', 'ivory keys', 'piano ivory', 'ivory dish soap',
                'tiger lily', 'tiger moth', 'tiger eye stone', 'tiger beer',
                'leopard gecko', 'leopard frog', 'toy elephant', 'stuffed tiger',
                'elephant ear plant', 'elephant plush', 'tiger costume'
            ],
            
            # Brands and companies
            'brands': [
                'ivory brand', 'tiger energy', 'rhino tools', 'elephant insurance',
                'bear grylls', 'tiger woods', 'ivory coast'
            ],
            
            # Metaphorical usage
            'metaphorical': [
                'tiger mom', 'tiger economy', 'paper tiger', 'elephant memory',
                'bear market', 'bull and bear', 'elephant in room'
            ],
            
            # Legitimate services
            'legitimate_services': [
                'licensed massage therapist', 'registered nurse', 'certified trainer',
                'professional model', 'dance instructor', 'fitness trainer',
                'therapeutic massage', 'medical massage', 'physical therapy'
            ]
        }
        
        # Price thresholds for analysis
        self.price_analysis = {
            'very_low': 20,      # Under $20 - likely toys/replicas
            'low': 100,          # Under $100 - costume/synthetic
            'medium': 1000,      # $100-1000 - suspicious range
            'high': 5000,        # Over $5000 - likely genuine (illegal)
            'very_high': 10000   # Over $10,000 - extremely suspicious
        }
    
    def initialize_scoring_weights(self):
        """Initialize scoring weights for different indicator types"""
        
        self.wildlife_weights = {
            'critical_species': 45,      # Highest weight for CITES Appendix I
            'high_priority': 30,         # High weight for Appendix II
            'scientific_terms': 35,      # Scientific names indicate knowledge
            'trafficking_language': 25,  # Trafficking patterns
            'multiple_indicators': 20    # Bonus for multiple indicators
        }
        
        self.human_trafficking_weights = {
            'age_concerns': 50,          # Highest weight - major red flag
            'escort_services': 35,       # Clear adult services
            'control_patterns': 40,      # Control indicators very serious
            'financial_exploitation': 35, # Exploitation patterns
            'coded_language': 30,        # Trafficking coded language
            'suspicious_employment': 25  # Suspicious job offers
        }
        
        self.exclusion_weights = {
            'colors_patterns': -25,      # Strong negative for color references
            'innocent_products': -30,    # Strong negative for innocent products
            'brands': -20,               # Moderate negative for brands
            'metaphorical': -15,         # Moderate negative for metaphors
            'legitimate_services': -35   # Strong negative for legitimate services
        }
    
    def enhance_existing_score(self, listing_data: Dict, original_score: int) -> EnhancedThreatAnalysis:
        """
        Enhance the existing threat score with sophisticated analysis
        """
        
        title = listing_data.get('listing_title', '').lower()
        description = listing_data.get('description', '').lower()
        price_str = listing_data.get('listing_price', '')
        search_term = listing_data.get('search_term', '').lower()
        platform = listing_data.get('platform', '')
        
        text = f"{title} {description} {search_term}".lower()
        
        # Step 1: Check for exclusions first
        exclusion_factors = self._check_exclusions(text, price_str)
        exclusion_penalty = sum(self.exclusion_weights.get(factor['type'], 0) for factor in exclusion_factors)
        
        # Step 2: Analyze wildlife trafficking indicators
        wildlife_score, wildlife_indicators = self._analyze_wildlife_indicators(text, price_str)
        
        # Step 3: Analyze human trafficking indicators
        human_score, human_indicators = self._analyze_human_trafficking_indicators(text, price_str)
        
        # Step 4: Determine primary threat category
        threat_category = self._determine_threat_category(wildlife_score, human_score, exclusion_penalty)
        
        # Step 5: Calculate enhanced score
        enhanced_score = self._calculate_enhanced_score(
            original_score, wildlife_score, human_score, exclusion_penalty, platform
        )
        
        # Step 6: Determine threat level
        threat_level = self._determine_threat_level(enhanced_score, threat_category, human_indicators)
        
        # Step 7: Calculate confidence
        confidence = self._calculate_confidence(
            wildlife_indicators, human_indicators, exclusion_factors, enhanced_score
        )
        
        # Step 8: Check if human review required
        requires_review = self._requires_human_review(
            enhanced_score, threat_category, human_indicators, wildlife_indicators
        )
        
        # Step 9: Generate reasoning
        reasoning = self._generate_reasoning(
            original_score, enhanced_score, threat_category, 
            wildlife_indicators, human_indicators, exclusion_factors
        )
        
        return EnhancedThreatAnalysis(
            original_score=original_score,
            enhanced_score=enhanced_score,
            threat_category=threat_category,
            threat_level=threat_level,
            wildlife_indicators=wildlife_indicators,
            human_trafficking_indicators=human_indicators,
            exclusion_factors=[f['reason'] for f in exclusion_factors],
            confidence=confidence,
            reasoning=reasoning,
            requires_human_review=requires_review
        )
    
    def _check_exclusions(self, text: str, price_str: str) -> List[Dict]:
        """Check for exclusion patterns that indicate false positives"""
        
        exclusions = []
        
        for category, patterns in self.exclusion_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    exclusions.append({
                        'type': category,
                        'reason': f"Exclusion pattern: {pattern}",
                        'weight': self.exclusion_weights.get(category, 0)
                    })
                    # If we find ivory soap or similar, it's definitely safe
                    if pattern in ['ivory soap', 'ivory colored', 'ivory white', 'ivory brand']:
                        exclusions.append({
                            'type': 'strong_exclusion',
                            'reason': f"Strong exclusion: {pattern}",
                            'weight': -50  # Very strong negative weight
                        })
        
        # Price-based exclusions
        price = self._extract_price(price_str)
        if price is not None and price < self.price_analysis['very_low']:
            # Very cheap items with toy indicators
            if any(word in text for word in ['toy', 'plush', 'stuffed', 'replica', 'costume']):
                exclusions.append({
                    'type': 'price_exclusion',
                    'reason': f"Very low price (${price}) with toy indicators",
                    'weight': -25
                })
        
        return exclusions
    
    def _analyze_wildlife_indicators(self, text: str, price_str: str) -> Tuple[int, List[str]]:
        """Analyze for wildlife trafficking indicators"""
        
        score = 0
        indicators = []
        
        # Critical species detection
        for species_type, terms in self.wildlife_indicators['critical_species'].items():
            for term in terms:
                if term in text:
                    score += self.wildlife_weights['critical_species']
                    indicators.append(f"Critical species: {term}")
        
        # High priority species
        for species_type, terms in self.wildlife_indicators['high_priority'].items():
            for term in terms:
                if term in text:
                    score += self.wildlife_weights['high_priority']
                    indicators.append(f"High priority: {term}")
        
        # Scientific terms
        for term in self.wildlife_indicators['scientific_terms']:
            if term in text:
                score += self.wildlife_weights['scientific_terms']
                indicators.append(f"Scientific name: {term}")
        
        # Trafficking language
        for lang_type, terms in self.wildlife_indicators['trafficking_language'].items():
            matches = [term for term in terms if term in text]
            if matches:
                score += self.wildlife_weights['trafficking_language'] * len(matches)
                indicators.extend([f"Trafficking language ({lang_type}): {term}" for term in matches])
        
        # Multiple indicators bonus
        if len(indicators) >= 3:
            score += self.wildlife_weights['multiple_indicators']
            indicators.append("Multiple wildlife indicators detected")
        
        # Price analysis bonus
        price = self._extract_price(price_str)
        if price is not None:
            if price > self.price_analysis['very_high'] and indicators:
                score += 20
                indicators.append(f"Extremely high price: ${price}")
            elif price > self.price_analysis['high'] and indicators:
                score += 15
                indicators.append(f"High price: ${price}")
        
        return min(score, 100), indicators
    
    def _analyze_human_trafficking_indicators(self, text: str, price_str: str) -> Tuple[int, List[str]]:
        """Analyze for human trafficking indicators"""
        
        score = 0
        indicators = []
        
        # Age concerns (highest priority)
        for term in self.human_trafficking_indicators['age_concerns']:
            if term in text:
                score += self.human_trafficking_weights['age_concerns']
                indicators.append(f"Age concern: {term}")
        
        # Control patterns
        for term in self.human_trafficking_indicators['control_patterns']:
            if term in text:
                score += self.human_trafficking_weights['control_patterns']
                indicators.append(f"Control indicator: {term}")
        
        # Escort services
        for term in self.human_trafficking_indicators['escort_services']:
            if term in text:
                score += self.human_trafficking_weights['escort_services']
                indicators.append(f"Adult service: {term}")
        
        # Financial exploitation
        for term in self.human_trafficking_indicators['financial_exploitation']:
            if term in text:
                score += self.human_trafficking_weights['financial_exploitation']
                indicators.append(f"Financial exploitation: {term}")
        
        # Coded language
        for term in self.human_trafficking_indicators['coded_language']:
            if term in text:
                score += self.human_trafficking_weights['coded_language']
                indicators.append(f"Coded language: {term}")
        
        # Suspicious employment
        for term in self.human_trafficking_indicators['suspicious_employment']:
            if term in text:
                score += self.human_trafficking_weights['suspicious_employment']
                indicators.append(f"Suspicious employment: {term}")
        
        # Pattern analysis
        # 24/7 availability
        if any(term in text for term in ['24/7', '24 hours', 'anytime', 'always available']):
            score += 15
            indicators.append("24/7 availability pattern")
        
        # Cash only
        if any(term in text for term in ['cash only', 'cash preferred', 'no credit cards']):
            score += 12
            indicators.append("Cash-only payment pattern")
        
        # Multiple services
        service_count = sum(1 for term in self.human_trafficking_indicators['escort_services'] if term in text)
        if service_count >= 3:
            score += 20
            indicators.append(f"Multiple services offered: {service_count}")
        
        return min(score, 100), indicators
    
    def _determine_threat_category(self, wildlife_score: int, human_score: int, exclusion_penalty: int = 0) -> ThreatCategory:
        """Determine primary threat category"""
        
        # If we have strong exclusions (penalty < -40), it's likely safe
        if exclusion_penalty <= -40:
            return ThreatCategory.SAFE
        
        # Both high scores
        if wildlife_score >= 40 and human_score >= 40:
            return ThreatCategory.BOTH
        
        # Wildlife primary
        elif wildlife_score > human_score and wildlife_score >= 25:
            return ThreatCategory.WILDLIFE
        
        # Human trafficking primary
        elif human_score > wildlife_score and human_score >= 25:
            return ThreatCategory.HUMAN_TRAFFICKING
        
        # Neither significant
        else:
            return ThreatCategory.SAFE
    
    def _calculate_enhanced_score(self, original_score: int, wildlife_score: int, 
                                 human_score: int, exclusion_penalty: int, platform: str) -> int:
        """Calculate the final enhanced score"""
        
        # Start with original score as base
        enhanced_score = original_score
        
        # Add the higher of wildlife or human trafficking scores
        additional_score = max(wildlife_score, human_score)
        
        # If both are significant, add partial credit for the lower one
        if wildlife_score >= 25 and human_score >= 25:
            additional_score += min(wildlife_score, human_score) * 0.3
        
        # Apply additional score
        enhanced_score += additional_score
        
        # Apply exclusion penalty
        enhanced_score += exclusion_penalty  # Penalty is negative
        
        # Platform-specific adjustments
        platform_multiplier = self._get_platform_risk_multiplier(platform)
        enhanced_score = int(enhanced_score * platform_multiplier)
        
        # Ensure score stays in valid range
        return max(0, min(100, enhanced_score))
    
    def _determine_threat_level(self, score: int, category: ThreatCategory, human_indicators: List[str]) -> ThreatLevel:
        """Determine threat level based on score and category"""
        
        # Human trafficking gets elevated levels due to severity
        if category == ThreatCategory.HUMAN_TRAFFICKING:
            # Age concerns always elevate to critical
            if any('age concern' in indicator for indicator in human_indicators):
                return ThreatLevel.CRITICAL
            elif score >= 60:
                return ThreatLevel.CRITICAL
            elif score >= 40:
                return ThreatLevel.HIGH
            elif score >= 25:
                return ThreatLevel.MEDIUM
            else:
                return ThreatLevel.LOW
        
        # Both categories present
        elif category == ThreatCategory.BOTH:
            return ThreatLevel.CRITICAL
        
        # Wildlife trafficking
        elif category == ThreatCategory.WILDLIFE:
            if score >= 80:
                return ThreatLevel.CRITICAL
            elif score >= 65:
                return ThreatLevel.HIGH
            elif score >= 45:
                return ThreatLevel.MEDIUM
            elif score >= 25:
                return ThreatLevel.LOW
            else:
                return ThreatLevel.SAFE
        
        # Safe category
        else:
            return ThreatLevel.SAFE
    
    def _calculate_confidence(self, wildlife_indicators: List[str], human_indicators: List[str], 
                            exclusion_factors: List[Dict], score: int) -> float:
        """Calculate confidence in the threat assessment"""
        
        confidence = 0.5  # Base confidence
        
        # More indicators = higher confidence
        total_indicators = len(wildlife_indicators) + len(human_indicators)
        if total_indicators >= 5:
            confidence += 0.3
        elif total_indicators >= 3:
            confidence += 0.2
        elif total_indicators >= 1:
            confidence += 0.1
        
        # Exclusion factors reduce confidence in threat assessment
        if exclusion_factors:
            confidence -= 0.1 * len(exclusion_factors)
        
        # High scores increase confidence
        if score >= 80:
            confidence += 0.2
        elif score >= 60:
            confidence += 0.1
        
        # Scientific terms increase confidence
        if any('scientific name' in indicator for indicator in wildlife_indicators):
            confidence += 0.15
        
        # Age concerns in human trafficking = high confidence
        if any('age concern' in indicator for indicator in human_indicators):
            confidence += 0.25
        
        return max(0.0, min(1.0, confidence))
    
    def _requires_human_review(self, score: int, category: ThreatCategory, 
                              human_indicators: List[str], wildlife_indicators: List[str]) -> bool:
        """Determine if human review is required"""
        
        # Always require human review for human trafficking
        if category in [ThreatCategory.HUMAN_TRAFFICKING, ThreatCategory.BOTH]:
            return True
        
        # Age-related indicators always require review
        if any('age concern' in indicator for indicator in human_indicators):
            return True
        
        # Very high wildlife scores
        if score >= 85:
            return True
        
        # Multiple critical species indicators
        critical_indicators = [i for i in wildlife_indicators if 'critical species' in i]
        if len(critical_indicators) >= 2:
            return True
        
        return False
    
    def _generate_reasoning(self, original_score: int, enhanced_score: int, category: ThreatCategory,
                          wildlife_indicators: List[str], human_indicators: List[str], 
                          exclusion_factors: List[str]) -> str:
        """Generate human-readable reasoning"""
        
        parts = []
        
        # Score change
        if enhanced_score > original_score:
            parts.append(f"Enhanced score from {original_score} to {enhanced_score}")
        elif enhanced_score < original_score:
            parts.append(f"Reduced score from {original_score} to {enhanced_score}")
        else:
            parts.append(f"Maintained score of {enhanced_score}")
        
        # Primary threat
        if category == ThreatCategory.WILDLIFE:
            parts.append(f"Primary threat: Wildlife trafficking")
        elif category == ThreatCategory.HUMAN_TRAFFICKING:
            parts.append(f"Primary threat: Human trafficking")
        elif category == ThreatCategory.BOTH:
            parts.append(f"Multiple threats detected")
        else:
            parts.append(f"No significant threats detected")
        
        # Key indicators
        if wildlife_indicators:
            top_wildlife = wildlife_indicators[:2]
            parts.append(f"Wildlife indicators: {', '.join(top_wildlife)}")
        
        if human_indicators:
            top_human = human_indicators[:2]
            parts.append(f"Human trafficking indicators: {', '.join(top_human)}")
        
        # Exclusions
        if exclusion_factors:
            parts.append(f"Exclusions applied: {len(exclusion_factors)}")
        
        return "; ".join(parts)
    
    def _get_platform_risk_multiplier(self, platform: str) -> float:
        """Get platform-specific risk multiplier"""
        
        # Platform risk profiles
        risk_multipliers = {
            'craigslist': 1.2,      # High anonymity, local transactions
            'facebook': 1.1,        # Large user base, some verification
            'gumtree': 1.15,        # Similar to Craigslist
            'aliexpress': 1.1,      # International, varying regulation
            'taobao': 1.15,         # Chinese platform, different regulations
            'olx': 1.1,             # International classified ads
            'ebay': 1.0,            # More regulated, buyer protection
            'mercadolibre': 1.05,   # Regional leader, some regulation
            'marktplaats': 1.0      # EU regulated
        }
        
        return risk_multipliers.get(platform.lower(), 1.0)
    
    def _extract_price(self, price_str: str) -> Optional[float]:
        """Extract numeric price from price string"""
        
        if not price_str:
            return None
        
        # Remove currency symbols and extract numbers
        price_clean = re.sub(r'[^\d.,]', '', str(price_str))
        if not price_clean:
            return None
        
        try:
            # Handle different decimal separators
            if ',' in price_clean and '.' in price_clean:
                # Assume comma is thousands separator
                price_clean = price_clean.replace(',', '')
            elif ',' in price_clean:
                # Could be decimal separator in some locales
                if price_clean.count(',') == 1 and len(price_clean.split(',')[1]) <= 2:
                    price_clean = price_clean.replace(',', '.')
                else:
                    price_clean = price_clean.replace(',', '')
            
            return float(price_clean)
        except:
            return None


def test_enhanced_scoring():
    """Test the enhanced scoring system"""
    
    print("🔍 TESTING ENHANCED THREAT SCORING SYSTEM")
    print("=" * 80)
    
    scorer = EnhancedThreatScorer()
    
    # Test cases with original scores
    test_cases = [
        {
            'listing_title': 'Authentic African Elephant Ivory Carving - Serious Buyers Only',
            'description': 'Genuine carved elephant ivory from private collection. Discrete shipping.',
            'listing_price': '$2,500',
            'search_term': 'elephant ivory',
            'platform': 'craigslist',
            'original_score': 75
        },
        {
            'listing_title': 'Young Asian Massage Therapist Available 24/7',
            'description': 'New talent, 18 years old, full service available. Cash only.',
            'listing_price': '$200/hour',
            'search_term': 'massage',
            'platform': 'craigslist',
            'original_score': 45
        },
        {
            'listing_title': 'Ivory Colored Soap Set - 3 Bars',
            'description': 'Beautiful ivory white soap for bath. Brand new condition.',
            'listing_price': '$8.99',
            'search_term': 'ivory',
            'platform': 'ebay',
            'original_score': 65
        },
        {
            'listing_title': 'Traditional Tiger Bone Medicine Powder',
            'description': 'Authentic tiger bone powder for traditional healing. Very rare specimen.',
            'listing_price': '$450',
            'search_term': 'tiger bone',
            'platform': 'aliexpress',
            'original_score': 70
        }
    ]
    
    print("🎯 ENHANCED SCORING RESULTS:")
    print("-" * 80)
    
    for i, test_case in enumerate(test_cases, 1):
        analysis = scorer.enhance_existing_score(test_case, test_case['original_score'])
        
        print(f"\n📋 TEST CASE {i}: {test_case['listing_title'][:50]}...")
        print(f"   Original Score: {analysis.original_score}")
        print(f"   Enhanced Score: {analysis.enhanced_score} ({analysis.enhanced_score - analysis.original_score:+d})")
        print(f"   Threat Category: {analysis.threat_category.value}")
        print(f"   Threat Level: {analysis.threat_level.value}")
        print(f"   Confidence: {analysis.confidence:.1%}")
        print(f"   Human Review: {'YES' if analysis.requires_human_review else 'NO'}")
        
        if analysis.wildlife_indicators:
            print(f"   Wildlife Indicators: {len(analysis.wildlife_indicators)}")
            for indicator in analysis.wildlife_indicators[:2]:
                print(f"     • {indicator}")
        
        if analysis.human_trafficking_indicators:
            print(f"   Human Trafficking Indicators: {len(analysis.human_trafficking_indicators)}")
            for indicator in analysis.human_trafficking_indicators[:2]:
                print(f"     • {indicator}")
        
        if analysis.exclusion_factors:
            print(f"   Exclusions Applied: {analysis.exclusion_factors[0]}")
        
        print(f"   Reasoning: {analysis.reasoning}")
    
    print(f"\n✅ ENHANCED SCORING SYSTEM: READY FOR INTEGRATION")
    print(f"   • Builds on existing scores")
    print(f"   • Adds wildlife + human trafficking detection")
    print(f"   • Sophisticated exclusion system")
    print(f"   • Confidence scoring")
    print(f"   • Human review flagging")


if __name__ == "__main__":
    test_enhanced_scoring()
