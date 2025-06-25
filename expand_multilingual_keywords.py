#!/usr/bin/env python3
"""
WildGuard AI - Quick Multilingual Keyword Expansion
Run this to immediately expand your 966+ keywords into 15+ languages
"""

import json
import time
import logging
import sys
from typing import List, Dict
import random

# Install deep-translator if not available
try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("Installing deep-translator...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "deep-translator>=1.11.4"])
    from deep_translator import GoogleTranslator

# Import existing keywords
from comprehensive_endangered_keywords import ALL_ENDANGERED_SPECIES_KEYWORDS

# Wildlife trafficking codewords (100+ terms)
WILDLIFE_TRAFFICKING_CODEWORDS = [
    # Core disguised terms
    'special material', 'rare material', 'unique material', 'natural material',
    'organic material', 'authentic material', 'traditional material', 'exotic material',
    'vintage specimen', 'antique specimen', 'museum specimen', 'collector specimen',
    'research specimen', 'scientific specimen', 'exhibition specimen', 'study specimen',
    
    # Quality claims
    'museum quality', 'gallery quality', 'exhibition quality', 'collector quality',
    'investment grade', 'heirloom quality', 'masterpiece quality', 'premium quality',
    'authentic piece', 'genuine article', 'real deal', 'certified authentic',
    'documented piece', 'provenance included', 'papers included', 'certificate included',
    
    # Rarity claims
    'extremely rare', 'very rare', 'ultra rare', 'super rare', 'one of a kind',
    'last available', 'final piece', 'last chance', 'limited availability',
    'exclusive piece', 'private collection', 'estate collection', 'family collection',
    'inherited piece', 'grandfather collection', 'generational piece', 'legacy item',
    
    # Legality claims
    'pre-ban', 'pre-1975', 'pre-1973', 'pre-convention', 'vintage import',
    'old stock', 'estate find', 'grandfather clause', 'legal import',
    'documentation available', 'papers available', 'permits included', 'cites permit',
    'legally obtained', 'ethically sourced', 'sustainable harvest', 'legal harvest',
    
    # Cultural covers
    'tribal authentic', 'indigenous craft', 'native american', 'aboriginal artifact',
    'ceremonial use', 'ritual use', 'shamanic tool', 'medicine man', 'witch doctor',
    'traditional remedy', 'ancient remedy', 'natural remedy', 'healing stone',
    'spiritual healing', 'energy stone', 'chakra stone', 'feng shui', 'voodoo authentic',
    
    # Medicine claims
    'traditional medicine', 'chinese medicine', 'tcm authentic', 'ayurvedic medicine',
    'natural medicine', 'herbal medicine', 'alternative medicine', 'holistic remedy',
    'healing properties', 'medicinal properties', 'therapeutic value', 'health benefits',
    'cure all', 'miracle cure', 'ancient cure', 'powerful medicine', 'rare medicine',
    
    # Transaction terms
    'serious buyers only', 'genuine buyers', 'collectors welcome', 'dealers welcome',
    'no questions asked', 'discrete sale', 'private sale', 'confidential sale',
    'cash only', 'pickup only', 'local pickup', 'will deliver', 'discrete shipping',
    'careful packaging', 'insured shipping', 'signature required', 'secure delivery',
    
    # Vague descriptions
    'know what this is', 'experts will understand', 'connoisseurs only', 'educated buyers',
    'special interest', 'niche market', 'specialized collector', 'particular buyer',
    'right person', 'serious inquiries', 'genuine interest', 'real collector',
    'true enthusiast', 'knowledgeable buyer', 'experienced collector', 'veteran collector',
    
    # Additional terms
    'investment piece', 'appreciating asset', 'store of value', 'portfolio piece',
    'below market', 'wholesale price', 'motivated seller', 'quick sale', 'must sell',
    'best offer', 'make offer', 'negotiate price', 'trade considered', 'package deal',
    'private matter', 'sensitive item', 'understand discretion', 'privacy important',
    'educational purpose', 'research purpose', 'academic study', 'university collection',
    'cultural preservation', 'heritage conservation', 'artistic study', 'craft tradition'
]

# 15+ major trafficking languages
TARGET_LANGUAGES = {
    'es': 'Spanish',      # Latin America
    'zh': 'Chinese',      # Traditional medicine markets
    'fr': 'French',       # West/Central Africa  
    'pt': 'Portuguese',   # Brazil trafficking
    'vi': 'Vietnamese',   # SE Asia hub
    'th': 'Thai',         # Thailand hub
    'id': 'Indonesian',   # Wildlife source
    'ru': 'Russian',      # Eastern Europe
    'ar': 'Arabic',       # Middle East
    'ja': 'Japanese',     # Ivory markets
    'ko': 'Korean',       # Traditional medicine
    'hi': 'Hindi',        # Indian subcontinent
    'sw': 'Swahili',      # East Africa
    'de': 'German',       # European markets
    'it': 'Italian',      # European markets
}

def quick_translate_batch(keywords: List[str], target_lang: str) -> List[str]:
    """Quick translation with error handling using deep-translator"""
    translator = GoogleTranslator(source='en', target=target_lang)
    translated = []
    
    print(f"  Translating to {TARGET_LANGUAGES[target_lang]}...")
    
    # Process one by one (deep-translator handles single translations better)
    for keyword in keywords:
        try:
            result = translator.translate(keyword)
            
            if result:
                translated_text = result.lower().strip()
                if translated_text and translated_text != keyword.lower():
                    translated.append(translated_text)
            
            time.sleep(0.1)  # Rate limiting
            
        except Exception as e:
            print(f"    Warning: Translation error for '{keyword}': {e}")
            time.sleep(0.5)
            continue
    
    print(f"    ✅ {len(translated)} translations completed")
    return translated

def main():
    """Main function - expand keywords into multiple languages"""
    
    print("🌍 WildGuard AI - Multilingual Keyword Expansion")
    print("=" * 60)
    
    # Combine all keywords
    all_keywords = list(set(ALL_ENDANGERED_SPECIES_KEYWORDS + WILDLIFE_TRAFFICKING_CODEWORDS))
    print(f"📊 Source keywords: {len(ALL_ENDANGERED_SPECIES_KEYWORDS):,} species terms")
    print(f"🔍 Source codewords: {len(WILDLIFE_TRAFFICKING_CODEWORDS):,} trafficking terms")
    print(f"📚 Total unique keywords: {len(all_keywords):,}")
    print(f"🌐 Target languages: {len(TARGET_LANGUAGES)}")
    
    # Sample keywords for faster testing (remove this for full expansion)
    sample_size = 100  # Use smaller sample for quick testing
    sample_keywords = random.sample(all_keywords, min(sample_size, len(all_keywords)))
    print(f"\n⚡ Using sample of {len(sample_keywords)} keywords for quick testing")
    print("   (Remove sample_size limit for full expansion)")
    
    multilingual_keywords = {
        'en': sample_keywords  # Start with English
    }
    
    # Translate to each language
    for lang_code, lang_name in TARGET_LANGUAGES.items():
        print(f"\n🔄 Processing {lang_name} ({lang_code})")
        
        try:
            translated = quick_translate_batch(sample_keywords, lang_code)
            if translated:
                multilingual_keywords[lang_code] = translated
                print(f"  ✅ Added {len(translated)} {lang_name} keywords")
            else:
                print(f"  ❌ No successful translations for {lang_name}")
                
        except Exception as e:
            print(f"  💥 Error with {lang_name}: {e}")
            continue
    
    # Save results
    output_data = {
        'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_languages': len(multilingual_keywords),
        'total_keywords': sum(len(keywords) for keywords in multilingual_keywords.values()),
        'keywords_by_language': multilingual_keywords
    }
    
    with open('multilingual_wildlife_keywords.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    # Results summary
    total_keywords = sum(len(keywords) for keywords in multilingual_keywords.values())
    
    print(f"\n🎉 EXPANSION COMPLETE!")
    print("=" * 60)
    print(f"Languages: {len(multilingual_keywords)}")
    print(f"Total keywords: {total_keywords:,}")
    print(f"Coverage expansion: {total_keywords // len(sample_keywords):.1f}x")
    print(f"Saved to: multilingual_wildlife_keywords.json")
    
    # Show samples
    print(f"\n🌍 SAMPLE KEYWORDS BY LANGUAGE:")
    for lang_code, keywords in multilingual_keywords.items():
        lang_name = TARGET_LANGUAGES.get(lang_code, lang_code.upper())
        sample = keywords[:3] if keywords else []
        print(f"  {lang_name}: {', '.join(sample)}")
    
    print(f"\n🚀 NEXT STEPS:")
    print("1. ✅ Multilingual keywords generated")
    print("2. Add to scanner: modify complete_enhanced_scanner.py")
    print("3. Use mixed language keyword batches in scanning")
    print("4. Run full expansion (remove sample_size limit)")

if __name__ == "__main__":
    main()
