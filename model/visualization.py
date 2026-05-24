import googlemaps
import os

GMAPS_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(key=GMAPS_KEY)

def visualize_route_map(locations, coordinates):

    waypoints = [coordinates[loc] for loc in locations if loc in coordinates]

    origin = waypoints[0]
    destination = waypoints[-1]

    result = gmaps.directions(
        origin=origin,
        destination=destination,
        waypoints=waypoints[1:-1],
        optimize_waypoints=True,
        departure_time="now"
    )

    route = result[0]

    # --------------------------
    # BUILD GOOGLE MAPS URL
    # --------------------------
    url = (
        "https://www.google.com/maps/dir/?api=1"
        f"&origin={origin[0]},{origin[1]}"
        f"&destination={destination[0]},{destination[1]}"
        f"&travelmode=driving"
    )

    return url
