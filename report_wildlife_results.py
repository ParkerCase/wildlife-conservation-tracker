#!/usr/bin/env python3
"""
Report wildlife scan results from JSON file
"""

import json
import sys


def report_results():
    try:
        with open("fixed_wildlife_scan_results.json", "r") as f:
            results = json.load(f)

        print(f'   🔧 SCAN TYPE: FIXED {results.get("scan_type", "unknown").upper()}')
        print(f'   📈 TOTAL SCANNED: {results.get("total_scanned", 0):,}')
        print(f'   💾 TOTAL STORED: {results.get("total_stored", 0):,}')
        print(f'   🌍 PLATFORMS: {len(results.get("platforms_scanned", []))}')
        print(
            f'   🔑 KEYWORDS: {results.get("keywords_used", 0)} (from 1,452 available)'
        )
        print(f'   ⚡ RATE: {results.get("listings_per_minute", 0):,} listings/minute')
        print(
            f'   🧠 INTELLIGENT SCORING: {"YES" if results.get("intelligent_scoring_enabled") else "NO"}'
        )
        print(f'   🎯 HIGH THREAT ITEMS: {results.get("high_threat_items", 0):,}')
        print(f'   🚨 CRITICAL ALERTS: {results.get("critical_alerts", 0):,}')
        print(f'   👁️  HUMAN REVIEW: {results.get("human_review_required", 0):,}')

        quality_metrics = results.get("quality_metrics", {})
        if quality_metrics:
            print(f'   📈 QUALITY SCORE: {quality_metrics.get("quality_score", 0):.2%}')

        # Calculate daily projection
        daily_projection = (
            results.get("total_scanned", 0) * 6
        )  # 6 runs per day (every 4 hours)
        print(f"   📅 DAILY PROJECTION: {daily_projection:,} listings")

        if daily_projection >= 50000:
            print(
                f"   ✅ WILDLIFE TARGET: On track for 50,000+ daily wildlife listings!"
            )
        else:
            print(f"   ⚠️  WILDLIFE TARGET: Below 50,000 daily target")

    except FileNotFoundError:
        print("❌ No FIXED results file found")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading results: {e}")
        sys.exit(1)


if __name__ == "__main__":
    report_results()
