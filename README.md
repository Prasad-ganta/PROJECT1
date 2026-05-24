# Trip Optimizer

ML-powered trip routing and duration prediction API.

## Project structure

- `api/` — FastAPI application
- `model/` — Training, prediction, and route optimization
- `visualization/` — Route map visualization
- `scripts/` — Dataset generation and retraining pipelines
- `data/` — Raw, processed data and distance matrices
- `tests/` — Unit tests

## Setup

```bash
pip install -r requirements.txt
Edit `.env` with your API keys.
```

## Run API

```bash
uvicorn api.main:app --reload
```

## Run tests

```bash
pytest tests/
```

## Retrain models

```bash
python scripts/retrain_pipeline.py
```
