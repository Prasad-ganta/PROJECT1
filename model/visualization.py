import os
import folium
import uuid


def visualize_route_map(locations, coordinates):
    """
    Returns:
    {
        "map_url": Google Maps link,
        "preview_url": Folium HTML map
    }
    """

    if not locations or not coordinates:
        return None, None

    # build coordinates list
    waypoints = []
    for loc in locations:
        if loc in coordinates:
            waypoints.append(coordinates[loc])

    if len(waypoints) < 2:
        return None, None

    origin = waypoints[0]
    destination = waypoints[-1]

    # ==========================
    # 1. GOOGLE MAPS URL (SAFE)
    # ==========================
    google_url = (
        "https://www.google.com/maps/dir/?api=1"
        f"&origin={origin[0]},{origin[1]}"
        f"&destination={destination[0]},{destination[1]}"
        f"&travelmode=driving"
    )

    # ==========================
    # 2. FOLIUM MAP (PREVIEW)
    # ==========================
    base_url = os.getenv(
        "BASE_URL",
        "http://localhost:8000"
    )

    file_id = str(uuid.uuid4())
    file_name = f"{file_id}.html"
    file_path = f"static/{file_name}"

    os.makedirs("static", exist_ok=True)

    m = folium.Map(location=origin, zoom_start=12)

    for point in waypoints:
        folium.Marker(location=point).add_to(m)

    folium.PolyLine(waypoints, color="blue", weight=5).add_to(m)

    m.save(file_path)

    preview_url = f"{base_url}/static/{file_name}"

    return google_url, preview_url
