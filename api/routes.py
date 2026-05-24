from fastapi import APIRouter, Depends, HTTPException
from api.schemas import DailyRouteRequest, WeeklyRouteRequest

from api.dependencies import (
    get_distance_matrix,
    get_xgboost_model
)

from model.optimizer import solve_route
from model.confidence import calculate_confidence
from model.monitoring import log_prediction
from model.visualization import visualize_route_map

import pandas as pd
import numpy as np
import subprocess
import logging

router = APIRouter()
logger = logging.getLogger("trip_optimizer")


# =====================
# HEALTH
# =====================
@router.get("/health")
async def health():
    return {"status": "ok"}


# =====================
# DAILY ROUTE
# =====================
@router.post("/predict/daily")
async def predict_daily_route(
    request: DailyRouteRequest,
    distance_matrix=Depends(get_distance_matrix),
    xgb_model=Depends(get_xgboost_model)
):

    # ---------------------
    # FILTER DISTANCE MATRIX
    # ---------------------
    filtered_matrix = {}

    for src in request.locations:
        if src not in distance_matrix:
            raise HTTPException(404, f"{src} not found")

        filtered_matrix[src] = {}

        for dst in request.locations:
            if dst not in distance_matrix[src]:
                raise HTTPException(404, f"{src}->{dst} not found")

            filtered_matrix[src][dst] = distance_matrix[src][dst]

    # ---------------------
    # OPTIMIZE ROUTE
    # ---------------------
    optimized_route = solve_route(filtered_matrix)

    # ---------------------
    # ETA PREDICTION
    # ---------------------
    total_eta = 0

    for _ in range(len(optimized_route) - 1):
        features = np.array([[10, 0, 1, 0, 30, 0, 0, 25, 5, 10]])
        total_eta += xgb_model.predict(features)[0]

    predicted_hours = round(total_eta / 60, 2)

    # ---------------------
    # CONFIDENCE
    # ---------------------
    confidence = calculate_confidence(total_eta)

    # ---------------------
    # COORDINATES (replace with DB or Google API later)
    # ---------------------
    coordinates = {
        "Shopping Center": [17.4450, 78.5270],
        "Hub West": [17.3950, 78.4300],
        "Store C": [17.3750, 78.4800],
        "Depot B": [17.3450, 78.4550],
    }

    # ---------------------
    # MAP GENERATION
    # ---------------------
    map_url = visualize_route_map(optimized_route, coordinates)

    # ---------------------
    # LOGGING
    # ---------------------
    log_prediction(
        logger=logger,
        model="xgboost",
        duration=predicted_hours,
        confidence=confidence
    )

    # ---------------------
    # RESPONSE
    # ---------------------
    return {
        "driver_id": request.driver_id,
        "date": request.date,
        "recommended_route": optimized_route,
        "predicted_time": f"{predicted_hours} hours",
        "confidence": confidence,
        "map_url": map_url
    }


# =====================
# WEEKLY ROUTE
# =====================
@router.post("/predict/weekly")
async def predict_weekly_route(request: WeeklyRouteRequest):

    df = pd.read_csv("data/raw/trips.csv")
    df.columns = df.columns.str.strip()

    driver_col = df.columns[0]
    driver_df = df[df[driver_col] == request.driver_id]

    if driver_df.empty:
        raise HTTPException(404, "Driver not found")

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    weekly_plan = {
        day.lower(): driver_df[
            driver_df["Day_Of_Week"] == day
        ]["Stop_Name"].head(3).tolist()
        for day in days
    }

    return {
        "driver_id": request.driver_id,
        "week": request.week,
        **weekly_plan,
        "weekly_distance": "dynamic"
    }


# =====================
# RETRAIN MODEL
# =====================
@router.post("/retrain")
async def retrain_model():

    subprocess.Popen([
        "python",
        "scripts/retrain_pipeline.py"
    ])

    return {
        "status": "success",
        "message": "Model retraining started"
    }
