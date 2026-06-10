import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import (
    classification_report, roc_curve, auc, ConfusionMatrixDisplay,
    precision_score, recall_score, f1_score, roc_auc_score
)
from src.config.logs_config import setup_log, auto_logger
from src.config.dir_config import Assets_Dir, Process_Dir

logger = setup_log(name="Model_Visualizer", filename="Models")

class ModelVisualizer:
    def __init__(self):
        self.save_dir = Assets_Dir

    @auto_logger(logger)
    def evaluate_and_plot(self, model, X_test, y_test, model_name="Best_Model"):
        logger.info(f"Generating Classification Report & Plots for {model_name}...")
        
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        
        # 1. Classification Report
        report = classification_report(y_test, y_pred, labels=[0,1], target_names=['Non-Fraud', 'Fraud'])
        logger.info(f"\n{'='*55}\nClassification Report:\n{report}{'='*55}")

        # 2. Plots
        fig, ax = plt.subplots(1, 2, figsize=(20, 8))
        
        ax[0].set_title(f'Confusion Matrix - {model_name}')
        ConfusionMatrixDisplay.from_predictions(y_test, y_pred, colorbar=False, values_format='', cmap='PuBu', ax=ax[0])
        ax[0].grid(False)

        fpr, tpr, _ = roc_curve(y_test, y_prob)
        ax[1].set_title(f'ROC Curve - {model_name}')
        ax[1].plot(fpr, tpr, label='AUC = %0.3f' % auc(fpr, tpr), c='steelblue')
        ax[1].plot([0, 1], [0, 1], '--', c='lightsteelblue')
        ax[1].legend(loc='lower right')
        
        save_path = self.save_dir / f"{model_name}_Evaluation.png"
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close()
        logger.info(f"Plots saved to: {save_path}")

    @auto_logger(logger)
    def extract_feature_importance(self, model, feature_names, model_name="LightGBM"):
        if hasattr(model, 'feature_importances_'):
            importance_df = pd.DataFrame({
                'Feature': feature_names, 'Importance': model.feature_importances_
            }).sort_values(by='Importance', ascending=False)
            
            logger.info(f"\nTop Features:\n{importance_df.head(10).to_string(index=False)}")
            save_file = Process_Dir / f"{model_name}_Feature_Importance.csv"
            importance_df.to_csv(save_file, index=False)

    @auto_logger(logger)
    def generate_benchmark_csv(self, all_trained_models, X_test, y_test, save_name="7_models_benchmark.csv"):
        """Đánh giá nhanh 7 mô hình trên tập Test và xuất file CSV cho Web UI."""
        logger.info("Generating benchmark CSV for Web UI (Fast Evaluation on Test Set)...")
        results = []
        
        for name, model in all_trained_models.items():
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else y_pred
            
            results.append({
                "Model": name,
                "Precision": round(precision_score(y_test, y_pred, zero_division=0), 4),
                "Recall": round(recall_score(y_test, y_pred, zero_division=0), 4),
                "F1_Score": round(f1_score(y_test, y_pred, zero_division=0), 4),
                "ROC_AUC": round(roc_auc_score(y_test, y_prob), 4)
            })
            
        df_results = pd.DataFrame(results).sort_values(by="F1_Score", ascending=False)
        
        # Loại bỏ hoàn toàn os.path.join, dùng pathlib trỏ thẳng về Process_Dir
        csv_path = Process_Dir / save_name
        df_results.to_csv(csv_path, index=False)
        
        logger.info(f"Đã xuất thành công bảng điểm mô hình ra file: {csv_path}")
        return df_results
