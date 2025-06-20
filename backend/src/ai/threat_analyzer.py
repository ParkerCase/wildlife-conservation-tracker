import anthropic
import json
import logging
from typing import Dict, List, Any
import asyncio
from datetime import datetime
import httpx
import base64
import os


class ThreatAnalyzer:
    api_call_count = 0
    api_call_limit = 5  # Limit Anthropic API calls per run for cost control

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.threat_patterns = self._load_threat_patterns()

    async def analyze_listing(self, listing: Dict) -> Dict:
        if ThreatAnalyzer.api_call_count >= ThreatAnalyzer.api_call_limit:
            return {
                "threat_score": 0,
                "threat_level": "LOW",
                "confidence": 0,
                "reasoning": "API call limit reached",
            }
        prompt = f"""
        Analyze this marketplace listing for illegal wildlife trade indicators:
        Platform: {listing.get('platform', 'Unknown')}
        Title: {listing.get('title', '')}
        Description: {listing.get('description', '')}
        Price: {listing.get('price', '')}
        Location: {listing.get('location', '')}
        Search Term: {listing.get('search_term', '')}
        Images: {len(listing.get('images', [])) if 'images' in listing else 0} attached
        Respond in JSON format with threat_score, threat_level, confidence, reasoning.
        """
        try:
            ThreatAnalyzer.api_call_count += 1
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}],
            )
            analysis = json.loads(response.content[0].text)
            analysis["listing_id"] = listing.get("id", "")
            analysis["analysis_timestamp"] = datetime.utcnow().isoformat()
            return analysis
        except Exception as e:
            logging.error(f"AI analysis failed: {e}")
            return {
                "threat_score": 0,
                "threat_level": "LOW",
                "confidence": 0,
                "error": str(e),
            }

    async def analyze_network(self, seller_data: Dict) -> Dict:
        """
        Analyze a seller's activity for trafficking network patterns using Anthropic Claude 3.
        seller_data: Dict with all relevant listings and metadata for the seller.
        Returns: Dict with seller_risk_score, connected_sellers, suspicious_patterns, reasoning.
        """
        prompt = f"""
        Analyze the following seller's activity for signs of trafficking networks.
        Data: {json.dumps(seller_data, indent=2)}
        Respond in JSON with: seller_risk_score, connected_sellers, suspicious_patterns, reasoning.
        """
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}],
            )
            return json.loads(response.content[0].text)
        except Exception as e:
            logging.error(f"Network analysis failed: {e}")
            return {"error": str(e)}

    async def analyze_image(self, image_url: str) -> Dict:
        """
        Analyze an image for illegal wildlife parts using Anthropic Claude 3 Vision via HTTP API.
        Downloads the image, encodes as base64, and sends as a content item in the Claude 3 Vision API payload.
        Returns: Dict with contains_illegal_parts, part_type, confidence, reasoning.
        """
        import httpx
        import base64
        import os

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(image_url)
                if resp.status_code != 200:
                    return {"error": f"Failed to download image: {resp.status_code}"}
                image_bytes = resp.content
                image_b64 = base64.b64encode(image_bytes).decode("utf-8")

            anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
            if not anthropic_api_key:
                return {"error": "Anthropic API key not set in environment"}

            # Build Claude 3 Vision API payload
            payload = {
                "model": "claude-3-opus-20240229",
                "max_tokens": 1024,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_b64,
                                },
                            },
                            {
                                "type": "text",
                                "text": "Does this image contain illegal wildlife parts? If so, what kind? Respond in JSON with contains_illegal_parts (true/false), part_type, confidence (0-1), and reasoning.",
                            },
                        ],
                    }
                ],
            }

            headers = {
                "x-api-key": anthropic_api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            }

            async with httpx.AsyncClient(timeout=30) as client:
                api_resp = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers=headers,
                    json=payload,
                )
                if api_resp.status_code != 200:
                    return {
                        "error": f"Anthropic API error: {api_resp.status_code} - {api_resp.text}"
                    }
                result = api_resp.json()
                # Try to extract the JSON from the response
                try:
                    # Claude 3 returns the response in result['content'][0]['text']
                    import json as pyjson

                    text = result["content"][0]["text"]
                    # Try to parse the first JSON object in the text
                    start = text.find("{")
                    end = text.rfind("}") + 1
                    if start != -1 and end != -1:
                        return pyjson.loads(text[start:end])
                    else:
                        return {"raw_response": text}
                except Exception as e:
                    return {
                        "error": f"Failed to parse Claude response: {e}",
                        "raw_response": result,
                    }
        except Exception as e:
            return {"error": str(e)}

    def _load_threat_patterns(self) -> Dict:
        return {
            "high_risk_species": [
                "elephant",
                "rhino",
                "tiger",
                "pangolin",
                "bear",
                "shark",
                "turtle",
                "leopard",
                "jaguar",
                "cheetah",
            ],
            "risk_multipliers": {
                "cash_only": 2.0,
                "discreet_shipping": 1.8,
                "no_questions": 2.5,
                "traditional_medicine": 1.5,
            },
        }
