import os

def visualize_route_map(locations, coordinates):
    """
    Returns Google Maps URL (always works)
    Optional: uses Google API if key exists
    """

    if not locations or not coordinates:
        return None

    waypoints = [coordinates[loc] for loc in locations if loc in coordinates]

    if len(waypoints) < 2:
        return None

    origin = waypoints[0]
    destination = waypoints[-1]

    # -----------------------------
    # ALWAYS WORKING GOOGLE MAP URL
    # -----------------------------
    base_url = "https://www.google.com/maps/dir/?api=1"

    url = (
        f"{base_url}"
        f"&origin={origin[0]},{origin[1]}"
        f"&destination={destination[0]},{destination[1]}"
        f"&travelmode=driving"
    )

    # -----------------------------
    # OPTIONAL GOOGLE API (SAFE)
    # -----------------------------
    GMAPS_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

    if GMAPS_KEY:
        try:
            import googlemaps

            gmaps = googlemaps.Client(key=GMAPS_KEY)

            gmaps.directions(
                origin=origin,
                destination=destination,
                waypoints=waypoints[1:-1],
                optimize_waypoints=True,
                departure_time="now"
            )

        except Exception as e:
            print("Google Maps API error:", e)

    return url
