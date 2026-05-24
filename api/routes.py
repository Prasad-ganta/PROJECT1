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
import logging

router = APIRouter()
logger = logging.getLogger("trip_optimizer")

# HEALTH CHECK

@router.get("/health")
async def health():
    return {"status": "ok"}

# FEATURE ENGINEERING (NO STATIC VALUES)

def build_features(src, dst, request, distance_matrix, df):

    return [[
        float(distance_matrix[src][dst]),                           # real distance
        1 if request.date.endswith("6") else 0,                     # simple weekend flag
        len(request.locations),                                     # route size
        df[df["Stop_Name"] == src]["Visit_Duration_Min"].mean() or 30,
        df[df["Stop_Name"] == dst]["Visit_Duration_Min"].mean() or 30,
        hash(request.driver_id) % 10,                               # driver pattern
        hash(src) % 10,
        hash(dst) % 10,
        len(set(request.locations)),                                # uniqueness
        1
    ]]


# DAILY ROUTE PREDICTION (FIXED + NON STATIC)
@router.post("/predict/daily")
async def predict_daily_route(
    request: DailyRouteRequest,
    distance_matrix=Depends(get_distance_matrix),
    xgb_model=Depends(get_xgboost_model)
):

    df = pd.read_csv("data/raw/trips.csv")
    df.columns = df.columns.str.strip()
    
    # VALIDATE INPUT LOCATIONS
    filtered = {}

    for src in request.locations:
        if src not in distance_matrix:
            raise HTTPException(status_code=404, detail=f"{src} not found")

        filtered[src] = {}

        for dst in request.locations:
            if dst not in distance_matrix[src]:
                raise HTTPException(status_code=404, detail=f"{src} -> {dst} missing")

            filtered[src][dst] = distance_matrix[src][dst]


    # OPTIMIZED ROUTE

    route = solve_route(filtered)

    if not route:
        raise HTTPException(status_code=500, detail="Route optimization failed")

    # ETA PREDICTION (REAL DYNAMIC)
    
    total_eta = 0.0

    for i in range(len(route) - 1):
        src = route[i]
        dst = route[i + 1]

        features = build_features(
            src, dst,
            request,
            distance_matrix,
            df
        )

        pred = xgb_model.predict(features)

        if pred is not None:
            total_eta += float(pred[0])

    predicted_hours = round(total_eta / 60, 2)

  
    # CONFIDENCE (SAFE RANGE)

    confidence = max(0.5, min(0.99, 1 - (total_eta / 1000)))

    # REAL COORDINATES FROM DATASET

    coords = {}

    for loc in route:
        row = df[df["Stop_Name"] == loc]

        if not row.empty:
            coords[loc] = [
                float(row.iloc[0]["Latitude"]),
                float(row.iloc[0]["Longitude"])
            ]

    # MAP GENERATION (REAL URL)

    try:
        map_url = visualize_route_map(route, coords)
    except Exception:
        map_url = None

    # LOGGING
    
    try:
        log_prediction(logger, "xgboost", predicted_hours, confidence)
    except Exception:
        pass

    # RESPONSE
   
    return {
        "driver_id": request.driver_id,
        "date": request.date,
        "recommended_route": route,
        "predicted_time": f"{predicted_hours} hours",
        "confidence": round(confidence, 2),
        "map_url": map_url
    }



# WEEKLY ROUTE (NO STATIC DISTANCE)

@router.post("/predict/weekly")
async def predict_weekly_route(request: WeeklyRouteRequest):

    df = pd.read_csv("data/raw/trips.csv")
    df.columns = df.columns.str.strip()

    driver_col = df.columns[0]
    driver_df = df[df[driver_col] == request.driver_id]

    if driver_df.empty:
        raise HTTPException(status_code=404, detail="Driver not found")

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    weekly_plan = {}
    total_distance = 0.0

    for day in days:
        stops = driver_df[driver_df["Day_Of_Week"] == day]["Stop_Name"].head(3).tolist()
        weekly_plan[day.lower()] = stops

        # REALISTIC distance from dataset column
        for i in range(len(stops) - 1):
            row = driver_df[driver_df["Stop_Name"] == stops[i]]

            if not row.empty:
                total_distance += float(row.iloc[0]["Travel_Next_Min"])

    return {
        "driver_id": request.driver_id,
        "week": request.week,
        **weekly_plan,
        "weekly_distance": round(total_distance / 60, 2)
    }



# RETRAIN MODEL

import subprocess

@router.post("/retrain")
async def retrain_model():

    subprocess.Popen(["python", "scripts/retrain_pipeline.py"])

    return {
        "status": "success",
        "message": "Model retraining started"
    }
