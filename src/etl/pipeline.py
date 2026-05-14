import pandas as pd
from src.config import dir_config
from src.etl.cleaner import lower_columns_name, fix_check_missing,format_datetime,clean_text_data

class DataPipeline:
    def __init__(self):
        self.rawpath = dir_config.Root_Data_File
        self.df = pd.read_csv(self.rawpath)
    
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

        print(df.head(5))
