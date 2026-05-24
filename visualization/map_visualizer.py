from typing import Any


def visualize_route(route: list[str], output_path: str = "route_map.html") -> str:
    """Generate a simple HTML map visualization for a route."""
    points = "\n".join(f"<li>{loc}</li>" for loc in route)
    html = f"""<!DOCTYPE html>
<html>
<head><title>Route Map</title></head>
<body>
  <h1>Optimized Route</h1>
  <ol>{points}</ol>
</body>
</html>"""
    with open(output_path, "w") as f:
        f.write(html)
    return output_path
