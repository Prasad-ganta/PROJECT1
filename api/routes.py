from fastapi import APIRouter, Depends, HTTPException
from api.schemas import DailyRouteRequest, WeeklyRouteRequest
from api.dependencies import get_distance_matrix, get_xgboost_model

from model.optimizer import solve_route
from model.confidence import calculate_confidence
from model.monitoring import log_prediction
from model.visualization import visualize_route_map

import pandas as pd
import numpy as np
import logging

router = APIRouter()
logger = logging.getLogger("trip_optimizer")


# =========================
# DAILY ROUTE (FIXED + MAP)
# =========================
from model.visualization import visualize_route_map

@router.post("/predict/daily")
async def predict_daily_route(
    request: DailyRouteRequest,
    distance_matrix=Depends(get_distance_matrix),
    xgb_model=Depends(get_xgboost_model)
):

    if not request.locations:
        raise HTTPException(400, "locations required")

    for loc in request.locations:
        if loc not in distance_matrix:
            raise HTTPException(404, f"{loc} not found")

    filtered = {
        i: {j: distance_matrix[i][j] for j in request.locations}
        for i in request.locations
    }

    route = solve_route(filtered)

    total_minutes = 0

    for i in range(len(route) - 1):
        src, dst = route[i], route[i + 1]
        dist = filtered[src][dst]

        features = np.array([[dist, 0, 1, 0, 30, 0, 0, dist / 2, len(route), 1]])

        total_minutes += float(xgb_model.predict(features)[0])

    hours = round(total_minutes / 60, 2)
    confidence = calculate_confidence(total_minutes)

    # ✅ IMPORTANT FIX (THIS WAS MISSING)
    coords = distance_matrix  # OR your actual coordinates dict

    map_url = visualize_route_map(route, coords)

    log_prediction(logger=logger, model="xgboost", duration=hours, confidence=confidence)

    return {
        "driver_id": request.driver_id,
        "date": request.date,
        "recommended_route": route,
        "predicted_time": f"{hours} hours",
        "confidence": confidence,
        "map_url": map_url   # ✅ NOW FIXED
    }


# =========================
# WEEKLY ROUTE (REAL FIX)
# =========================
@router.post("/predict/weekly")
async def predict_weekly_route(
    request: WeeklyRouteRequest,
    distance_matrix=Depends(get_distance_matrix)
):

    df = pd.read_csv("data/raw/trips.csv")
    df.columns = df.columns.str.strip()

    driver_df = df[df.iloc[:, 0] == request.driver_id]

    if driver_df.empty:
        raise HTTPException(404, "Driver not found")

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    weekly_plan = {}
    total_distance = 0

    for day in days:
        stops = driver_df[driver_df["Day_Of_Week"] == day]["Stop_Name"].tolist()[:3]
        weekly_plan[day.lower()] = stops

        for i in range(len(stops) - 1):
            a, b = stops[i], stops[i + 1]

            if a in distance_matrix and b in distance_matrix[a]:
                total_distance += distance_matrix[a][b]

    return {
        "driver_id": request.driver_id,
        "week": request.week,
        **weekly_plan,
        "weekly_distance_km": round(total_distance / 1000, 2)
    }
