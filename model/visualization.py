import os
import googlemaps


# =========================
# SAFE CLIENT CREATION
# =========================
def get_gmaps_client():
    key = os.getenv("GOOGLE_MAPS_API_KEY")

    if not key:
        raise ValueError("GOOGLE_MAPS_API_KEY is missing in Railway Variables")

    return googlemaps.Client(key=key)


# =========================
# ROUTE VISUALIZATION
# =========================
def visualize_route_map(locations, coordinates):

    if not locations or not coordinates:
        return None

    # filter valid coordinates
    waypoints = [
        coordinates[loc]
        for loc in locations
        if loc in coordinates
    ]

    if len(waypoints) < 2:
        return None

    origin = waypoints[0]
    destination = waypoints[-1]

    gmaps = get_gmaps_client()

    # =========================
    # GOOGLE DIRECTIONS API
    # =========================
    result = gmaps.directions(
        origin=origin,
        destination=destination,
        waypoints=waypoints[1:-1],
        optimize_waypoints=True,
        departure_time="now"
    )

    # (optional safety check)
    if not result:
        return None

    route = result[0]

    # =========================
    # GOOGLE MAPS LINK (FINAL OUTPUT)
    # =========================
    url = (
        "https://www.google.com/maps/dir/?api=1"
        f"&origin={origin[0]},{origin[1]}"
        f"&destination={destination[0]},{destination[1]}"
        f"&travelmode=driving"
    )

    return url
