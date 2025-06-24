#!/usr/bin/env python3
"""
WildGuard AI - Multilingual Integration for Complete Enhanced Scanner
Add this code to your complete_enhanced_scanner.py for multilingual support
"""

import json
import random
import logging
from typing import List, Dict

class MultilingualScannerMixin:
    """Mixin to add multilingual keyword support to existing scanner"""
    
    def load_multilingual_keywords(self):
        """Load multilingual keywords from generated file"""
        try:
            with open('multilingual_wildlife_keywords.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.keywords_by_language = data['keywords_by_language']
                
                # Flatten all keywords into single list
                self.multilingual_keywords = []
                for lang_keywords in self.keywords_by_language.values():
                    self.multilingual_keywords.extend(lang_keywords)
                
                # Remove duplicates
                self.multilingual_keywords = list(set(self.multilingual_keywords))
                
                logging.info(f"🌍 Loaded multilingual keywords:")
                logging.info(f"  Languages: {len(self.keywords_by_language)}")
                logging.info(f"  Total keywords: {len(self.multilingual_keywords):,}")
                
                # Show language breakdown
                for lang_code, keywords in self.keywords_by_language.items():
                    lang_name = self.get_language_name(lang_code)
                    logging.info(f"  {lang_name}: {len(keywords):,} keywords")
                
                return True
                
        except Exception as e:
            logging.warning(f"Could not load multilingual keywords: {e}")
            logging.info("Falling back to English-only keywords")
            self.multilingual_keywords = self.all_keywords
            self.keywords_by_language = {'en': self.all_keywords}
            return False
    
    def get_language_name(self, lang_code: str) -> str:
        """Get human-readable language name"""
        language_names = {
            'en': 'English', 'es': 'Spanish', 'zh': 'Chinese', 'fr': 'French',
            'pt': 'Portuguese', 'vi': 'Vietnamese', 'th': 'Thai', 'id': 'Indonesian',
            'ru': 'Russian', 'ar': 'Arabic', 'ja': 'Japanese', 'ko': 'Korean',
            'hi': 'Hindi', 'sw': 'Swahili', 'de': 'German', 'it': 'Italian'
        }
        return language_names.get(lang_code, lang_code.upper())
    
    def get_multilingual_keyword_batch(self, batch_size: int = 15) -> List[str]:
        """Get a keyword batch mixing multiple languages"""
        
        if not hasattr(self, 'multilingual_keywords') or not self.multilingual_keywords:
            # Fallback to original method if multilingual not loaded
            return self.get_next_keyword_batch(batch_size)
        
        # Language distribution strategy:
        # 60% English (most platforms are English-based)
        # 40% other languages (to catch international listings)
        english_ratio = 0.6
        english_count = int(batch_size * english_ratio)
        other_count = batch_size - english_count
        
        keywords = []
        
        # Add English keywords
        english_keywords = self.keywords_by_language.get('en', [])
        if english_keywords and english_count > 0:
            sample_size = min(english_count, len(english_keywords))
            keywords.extend(random.sample(english_keywords, sample_size))
        
        # Add other language keywords
        if other_count > 0:
            other_lang_keywords = []
            for lang_code, lang_keywords in self.keywords_by_language.items():
                if lang_code != 'en':
                    other_lang_keywords.extend(lang_keywords)
            
            if other_lang_keywords:
                sample_size = min(other_count, len(other_lang_keywords))
                keywords.extend(random.sample(other_lang_keywords, sample_size))
        
        # Fill remaining slots if needed
        while len(keywords) < batch_size and self.multilingual_keywords:
            remaining = batch_size - len(keywords)
            additional = random.sample(self.multilingual_keywords, min(remaining, len(self.multilingual_keywords)))
            keywords.extend([k for k in additional if k not in keywords])
        
        return keywords[:batch_size]
    
    def get_targeted_language_batch(self, target_languages: List[str], batch_size: int = 15) -> List[str]:
        """Get keywords from specific languages (for geographic targeting)"""
        
        if not hasattr(self, 'keywords_by_language'):
            return self.get_next_keyword_batch(batch_size)
        
        keywords = []
        keywords_per_lang = batch_size // len(target_languages)
        
        for lang_code in target_languages:
            lang_keywords = self.keywords_by_language.get(lang_code, [])
            if lang_keywords:
                sample_size = min(keywords_per_lang, len(lang_keywords))
                keywords.extend(random.sample(lang_keywords, sample_size))
        
        # Fill remaining slots
        while len(keywords) < batch_size and self.multilingual_keywords:
            remaining = batch_size - len(keywords)
            additional = random.sample(self.multilingual_keywords, min(remaining, len(self.multilingual_keywords)))
            keywords.extend([k for k in additional if k not in keywords])
        
        return keywords[:batch_size]


# ============================================================================
# INTEGRATION INSTRUCTIONS
# ============================================================================

"""
TO INTEGRATE MULTILINGUAL SUPPORT INTO YOUR EXISTING SCANNER:

1. Add this mixin to your CompleteEnhancedScanner class:

class CompleteEnhancedScanner(MultilingualScannerMixin):
    def __init__(self):
        # ... your existing init code ...
        
        # Add multilingual support
        self.load_multilingual_keywords()

2. Replace get_next_keyword_batch() calls with get_multilingual_keyword_batch():

# OLD:
keyword_batch = self.get_next_keyword_batch()

# NEW:
keyword_batch = self.get_multilingual_keyword_batch()

3. For geographic targeting, use targeted language batches:

# Target Latin America
spanish_batch = self.get_targeted_language_batch(['es', 'pt'])

# Target Asia
asian_batch = self.get_targeted_language_batch(['zh', 'vi', 'th', 'id'])

# Target Europe  
european_batch = self.get_targeted_language_batch(['fr', 'de', 'it'])

4. Update your scanning loop logging:

logging.info(f"🌍 Scanning {platform} with multilingual batch: {len(keyword_batch)} keywords")

"""

# Example integration for complete_enhanced_scanner.py
def example_integration():
    """
    Example of how to modify your existing scanner
    """
    
    integration_example = '''
# Add to the top of complete_enhanced_scanner.py:
from multilingual_integration import MultilingualScannerMixin

# Modify your class definition:
class CompleteEnhancedScanner(MultilingualScannerMixin):
    def __init__(self):
        # ... existing init code ...
        
        # Add multilingual support
        multilingual_loaded = self.load_multilingual_keywords()
        if multilingual_loaded:
            logging.info("🌍 Multilingual scanning ENABLED")
        else:
            logging.info("📚 Using English-only keywords")

    # Update your scanning method:
    async def run_continuous_scanner(self):
        # ... existing code ...
        
        while True:
            # ... existing code ...
            
            # CHANGE THIS LINE:
            # keyword_batch = self.get_next_keyword_batch()
            
            # TO THIS:
            keyword_batch = self.get_multilingual_keyword_batch()
            
            logging.info(f"🌍 Scanning {platform} with multilingual keywords: {len(keyword_batch)}")
            
            # ... rest of existing code ...
    '''
    
    return integration_example

if __name__ == "__main__":
    print("🌍 WildGuard AI - Multilingual Scanner Integration")
    print("=" * 60)
    print("This file contains the multilingual integration code.")
    print("Follow the integration instructions above to add")
    print("multilingual support to your existing scanner.")
    print("\nSteps:")
    print("1. Run: python expand_multilingual_keywords.py")
    print("2. Copy the integration code into complete_enhanced_scanner.py")
    print("3. Your scanner will now use 15+ languages automatically!")
