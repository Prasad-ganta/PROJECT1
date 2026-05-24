import pandas as pd
import joblib
from pathlib import Path

from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


FEATURES = [
    "Hour",
    "Is_Weekend",
    "Traffic_Level",
    "Cluster",
    "Visit_Duration_Min",
    "Stop_Encoded",
    "Avg_Stop_Time",
    "Daily_Visits",
    "Stop_Frequency",
    "Route_Efficiency",
]

TARGET = "Travel_Next_Min"


def train_xgboost(
    data_path: str = "data/processed/processed_trips.csv",
    output_path: str = "saved_models/xgboost_model.pkl",
) -> XGBRegressor:

    df = pd.read_csv(data_path)

    missing = [c for c in FEATURES + [TARGET] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in processed data: {missing}")

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = XGBRegressor(
        n_estimators=150,
        learning_rate=0.05,
        max_depth=8,
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"MAE: {mae:.4f}")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)
    print(f"XGBoost model saved → {output_path}")

    return model


if __name__ == "__main__":
    train_xgboost()