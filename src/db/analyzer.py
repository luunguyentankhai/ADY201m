import pandas as pd
from src.config import db_config, dir_config
from sqlalchemy import text

class FraudAnalyzer:
    def __init__(self):
        self.engine = db_config.db_engine()
        self.sql_dir = dir_config.sql_dir

    def _execute_sql(self, filename):
        file_path = self.sql_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Filename does not exist: {file_path}")

        query = file_path.read_text(encoding="utf-8")

        try:
            df = pd.read_sql(text(query), con=self.engine)
            return df
        except Exception as e:
            print(f"ERROR: {e}\n {filename}")
            return None

    def get_fraud_rate(self):
        print(f"Analyzing fraud rate")
        return self._execute_sql("get_fraud_rate.sql")

    def get_anomalies(self):
        print(f"Scanning for anomalous transactions")
        return self._execute_sql("get_anomalies.sql")

    def get_ml_feature(self):
        print(f"Fetching Feature Table for ML")

        df_feature = self._execute_sql("get_feature.sql")
        if df_feature is not None:
            return df_feature
        return df_feature

    def get_fraud_patterns(self):
        print(f"Detecting recurring fraud patterns")
        return self._execute_sql("get_patterns.sql")

