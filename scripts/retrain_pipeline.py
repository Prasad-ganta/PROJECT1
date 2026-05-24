"""End-to-end retraining pipeline."""

import argparse
from pathlib import Path

import pandas as pd

from model.train_lstm import train_lstm
from model.train_xgboost import train_xgboost


def preprocess(raw_path: str, processed_path: str) -> None:
    df = pd.read_csv(raw_path)
    df = df.dropna(subset=["origin", "destination"])
    Path(processed_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(processed_path, index=False)


def run_pipeline(
    raw_path: str = "data/raw/trips.csv",
    processed_path: str = "data/processed/processed_trips.csv",
) -> None:
    preprocess(raw_path, processed_path)
    train_xgboost(processed_path)
    train_lstm(processed_path)
    print("Retrain pipeline complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", default="data/raw/trips.csv")
    parser.add_argument("--processed", default="data/processed/processed_trips.csv")
    args = parser.parse_args()
    run_pipeline(args.raw, args.processed)
