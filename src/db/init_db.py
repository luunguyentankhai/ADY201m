import pandas as pd
import time
from sqlalchemy import text, exc
from src.config.dir_config import Root_Data_File, sql_dir
from src.config.db_config import db_engine
from src.config.logs_config import setup_log, auto_logger
from src.db.db_manager import PostgresManager

logger = setup_log(name="DB_init", filename="DataBase")

@auto_logger(logger)
<<<<<<< Updated upstream
def initialize_and_seed(table_name="Online_Payments_Fraud_Detection_Dataset",
=======
def initialize_and_seed(table_name="fraud_detection",
>>>>>>> Stashed changes
                        chunk_size=50000, 
                        force_reset=True,
                        data_src=Root_Data_File
                        ):

    engine = db_engine()
    manager = PostgresManager()
    
    schema_path = sql_dir / "schema.sql"
    
    logger.info(f"Checking schema.sql file and cleaning table '{table_name}'")
    
    if not schema_path.exists():
        raise FileNotFoundError(f"Not Found file schema.sql at {schema_path}")
        
    with open(schema_path, 'r', encoding="utf-8") as f:
        schema_sql = f.read()
        
    with engine.begin() as conn:
        conn.execute(text(schema_sql))
        
        if force_reset:
            conn.execute(text(f'TRUNCATE TABLE "{table_name}" RESTART IDENTITY CASCADE;'))
            
    logger.info("Structure ready, Storage spacious")
    
    logger.info("Starting push data into cloud DB")
    
    if not data_src.exists():
        raise FileNotFoundError(f"Not found data file at {data_src}")
        
    # Fix Typo: chunk_size
    data_chunks = pd.read_csv(data_src, chunksize=chunk_size)
    total_inserted_rows = 0
    
    max_retries = 3
    for chunk in data_chunks:
        for attempt in range(max_retries):
            try:
                manager.bulk_insert_chunk(chunk, table_name=table_name)
                total_inserted_rows += len(chunk)
                logger.info(f"Pushing success: {total_inserted_rows:,} rows")
                break                 
            except exc.OperationalError as e:
                logger.warning(f"SSL connection dropped at row {total_inserted_rows:,}. Retrying ({attempt + 1}/{max_retries}) in 5 seconds...")
                time.sleep(5)                 
        else:
            raise ConnectionError(f"Failed after {max_retries} retries due to persistent network issues. Process aborted.")
        
    logger.info("Done loop pushing data")
    return total_inserted_rows
