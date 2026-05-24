from model.optimizer import optimize_route


def test_optimize_route_empty():
    result = optimize_route([], {})
    assert result["route"] == []
    assert result["total_distance_km"] == 0.0


def test_optimize_route_greedy():
    matrix = {
        "A": {"B": 5.0, "C": 10.0},
        "B": {"A": 5.0, "C": 3.0},
        "C": {"A": 10.0, "B": 3.0},
    }
    trips = [{"origin": "A", "destination": "B"}]
    result = optimize_route(trips, matrix, start="A")
    assert result["route"][0] == "A"
    assert len(result["route"]) >= 2
