from logging import setLoggerClass
import time
import joblib
from src import config
from src.config.logs_config import setup_log, auto_logger
from src.utils.hardware import free_resoucre_and_cooldown  # Gọi lại tản nhiệt
from src.config.dir_config import Models_Dir

logger = setup_log(name="Model_Trainer", filename="Models")

class FraudModelTrainer:
    def __init__(self):
        self.save_path = Models_Dir

    @auto_logger(logger)
    def train_models(self, models_dict, X_train, y_train, X_val, y_val, cooldown_sec=45):
        """Trains and saves ALL models to disk for Web UI Testing."""
        logger.info(f"Training and saving all {len(models_dict)} models...")
        
        trained_models = {}
        total_models = len(models_dict)
        current = 1
        
        for name, model in models_dict.items():
            logger.info(f"[{current}/{total_models}] Training {name}...")
            start_time = time.time()
            
            # Tính năng Early Stopping cho các thuật toán Boosting xịn
            if name in ['LightGBM', 'XGBoost', 'CatBoost']:
                model.fit(X_train, y_train, eval_set=[(X_val, y_val)])
            else:
                model.fit(X_train, y_train)
                
            elapsed_time = time.time() - start_time
            
            # Làm sạch tên file (Bỏ dấu cách, dấu ngoặc) và Lưu model
            safe_name = name.replace(" ", "_").replace("(", "").replace(")", "")
            model_file = self.save_path / f"{safe_name}.pkl"
            joblib.dump(model, model_file)
            logger.info(f"Saved {name} to {model_file} (Took {elapsed_time:.2f}s)")
            
            trained_models[name] = model
            
            # KÍCH HOẠT TẢN NHIỆT SAU MỖI MÔ HÌNH
            if current < total_models:
                free_resoucre_and_cooldown(sec=cooldown_sec)
            
            current += 1
            
        return trained_models
