import gc
from lightgbm import LGBMClassifier

from src.config.logs_config import setup_log
from src.db.utils import fetch_feature_store
from src.etl.preprocessing import DataSplitter, FeatureScaler
from src.utils.hardware import hardware_optimized_models, free_resoucre_and_cooldown 
from src.models.evaluator import model_comparison_evaluate
from src.models.trainer import FraudModelTrainer
from src.models.visualizer import ModelVisualizer

logger = setup_log(name="Pipeline", filename="app")

if __name__ == "__main__":
    logger.info("Initializing Fraud Detection End-to-End Pipeline...")
    
    # 1. DATA EXTRACTION
    raw_df = fetch_feature_store()
    
    if raw_df is not None:
        feature_names = raw_df.drop(columns=['step',  'is_fraud'], errors='ignore').columns.tolist()

        # 2. DATA PREPARATION
        logger.info("Phase 1 & 2: Splitting and Scaling (Using Full Data)...")
        splitter = DataSplitter(target_col='is_fraud')
        X_train, X_val, X_test, y_train, y_val, y_test = splitter.split_train_val_test(raw_df)
        
        # CHỈ XÓA raw_df để giải phóng RAM, KHÔNG XÓA X_train lúc này
        del raw_df
        gc.collect()
        
        # Scale toàn bộ tập dữ liệu gốc
        scaler = FeatureScaler()
        X_train_final, X_val_final, X_test_final = scaler.scale_and_save(X_train, X_val, X_test)
        
        # SAU KHI scale xong ra X_train_final, bây giờ mới được phép xóa X_train gốc
        del X_train
        gc.collect()
        
        # 3 & 4. TRAIN VÀ SAVE CẢ 7 MÔ HÌNH (Phục vụ cho backend Web UI)
        logger.info("Phase 3 & 4: Training & Saving ALL 7 Models...")
        
        # Đã gộp gọn phần khai báo trùng lặp của bạn
        imbalance_ratio = sum(y_train == 0) / sum(y_train == 1)
        models_dict = hardware_optimized_models(imbalance_ratio, use_gpu=False)
        
        trainer = FraudModelTrainer()
        all_trained_models = trainer.train_models(
            models_dict, X_train_final, y_train, X_val_final, y_val, cooldown_sec=60
        )
        
        # 5. EVALUATION & VISUALIZATION
        logger.info("Phase 5: Generating Assets...")
        viz = ModelVisualizer()
        
        best_model = all_trained_models["LightGBM"]
        viz.evaluate_and_plot(best_model, X_test_final, y_test, model_name="LightGBM")
        viz.extract_feature_importance(best_model, feature_names, model_name="LightGBM")
        viz.generate_benchmark_csv(all_trained_models, X_test_final, y_test)
        
    logger.info("Pipeline execution completed successfully!")
