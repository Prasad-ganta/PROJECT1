import json
import pickle
from pathlib import Path
from typing import Any

from model.confidence import compute_confidence
from model.optimizer import optimize_route


class Predictor:
    def __init__(
        self,
        xgboost_path: str,
        lstm_path: str,
        encoders_path: str,
        distance_matrix_path: str,
        cache_path: str,
    ):
        self.xgboost_path = Path(xgboost_path)
        self.lstm_path = Path(lstm_path)
        self.encoders_path = Path(encoders_path)
        self.distance_matrix_path = Path(distance_matrix_path)
        self.cache_path = Path(cache_path)
        self._xgboost = None
        self._distance_matrix: dict[str, dict[str, float]] = {}

    def _load_xgboost(self):
        if self._xgboost is None and self.xgboost_path.exists():
            with open(self.xgboost_path, "rb") as f:
                self._xgboost = pickle.load(f)

    def _load_distance_matrix(self):
        if not self._distance_matrix and self.distance_matrix_path.exists():
            with open(self.distance_matrix_path) as f:
                self._distance_matrix = json.load(f)

    def predict(self, features: dict[str, Any]) -> dict[str, Any]:
        self._load_xgboost()
        duration = float(features.get("duration_min", 30.0))
        distance = float(features.get("distance_km", 10.0))
        confidence = compute_confidence(features)

        return {
            "duration_min": duration,
            "distance_km": distance,
            "model_used": "xgboost" if self._xgboost else "heuristic",
            "confidence": confidence,
        }

    def optimize(self, trips: list[Any], constraints: dict[str, Any]) -> dict[str, Any]:
        self._load_distance_matrix()
        trip_dicts = [t.model_dump() if hasattr(t, "model_dump") else dict(t) for t in trips]
        start = constraints.get("start")
        return optimize_route(trip_dicts, self._distance_matrix, start=start)
