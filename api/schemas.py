from typing import List
from pydantic import BaseModel

# DAILY

class DailyRouteRequest(BaseModel):
    driver_id: str
    date: str
    locations: List[str]


class DailyRouteResponse(BaseModel):
    driver_id: str
    date: str
    recommended_route: List[str]
    predicted_time: str
    confidence: float
    map_url: str | None = None

# WEEKLY

class WeeklyRouteRequest(BaseModel):
    driver_id: str
    week: str   # FIXED (you were missing this earlier)


class WeeklyRouteResponse(BaseModel):
    driver_id: str
    week: str

    monday: List[str]
    tuesday: List[str]
    wednesday: List[str]
    thursday: List[str]
    friday: List[str]

    weekly_distance: float


# =====================
class HealthResponse(BaseModel):
    status: str
