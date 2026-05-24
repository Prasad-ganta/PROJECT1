from unittest.mock import patch

from model.google_maps import get_distance_duration


def test_missing_api_key():
    result = get_distance_duration("A", "B", api_key="")
    assert result["status"] == "missing_api_key"


@patch("model.google_maps.requests.get")
def test_successful_response(mock_get):
    mock_get.return_value.json.return_value = {
        "status": "OK",
        "rows": [
            {
                "elements": [
                    {
                        "status": "OK",
                        "distance": {"value": 5000},
                        "duration": {"value": 600},
                    }
                ]
            }
        ],
    }
    mock_get.return_value.raise_for_status = lambda: None

    result = get_distance_duration("Origin", "Dest", api_key="test-key")
    assert result["status"] == "OK"
    assert result["distance_km"] == 5.0
    assert result["duration_min"] == 10.0
