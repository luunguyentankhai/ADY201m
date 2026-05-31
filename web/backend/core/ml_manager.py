import joblib
from pathlib import Path
from web.backend.config.logs_config import logger
from web.backend.config.settings import settings

class MLManager:
    _instance = None
    _is_loaded = False

    scaler = None
    models = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLManager, cls).__new__(cls)
        return cls._instance

    def load_assets(self):
        if self._is_loaded:
            return

        logger.info(f"[ML MANAGER] Add AI into RAM")

        model_dir = settings.MODEL_DIR

        try:
            scaler_path = model_dir / "fraud_scaler.pkl"
            self.scaler = joblib.load(scaler_path)
            logger.info(f"[ML MANAGER] Added fraud_scaler.pkl")

            model_name = [
                "LightGBM.pkl",
                "XGBoost.pkl",
                "CatBoost.pkl",
                "Logistic_Regression_SGD.pkl",
                "Random_Forest.pkl"
            ]

            for name in model_name:
                path = model_dir / name
                if path.exists():
                    model_key = name.replace(".pkl", "")
                    self.models[model_key] = joblib.load(path)
                    logger.info(f"[ML MANAGER] Added Model {name}")
                else:
                    logger.warning(f"[ML MANAGER] Cant found file {name}")

            self._is_loaded = True
            logger.info(f"[ML MANAGER] Models loaded on RAM")

        except Exception as e:
            logger.error(f"[ML MANAGER] Crash when load models {e}")
            raise e

    def get_status(self) -> dict:
        return {
                "ai_engine_active": self._is_loaded,
                "scaler_ready": self.scaler is not None,
                "models_on_ram": list(self.models.keys()),
                "total_models_loaded": len(self.models),
        }

ml_manager = MLManager()
