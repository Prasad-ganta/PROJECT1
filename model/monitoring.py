import logging
from pathlib import Path


def setup_logging(log_path: str = "logs/app.log", level: int = logging.INFO) -> logging.Logger:
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(),
        ],
    )

    return logging.getLogger("trip_optimizer")


def log_prediction(*, logger: logging.Logger, model: str, duration: float, confidence: float) -> None:
    logger.info(
        "prediction model=%s duration=%.2f confidence=%.2f",
        model,
        duration,
        confidence
    )