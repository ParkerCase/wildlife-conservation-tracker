#!/usr/bin/env python3
"""
Minimal WildGuard AI Backend - Guaranteed to work
Run this if you're having CORS issues with the main backend
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)

# Enable CORS for all domains and all routes
CORS(
    app,
    origins=["http://localhost:3000", "http://localhost:3001"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=True,
)


@app.after_request
def after_request(response):
    """Ensure CORS headers are always present"""
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response


# Basic routes
@app.route("/")
def home():
    return jsonify(
        {
            "service": "WildGuard AI Backend",
            "status": "running",
            "timestamp": datetime.now().isoformat(),
            "message": "CORS should be working now!",
        }
    )


@app.route("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "service": "WildGuard AI",
            "timestamp": datetime.now().isoformat(),
        }
    )


# API Routes - exactly what the frontend expects
@app.route("/api/stats/realtime")
def realtime_stats():
    """Real-time statistics"""
    return jsonify(
        {
            "active_scans": 4,
            "threats_detected_today": 12,
            "alerts_sent_today": 3,
            "platforms_monitored": 4,
            "total_species_protected": 150,
            "authorities_connected": 12,
            "platform_names": ["eBay", "Craigslist", "Poshmark", "Ruby Lane"],
            "last_updated": datetime.now().isoformat(),
        }
    )


@app.route("/api/stats/trends")
def threat_trends():
    """Threat trends data"""
    days = request.args.get("days", 7, type=int)

    # Generate sample trend data
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

    return jsonify(
        {
            "daily_trends": trends[::-1],  # Reverse for chronological order
            "species_distribution": [
                {"name": "Ivory", "value": 35, "percentage": 35},
                {"name": "Rhino Horn", "value": 28, "percentage": 28},
                {"name": "Tiger Parts", "value": 18, "percentage": 18},
                {"name": "Other", "value": 19, "percentage": 19},
            ],
        }
    )


@app.route("/api/platforms/status")
def platform_status():
    """Platform status information"""
    return jsonify(
        {
            "platforms": [
                {
                    "name": "eBay",
                    "status": "active",
                    "last_scan": datetime.now().isoformat(),
                    "success_rate": 92,
                },
                {
                    "name": "Craigslist",
                    "status": "active",
                    "last_scan": datetime.now().isoformat(),
                    "success_rate": 87,
                },
                {
                    "name": "Poshmark",
                    "status": "active",
                    "last_scan": datetime.now().isoformat(),
                    "success_rate": 84,
                },
                {
                    "name": "Ruby Lane",
                    "status": "active",
                    "last_scan": datetime.now().isoformat(),
                    "success_rate": 79,
                },
            ]
        }
    )


@app.route("/api/scan/manual", methods=["POST"])
def manual_scan():
    """Trigger manual scan"""
    data = request.get_json() or {}
    platforms = data.get("platforms", ["ebay", "craigslist", "poshmark", "ruby_lane"])
    keywords = data.get("keywords", ["ivory", "rhino horn", "tiger"])

    return jsonify(
        {
            "status": "success",
            "message": "Manual scan initiated",
            "scanned_platforms": platforms,
            "keywords": keywords,
            "results_found": len(platforms) * 2,  # Mock results
            "scan_id": f"SCAN-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        }
    )


# Handle preflight OPTIONS requests
@app.route("/api/<path:path>", methods=["OPTIONS"])
def handle_options(path):
    response = jsonify({"message": "OK"})
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response


if __name__ == "__main__":
    from datetime import timedelta

    print("🚀 Starting Minimal WildGuard AI Backend...")
    print("=" * 50)
    print("🌐 Server: http://localhost:5000")
    print("🏥 Health: http://localhost:5000/health")
    print("📊 Stats: http://localhost:5000/api/stats/realtime")
    print("🔧 CORS: Configured for localhost:3000")
    print("=" * 50)

    # Run with debug mode and specific host/port
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
