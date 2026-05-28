import pandas as pd
from src.config import db_config
from src.config.logs_config import setup_log, auto_logger

logger = setup_log(name="DB_Manager", filename="DataBase")

@auto_logger(logger)
def fetch_feature_store():
    """Extracts the entire Feature Store from PostgreSQL."""
    logger.info("Connecting to PostgreSQL to fetch vw_model_features...")
    engine = db_config.db_engine()
    
    try:
        df = pd.read_sql("SELECT * FROM vw_model_features", con=engine)
        logger.info(f"Successfully loaded dataset. Shape: {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Database connection or query failed: {e}")
        return None
