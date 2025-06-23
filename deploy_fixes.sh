#!/bin/bash

# Deploy Conservation Bot Fixes to GitHub
# This script commits and pushes the targeted fixes requested

echo "🚀 Deploying Conservation Bot targeted fixes..."

# Add all changes
git add .

# Commit with descriptive message
git commit -m "Fix: Targeted corrections for dashboard accuracy

✅ Fixed keyword count calculation (now shows 1000+ instead of 591)
✅ Fixed scan frequency display (now shows 'Continuous 24/7' instead of '15min')
✅ Added proper timestamp filtering for date ranges
✅ Enhanced threat analytics with non-null URL filtering
✅ Added pagination to Evidence Archive (50 items per page)
✅ Updated Intelligence Reports operational section
✅ Improved data accuracy across all components

All changes maintain existing functionality while fixing the specific issues identified."

# Push to main branch
git push origin main

echo "✅ All targeted fixes have been deployed to GitHub!"
echo ""
echo "📋 Summary of fixes applied:"
echo "  • Keyword count now calculates correctly (1000+ total)"
echo "  • Scan frequency shows 'Continuous 24/7' instead of incorrect '15min'"
echo "  • Threat details only load records with non-null listing_url"
echo "  • Evidence archive includes pagination for better performance"
echo "  • Date filters use proper timestamp column filtering"
echo "  • All data displays are now accurate and live with Supabase"
echo ""
echo "🎯 All requested issues have been resolved with minimal, targeted changes."
