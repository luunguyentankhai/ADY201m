import io
from time import struct_time
import pandas as pd
import numpy as np
from web.backend.config.logs_config import logger
from web.backend.core.ml_manager import ml_manager

class PredictService:
    def process_and_predict(self, file_content: bytes) -> dict:
        try:
            logger.info(f"Read CSV on buffer")
            df = pd.read_csv(io.BytesIO(file_content))

            # TODO: làm sau khi xong frontend
            # logger.info(f"Calculating EDA")
            # eda_result = self._excute_eda(df)

            logger.info(f"Preprocessing")
            X_ready = self._excute_preprocessing(df)

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
                    # "eda_data": eda_results
                }

        except Exception as e:
            logger.error(f"[PredictService] Error: {str(e)}")
            raise e

    # def _excute_eda(self, df: pd.DataFrame) -> dict:
    #     pass
    
    def _excute_preprocessing(self, df: pd.DataFrame) -> pd.DataFrame:
        df_clean = df.copy()
        df_clean = self.__cleaning(df_clean)

        num_cols = ['amount', 'oldbalance_orig', 'newbalance_orig', 'oldbalance_dest','newbalance_dest']
        for col in num_cols:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].fillna(0)

        # Hour_of_day
        if 'step' in df_clean.columns:
            df_clean['hour_of_day'] = df_clean['step'] % 24
            df_clean = df_clean.drop(columns=['step'])
        

        df_clean['is_amount_zero'] = (df_clean.get('amount', 0) == 0).astype(int)
        
        df_clean['error_balance_orig']= (
                    df_clean.get('newbalance_orig', 0) + 
                    df_clean.get('amount', 0) -
                    df_clean.get('oldbalance_orig', 0)
                )

        df_clean['error_balance_dest']=(
                    df_clean.get('oldbalance_dest', 0) + 
                    df_clean.get('amount', 0) -
                    df_clean.get('newbalance_dest', 0)
                )

        if 'name_dest' in df_clean.columns:
            df_clean['is_merchant_dest']= df_clean['name_dest'].str.startswith('M', na=False).astype(int)
        else:
            df_clean['is_merchant_dest']= 0

        if 'type' in df_clean.columns:
            df_clean['type_cash_out'] = (df_clean['type'] == 'CASH_OUT').astype(int)
            df_clean['type_debit'] = (df_clean['type'] == 'DEBIT').astype(int)
            df_clean['type_payment'] = (df_clean['type'] == 'PAYMENT').astype(int)
            df_clean['type_transfer'] = (df_clean['type'] == 'TRANSFER').astype(int)

        df_clean['is_orig_empty_after']=(df_clean.get('newbalance_orig', 0) == 0).astype(int)
        df_clean['is_dest_empty_before']=(df_clean.get('oldbalance_dest', 0) == 0).astype(int)

        cols_drop = ['type', 'name_orig', 'name_dest', 'is_fraud', 'isflaggedfraud']
        df_clean = df_clean.drop(columns=[c for c in cols_drop if c in df_clean.columns])

        if ml_manager.scaler:
            df_clean[df_clean.columns] = ml_manager.scaler.transform(df_clean)

        return df_clean
    
    def __cleaning(self, df: pd.DataFrame) -> pd.DataFrame:
        crit_cols = ['amount', 'nameOrig', 'nameDest', 'isFraud']
        float_cols = ['amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest']
        
        # Lower columns name
        rename_map = {
            'nameOrig': 'name_orig',
            'oldbalanceOrg': 'oldbalance_orig',
            'newbalanceOrig': 'newbalance_orig',
            'nameDest': 'name_dest',
            'oldbalanceDest': 'oldbalance_dest',
            'newbalanceDest': 'newbalance_dest',
            'isFraud': 'is_fraud',
            'isFlaggedFraud': 'isflaggedfraud'
        }

        df = df.rename(columns=rename_map)
        df.columns = df.columns.str.lower()
        
        # Clean text
        str_cols = df.select_dtypes(include=["object", "string"]).columns
        for col in str_cols:
            df[col] = df[col].astype(str).str.strip()
        

        # Handle dup
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            logger.warning(f"Found {dup_count} duplicated row")
            df = df.drop_duplicates()
        
        # Handle missing values
        if df.isna().sum().sum() > 0:
            cols_check = [col for col in crit_cols if col in df.columns]
            df = df.dropna(subset=cols_check)
            
            cols_fill = [col for col in float_cols if col in df.columns]
            df[cols_fill] = df[cols_fill].fillna(0)

        return df


predict_service = PredictService()
