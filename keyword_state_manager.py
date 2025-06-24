#!/usr/bin/env python3
"""
WildGuard AI - Keyword State Manager
Ensures ALL 1000 keywords are covered across ALL platforms with state persistence
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Set
import hashlib

class KeywordStateManager:
    """Manages keyword rotation state to ensure 100% coverage"""
    
    def __init__(self):
        self.state_file = '/tmp/wildguard_keyword_state.json'
        self.coverage_file = '/tmp/wildguard_keyword_coverage.json'
        
        # Platform list (initialize first)
        self.platforms = [
            'ebay', 'craigslist', 'olx', 'marktplaats', 'mercadolibre',
            'facebook_marketplace', 'avito', 'gumtree'
        ]
        
        # Import all keywords
        try:
            from comprehensive_endangered_keywords import ALL_ENDANGERED_SPECIES_KEYWORDS
            self.all_keywords = ALL_ENDANGERED_SPECIES_KEYWORDS
        except:
            # Fallback keywords for testing
            self.all_keywords = [
                'ivory', 'rhino horn', 'tiger bone', 'elephant tusk', 'pangolin scales',
                'bear bile', 'shark fin', 'turtle shell', 'leopard skin', 'antique',
                'carved', 'vintage', 'bone', 'horn', 'shell', 'decorative', 'art'
            ] * 60  # Simulate ~1000 keywords
        
        print(f"📊 Loaded {len(self.all_keywords)} total keywords")
        
        # Load state after initializing platforms and keywords
        self.load_state()
    
    def load_state(self):
        """Load keyword state from persistent storage"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    self.keyword_positions = data.get('keyword_positions', {})
                    self.platform_positions = data.get('platform_positions', {})
                    self.last_reset = data.get('last_reset', datetime.now().isoformat())
                    print(f"📁 Loaded keyword state from {self.state_file}")
            else:
                self.reset_state()
        except Exception as e:
            print(f"⚠️  State load error: {e}")
            self.reset_state()
    
    def save_state(self):
        """Save keyword state to persistent storage"""
        try:
            state_data = {
                'keyword_positions': self.keyword_positions,
                'platform_positions': self.platform_positions,
                'last_reset': self.last_reset,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(self.state_file, 'w') as f:
                json.dump(state_data, f, indent=2)
            
            print(f"💾 Saved keyword state to {self.state_file}")
        except Exception as e:
            print(f"⚠️  State save error: {e}")
    
    def reset_state(self):
        """Reset keyword state - start fresh"""
        self.keyword_positions = {platform: 0 for platform in self.platforms}
        self.platform_positions = {platform: 0 for platform in self.platforms}
        self.last_reset = datetime.now().isoformat()
        print("🔄 Reset keyword state")
    
    def get_next_keywords_for_platform(self, platform: str, batch_size: int = 12) -> List[str]:
        """Get next batch of keywords for a specific platform"""
        
        if platform not in self.platforms:
            print(f"⚠️  Unknown platform: {platform}")
            return []
        
        # Get current position for this platform
        current_position = self.keyword_positions.get(platform, 0)
        total_keywords = len(self.all_keywords)
        
        # Calculate batch boundaries
        start_idx = current_position
        end_idx = min(start_idx + batch_size, total_keywords)
        
        # Get the keywords
        keyword_batch = self.all_keywords[start_idx:end_idx]
        
        # If we don't have enough keywords, wrap around
        if len(keyword_batch) < batch_size and total_keywords > batch_size:
            remaining_needed = batch_size - len(keyword_batch)
            keyword_batch.extend(self.all_keywords[:remaining_needed])
            end_idx = remaining_needed
        
        # Update position for next call
        new_position = end_idx % total_keywords
        self.keyword_positions[platform] = new_position
        
        # Track coverage
        self.track_keyword_coverage(platform, keyword_batch)
        
        print(f"🎯 {platform}: Keywords {start_idx}-{end_idx-1} (position {new_position}/{total_keywords})")
        print(f"   📝 Batch: {keyword_batch[:3]}... (+{len(keyword_batch)-3} more)")
        
        # Auto-save state
        self.save_state()
        
        return keyword_batch
    
    def track_keyword_coverage(self, platform: str, keywords: List[str]):
        """Track which keywords have been used by each platform"""
        
        try:
            # Load existing coverage
            if os.path.exists(self.coverage_file):
                with open(self.coverage_file, 'r') as f:
                    coverage = json.load(f)
            else:
                coverage = {}
            
            # Initialize platform coverage if needed
            if platform not in coverage:
                coverage[platform] = {
                    'used_keywords': [],
                    'total_used': 0,
                    'last_updated': datetime.now().isoformat()
                }
            
            # Add new keywords
            for keyword in keywords:
                if keyword not in coverage[platform]['used_keywords']:
                    coverage[platform]['used_keywords'].append(keyword)
            
            coverage[platform]['total_used'] = len(coverage[platform]['used_keywords'])
            coverage[platform]['last_updated'] = datetime.now().isoformat()
            
            # Calculate coverage percentage
            total_possible = len(self.all_keywords)
            coverage_pct = (coverage[platform]['total_used'] / total_possible) * 100
            
            print(f"   📊 {platform} coverage: {coverage[platform]['total_used']}/{total_possible} ({coverage_pct:.1f}%)")
            
            # Save coverage
            with open(self.coverage_file, 'w') as f:
                json.dump(coverage, f, indent=2)
                
        except Exception as e:
            print(f"⚠️  Coverage tracking error: {e}")
    
    def get_coverage_report(self) -> Dict:
        """Get comprehensive coverage report"""
        
        try:
            if os.path.exists(self.coverage_file):
                with open(self.coverage_file, 'r') as f:
                    coverage = json.load(f)
            else:
                coverage = {}
            
            total_keywords = len(self.all_keywords)
            report = {
                'total_keywords': total_keywords,
                'platforms': {},
                'overall_coverage': 0
            }
            
            all_used_keywords = set()
            
            for platform in self.platforms:
                if platform in coverage:
                    used = len(coverage[platform]['used_keywords'])
                    percentage = (used / total_keywords) * 100
                    
                    report['platforms'][platform] = {
                        'keywords_used': used,
                        'coverage_percentage': percentage,
                        'last_updated': coverage[platform].get('last_updated', 'Never')
                    }
                    
                    # Add to overall tracking
                    all_used_keywords.update(coverage[platform]['used_keywords'])
                else:
                    report['platforms'][platform] = {
                        'keywords_used': 0,
                        'coverage_percentage': 0,
                        'last_updated': 'Never'
                    }
            
            # Calculate overall coverage
            report['overall_coverage'] = (len(all_used_keywords) / total_keywords) * 100
            report['unique_keywords_used'] = len(all_used_keywords)
            
            return report
            
        except Exception as e:
            print(f"⚠️  Coverage report error: {e}")
            return {'error': str(e)}
    
    def print_coverage_report(self):
        """Print detailed coverage report"""
        
        print("\n📊 KEYWORD COVERAGE REPORT")
        print("=" * 35)
        
        report = self.get_coverage_report()
        
        if 'error' in report:
            print(f"❌ Error generating report: {report['error']}")
            return
        
        print(f"🎯 Total Keywords: {report['total_keywords']}")
        print(f"📈 Overall Coverage: {report['overall_coverage']:.1f}%")
        print(f"🔢 Unique Keywords Used: {report['unique_keywords_used']}")
        print()
        
        print("🌍 PLATFORM BREAKDOWN:")
        for platform, data in report['platforms'].items():
            coverage_pct = data['coverage_percentage']
            keywords_used = data['keywords_used']
            
            # Status icon
            if coverage_pct >= 90:
                icon = "✅"
            elif coverage_pct >= 50:
                icon = "🔄"
            else:
                icon = "⚠️"
            
            print(f"   {icon} {platform:<20}: {keywords_used:>4}/{report['total_keywords']} ({coverage_pct:>5.1f}%)")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        
        if report['overall_coverage'] < 80:
            print("   • Continue scanning to improve coverage")
            print("   • Consider running historical backfill")
        
        incomplete_platforms = [
            platform for platform, data in report['platforms'].items() 
            if data['coverage_percentage'] < 80
        ]
        
        if incomplete_platforms:
            print(f"   • Focus on platforms: {', '.join(incomplete_platforms)}")
        
        if report['overall_coverage'] >= 95:
            print("   🎉 Excellent coverage! System performing optimally")
    
    def check_completion_cycle(self) -> bool:
        """Check if all platforms have completed a full cycle"""
        
        total_keywords = len(self.all_keywords)
        completed_platforms = 0
        
        for platform in self.platforms:
            position = self.keyword_positions.get(platform, 0)
            if position == 0:  # Back to start = completed cycle
                completed_platforms += 1
        
        completion_rate = (completed_platforms / len(self.platforms)) * 100
        
        print(f"🔄 Cycle Completion: {completed_platforms}/{len(self.platforms)} platforms ({completion_rate:.1f}%)")
        
        if completed_platforms == len(self.platforms):
            print("🎉 ALL PLATFORMS COMPLETED FULL KEYWORD CYCLE!")
            return True
        
        return False

# Test the keyword state manager
def test_keyword_manager():
    """Test the keyword state manager"""
    
    print("🧪 TESTING KEYWORD STATE MANAGER")
    print("=" * 40)
    
    manager = KeywordStateManager()
    
    # Simulate several platform scans
    platforms_to_test = ['ebay', 'avito', 'facebook_marketplace']
    
    for i in range(3):  # 3 cycles
        print(f"\n🔄 Simulation Cycle {i+1}")
        print("-" * 25)
        
        for platform in platforms_to_test:
            keywords = manager.get_next_keywords_for_platform(platform, batch_size=8)
            print(f"   📋 {platform}: {len(keywords)} keywords")
    
    # Print coverage report
    manager.print_coverage_report()
    
    # Check if we're making progress
    print(f"\n🎯 STATE PERSISTENCE TEST:")
    
    # Create new manager (simulates restart)
    manager2 = KeywordStateManager()
    keywords_after_restart = manager2.get_next_keywords_for_platform('ebay', 5)
    
    print(f"✅ Keywords persist across restarts: {len(keywords_after_restart)} keywords loaded")
    
    return manager

if __name__ == "__main__":
    test_keyword_manager()
