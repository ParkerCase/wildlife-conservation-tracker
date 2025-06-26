#!/usr/bin/env python3
"""
WildGuard AI - Advanced Quality Filtering System
Prevents UNRATED classifications and focuses on quality detections
"""

import re
import logging
import os
from typing import Dict, List, Tuple, Any
import json


class WildlifeQualityFilter:
    """Advanced quality filtering to reduce UNRATED classifications from 95% to ~15%"""

    def __init__(self):
        # Terms that indicate NON-wildlife items (immediate rejection)
        self.reject_terms = {
            # Art & Decorative Items
            "art": [
                "painting",
                "photograph",
                "photo",
                "replica",
                "print",
                "poster",
                "artwork",
                "drawing",
                "sketch",
                "canvas",
                "framed",
                "sculpture",
                "statue",
                "carving replica",
                "art piece",
                "wall art",
                "picture frame",
            ],
            # Vintage & Decorative
            "vintage_decor": [
                "vintage decor",
                "antique decoration",
                "decorative",
                "ornament",
                "figurine",
                "collectible figure",
                "display piece",
                "shelf decor",
                "home decoration",
                "interior design",
                "decorative item",
            ],
            # Fake & Imitation
            "fake": [
                "fake",
                "imitation",
                "artificial",
                "synthetic",
                "faux",
                "mock",
                "reproduction",
                "copy",
                "replica item",
                "simulation",
                "substitute",
                "man-made",
                "manufactured replica",
            ],
            # Toys & Games
            "toys": [
                "toy",
                "plush",
                "stuffed",
                "teddy",
                "doll",
                "game",
                "puzzle",
                "model kit",
                "miniature model",
                "action figure",
                "play set",
                "children toy",
                "kids toy",
                "baby toy",
                "soft toy",
            ],
            # Clothing & Accessories
            "clothing": [
                "costume",
                "mask",
                "hat",
                "shirt",
                "clothing",
                "apparel",
                "costume jewelry",
                "fashion accessory",
            ],
            # Books & Media
            "media": [
                "book",
                "magazine",
                "dvd",
                "cd",
                "video",
                "documentary",
                "film",
                "movie",
                "ebook",
                "audiobook",
                "digital book",
                "reading material",
                "educational material",
                "study guide",
            ],
            # Digital & Virtual
            "digital": [
                "digital",
                "virtual",
                "nft",
                "crypto",
                "blockchain",
                "download",
                "pdf",
                "digital art",
                "virtual item",
                "online content",
                "app",
                "software",
                "digital download",
                "virtual reality",
            ],
        }

        # Terms that indicate REAL wildlife (boost quality score)
        self.wildlife_terms = {
            # Live animals (critical for trafficking)
            "live": [
                "live",
                "alive",
                "living",
                "breathing",
                "baby animal",
                "juvenile",
                "adult animal",
                "breeding",
                "captive",
                "wild caught",
                "exotic pet",
                "rare animal",
                "endangered species",
            ],
            # Animal parts (concerning for trafficking)
            "parts": [
                "ivory",
                "horn",
                "tusk",
                "bone",
                "skull",
                "skin",
                "hide",
                "pelt",
                "fur",
                "feather",
                "scale",
                "shell",
                "carapace",
                "antler",
                "claw",
                "tooth",
                "teeth",
                "whisker",
                "tail",
            ],
            # Products from animals
            "products": [
                "meat",
                "oil",
                "powder",
                "medicine",
                "traditional medicine",
                "ground",
                "dried",
                "preserved",
                "bile",
                "gallbladder",
                "musk",
                "ambergris",
                "caviar",
                "fin",
                "cartilage",
            ],
            # Trafficking indicators
            "trafficking": [
                "rare specimen",
                "endangered",
                "protected",
                "wild",
                "exotic",
                "illegal",
                "permit required",
                "license",
                "cites",
                "pre-ban",
                "documentation",
                "certificate",
                "authentic",
                "traditional use",
            ],
        }

        # Multilingual reject terms (key languages for each platform)
        self.multilingual_rejects = {
            "spanish": [
                "pintura",
                "fotografía",
                "foto",
                "réplica",
                "imitación",
                "juguete",
                "peluche",
                "decoración",
                "artesanía",
                "adorno",
                "figura decorativa",
            ],
            "portuguese": [
                "pintura",
                "fotografia",
                "foto",
                "réplica",
                "imitação",
                "brinquedo",
                "pelúcia",
                "decoração",
                "artesanato",
                "enfeite",
                "peça decorativa",
            ],
            "dutch": [
                "schilderij",
                "foto",
                "replica",
                "imitatie",
                "speelgoed",
                "pluche",
                "decoratie",
                "kunstwerk",
                "ornament",
                "figuur",
            ],
            "german": [
                "gemälde",
                "foto",
                "replik",
                "imitation",
                "spielzeug",
                "plüsch",
                "dekoration",
                "kunstwerk",
                "ornament",
                "figur",
            ],
            "french": [
                "peinture",
                "photo",
                "réplique",
                "imitation",
                "jouet",
                "peluche",
                "décoration",
                "artwork",
                "ornement",
                "figurine",
            ],
            "russian": [
                "картина",
                "фото",
                "реплика",
                "имитация",
                "игрушка",
                "плюш",
                "декорация",
                "украшение",
                "фигурка",
                "поделка",
            ],
            "italian": [
                "dipinto",
                "foto",
                "replica",
                "imitazione",
                "giocattolo",
                "peluche",
                "decorazione",
                "ornamento",
                "figurina",
                "soprammobile",
            ],
            "chinese": [
                "画",
                "照片",
                "复制品",
                "仿制",
                "玩具",
                "毛绒",
                "装饰",
                "工艺品",
                "摆件",
                "模型",
            ],
            "vietnamese": [
                "tranh",
                "ảnh",
                "bản sao",
                "giả",
                "đồ chơi",
                "nhồi bông",
                "trang trí",
                "đồ thủ công",
                "vật trang trí",
            ],
        }

        # Critical species that should always get high scores
        self.critical_species = [
            "ivory",
            "elephant",
            "rhino",
            "rhinoceros",
            "tiger",
            "leopard",
            "pangolin",
            "bear",
            "lion",
            "jaguar",
            "cheetah",
            "snow leopard",
            "orangutan",
            "gorilla",
            "whale",
            "shark",
            "turtle",
            "tortoise",
            "eagle",
            "falcon",
            "parrot",
        ]

        # High-risk regions for wildlife trafficking
        self.high_risk_regions = [
            "africa",
            "asia",
            "southeast asia",
            "south america",
            "china",
            "vietnam",
            "laos",
            "myanmar",
            "cambodia",
            "thailand",
            "indonesia",
            "philippines",
            "brazil",
            "peru",
            "colombia",
            "madagascar",
            "kenya",
            "tanzania",
            "zimbabwe",
        ]

        logging.info(
            "✅ WildlifeQualityFilter initialized with comprehensive filtering rules"
        )

    def assess_quality(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main quality assessment function
        Returns: {shouldInclude, qualityScore, threatLevel, confidence, reason}
        """
        try:
            title = (listing.get("title", "") or "").lower().strip()
            description = (listing.get("description", "") or "").lower().strip()
            full_text = f"{title} {description}".strip()

            if not full_text or len(full_text) < 3:
                return {
                    "shouldInclude": False,
                    "qualityScore": 0.0,
                    "threatLevel": "UNRATED",
                    "confidence": 0.9,
                    "reason": "Empty or too short text",
                }

            # Immediate rejection check
            rejection_result = self.should_reject(full_text)
            if rejection_result["should_reject"]:
                return {
                    "shouldInclude": False,
                    "qualityScore": 0.0,
                    "threatLevel": "UNRATED",
                    "confidence": rejection_result["confidence"],
                    "reason": f"Rejected: {rejection_result['reason']}",
                }

            # Calculate quality score
            quality_score = self.calculate_quality_score(full_text, listing)

            # Determine threat level based on quality score
            threat_level = self.determine_threat_level(
                quality_score, full_text, listing
            )

            # Calculate confidence level
            confidence = self.calculate_confidence(quality_score, full_text)

            # Decision: Only include if quality score > 20% (OPTIMIZED)
            quality_threshold = float(os.getenv('QUALITY_THRESHOLD', '0.2'))
            should_include = quality_score > quality_threshold

            return {
                "shouldInclude": should_include,
                "qualityScore": round(quality_score, 3),
                "threatLevel": threat_level,
                "confidence": round(confidence, 3),
                "reason": (
                    f"Quality score: {quality_score:.1%}"
                    if should_include
                    else "Quality score too low"
                ),
            }

        except Exception as e:
            logging.error(f"Quality assessment error: {e}")
            return {
                "shouldInclude": False,
                "qualityScore": 0.0,
                "threatLevel": "UNRATED",
                "confidence": 0.1,
                "reason": f"Assessment error: {str(e)}",
            }

    def should_reject(self, text: str) -> Dict[str, Any]:
        """Check if listing should be immediately rejected"""
        # Check English reject terms
        for category, terms in self.reject_terms.items():
            for term in terms:
                if term in text:
                    return {
                        "should_reject": True,
                        "reason": f"Contains {category} term: '{term}'",
                        "confidence": 0.9,
                    }

        # Check multilingual reject terms
        for language, terms in self.multilingual_rejects.items():
            for term in terms:
                if term in text:
                    return {
                        "should_reject": True,
                        "reason": f"Contains {language} reject term: '{term}'",
                        "confidence": 0.85,
                    }

        # Check for obvious non-wildlife patterns
        if self.contains_obvious_non_wildlife_patterns(text):
            return {
                "should_reject": True,
                "reason": "Contains obvious non-wildlife patterns",
                "confidence": 0.8,
            }

        return {"should_reject": False, "reason": None, "confidence": 0.0}

    def contains_obvious_non_wildlife_patterns(self, text: str) -> bool:
        """Check for patterns that clearly indicate non-wildlife items"""
        non_wildlife_patterns = [
            r"\b(size|sizes?)\s+(xs|s|m|l|xl|xxl)\b",  # Clothing sizes
            r"\b(brand\s+new|mint\s+condition|unopened)\b",  # New items
            r"\b(digital\s+download|instant\s+download)\b",  # Digital items
            r"\b(home\s+decor|wall\s+hanging|shelf\s+display)\b",  # Decorative items
            r"\b(costume\s+party|halloween|cosplay)\b",  # Costume items
            r"\b(children\'?s?\s+toy|kids\s+toy|baby\s+toy)\b",  # Toys
            r"\b(art\s+print|canvas\s+print|poster\s+print)\b",  # Art prints
            r"\b(replica\s+gun|toy\s+gun|airsoft)\b",  # Toy weapons
            r"\b(video\s+game|board\s+game|card\s+game)\b",  # Games
        ]

        for pattern in non_wildlife_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True

        return False

    def calculate_quality_score(self, text: str, listing: Dict[str, Any]) -> float:
        """Calculate quality score (0-1) based on multiple factors (OPTIMIZED)"""
        score = 0.3  # Lowered base score to rely more on content analysis

        # Wildlife terms boost (ENHANCED scoring)
        wildlife_matches = 0
        for category, terms in self.wildlife_terms.items():
            for term in terms:
                if term in text:
                    wildlife_matches += 1
                    if category == "live":
                        score += 0.18  # INCREASED - Live animals critical
                    elif category == "parts":
                        score += 0.15  # INCREASED - Animal parts very concerning
                    elif category == "trafficking":
                        score += 0.13  # INCREASED - Trafficking indicators important
                    else:
                        score += 0.10  # INCREASED - General wildlife terms

        # Critical species boost (ENHANCED)
        critical_matches = 0
        for species in self.critical_species:
            if species in text:
                critical_matches += 1
                score += 0.18  # INCREASED for critical species

        # Price analysis
        price_str = str(listing.get("price", "") or "").lower()
        price_numbers = re.findall(r"[\d,]+\.?\d*", price_str)
        if price_numbers:
            try:
                price = float(price_numbers[0].replace(",", ""))
                if price > 10000:  # Very high prices suspicious for wildlife
                    score += 0.18  # INCREASED
                elif price > 1000:
                    score += 0.12  # INCREASED
                elif price > 100:
                    score += 0.08   # INCREASED
                elif price > 0 and price < 10:  # Very low prices likely fake
                    score -= 0.15
            except (ValueError, IndexError):
                pass

        # Geographic risk analysis
        location = (listing.get("location", "") or "").lower()
        for region in self.high_risk_regions:
            if region in location:
                score += 0.08
                break

        # Text quality indicators
        title_length = len(listing.get("title", "") or "")
        if title_length > 50:  # Detailed titles often better
            score += 0.05
        elif title_length < 10:  # Very short titles often low quality
            score -= 0.10

        # Search term relevance
        search_term = (listing.get("search_term", "") or "").lower()
        if search_term in text:
            score += 0.05

        # Platform-specific adjustments
        platform = listing.get("platform", "").lower()
        if platform == "avito":  # High-performing platform
            score += 0.03
        elif platform == "facebook_marketplace":  # Often lower quality
            score -= 0.02

        # Suspicious terms that lower quality
        suspicious_terms = [
            "quick sale",
            "must sell",
            "no questions",
            "cash only",
            "discrete",
            "urgent sale",
            "moving sale",
        ]
        for term in suspicious_terms:
            if term in text:
                score -= 0.05

        # Ensure score stays within bounds
        return max(0.0, min(1.0, score))

    def determine_threat_level(
        self, quality_score: float, text: str, listing: Dict[str, Any]
    ) -> str:
        """Determine threat level based on quality score and content analysis (OPTIMIZED)"""
        quality_threshold = float(os.getenv('QUALITY_THRESHOLD', '0.2'))
        if quality_score < quality_threshold:
            return "UNRATED"

        # Check for CRITICAL indicators
        critical_indicators = [
            "live",
            "ivory",
            "rhino horn",
            "tiger bone",
            "pangolin scale",
            "bear bile",
            "elephant tusk",
            "endangered",
            "protected species",
        ]

        if quality_score > 0.75 and any(  # LOWERED threshold
            indicator in text for indicator in critical_indicators
        ):
            return "CRITICAL"

        # Check for HIGH threat indicators
        high_indicators = [
            "traditional medicine",
            "authentic",
            "rare specimen",
            "wild caught",
            "illegal",
            "black market",
            "no permit",
            "undocumented",
        ]

        if quality_score > 0.65 or any(  # LOWERED threshold
            indicator in text for indicator in high_indicators
        ):
            return "HIGH"

        # MEDIUM threat
        if quality_score > 0.45:  # LOWERED threshold
            return "MEDIUM"

        # LOW threat
        return "LOW"

    def calculate_confidence(self, quality_score: float, text: str) -> float:
        """Calculate confidence level for the assessment"""
        confidence = 0.5  # Base confidence

        # Higher confidence for extreme scores
        if quality_score > 0.8 or quality_score < 0.2:
            confidence = 0.9
        elif quality_score > 0.6 or quality_score < 0.4:
            confidence = 0.75

        # Boost confidence for clear indicators
        clear_wildlife = sum(
            1
            for category in self.wildlife_terms.values()
            for term in category
            if term in text
        )
        if clear_wildlife > 3:
            confidence += 0.1

        clear_rejects = sum(
            1
            for category in self.reject_terms.values()
            for term in category
            if term in text
        )
        if clear_rejects > 0:
            confidence = 0.95

        # Text length affects confidence
        if len(text) > 100:
            confidence += 0.05
        elif len(text) < 20:
            confidence -= 0.1

        return max(0.1, min(0.99, confidence))

    def get_filter_stats(self) -> Dict[str, int]:
        """Get statistics about filter rules"""
        return {
            "reject_categories": len(self.reject_terms),
            "total_reject_terms": sum(
                len(terms) for terms in self.reject_terms.values()
            ),
            "wildlife_categories": len(self.wildlife_terms),
            "total_wildlife_terms": sum(
                len(terms) for terms in self.wildlife_terms.values()
            ),
            "multilingual_languages": len(self.multilingual_rejects),
            "critical_species": len(self.critical_species),
            "high_risk_regions": len(self.high_risk_regions),
        }


# Example usage and testing
if __name__ == "__main__":
    # Initialize filter
    filter_system = WildlifeQualityFilter()

    # Print statistics
    stats = filter_system.get_filter_stats()
    print("🔍 WildlifeQualityFilter Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Test cases
    test_cases = [
        {
            "title": "Rare elephant ivory carving authentic",
            "description": "Traditional carved ivory from elephant tusk",
            "price": "$5000",
            "platform": "ebay",
        },
        {
            "title": "Elephant painting wall art",
            "description": "Beautiful elephant artwork for home decoration",
            "price": "$50",
            "platform": "etsy",
        },
        {
            "title": "Live baby tiger for sale",
            "description": "Exotic tiger cub needs new home",
            "price": "$15000",
            "platform": "craigslist",
        },
        {
            "title": "Tiger plush toy stuffed animal",
            "description": "Cute tiger toy for children",
            "price": "$20",
            "platform": "ebay",
        },
    ]

    print("\n🧪 Testing Quality Filter:")
    for i, test_case in enumerate(test_cases, 1):
        result = filter_system.assess_quality(test_case)
        print(f"\n--- Test Case {i} ---")
        print(f"Title: {test_case['title']}")
        print(f"Result: {'✅ ACCEPT' if result['shouldInclude'] else '❌ REJECT'}")
        print(f"Threat Level: {result['threatLevel']}")
        print(f"Quality Score: {result['qualityScore']:.1%}")
        print(f"Confidence: {result['confidence']:.1%}")
        print(f"Reason: {result['reason']}")
