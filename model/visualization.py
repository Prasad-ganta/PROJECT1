import folium
import uuid
import os

def visualize_route_map(route, coords):

    if not route or not coords:
        return None

    start = coords[route[0]]
    m = folium.Map(location=start, zoom_start=12)

    points = []

    for stop in route:
        if stop in coords:
            lat, lon = coords[stop]
            points.append((lat, lon))
            folium.Marker([lat, lon], tooltip=stop).add_to(m)

    if len(points) > 1:
        folium.PolyLine(points, color="blue").add_to(m)

    os.makedirs("static", exist_ok=True)

    file_id = str(uuid.uuid4())
    file_path = f"static/{file_id}.html"

    m.save(file_path)

    return f"http://127.0.0.1:8000/static/{file_id}.html"