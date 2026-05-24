import os
from typing import Any

import requests


def get_distance_duration(
    origin: str,
    destination: str,
    api_key: str | None = None,
) -> dict[str, Any]:
    """Fetch distance and duration from Google Maps Distance Matrix API."""
    key = api_key or os.getenv("GOOGLE_MAPS_API_KEY", "")
    if not key:
        return {"distance_km": 0.0, "duration_min": 0.0, "status": "missing_api_key"}

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {"origins": origin, "destinations": destination, "key": key}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "OK":
        return {"distance_km": 0.0, "duration_min": 0.0, "status": data.get("status")}

    element = data["rows"][0]["elements"][0]
    if element.get("status") != "OK":
        return {"distance_km": 0.0, "duration_min": 0.0, "status": element.get("status")}

    distance_m = element["distance"]["value"]
    duration_s = element["duration"]["value"]
    return {
        "distance_km": round(distance_m / 1000, 2),
        "duration_min": round(duration_s / 60, 2),
        "status": "OK",
    }
