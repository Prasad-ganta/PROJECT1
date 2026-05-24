from pathlib import Path

import numpy as np
import pandas as pd
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential


def build_lstm_model(input_shape: tuple[int, int]) -> Sequential:
    model = Sequential(
        [
            LSTM(64, input_shape=input_shape, return_sequences=False),
            Dense(32, activation="relu"),
            Dense(1),
        ]
    )
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    return model


def train_lstm(
    data_path: str = "data/processed/processed_trips.csv",
    output_path: str = "saved_models/lstm_model.h5",
    seq_len: int = 5,
) -> Sequential:
    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()

    # Use Travel_Next_Min (real dataset target), fall back to duration_min
    if "Travel_Next_Min" in df.columns:
        target_col = "Travel_Next_Min"
    elif "duration_min" in df.columns:
        target_col = "duration_min"
    else:
        raise ValueError(
            f"No target column found. Available columns: {df.columns.tolist()}"
        )

    print(f"Training LSTM on target column: '{target_col}'")

    values = df[[target_col]].fillna(0).values.astype(np.float32)

    sequences, targets = [], []
    for i in range(len(values) - seq_len):
        sequences.append(values[i : i + seq_len])
        targets.append(values[i + seq_len])

    X = np.array(sequences)
    y = np.array(targets)

    model = build_lstm_model((seq_len, 1))
    if len(X) > 0:
        model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2, verbose=1)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    model.save(output_path)
    print(f"LSTM model saved → {output_path}")
    return model


if __name__ == "__main__":
    train_lstm()