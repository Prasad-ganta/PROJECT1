from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routes import router

app = FastAPI(title="Trip Optimizer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ CRITICAL FIX (prevents static crash)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
