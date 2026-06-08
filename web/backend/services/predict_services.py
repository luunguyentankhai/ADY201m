import io
from time import struct_time
import pandas as pd
import numpy as np
from web.backend import models
from web.backend.config.logs_config import logger
from web.backend.core.ml_manager import ml_manager

from web.backend.services.model_preprocessing import preprocessing
from web.backend.services.eda_service import eda_service
from web.backend.models.transaction_schema import TransactionInput

class PredictService:
    def process_and_predict(self, file_content: bytes) -> dict:
        try:
            logger.info(f"Read CSV on buffer")
            df = pd.read_csv(io.BytesIO(file_content))

            logger.info(f"Preprocessing cleaning")
            df_clean = preprocessing.clean_data(df)
            
            logger.info(f"Preprocessing add_features")
            df_enriched = preprocessing.add_features(df_clean)
            
            logger.info(f"Calculating EDA")
            eda_result = eda_service.excute_eda(df_enriched)

            logger.info(f"Preprocessing Models prepare")
            X_ready = preprocessing.prepare_for_model(df_enriched)

            # TODO: làm sau khi xong frontend
            logger.info(f"Push data into LightGBM Models")

            model = ml_manager.models.get("LightGBM")
            if not model:
                raise ValueError(f"Not Found Models")

            predictions = model.predict(X_ready)

            fraud_count = int(np.sum(predictions))
            total_rows = len(predictions)
            fraud_rate = (fraud_count / total_rows) * 100

            return {
                    "summary": {
                        "total_transactions": total_rows,
                        "fraud_detected": fraud_count,
                        "fraud_rate_percent": round(fraud_rate,2)
                    },
                    "eda_data": eda_result
                }

        except Exception as e:
            logger.error(f"[PredictService] Error: {str(e)}")
            raise e

    # TODO: page check 1 line input
    # TODO: connect docker db into frontend
    def predict_single(self, tx_data: TransactionInput) -> dict:
        try:
            logger.info(f"Processing single transaction from: {tx_data.nameOrig}")

            df = pd.DataFrame([tx_data.model_dump()])
            
            df_clean = preprocessing.clean_data(df)
            df_enriched = preprocessing.add_features(df_clean)
            X_ready = preprocessing.prepare_for_model(df_enriched)

            target_models = ["LightGBM", "XGBoost", "CatBoost", "Random_Forest", "Logistic_Regression_SGD"]
            results = []
            fraud_vote = 0

            for m_name in target_models:
                model = ml_manager.models.get(m_name)
                if not model:
                    logger.warning(f"Model '{m_name}' is not loaded")
                    continue
                
                is_fraud = int(model.predict(X_ready)[0])

                try:
                    prob = float(model.predict_prob(X_ready)[0][1])
                except AttributeError:
                    prob = float(is_fraud)

                if is_fraud == 1:
                    fraud_vote += 1

                results.append({
                    "model_name": m_name,
                    "is_fraud": bool(is_fraud),
                    "confidence_score": round(prob *100,2)
                    })

            active_models_count = len(results)
            if active_models_count == 0:
                raise ValueError("No models available for prediction.")
                
            is_final_fraud = fraud_vote >= (active_models_count / 2)

            logger.info(f"Ensemble Voting: {fraud_vote}/{active_models_count} flagged as FRAUD.")

            return {
                "transaction_id": f"{tx_data.nameOrig}_to_{tx_data.nameDest}",
                "final_decision": "FRAUD" if is_final_fraud else "SAFE",
                "voting_ratio": f"{fraud_vote}/{active_models_count}",
                "model_details": results
                }
        except Exception as e:
            logger.error(f"[PredictService - Single] Critical Error: {str(e)}")
            raise e



predict_service = PredictService()
