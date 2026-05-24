import os

def visualize_route_map(locations, coordinates):
    GMAPS_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

    # convert locations → coordinates
    waypoints = [coordinates[loc] for loc in locations if loc in coordinates]

    if len(waypoints) < 2:
        return None

    origin = waypoints[0]
    destination = waypoints[-1]

    # ----------------------------
    # ALWAYS WORKING FALLBACK URL
    # ----------------------------
    base_url = "https://www.google.com/maps/dir/?api=1"
    url = (
        f"{base_url}"
        f"&origin={origin[0]},{origin[1]}"
        f"&destination={destination[0]},{destination[1]}"
        f"&travelmode=driving"
    )

    # ----------------------------
    # OPTIONAL: Google Directions API (only if key exists)
    # ----------------------------
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

        except Exception:
            # don't crash API
            pass

    return url
