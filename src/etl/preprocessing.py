import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from src.config.dir_config import Models_Dir
from src.config.logs_config import setup_log, auto_logger

logger = setup_log(name="Data_Preprocessing", filename="Models")

class DataSplitter:
    def __init__(self, target_col='is_fraud', random_state=42):
        self.target_col = target_col
        self.random_state = random_state

    @auto_logger(logger)
    def split_train_val_test(self, df):
        """Executes a 70/15/15 split for Train, Validation, and Test sets."""
        logger.info("Executing Data Splitter. Dropping 'step' column as per Data Contract.")
        if 'step' in df.columns:
            X = df.drop(columns=['step'])
        else:
            X = df.copy()

        y = X.pop(self.target_col)
        
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, 
            y, 
            test_size=0.15, 
            stratify=y, 
            random_state=self.random_state
        )

        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, 
            y_temp, 
            test_size=0.1765, 
            stratify=y_temp, 
            random_state=self.random_state
        )

        return X_train, X_val, X_test, y_train, y_val, y_test

    @auto_logger(logger)
    def smart_undersample(self, X_train, y_train, target_normal_size=1_000_000):
        """Reduces majority class while preserving 100% of minority class."""
        X_fraud, y_fraud = X_train[y_train == 1], y_train[y_train == 1]
        X_normal, y_normal = X_train[y_train == 0], y_train[y_train == 0]
        
        X_normal_sampled = X_normal.sample(
                n=target_normal_size, 
                random_state=self.random_state)
        y_normal_sampled = y_normal.sample(
                n=target_normal_size, 
                random_state=self.random_state)
        
        X_train_sampled = pd.concat([X_fraud, X_normal_sampled])
        y_train_sampled = pd.concat([y_fraud, y_normal_sampled])
        return X_train_sampled, y_train_sampled

class FeatureScaler:
    def __init__(self):
        self.scaler = StandardScaler()

    @auto_logger(logger)
    def scale_and_save(self, X_train, X_val, X_test):
        """Fits StandardScaler on Train, transforms all splits, and saves to disk."""
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(X_test)
        
        scaler_file = Models_Dir / "fraud_scaler.pkl"
        joblib.dump(self.scaler, scaler_file)
        
        return X_train_scaled, X_val_scaled, X_test_scaled
