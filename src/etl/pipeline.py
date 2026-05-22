import pandas as pd
from src.config import dir_config
from src.etl.cleaner import DataCleaner
from src.config.logs_config import setup_log, auto_logger
from src.db.init_db import initialize_and_seed

logger = setup_log(name="Main_Pipeline", filename="app")

class DataPipeline:
    def __init__(self):
        self.rawpath = dir_config.Root_Data_File
        self.df = pd.read_csv(self.rawpath)
    
    @auto_logger(logger)
    def Pre_read(self, df):
        print(df.head(10))
        print(f"{'='*50}")
        print(df.tail(10))
        print(f"{'='*50}")
        print(df.info())
        print(f"{'='*50}")
    
    @auto_logger(logger)
    def Cleaning(self):
        logger.info(f"Cleaning Data...")
        cleaner = DataCleaner()
        
        cleaner_file_path = cleaner.run()

        return cleaner_file_path

    @auto_logger(logger)
    def Run_Pipeline(self):

        # ===
        df = self.df
        self.Pre_read(df)
        
        # ===
        logger.info(f"Starting Pull and Push data")
        try:
            cleaning = self.Cleaning()

            logger.info(f"Pushing data to DB")
            total_row = initialize_and_seed(
                    table_name="Online_Payments_Fraud_Detection_Dataset",
                    chunk_size=100000,
                    force_reset=True,
                    data_src=cleaning
                    )
            logger.info(f"PIPELINE SUCCESSFUL! Sync {total_row:,} rows")

        except Exception as e:
            logger.error(f"Pipeline Fail: {e}")
            raise
        

# TODO: làm tiền xử lý và gọi nó trong pipeline.py tên của file tiền xử lý là preprocessing


