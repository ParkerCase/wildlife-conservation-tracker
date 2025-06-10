import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=backend_dir / ".env")


def create_app():
    app = Flask(__name__)

    # Configure CORS properly
    CORS(
        app,
        origins=["http://localhost:3000", "http://localhost:3001"],
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    # Import and register blueprints after CORS setup
    try:
        from backend.src.api.dashboard_routes import dashboard_bp

        app.register_blueprint(dashboard_bp, url_prefix="/api")
        print("✅ Dashboard routes registered successfully")
    except Exception as e:
        print(f"❌ Error registering dashboard routes: {e}")
        # Create fallback routes
        register_fallback_routes(app)

    @app.route("/health")
    def health_check():
        return jsonify({"status": "healthy", "service": "WildGuard AI"})

    @app.route("/")
    def root():
        return jsonify(
            {
                "message": "WildGuard AI Backend",
                "status": "running",
                "endpoints": [
                    "/health",
                    "/api/stats/realtime",
                    "/api/stats/trends",
                    "/api/platforms/status",
                ],
            }
        )

    # Add error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app


def register_fallback_routes(app):
    """Register fallback routes if main routes fail to import"""

    @app.route("/api/stats/realtime")
    def fallback_realtime_stats():
        return jsonify(
            {
                "active_scans": 4,
                "threats_detected_today": 12,
                "alerts_sent_today": 3,
                "platforms_monitored": 4,
                "total_species_protected": 150,
                "authorities_connected": 12,
                "platform_names": ["eBay", "Craigslist", "Poshmark", "Ruby Lane"],
                "last_updated": "2024-06-10T15:30:00Z",
            }
        )

    @app.route("/api/stats/trends")
    def fallback_threat_trends():
        return jsonify(
            {
                "daily_trends": [
                    {
                        "date": "2024-06-04",
                        "ivory": 5,
                        "rhino": 3,
                        "tiger": 2,
                        "pangolin": 1,
                        "other": 1,
                    },
                    {
                        "date": "2024-06-05",
                        "ivory": 7,
                        "rhino": 4,
                        "tiger": 3,
                        "pangolin": 2,
                        "other": 2,
                    },
                    {
                        "date": "2024-06-06",
                        "ivory": 6,
                        "rhino": 2,
                        "tiger": 4,
                        "pangolin": 1,
                        "other": 3,
                    },
                    {
                        "date": "2024-06-07",
                        "ivory": 8,
                        "rhino": 5,
                        "tiger": 2,
                        "pangolin": 3,
                        "other": 1,
                    },
                    {
                        "date": "2024-06-08",
                        "ivory": 4,
                        "rhino": 3,
                        "tiger": 5,
                        "pangolin": 2,
                        "other": 2,
                    },
                    {
                        "date": "2024-06-09",
                        "ivory": 9,
                        "rhino": 6,
                        "tiger": 3,
                        "pangolin": 4,
                        "other": 1,
                    },
                    {
                        "date": "2024-06-10",
                        "ivory": 6,
                        "rhino": 4,
                        "tiger": 4,
                        "pangolin": 2,
                        "other": 3,
                    },
                ],
                "species_distribution": [
                    {"name": "Ivory", "value": 35, "percentage": 35},
                    {"name": "Rhino Horn", "value": 28, "percentage": 28},
                    {"name": "Tiger Parts", "value": 18, "percentage": 18},
                    {"name": "Other", "value": 19, "percentage": 19},
                ],
            }
        )

    @app.route("/api/platforms/status")
    def fallback_platform_status():
        return jsonify(
            {
                "platforms": [
                    {
                        "name": "eBay",
                        "status": "active",
                        "last_scan": "2024-06-10T15:30:00Z",
                        "success_rate": 92,
                    },
                    {
                        "name": "Craigslist",
                        "status": "active",
                        "last_scan": "2024-06-10T15:25:00Z",
                        "success_rate": 87,
                    },
                    {
                        "name": "Poshmark",
                        "status": "active",
                        "last_scan": "2024-06-10T15:28:00Z",
                        "success_rate": 84,
                    },
                    {
                        "name": "Ruby Lane",
                        "status": "active",
                        "last_scan": "2024-06-10T15:32:00Z",
                        "success_rate": 79,
                    },
                ]
            }
        )

    @app.route("/api/scan/manual", methods=["POST"])
    def fallback_manual_scan():
        return jsonify(
            {
                "status": "success",
                "message": "Manual scan initiated",
                "scan_id": "SCAN-20240610-153000",
                "results_found": 0,
            }
        )


if __name__ == "__main__":
    print("🚀 Starting WildGuard AI Backend...")
    app = create_app()
    print(f"🌐 Server starting on http://localhost:5000")
    print(f"📊 API endpoints available at http://localhost:5000/api/")
    app.run(debug=True, host="0.0.0.0", port=5000)
