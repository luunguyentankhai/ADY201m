import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import make_scorer, average_precision_score
from src.config.logs_config import setup_log, auto_logger
from src.config.dir_config import Process_Dir

logger = setup_log(name="Model_Evaluator", filename="Models")

@auto_logger(logger)
def model_comparison_evaluate(classifiers, X, y, n_splits=5):
    """Optimized Stratified K-Fold CV. Computes all metrics simultaneously."""
    logger.info(f"Starting {n_splits}-Fold Cross-Validation for {len(classifiers)} models.")
    
    skfold = StratifiedKFold(
            n_splits=n_splits, 
            shuffle=True, 
            random_state=42
            )
    pr_auc_scorer = make_scorer(
            average_precision_score, 
            response_method='predict_proba'
            )
    
    scoring_metrics = {
        'precision': 'precision', 
        'recall': 'recall', 
        'f1': 'f1', 
        'roc_auc': 'roc_auc', 
        'pr_auc': pr_auc_scorer
    }
    
    results_list = []
    
    for name, model in classifiers.items():
        logger.info(f"Evaluating {name} (K-Fold)...")
        # Nút thắt hiệu năng: Chạy cross_validate 1 lần duy nhất cho 5 metrics, n_jobs=1 để tránh đụng độ luồng
        cv_results = cross_validate(
            estimator=model, 
            X=X, 
            y=y, 
            scoring=scoring_metrics, 
            cv=skfold, 
            n_jobs=1, 
            return_train_score=False
        )
        
        model_result = {"Model": name}
        for metric in scoring_metrics.keys():
            mean_score = cv_results[f'test_{metric}'].mean()
            std_score = cv_results[f'test_{metric}'].std()
            model_result[f"{metric}_mean"] = round(mean_score, 4)
            model_result[f"{metric}_std"] = round(std_score, 4)
            
        results_list.append(model_result)
        
    df_results = pd.DataFrame(results_list)
    logger.info(f"\n{'='*60}\nCROSS-VALIDATION RESULTS:\n{df_results.to_string(index=False)}\n{'='*60}")
    
    csv_path = Process_Dir / "7_models_benchmark.csv"
    df_results.to_csv(csv_path, index=False)
    logger.info(f"Save result 7 models at: {csv_path}")

    return df_results
