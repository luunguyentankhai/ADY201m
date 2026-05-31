from web.backend.config.dir_config import DATA_DIR
from pydantic_settings import BaseSettings
from pathlib import Path
import pandas as pd


class Settings(BaseSettings):
    APP_NAME: str = "Fraud Detection Web"
    APP_VERSION: str = "1.0.0"
    DEBUG_MODE: bool = True

    MODEL_DIR: Path = DATA_DIR / "processed" / "Models"

    CORS_ORIGINS: list[str] = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:8000",
            "http://localhost:8000"
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"

settings = Settings()


