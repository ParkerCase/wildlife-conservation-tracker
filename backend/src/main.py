import asyncio
import logging
import argparse
from typing import Dict
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from src.monitoring.platform_scanner import PlatformScanner
from src.ai.threat_analyzer import ThreatAnalyzer
from src.evidence.evidence_archiver import EvidenceArchiver
from src.alerts.alert_system import AlertSystem
from src.dashboard.monitoring_dashboard import MonitoringDashboard
from src.utils.language_processor import LanguageProcessor
from src.api.dashboard_routes import dashboard_bp


logging.basicConfig(level=logging.INFO)

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

print("SUPABASE_URL:", os.getenv("SUPABASE_URL"))
print("SUPABASE_KEY:", os.getenv("SUPABASE_KEY"))

app = Flask(__name__)
CORS(app)
app.register_blueprint(dashboard_bp, url_prefix="/api")


class ConservationBot:
    def __init__(self, config: Dict):
        self.config = config
        self.scanner = PlatformScanner()
        self.analyzer = ThreatAnalyzer(config.get("anthropic_api_key", ""))
        self.archiver = EvidenceArchiver()
        self.alert_system = AlertSystem()
        self.dashboard = MonitoringDashboard()
        self.language_processor = LanguageProcessor()
        self.is_running = False
        self.scan_interval = config.get("scan_interval_minutes", 15)

    async def start_monitoring(self):
        logging.info("Stub: start_monitoring")

    async def _start_dashboard(self, port=None):
        import uvicorn

        port = port or int(os.getenv("DASHBOARD_PORT", 8000))
        config = uvicorn.Config(
            self.dashboard.app, host="0.0.0.0", port=port, log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()

    async def _run_scan_cycle(self):
        logging.info("Starting scan cycle...")
        # Scan all platforms
        async with self.scanner as scanner:
            raw_listings = await scanner.scan_all_platforms()
        logging.info(f"Scanned {len(raw_listings)} listings across all platforms")
        # Limit to 10 listings for initial test
        raw_listings = raw_listings[:10]
        # Process each listing
        for listing in raw_listings:
            try:
                # Multi-language processing
                language_analysis = (
                    await self.language_processor.process_multilanguage_text(
                        f"{listing.get('title', '')} {listing.get('description', '')}"
                    )
                )
                listing_with_language = {**listing, **language_analysis}
                # Image recognition (if images present)
                image_results = []
                images = listing.get("images") or []
                if isinstance(listing.get("image"), str):
                    images.append(listing["image"])  # Some scrapers use 'image'
                for img_url in images:
                    img_result = await self.analyzer.analyze_image(img_url)
                    image_results.append({"image_url": img_url, **img_result})
                # AI threat analysis
                threat_analysis = await self.analyzer.analyze_listing(
                    listing_with_language
                )
                threat_analysis["image_analysis"] = image_results
                # Print the actual results for demo
                print("\n=== LISTING ANALYSIS RESULT ===")
                print("Listing:", listing)
                print("Language Analysis:", language_analysis)
                print("Threat Analysis:", threat_analysis)
                # Only archive and log if threat_score >= 50
                if threat_analysis.get("threat_score", 0) >= 50:
                    evidence_result = await self.archiver.preserve_evidence(
                        listing_with_language, threat_analysis
                    )
                    await self.dashboard.log_detection(evidence_result, threat_analysis)
                    logging.info(
                        f"Threat detected: {threat_analysis.get('threat_score', 0)} on {listing.get('platform', 'unknown')} - Evidence ID: {evidence_result.get('evidence_id', 'unknown')}"
                    )
            except Exception as e:
                logging.error(f"Error processing listing: {e}")
        logging.info("Scan cycle complete.")


def load_config() -> Dict:
    return {
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
        "ebay_app_id": os.getenv("EBAY_APP_ID"),
        "ebay_dev_id": os.getenv("EBAY_DEV_ID"),
        "ebay_cert_id": os.getenv("EBAY_CERT_ID"),
        "aws_access_key": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "s3_bucket_name": os.getenv("S3_BUCKET_NAME", "wildlife-crime-evidence"),
        "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "email_user": os.getenv("EMAIL_USER"),
        "email_password": os.getenv("EMAIL_PASSWORD"),
        "scan_interval_minutes": int(os.getenv("SCAN_INTERVAL_MINUTES", "15")),
    }


async def main():
    parser = argparse.ArgumentParser(description="Wildlife Conservation Monitoring Bot")
    parser.add_argument(
        "--mode",
        choices=["monitor", "scan-once", "dashboard"],
        default="monitor",
        help="Operation mode",
    )
    parser.add_argument(
        "--dashboard-port",
        type=int,
        default=None,
        help="Port to run the dashboard on (overrides DASHBOARD_PORT env var)",
    )
    args = parser.parse_args()
    config = load_config()
    bot = ConservationBot(config)
    if args.mode == "monitor":
        await bot.start_monitoring()
    elif args.mode == "scan-once":
        await bot._run_scan_cycle()
    elif args.mode == "dashboard":
        await bot._start_dashboard(port=args.dashboard_port)

    if args.mode == "api":
        app.run(debug=True, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    asyncio.run(main())
