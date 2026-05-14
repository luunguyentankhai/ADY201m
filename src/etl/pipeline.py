import pandas as pd
from src.config import dir_config
from src.etl.cleaner import lower_columns_name, fix_check_missing,format_datetime,clean_text_data
from src.db.db_manager import PostgresManager

class DataPipeline:
    def __init__(self):
        self.rawpath = dir_config.Root_Data_File
        self.df = pd.read_csv(self.rawpath)
        self.db = PostgresManager()
    
    def Run_Pipeline(self):

        # ===
        df = self.df
        print(df.head(5))
        print(df.info())

        # ===
        df = lower_columns_name(df)
        df = format_datetime(df)
        df = clean_text_data(df)
        df = fix_check_missing(df)

        # ===

        df_users = df[["user_id"]].drop_duplicates()
        self.db.upsert(df_users, table_name='users', pk_column="user_id")

        # ---
        self.db.upsert(df, table_name='transactions', pk_column="transaction_id")


# TODO: làm tiền xử lý và gọi nó trong pipeline.py tên của file tiền xử lý là preprocessing


