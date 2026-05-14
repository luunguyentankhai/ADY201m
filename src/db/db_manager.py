from sqlalchemy import text
from src.config.db_config import db_engine

class PostgresManager:
    def __init__(self):
        self.engine = db_engine()

    def upsert(self, df, table_name, pk_column, chunk_size=10000):
        if df.empty:
            print("Data is empty")
            return

        temp_table = f"stg_{table_name}"

        try:
            
            with self.engine.begin() as conn:
                df.to_sql(temp_table, con=conn, if_exists='replace', index=False, chunksize=chunk_size)
                columns = ", ".join([f"{col}" for col in df.columns])

                upsert_sql = text(f"""
                    INSERT INTO {table_name} ({columns})
                    SELECT {columns} FROM {temp_table}
                    ON CONFLICT ({pk_column}) DO NOTHING;
                """)

                conn.execute(upsert_sql)

                conn.execute(text(f"DROP TABLE {temp_table}"))

            print(f"Data push on {table_name} safe")

        except Exception as e:
            print(f"ERROR: {e}")
