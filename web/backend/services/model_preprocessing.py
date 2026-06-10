import pandas as pd
from web.backend.core.ml_manager import ml_manager
from web.backend.config.logs_config import logger

class Preprocessing:
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:

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
    
    def add_features(self, df: pd.DataFrame) -> pd.DataFrame:

        df_feat = df.copy()

        if 'step' in df_feat.columns:
            df_feat['hour_of_day']= df_feat['step'] % 24

        df_feat['error_balance_orig']= (
                    df_feat.get('newbalance_orig', 0) + 
                    df_feat.get('amount', 0) -
                    df_feat.get('oldbalance_orig', 0)
                )

        df_feat['error_balance_dest']=(
                    df_feat.get('oldbalance_dest', 0) + 
                    df_feat.get('amount', 0) -
                    df_feat.get('newbalance_dest', 0)
                )

        if 'name_dest' in df_feat.columns:
            df_feat['is_merchant_dest']= df_feat['name_dest'].str.startswith('M', na=False).astype(int)
        else:
            df_feat['is_merchant_dest']= 0

        return df_feat

    def prepare_for_model(self, df: pd.DataFrame) -> pd.DataFrame:

        df_model = df.copy() 

        if 'type' in df_model.columns:
            df_model['type_cash_out'] = (df_model['type'] == 'CASH_OUT').astype(int)
            df_model['type_debit'] = (df_model['type'] == 'DEBIT').astype(int)
            df_model['type_payment'] = (df_model['type'] == 'PAYMENT').astype(int)
            df_model['type_transfer'] = (df_model['type'] == 'TRANSFER').astype(int)

        cols_drop = ['step', 'type', 'name_orig', 'name_dest', 'is_fraud', 'isflaggedfraud']
        df_model = df_model.drop(columns=[c for c in cols_drop if c in df_model.columns])

        if ml_manager.scaler:
            try:
                expected_features = ml_manager.scaler.feature_names_in_

                df_model = df_model[expected_features]


                df_model[expected_features] = ml_manager.scaler.transform(df_model)
            
            except KeyError as ke:
                logger.error(f"Missing columns required by Scaler: {ke}")
                raise ValueError(f"Feature mismatch. Check backend logs for missing columns.")
            except Exception as e:
                logger.error(f"Scaler transformation failed: {e}")
                raise e
        return df_model

preprocessing = Preprocessing()


        
