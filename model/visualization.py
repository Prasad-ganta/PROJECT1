import os
import uuid
import folium


def visualize_route_map(locations, coordinates):
    """
    Returns:
    - google_maps_url
    - folium_map_url
    """

    if not locations or not coordinates:
        return None, None

    waypoints = [coordinates[loc] for loc in locations if loc in coordinates]

    if len(waypoints) < 2:
        return None, None

    origin = waypoints[0]
    destination = waypoints[-1]

    # -----------------------------
    # 1. GOOGLE MAPS URL (SAFE)
    # -----------------------------
    google_url = (
        "https://www.google.com/maps/dir/?api=1"
        f"&origin={origin[0]},{origin[1]}"
        f"&destination={destination[0]},{destination[1]}"
        f"&travelmode=driving"
    )

    # -----------------------------
    # 2. FOLIUM MAP (DASHBOARD)
    # -----------------------------
    try:
        m = folium.Map(location=origin, zoom_start=12)

        points = []

        for loc in locations:
            if loc in coordinates:
                lat, lon = coordinates[loc]
                points.append((lat, lon))
                folium.Marker([lat, lon], tooltip=loc).add_to(m)

        if len(points) > 1:
            folium.PolyLine(points, color="blue", weight=5).add_to(m)

        os.makedirs("static", exist_ok=True)

        file_id = str(uuid.uuid4())
        file_name = f"{file_id}.html"
        file_path = os.path.join("static", file_name)

        m.save(file_path)

        base_url = os.getenv("BASE_URL", "http://localhost:8000")
        folium_url = f"{base_url}/static/{file_name}"

    except Exception:
        folium_url = None

    return google_url, folium_url
