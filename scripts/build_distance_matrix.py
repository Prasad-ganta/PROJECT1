"""Build pairwise distance matrix from stop locations using the Haversine formula."""

import argparse
import json
import math
from itertools import product
from pathlib import Path

import pandas as pd


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Straight-line distance between two lat/lon points in kilometres."""
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return round(R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 3)


def build_distance_matrix(
    data_path: str = "data/processed/processed_trips.csv",
    output_path: str = "data/matrices/distance_matrix.json",
) -> dict:
    df = pd.read_csv(data_path)

    # Clean column names in case of leading/trailing whitespace
    df.columns = df.columns.str.strip()

    required = {"Stop_Name", "Latitude", "Longitude"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    # One representative lat/lon per stop (mean across all visits)
    stops = (
        df.groupby("Stop_Name")[["Latitude", "Longitude"]]
        .mean()
        .reset_index()
    )
    print(f"Building distance matrix for {len(stops)} unique stops...")

    matrix: dict[str, dict[str, float]] = {}

    for _, row_o in stops.iterrows():
        o = row_o["Stop_Name"]
        matrix[o] = {}
        for _, row_d in stops.iterrows():
            d = row_d["Stop_Name"]
            if o == d:
                matrix[o][d] = 0.0
            else:
                matrix[o][d] = haversine_km(
                    row_o["Latitude"], row_o["Longitude"],
                    row_d["Latitude"], row_d["Longitude"],
                )

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(matrix, f, indent=2)

    print(f"Distance matrix saved → {output_path}")
    return matrix


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/processed/processed_trips.csv")
    parser.add_argument("--output", default="data/matrices/distance_matrix.json")
    args = parser.parse_args()
    build_distance_matrix(args.data, args.output)