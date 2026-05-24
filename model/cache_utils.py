import json
from pathlib import Path
from typing import Any


def load_cache(cache_path: str) -> dict[str, Any]:
    path = Path(cache_path)
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def save_cache(cache_path: str, cache: dict[str, Any]) -> None:
    path = Path(cache_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(cache, f, indent=2)


def cache_key(origin: str, destination: str) -> str:
    return f"{origin}|{destination}"


def get_cached_distance(cache: dict[str, Any], origin: str, destination: str) -> float | None:
    return cache.get(cache_key(origin, destination))


def set_cached_distance(cache: dict[str, Any], origin: str, destination: str, distance_km: float) -> None:
    cache[cache_key(origin, destination)] = distance_km
