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

            logger.info(f"Calculating EDA")
            eda_result = self._excute_eda(df)

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
                    "eda_data": eda_result
                }

        except Exception as e:
            logger.error(f"[PredictService] Error: {str(e)}")
            raise e

    def _excute_eda(self, df: pd.DataFrame) -> dict:
        logger.info("Extracing EDA")

        eda_dict = {}

        target_col = 'isFraud' if 'isFraud' in df.columns else 'if_fraud' if 'is_fraud' in df.columns else None
        
        # TODO: mixed charts (bar + line) Khối lượng và tỉ lệ lừa đảo theo giao dịch
        if 'type' in df.columns:
            logger.info(f"Volume vs Fraud Rate by transaction")
            if target_col:
                grouped_type = df.groupby('type').agg(
                        total_volume=(target_col, 'count'),
                        fraud_case=(target_col, 'sum')
                        )
                grouped_type['fraud_rate']=(grouped_type['fraud_case'] / grouped_type['total_volume']) * 100
                eda_dict['mixed_volume_vs_rate']= {
                        "categories": grouped_type.index.tolist(),
                        "volume_bar": grouped_type['total_volume'].tolist(),
                        "rate_line": grouped_type['fraud_case'].round(2).tolist()
                        }
            else:
                type_counts=df['type'].value_counts()
                eda_dict['mixed_volume_vs_rate']={
                        "categories": type_counts.index.tolist(),
                        "volume_bar": type_counts.tolist(),
                        "rate_line": [0] * len(type_counts)
                        }


        # TODO: stacked bar chart phân bố dải tiền và mật độ lừa đảo

        if 'amount' in df.columns:
            logger.info("Amount ranges vs Fraud density")
            bins = [-1, 10000, 100000, 500000, float('inf')]
            labels = ['<10K', '10K - 100K', '100K - 500K', '>500K']
    
            df_temp = df.copy()
            df_temp['amount_range'] = pd.cut(df_temp['amount'], bins=bins, labels=labels)
            
            if target_col:
                grouped_amt = df_temp.groupby('amount_range', observed=False).agg(
                    total=(target_col, 'count'),
                    fraud=(target_col, 'sum')
                )
                grouped_amt['normal'] = grouped_amt['total'] - grouped_amt['fraud']
                eda_dict['stacked_amount_ranges'] = {
                    "categories": labels,
                    "normal_tx": grouped_amt['normal'].tolist(),
                    "fraud_tx": grouped_amt['fraud'].tolist()
                }
            else:
                amt_counts = df_temp['amount_range'].value_counts(sort=False)
                eda_dict['stacked_amount_ranges'] = {
                    "categories": labels,
                    "normal_tx": amt_counts.tolist(),
                    "fraud_tx": [0] * len(labels)
                }

        # TODO: multi-line chart hoạt động giao dịch theo giờ
        if 'step' in df.columns:
            logger.info("Hourly activity distribution")
            df_temp = df.copy()
            df_temp['hour'] = df_temp['step'] % 24
            

            if target_col:
                grouped_hour = df_temp.groupby('hour').agg(
                    total=(target_col, 'count'),
                    fraud=(target_col, 'sum')
                )
                grouped_hour['normal'] = grouped_hour['total'] - grouped_hour['fraud']
                
                # Đảm bảo luôn đủ 24 giờ kể cả khi không có dữ liệu tại khung giờ đó
                full_hours = pd.DataFrame(index=range(24))
                grouped_hour = full_hours.join(grouped_hour).fillna(0)
                
                eda_dict['multi_line_hourly'] = {
                    "hours": list(range(24)),
                    "normal_activity": grouped_hour['normal'].tolist(),
                    "fraud_activity": grouped_hour['fraud'].tolist()
                }
            else:
                hour_counts = df_temp['hour'].value_counts().sort_index()
                full_hours = pd.Series(0, index=range(24))
                full_hours.update(hour_counts)
                eda_dict['multi_line_hourly'] = {
                    "hours": list(range(24)),
                    "normal_activity": full_hours.tolist(),
                    "fraud_activity": [0] * 24
                }

        # TODO: Donut chart phân tích hành vi làm trống số dư
        col_new_bal = 'newbalanceOrig' if 'newbalanceOrig' in df.columns else 'newbalance_orig'
        if col_new_bal in df.columns:
            logger.info(f"Analyzing zero-balance behavior on origin accounts")
            zero_count = int((df[col_new_bal] == 0).sum())
            non_zero_count = int((df[col_new_bal] != 0).sum())
            eda_dict['zero_balance_behavior'] = {
                "Account_Empty": zero_count,
                "Account_Has_Money": non_zero_count
            }

        # TODO: Bar chart bất cân đối kế toán
        col_old_bal = 'oldbalanceOrg' if 'oldbalanceOrg' in df.columns else 'oldbalance_orig'
        if all(c in df.columns for c in ['amount', col_old_bal, col_new_bal]):
            logger.info(f"Detecting accounting anomalies based on balance changes")
            error_margin = (df[col_old_bal] - df[col_new_bal]) - df['amount']
            anomalies_count = int((error_margin.round(2) != 0).sum())
            normal_count = int(len(df) - anomalies_count)
            
            eda_dict['accounting_anomalies'] = {
                "Perfect_Math": normal_count,
                "Suspicious_Anomaly": anomalies_count
            }

        eda_dict['summary'] = {
            "total_rows": len(df),
            "total_volume": float(df['amount'].sum()) if 'amount' in df.columns else 0.0
        }

        logger.info(f"XONG")
        return eda_dict
            

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
