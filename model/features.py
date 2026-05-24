import pandas as pd
import joblib
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans


def create_features(
    data_path: str = "data/raw/trips.csv",
    output_path: str = "data/processed/processed_trips.csv",
    encoders_path: str = "saved_models/label_encoders.pkl",
):
    # LOAD DATA
    df = pd.read_csv(data_path)
    print("Raw data shape:", df.shape)

    # Strip whitespace from column names (your CSV has a leading-space column)
    df.columns = df.columns.str.strip()
    print("Columns found:", df.columns.tolist())

    # =========================
    # DATE / TIME FEATURES
    # =========================

    df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%Y", errors="coerce")

    df["Visit_Time"] = pd.to_datetime(df["Visit_Time"], format="%H:%M", errors="coerce")

    df["Hour"] = df["Visit_Time"].dt.hour

    df["Is_Weekend"] = df["Day_Of_Week"].isin(["Saturday", "Sunday"]).astype(int)

    # =========================
    # TRAFFIC FEATURE
    # =========================

    def traffic(hour):
        if pd.isna(hour):
            return 0
        if 8 <= hour <= 10:
            return 2
        if 17 <= hour <= 19:
            return 2
        if 11 <= hour <= 16:
            return 1
        return 0

    df["Traffic_Level"] = df["Hour"].apply(traffic)

    # =========================
    # ENCODING FEATURES
    # Driver_ID is not in this dataset — use Stop_Name only
    # =========================

    stop_encoder = LabelEncoder()
    df["Stop_Encoded"] = stop_encoder.fit_transform(df["Stop_Name"].astype(str))

    # =========================
    # LOCATION CLUSTERING
    # =========================

    n_clusters = min(5, len(df))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
    df["Cluster"] = kmeans.fit_predict(df[["Latitude", "Longitude"]])

    # =========================
    # STOP FEATURES
    # =========================

    df["Stop_Frequency"] = df.groupby("Stop_Name")["Stop_Name"].transform("count")

    # Avg travel time per stop (replaces Avg_Driver_Time which needed Driver_ID)
    df["Avg_Stop_Time"] = df.groupby("Stop_Name")["Travel_Next_Min"].transform("mean")

    # Daily visits per stop per date
    df["Daily_Visits"] = df.groupby(["Stop_Name", "Date"])["Stop_Name"].transform("count")

    # =========================
    # ROUTE FEATURE
    # =========================

    df["Route_Efficiency"] = df["Visit_Duration_Min"] / (df["Travel_Next_Min"] + 1)

    # =========================
    # CLEAN DATA
    # =========================

    df = df.dropna(subset=[
        "Hour", "Is_Weekend", "Traffic_Level", "Cluster",
        "Visit_Duration_Min", "Travel_Next_Min",
        "Stop_Encoded", "Avg_Stop_Time",
        "Daily_Visits", "Stop_Frequency", "Route_Efficiency",
    ])

    print("Processed data shape:", df.shape)

    # =========================
    # SAVE PROCESSED DATA
    # =========================

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved processed data → {output_path}")

    # =========================
    # SAVE ENCODERS
    # =========================

    Path(encoders_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "stop_encoder": stop_encoder,
            "kmeans": kmeans,
        },
        encoders_path,
    )
    print(f"Saved encoders → {encoders_path}")
    print("Feature engineering completed successfully!")


if __name__ == "__main__":
    create_features()