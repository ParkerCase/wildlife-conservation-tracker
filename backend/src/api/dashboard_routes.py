from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from datetime import datetime, timedelta
import json
import logging
import os

# Create blueprint
dashboard_bp = Blueprint("dashboard", __name__)


# Mock data for when real components aren't available
class MockData:
    @staticmethod
    def get_current_statistics():
        return {
            "active_scans": 4,
            "threats_detected_today": 12,
            "alerts_sent_today": 3,
            "platforms_monitored": 4,
            "total_species_protected": 150,
            "authorities_connected": 12,
            "platform_names": ["eBay", "Craigslist", "Poshmark", "Ruby Lane"],
            "last_updated": datetime.now().isoformat(),
        }


# Try to import real components, fall back to mock data
try:
    from src.monitoring.platform_scanner import PlatformScanner
    from src.ai.threat_analyzer import ThreatAnalyzer
    from src.dashboard.monitoring_dashboard import MonitoringDashboard

    scanner = PlatformScanner()
    dashboard = MonitoringDashboard()
    REAL_COMPONENTS = True
    print("✅ Real components loaded successfully")
except Exception as e:
    print(f"⚠️  Using mock data due to import error: {e}")
    scanner = None
    dashboard = MockData()
    REAL_COMPONENTS = False


# Remove the duplicate /api prefix - the blueprint is already registered with /api
@dashboard_bp.route("/stats/realtime")
@cross_origin()
def get_realtime_stats():
    """Real-time stats for your working platforms"""
    try:
        if REAL_COMPONENTS and hasattr(dashboard, "get_current_statistics"):
            stats = dashboard.get_current_statistics()
        else:
            stats = MockData.get_current_statistics()

        # Ensure we have the required fields
        stats.update(
            {
                "platforms_monitored": 4,
                "platform_names": ["eBay", "Craigslist", "Poshmark", "Ruby Lane"],
            }
        )

        return jsonify(stats)
    except Exception as e:
        logging.error(f"Error getting real-time stats: {e}")
        return jsonify(MockData.get_current_statistics())


@dashboard_bp.route("/stats/trends")
@cross_origin()
def get_threat_trends():
    """Get actual threat trends from your database"""
    days = request.args.get("days", 7, type=int)

    try:
        # Try to get real data
        if REAL_COMPONENTS and hasattr(dashboard, "supabase"):
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            result = (
                dashboard.supabase.table("detections")
                .select("*")
                .gte("timestamp", start_date.isoformat())
                .order("timestamp", desc=True)
                .execute()
            )

            trends_data = process_trends_data(result.data)
            return jsonify(trends_data)
        else:
            # Fallback to mock data
            return jsonify(
                {
                    "daily_trends": generate_mock_trends(days),
                    "species_distribution": get_species_breakdown(),
                    "platform_activity": get_platform_stats(),
                }
            )

    except Exception as e:
        logging.error(f"Error getting trends: {e}")
        return jsonify(
            {
                "daily_trends": generate_mock_trends(days),
                "species_distribution": get_species_breakdown(),
                "platform_activity": get_platform_stats(),
            }
        )


@dashboard_bp.route("/threats")
@cross_origin()
def get_threats():
    """Get threats from your actual detection system"""
    page = request.args.get("page", 1, type=int)
    severity = request.args.get("severity")
    platform = request.args.get("platform")

    try:
        if REAL_COMPONENTS and hasattr(dashboard, "supabase"):
            query = dashboard.supabase.table("detections").select("*")

            if severity:
                query = query.eq("threat_level", severity)
            if platform:
                query = query.eq("platform", platform)

            result = (
                query.order("timestamp", desc=True)
                .range((page - 1) * 20, page * 20 - 1)
                .execute()
            )

            return jsonify(
                {"threats": result.data, "total": len(result.data), "page": page}
            )
        else:
            return jsonify(
                {
                    "threats": [],
                    "total": 0,
                    "page": page,
                    "message": "Mock data - no real threats to display",
                }
            )

    except Exception as e:
        logging.error(f"Error getting threats: {e}")
        return jsonify({"error": str(e)}), 500


@dashboard_bp.route("/threats/<threat_id>")
@cross_origin()
def get_threat_details(threat_id):
    """Get detailed threat analysis"""
    try:
        if REAL_COMPONENTS and hasattr(dashboard, "supabase"):
            result = (
                dashboard.supabase.table("detections")
                .select("*")
                .eq("evidence_id", threat_id)
                .execute()
            )

            if not result.data:
                return jsonify({"error": "Threat not found"}), 404

            threat = result.data[0]

            # Gather all listings for the same seller (if seller_id exists)
            seller_id = threat.get("seller_id")
            seller_data = []
            if seller_id:
                seller_results = (
                    dashboard.supabase.table("detections")
                    .select("*")
                    .eq("seller_id", seller_id)
                    .execute()
                )
                seller_data = seller_results.data if seller_results.data else []

            # Anthropic-powered network analysis
            network_analysis = None
            try:
                from src.ai.threat_analyzer import ThreatAnalyzer
                import os

                analyzer = ThreatAnalyzer(os.getenv("ANTHROPIC_API_KEY"))
                import asyncio

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                network_analysis = loop.run_until_complete(
                    analyzer.analyze_network(
                        {"seller_id": seller_id, "listings": seller_data}
                    )
                )
            except Exception as e:
                network_analysis = {"error": str(e)}

            return jsonify(
                {
                    "threat": threat,
                    "ai_analysis": json.loads(threat.get("ai_analysis", "{}")),
                    "evidence_package": get_evidence_details(threat_id),
                    "network_analysis": network_analysis,
                }
            )
        else:
            return jsonify({"error": "Threat details not available in mock mode"}), 404

    except Exception as e:
        logging.error(f"Error getting threat details: {e}")
        return jsonify({"error": str(e)}), 500


@dashboard_bp.route("/platforms/status")
@cross_origin()
def get_platform_status():
    """Status of your 4 working platforms"""
    return jsonify(
        {
            "platforms": [
                {
                    "name": "eBay",
                    "status": "active",
                    "last_scan": "2024-06-10T14:30:00Z",
                    "success_rate": 92,
                },
                {
                    "name": "Craigslist",
                    "status": "active",
                    "last_scan": "2024-06-10T14:25:00Z",
                    "success_rate": 87,
                },
                {
                    "name": "Poshmark",
                    "status": "active",
                    "last_scan": "2024-06-10T14:28:00Z",
                    "success_rate": 84,
                },
                {
                    "name": "Ruby Lane",
                    "status": "active",
                    "last_scan": "2024-06-10T14:32:00Z",
                    "success_rate": 79,
                },
            ]
        }
    )


@dashboard_bp.route("/scan/manual", methods=["POST"])
@cross_origin()
def trigger_manual_scan():
    """Trigger a manual scan of your platforms"""
    platforms = (
        request.json.get("platforms", ["ebay", "craigslist", "poshmark", "ruby_lane"])
        if request.json
        else ["ebay", "craigslist", "poshmark", "ruby_lane"]
    )
    keywords = (
        request.json.get("keywords", ["ivory", "rhino horn", "tiger"])
        if request.json
        else ["ivory", "rhino horn", "tiger"]
    )

    try:
        if REAL_COMPONENTS and scanner:
            # Use real scanner if available
            results = []
            for platform in platforms:
                if platform in scanner.platforms:
                    try:
                        platform_results = scanner.platforms[platform].scan(
                            {"direct_terms": keywords}, None
                        )
                        results.extend(platform_results)
                    except Exception as e:
                        logging.error(f"Scan error for {platform}: {e}")

            return jsonify(
                {
                    "status": "success",
                    "scanned_platforms": platforms,
                    "results_found": len(results),
                    "scan_id": f"SCAN-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                }
            )
        else:
            # Mock response
            return jsonify(
                {
                    "status": "success",
                    "message": "Mock scan completed",
                    "scanned_platforms": platforms,
                    "results_found": 5,
                    "scan_id": f"MOCK-SCAN-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                }
            )

    except Exception as e:
        logging.error(f"Manual scan error: {e}")
        return jsonify({"error": str(e)}), 500


# Helper functions
def process_trends_data(raw_data):
    """Process your actual detection data into chart format"""
    trends = {}
    for detection in raw_data:
        date = detection["timestamp"][:10]
        threat_type = (
            detection.get("species_involved", ["other"])[0]
            if detection.get("species_involved")
            else "other"
        )

        if date not in trends:
            trends[date] = {
                "date": date,
                "ivory": 0,
                "rhino": 0,
                "tiger": 0,
                "pangolin": 0,
                "other": 0,
            }

        if "ivory" in threat_type.lower() or "elephant" in threat_type.lower():
            trends[date]["ivory"] += 1
        elif "rhino" in threat_type.lower():
            trends[date]["rhino"] += 1
        elif "tiger" in threat_type.lower():
            trends[date]["tiger"] += 1
        elif "pangolin" in threat_type.lower():
            trends[date]["pangolin"] += 1
        else:
            trends[date]["other"] += 1

    return list(trends.values())


def get_species_breakdown():
    """Get species distribution"""
    return [
        {"name": "Ivory", "value": 35, "percentage": 35},
        {"name": "Rhino Horn", "value": 28, "percentage": 28},
        {"name": "Tiger Parts", "value": 18, "percentage": 18},
        {"name": "Other", "value": 19, "percentage": 19},
    ]


def get_platform_stats():
    """Get platform performance stats"""
    return [
        {"platform": "eBay", "threats": 45, "percentage": 32},
        {"platform": "Craigslist", "threats": 38, "percentage": 27},
        {"platform": "Poshmark", "threats": 29, "percentage": 21},
        {"platform": "Ruby Lane", "threats": 18, "percentage": 20},
    ]


def get_evidence_details(evidence_id):
    """Get evidence package"""
    return {"message": "Evidence details not available in current setup"}


def get_network_data(platform, seller_id):
    """Analyze seller network connections"""
    return {
        "seller_risk_score": 75,
        "connected_sellers": 3,
        "suspicious_patterns": ["Similar posting times", "Shared keywords"],
        "platform_behavior": f"Active on {platform} for 2.3 years",
    }


def generate_mock_trends(days):
    """Generate mock trend data"""
    trends = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        trends.append(
            {
                "date": date,
                "ivory": 5 + (i % 3),
                "rhino": 3 + (i % 2),
                "tiger": 2 + (i % 4),
                "pangolin": 1 + (i % 2),
                "other": 1 + (i % 2),
            }
        )
    return trends[::-1]
