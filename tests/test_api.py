from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_optimize():
    payload = {
        "trips": [
            {"origin": "A", "destination": "B"},
            {"origin": "B", "destination": "C"},
        ],
        "constraints": {},
    }
    response = client.post("/api/v1/optimize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "route" in data
    assert "total_distance_km" in data
