import pandas as pd
from src.config import dir_config
from src.etl.cleaner import DataCleaner
from src.config.logs_config import setup_log, auto_logger
from src.db.init_db import initialize_and_seed

logger = setup_log(name="Main_Pipeline", filename="app")

class DataPipeline:    
    @auto_logger(logger)
    def Cleaning(self):
        logger.info(f"Cleaning Data...")
        cleaner = DataCleaner()
        
        cleaner_file_path = cleaner.run()

        return cleaner_file_path

    @auto_logger(logger)
    def Run_Pipeline(self):
        # ===
        logger.info(f"Starting Pull and Push data")
        try:
            cleaning = self.Cleaning()

            logger.info(f"Pushing data to DB")
            total_row = initialize_and_seed(
                    table_name="fraud_detection",
                    chunk_size=100000,
                    force_reset=True,
                    data_src=cleaning
                    )
            logger.info(f"PIPELINE SUCCESSFUL! Sync {total_row:,} rows")

        except Exception as e:
            logger.error(f"Pipeline Fail: {e}")
            raise
        



