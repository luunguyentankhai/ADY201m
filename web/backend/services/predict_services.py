import io
from time import struct_time
import pandas as pd
import numpy as np
from web.backend.config.logs_config import logger
from web.backend.core.ml_manager import ml_manager

from web.backend.services.model_preprocessing import preprocessing
from web.backend.services.eda_service import eda_service

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


predict_service = PredictService()
