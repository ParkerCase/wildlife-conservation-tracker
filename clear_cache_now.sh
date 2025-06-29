#!/bin/bash
# IMMEDIATE CACHE CLEARING SCRIPT

echo "🔥 CLEARING PYTHON CACHE IMMEDIATELY"
echo "======================================"

# Remove the specific problematic cache directory
echo "🗑️  Removing __pycache__ directory..."
rm -rf /Users/parkercase/conservation-bot/__pycache__

# Remove any other cache files
find /Users/parkercase/conservation-bot -name "*.pyc" -delete
find /Users/parkercase/conservation-bot -name "__pycache__" -type d -exec rm -rf {} +

echo "✅ Python cache cleared!"

# Verify the files exist and are fixed
echo ""
echo "🔍 VERIFYING FIXED FILES:"

if grep -q "self.ua = UserAgent()  # FIXED: Added missing ua attribute" /Users/parkercase/conservation-bot/enhanced_platform_scanner.py; then
    echo "✅ enhanced_platform_scanner.py has ua fixes"
else
    echo "❌ enhanced_platform_scanner.py missing ua fixes"
fi

if grep -q "FIXED CONTINUOUS REAL WILDLIFE SCANNER" /Users/parkercase/conservation-bot/continuous_real_wildlife_scanner.py; then
    echo "✅ continuous_real_wildlife_scanner.py is fixed version"
else
    echo "❌ continuous_real_wildlife_scanner.py not fixed version"
fi

if grep -q "FIXED CONTINUOUS REAL HUMAN TRAFFICKING SCANNER" /Users/parkercase/conservation-bot/continuous_real_ht_scanner.py; then
    echo "✅ continuous_real_ht_scanner.py is fixed version"
else
    echo "❌ continuous_real_ht_scanner.py not fixed version"
fi

echo ""
echo "🚀 CACHE CLEARED - NEXT GITHUB ACTIONS RUN SHOULD WORK!"
echo "======================================"
