from src.config.db_config import db_engine
import pandas as pd
from sqlalchemy import text

def get_df(columns, conditions=None, table_name="transactions"):
    engine = db_engine()

    if columns == "*" or columns==["*"]:
        cols_str = "*"
    else:
        cols_str = ", ".join(columns)

    query= f"SELECT {cols_str} FROM {table_name}"

    if conditions:

        query+= f"WHERE {conditions}"

    try:
        
        df = pd.read_sql(text(query), con=engine)
        return df
    except Exception as e:
        print(f"ERROR: {e}")
        return None

