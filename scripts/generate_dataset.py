"""Generate synthetic trip dataset for development."""

import argparse
from pathlib import Path

import pandas as pd


def generate_dataset(output_path: str = "data/raw/trips.csv", n_rows: int = 100) -> None:
    locations = ["A", "B", "C", "D", "E"]
    rows = []
    for i in range(n_rows):
        origin = locations[i % len(locations)]
        destination = locations[(i + 2) % len(locations)]
        rows.append(
            {
                "trip_id": i + 1,
                "origin": origin,
                "destination": destination,
                "departure_time": f"2025-01-{(i % 28) + 1:02d} 08:00:00",
                "distance_km": round(5 + (i % 20) * 0.5, 2),
                "duration_min": round(10 + (i % 30), 2),
            }
        )

    df = pd.DataFrame(rows)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Wrote {len(df)} rows to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/raw/trips.csv")
    parser.add_argument("--rows", type=int, default=100)
    args = parser.parse_args()
    generate_dataset(args.output, args.rows)
