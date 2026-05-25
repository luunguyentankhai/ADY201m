import pandas as pd
from src.config import db_config, dir_config
from sqlalchemy import text
from src.config.logs_config import setup_log, auto_logger

logger = setup_log(name="SQL_queries", filename="DataBase")


class FraudAnalyzer:
    def __init__(self):
        self.engine = db_config.db_engine()
        self.sql_dir = dir_config.sql_dir 
    
    @auto_logger(logger)
    def _execute_sql(self, filename):
        file_path = self.sql_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Filename does not exist: {file_path}")

        query = file_path.read_text(encoding="utf-8")

        try:
            df = pd.read_sql(text(query), con=self.engine)
            return df
        except Exception as e:
            logger.error(f"ERROR: {e}\n {filename}")
            return None

    @auto_logger(logger)
    def _execute_ddl(self, filename):
        file_path = self.sql_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"SQL file missing: {file_path}")

        query = file_path.read_text(encoding="utf-8")

        try:
            with self.engine.begin() as conn:
                conn.execute(text(query))
            logger.info(f"Successfully executed DDL script: {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to execute DDL {filename}: {e}")
            return False
    
    @auto_logger(logger)
    def get_fraud_rate(self):
        logger.info(f"Analyzing fraud rate")
        return self._execute_sql("get_fraud_rate.sql")

    @auto_logger(logger)
    def get_anomalies(self):
        logger.info(f"Scanning for anomalous transactions")
        return self._execute_sql("get_anomalies.sql")

    @auto_logger(logger)
    def get_ml_feature(self):
        logger.info(f"Fetching Feature Table for ML")

        return self._execute_ddl("get_feature.sql")
         

    @auto_logger(logger)
    def get_fraud_patterns(self):
        logger.info(f"Detecting recurring fraud patterns")
        return self._execute_sql("get_patterns.sql")

