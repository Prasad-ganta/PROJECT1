from fastapi import APIRouter, Depends, HTTPException
from api.schemas import DailyRouteRequest, WeeklyRouteRequest
from api.dependencies import get_distance_matrix, get_xgboost_model

from model.optimizer import solve_route
from model.confidence import calculate_confidence
from model.monitoring import log_prediction

import pandas as pd
import numpy as np
import logging

router = APIRouter()
logger = logging.getLogger("trip_optimizer")


# =========================
# DAILY ROUTE (REAL AI ML)
# =========================
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

    # Build filtered graph
    filtered = {
        i: {j: distance_matrix[i][j] for j in request.locations}
        for i in request.locations
    }

    # Optimize route (OR-Tools / fallback)
    route = solve_route(filtered)

    total_minutes = 0

    # ML prediction per route segment
    for i in range(len(route) - 1):
        src, dst = route[i], route[i + 1]
        dist = filtered[src][dst]

        features = np.array([[
            dist,
            0,
            1,
            0,
            30,
            0,
            0,
            dist / 2,
            len(route),
            1
        ]])

        total_minutes += float(xgb_model.predict(features)[0])

    hours = round(total_minutes / 60, 2)
    confidence = calculate_confidence(total_minutes)

    log_prediction(
        logger=logger,
        model="xgboost",
        duration=hours,
        confidence=confidence
    )

    return {
        "driver_id": request.driver_id,
        "date": request.date,
        "recommended_route": route,
        "predicted_time": f"{hours} hours",
        "confidence": confidence
    }


# =========================
# WEEKLY ROUTE (REAL AI OPTIMIZED)
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

    # -------------------------
    # GREEDY OPTIMIZER (SAFE AI)
    # -------------------------
    def greedy_optimize(stops):
        if len(stops) <= 2:
            return stops

        unvisited = stops[:]
        current = unvisited.pop(0)
        route = [current]

        while unvisited:
            next_stop = min(
                unvisited,
                key=lambda x: distance_matrix.get(current, {}).get(x, 1e9)
            )
            route.append(next_stop)
            unvisited.remove(next_stop)
            current = next_stop

        return route

    # -------------------------
    # BUILD WEEKLY PLAN
    # -------------------------
    for day in days:

        stops = driver_df[
            driver_df["Day_Of_Week"] == day
        ]["Stop_Name"].tolist()

        if not stops:
            weekly_plan[day.lower()] = []
            continue

        optimized_route = greedy_optimize(stops)
        weekly_plan[day.lower()] = optimized_route

        # calculate distance for this day
        for i in range(len(optimized_route) - 1):
            a, b = optimized_route[i], optimized_route[i + 1]

            if a in distance_matrix and b in distance_matrix[a]:
                total_distance += distance_matrix[a][b]

    return {
        "driver_id": request.driver_id,
        "week": request.week,
        **weekly_plan,
        "weekly_distance_km": round(total_distance / 1000, 2)
    }


# =========================
# RETRAIN PIPELINE
# =========================
@router.post("/retrain")
async def retrain_model():
    import subprocess

    subprocess.Popen(["python", "scripts/retrain_pipeline.py"])

    return {"status": "success"}
