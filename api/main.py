from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

import os

app = FastAPI(title="Trip Optimizer API", version="1.0.0")

# prevent runtime crashes if folders missing
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/matrices", exist_ok=True)
os.makedirs("saved_models", exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
