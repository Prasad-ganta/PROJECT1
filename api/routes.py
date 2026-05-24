from fastapi import APIRouter
from api.schemas import DailyRouteRequest
from model.visualization import visualize_route_map

router = APIRouter()


# Dummy ML logic (replace with your XGBoost later)
def fake_optimizer(locations):
    return sorted(locations)


def fake_time():
    return 1.25


def fake_confidence():
    return 0.90


@router.post("/predict/daily")
def predict_daily(request: DailyRouteRequest):

    # ------------------------
    # STEP 1: optimize route
    # ------------------------
    optimized_route = fake_optimizer(request.locations)

    # ------------------------
    # STEP 2: coordinates (example)
    # ------------------------
    coordinates = {
        "Shopping Center": (16.5062, 80.6480),
        "Hub West": (16.5100, 80.6200),
        "Store C": (16.5200, 80.6300),
        "Depot B": (16.5300, 80.6400),
    }

    # ------------------------
    # STEP 3: ML outputs
    # ------------------------
    predicted_hours = fake_time()
    confidence = fake_confidence()

    # ------------------------
    # STEP 4: map generation
    # ------------------------
    map_url = visualize_route_map(optimized_route, coordinates)

    return {
        "driver_id": request.driver_id,
        "date": request.date,
        "recommended_route": optimized_route,
        "predicted_time": f"{predicted_hours} hours",
        "confidence": confidence,
        "map_url": map_url
    }
