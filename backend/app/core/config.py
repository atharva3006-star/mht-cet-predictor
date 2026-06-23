"""
Central configuration: file paths and a lazily-initialized
PredictionEngine singleton shared across API routes.
"""

import json
from pathlib import Path
from functools import lru_cache

from app.core.prediction_engine import PredictionEngine

BASE_DIR = Path(__file__).resolve().parent.parent  # -> app/
MASTER_CSV_PATH = BASE_DIR / "data" / "processed" / "mhtcet_cutoffs_master.csv"
CATEGORY_MAP_PATH = BASE_DIR / "data" / "meta" / "category_map.json"


@lru_cache()
def get_engine() -> PredictionEngine:
    """Returns a single shared PredictionEngine instance (loaded once)."""
    return PredictionEngine(str(MASTER_CSV_PATH))


@lru_cache()
def get_category_map() -> dict:
    with open(CATEGORY_MAP_PATH) as f:
        return json.load(f)