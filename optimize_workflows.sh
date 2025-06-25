#!/bin/bash
# WildGuard AI - Optimize GitHub Actions Workflows
# This script disables problematic workflows and keeps only the optimal one

echo "🔧 OPTIMIZING WILDGUARD AI WORKFLOWS"
echo "===================================="

cd .github/workflows

echo "📋 Current workflows:"
ls -la *.yml

echo ""
echo "🚫 Disabling problematic workflows..."

# Disable Enhanced Production Scanner (has division by zero error + partial coverage)
if [ -f "enhanced-production-scanner.yml" ]; then
    mv enhanced-production-scanner.yml enhanced-production-scanner.yml.disabled
    echo "   ✅ Disabled: enhanced-production-scanner.yml"
fi

# Disable Gumtree/Avito Scanner (redundant)
if [ -f "gumtree-avito-scanner.yml" ]; then
    mv gumtree-avito-scanner.yml gumtree-avito-scanner.yml.disabled
    echo "   ✅ Disabled: gumtree-avito-scanner.yml"
fi

echo ""
echo "✅ ACTIVE WORKFLOWS (OPTIMAL SETUP):"
ls -la *.yml | grep -v disabled

echo ""
echo "🎯 RECOMMENDED WORKFLOW:"
echo "   • complete-enhanced-scanner.yml (7 platforms, every 3 hours)"
echo "   • Target: 120,000+ listings/day"
echo "   • Platforms: eBay, Craigslist, OLX, Marktplaats, MercadoLibre, Gumtree, Avito"

echo ""
echo "🚀 NEXT STEPS:"
echo "1. Commit these changes: git add . && git commit -m 'Optimize workflows'"
echo "2. Push to GitHub: git push origin main"
echo "3. Test: Go to GitHub Actions → Run 'WildGuard Complete Enhanced Scanner'"
echo "4. Monitor: Should show 120,000+ listings/day"

echo ""
echo "✅ OPTIMIZATION COMPLETE!"
