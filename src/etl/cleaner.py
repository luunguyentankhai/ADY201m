import pandas as pd
import numpy as np
from src.config.logs_config import setup_log, auto_logger
from src.config.dir_config import Root_Data_File, Process_Dir

logger = setup_log(name="Data_Cleaner", filename="app")

class DataCleaner:
    def __init__(self, chunk_size=100000):
        self.chunk_size = chunk_size
        self.raw_path = Root_Data_File
        self.Processed_path = Process_Dir / "Cleaned_Data.csv"

        self.crit_cols = ['amount', 'nameOrig', 'nameDest', 'isFraud']
        self.float_cols = ['amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest']

    def _clean_text_data(self, df):
        str_cols = df.select_dtypes(include=["object", "string"]).columns
        for col in str_cols:
            df[col] = df[col].astype(str).str.strip()
        return df

    def _process_chunk(self, chunk):

        chunk = self._clean_text_data(chunk)

        chunk = chunk.drop_duplicates()

        cols_check = [col for col in self.crit_cols if col in chunk.columns]
        chunk = chunk.dropna(subset=cols_check)

        if 'amount' in chunk.columns:
            chunk = chunk[chunk['amount'] >= 0]

        return chunk
    
    @auto_logger(logger)
    def run(self):
        if not self.raw_path.exists():
            raise FileNotFoundError(f"Raw data file not found at: {self.raw_path}")

        if self.Processed_path.exists():
            self.Processed_path.unlink()
            logger.info("Deleted old Cleaned_Data.csv file.")

        logger.info("Starting data cleaning pipeline...")
        
        data_chunks = pd.read_csv(self.raw_path, chunksize=self.chunk_size)
        total_raw_rows = 0
        total_cleaned_rows = 0

        for i, chunk in enumerate(data_chunks):
            total_raw_rows += len(chunk)

            clean_chunk = self._process_chunk(chunk)

            clean_chunk.to_csv(self.Processed_path, mode='a', index=False, header=(i == 0))
            
            total_cleaned_rows += len(clean_chunk)
            logger.info(f"Processed {total_raw_rows:,} rows -> Retained {total_cleaned_rows:,} valid rows.")

        logger.info(f"Pipeline finished! Cleaned data saved to: {self.Processed_path}")
        logger.info(f"Total rows dropped (Garbage/Duplicates): {total_raw_rows - total_cleaned_rows:,}")
        
        return self.Processed_path
