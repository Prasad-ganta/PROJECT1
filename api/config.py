from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Trip Optimizer API"
    debug: bool = False
    google_maps_api_key: str = ""
    xgboost_model_path: str = "saved_models/xgboost_model.pkl"
    lstm_model_path: str = "saved_models/lstm_model.h5"
    label_encoders_path: str = "saved_models/label_encoders.pkl"
    distance_matrix_path: str = "data/matrices/distance_matrix.json"
    distance_cache_path: str = "cache/distance_cache.json"
    log_path: str = "logs/app.log"


@lru_cache
def get_settings() -> Settings:
    return Settings()
