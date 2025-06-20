from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import json
from typing import Dict, List
from datetime import datetime, timedelta
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


class MonitoringDashboard:
    def __init__(self):
        self.app = FastAPI()
        self.active_connections: List[WebSocket] = []
        self.real_time_data = {
            "active_scans": 0,
            "threats_detected_today": 0,
            "alerts_sent_today": 0,
            "platforms_monitored": 4,
            "total_species_protected": 150,
            "authorities_connected": 12,
        }
        self.supabase: Client = create_client(
            os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY")
        )
        self.setup_routes()

    def setup_routes(self):
        @self.app.get("/")
        async def dashboard_home():
            return HTMLResponse("<h1>Dashboard Stub</h1>")

    def get_current_statistics(self) -> Dict:
        today = datetime.now().strftime("%Y-%m-%d")
        # Threats detected today
        threats_today = (
            self.supabase.table("detections")
            .select("*")
            .gte("timestamp", today + "T00:00:00")
            .lte("timestamp", today + "T23:59:59")
            .execute()
        )
        threats_count = len(threats_today.data) if threats_today.data else 0

        # Alerts sent today
        alerts_today = (
            self.supabase.table("detections")
            .select("*")
            .gte("timestamp", today + "T00:00:00")
            .lte("timestamp", today + "T23:59:59")
            .eq("alert_sent", True)
            .execute()
        )
        alerts_count = len(alerts_today.data) if alerts_today.data else 0

        # Platforms monitored (unique platforms in detections)
        platforms = set()
        if threats_today.data:
            for d in threats_today.data:
                if "platform" in d and d["platform"]:
                    platforms.add(d["platform"])
        platforms_monitored = len(platforms)

        # Total species protected (unique species in detections)
        species = set()
        if threats_today.data:
            for d in threats_today.data:
                if "species_involved" in d and d["species_involved"]:
                    try:
                        s = json.loads(d["species_involved"])
                        if isinstance(s, list):
                            species.update(s)
                        else:
                            species.add(s)
                    except Exception:
                        species.add(d["species_involved"])
        total_species_protected = len(species)

        # Authorities connected (if you have a table)
        try:
            authorities = self.supabase.table("authorities").select("*").execute()
            authorities_connected = len(authorities.data) if authorities.data else 0
        except Exception:
            authorities_connected = 0

        return {
            "active_scans": platforms_monitored,  # or another real metric
            "threats_detected_today": threats_count,
            "alerts_sent_today": alerts_count,
            "platforms_monitored": platforms_monitored,
            "total_species_protected": total_species_protected,
            "authorities_connected": authorities_connected,
            "last_updated": datetime.now().isoformat(),
            "platform_names": list(platforms),
        }

    def get_recent_detections(self, limit: int = 20) -> List[Dict]:
        result = (
            self.supabase.table("detections")
            .select("*")
            .order("timestamp", desc=True)
            .limit(limit)
            .execute()
        )
        return result.data if result.data else []

    async def log_detection(self, evidence_package: Dict, analysis: Dict) -> None:
        detection = {
            "evidence_id": evidence_package["evidence_id"],
            "timestamp": evidence_package["timestamp"],
            "platform": evidence_package["platform"],
            "threat_score": analysis.get("threat_score", 0),
            "threat_level": analysis.get("threat_level", "LOW"),
            "species_involved": json.dumps(analysis.get("species_involved", [])),
            "alert_sent": False,
            "status": "detected",
        }
        self.supabase.table("detections").insert(detection).execute()
        self.real_time_data["threats_detected_today"] += 1
        await self.broadcast_update({"type": "new_detection", "data": detection})
