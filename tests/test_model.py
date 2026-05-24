from model.confidence import compute_confidence
from model.features import build_feature_frame
import pandas as pd


def test_compute_confidence_full():
    features = {
        "distance_km": 10.0,
        "duration_min": 20.0,
        "origin": "A",
        "destination": "B",
    }
    assert compute_confidence(features) == 1.0


def test_build_feature_frame():
    df = pd.DataFrame(
        {
            "origin": ["A"],
            "destination": ["B"],
            "departure_time": ["2025-01-01 08:00:00"],
            "distance_km": [10.0],
            "duration_min": [20.0],
        }
    )
    result = build_feature_frame(df)
    assert "hour" in result.columns
    assert "day_of_week" in result.columns
