AI Route Prediction System
What this project is

This is a route planning system that helps drivers decide the best order to visit multiple places in a day or across a week. It’s mainly useful for field sales, delivery teams, or logistics work where planning routes manually takes time and often leads to inefficiency.

The system uses historical patterns, distance calculations from Google Maps, and a simple ML model to suggest better routes and estimate travel time.

It also provides a map view so the route can be visually checked instead of only looking at JSON output.

What it does
Takes a list of locations for a driver
Finds the best visiting order
Estimates total travel time
Creates daily optimized routes
Splits work into weekly plans
Gives confidence score for predictions
Generates a map view of the route
Tech stack
Python
FastAPI
Scikit-learn / XGBoost
Google Maps API
Pandas, NumPy
Folium / HTML map visualization
How to run

Install dependencies:

pip install -r requirements.txt

Start the server:

uvicorn api.main:app --reload

Open in browser:

http://127.0.0.1:8000
API Details
1. Daily Route Prediction
Endpoint
POST /predict/daily
Request
{
  "driver_id": "D1",
  "date": "2026-05-24",
  "locations": [
    "Shopping Center",
    "Hub West",
    "Store C",
    "Depot B"
  ]
}
Response
{
  "driver_id": "D1",
  "date": "2026-05-26",
  "recommended_route": [
    "Store C",
    "Depot B"
  ],
  "predicted_time": "0.62 hours",
  "confidence": 0.96,
  "map_url": "http://127.0.0.1:8000/static/cd0602ed-7db1-4027-9b6c-2cac941c7823.html"
}
What this means
recommended_route → best order of visiting locations
predicted_time → estimated travel time
confidence → how confident the model is
map_url → opens visual route on map
2. Weekly Route Prediction
Endpoint
POST /predict/weekly
Request
{
  "driver_id": "D1",
  "week": "2026-W30"
}
Response
{
  "monday": ["A", "B", "C"],
  "tuesday": ["D", "E"],
  "wednesday": ["F", "G"],
  "thursday": ["H", "I"],
  "friday": ["J", "K"],
  "weekly_distance": "230 km"
}
What this means
Each day has a planned set of stops
Work is distributed across the week
Helps reduce workload imbalance
weekly_distance shows total travel covered
3. Health Check
GET /health
Response
{
  "status": "ok"
}
How it works (simple explanation)
User gives locations for a driver
System uses Google Maps API to get distances and travel time
ML model predicts best visiting order
Weekly planner distributes locations across days
A map is generated for visualization
Final result is returned through API
Real-world use cases

This is similar to systems used in:

Amazon / Flipkart delivery routing
Swiggy / Zomato delivery optimization
Uber / Ola navigation systems
FMCG field sales planning
Logistics companies like DHL / FedEx
Future improvements

If extended further, this system can include:

Live traffic-based rerouting
Smarter optimization (graph / reinforcement learning)
Real-time driver tracking dashboard
Docker deployment
Redis caching for faster API response
