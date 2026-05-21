from sqlalchemy import text
from src.config.db_config import db_engine
from src.config.logs_config import setup_log,auto_logger

logger = setup_log(name="PostgresManager", filename="app")

class PostgresManager:
    def __init__(self):
        self.engine = db_engine()

    @auto_logger(logger)
    def bulk_insert_chunk(self, df, table_name):
        if df.empty:
            logger.warning(f"DataFrame is empty, skip bulk_insert for table {table_name}")
            return
        with self.engine.begin() as conn:
            df.to_sql(
                name=table_name,
                con=conn,
                if_exists='append',
                index=False,
                method='multi'
            )

    @auto_logger(logger)
    def upsert(self, df, table_name, pk_column, chunk_size=50000):
        if df.empty:
            logger.warning(f"DataFrame is empty, skip upsert for table {table_name}")
            return

        temp_table = f"stg_{table_name}"
        columns_list = [f"{col}" for col in df.columns]
        columns = ", ".join(columns_list)

        upsert_sql = text(f"""
                INSERT INTO {table_name} ({columns})
                SELECT {columns} FROM {temp_table}
                ON CONFLICT ({pk_column}) DO NOTHING;
            """)

            
        with self.engine.begin() as conn:
            df.to_sql(
                    name=temp_table, 
                    con=conn, 
                    if_exists='replace', 
                    index=False, 
                    chunksize=chunk_size
                )
                
            conn.execute(upsert_sql)

            conn.execute(text(f"DROP TABLE {temp_table}"))

        logger.info(f"Data push on {table_name} safe")

        with self.engine.connect() as conn:
            conn.execution_options(isolation_level="AUTOCOMMIT").execute(text(f"VACUUM {table_name};"))

        logger.info(f"Running VACUUM clean table {table_name}")

       
