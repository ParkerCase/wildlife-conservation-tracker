#!/usr/bin/env python3
"""
Apply the fixes discovered in diagnostics to the actual scanner files
"""

def update_craigslist_scanner():
    """Update CraigslistScanner with working selectors"""
    scanner_file = '/Users/parkercase/conservation-bot/src/monitoring/platform_scanner.py'
    
    with open(scanner_file, 'r') as f:
        content = f.read()
    
    # Update the selectors to use current working ones
    old_selectors = '''    SELECTORS = {
        "listings": ".result-row",
        "title": ".result-title",
        "price": ".result-price",
        "location": ".result-hood",
        "date": ".result-date",
        "image": ".result-image img",
        "url": ".result-title",
    }'''
    
    new_selectors = '''    SELECTORS = {
        "listings": ".cl-search-result",  # Updated for current Craigslist
        "title": "a.cl-app-anchor",       # Working selector found in diagnostics
        "price": ".priceinfo",
        "location": ".location",
        "date": ".result-date",
        "image": ".result-image img",
        "url": "a.cl-app-anchor",
    }'''
    
    content = content.replace(old_selectors, new_selectors)
    
    with open(scanner_file, 'w') as f:
        f.write(content)
    
    print("✅ Updated CraigslistScanner selectors")

def update_aliexpress_scanner():
    """Update AliExpressScanner with working selectors"""
    scanner_file = '/Users/parkercase/conservation-bot/src/monitoring/international_platforms.py'
    
    with open(scanner_file, 'r') as f:
        content = f.read()
    
    # Update the search URL to the one that works
    old_url = 'self.search_url = "https://www.aliexpress.com/wholesale"'
    new_url = 'self.search_url = "https://www.aliexpress.us/w/wholesale"'
    
    content = content.replace(old_url, new_url)
    
    # Update the product selector
    old_selector = 'div[data-product-id]'
    new_selector = '.search-item-card-wrapper-gallery'
    
    content = content.replace(old_selector, new_selector)
    
    with open(scanner_file, 'w') as f:
        f.write(content)
    
    print("✅ Updated AliExpressScanner URL and selectors")

def main():
    print("🔧 APPLYING PLATFORM FIXES...")
    print("=" * 40)
    
    update_craigslist_scanner()
    update_aliexpress_scanner()
    
    print()
    print("✅ All fixes applied successfully!")
    print("   - Craigslist: Updated to .cl-search-result + a.cl-app-anchor")
    print("   - AliExpress: Updated to .search-item-card-wrapper-gallery")

if __name__ == "__main__":
    main()
