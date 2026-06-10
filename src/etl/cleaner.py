import pandas as pd
import numpy as np
from src.config.logs_config import setup_log, auto_logger
from src.config.dir_config import Root_Data_File, Process_Dir

logger = setup_log(name="Data_Cleaner", filename="data")

class DataCleaner:
    def __init__(self, chunk_size=100000):
        self.chunk_size = chunk_size
        self.raw_path = Root_Data_File
        self.Processed_path = Process_Dir / "Cleaned_Data.csv"

        self.crit_cols = ['amount', 'nameOrig', 'nameDest', 'isFraud']
        self.float_cols = ['amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest']

    def _lower_columns_name(self, df):
        rename_map = {
            'nameOrig': 'name_orig',
            'oldbalanceOrg': 'oldbalance_orig',
            'newbalanceOrig': 'newbalance_orig',
            'nameDest': 'name_dest',
            'oldbalanceDest': 'oldbalance_dest',
            'newbalanceDest': 'newbalance_dest',
            'isFraud': 'is_fraud'
        }
        df = df.rename(columns=rename_map)
        df.columns = df.columns.str.lower()
        return df

    def _clean_text_data(self, df):
        str_cols = df.select_dtypes(include=["object", "string"]).columns
        for col in str_cols:
            df[col] = df[col].astype(str).str.strip()
        return df

    def _handle_duplicates(self, df):
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            logger.warning(f"Found {dup_count} duplicate row. Deleting...")
            df = df.drop_duplicates()
        return df

    def _handle_missing_values(self, df):
        if df.isna().sum().sum() > 0:
            cols_check = [col for col in self.crit_cols if col in df.columns]
            df = df.dropna(subset=cols_check)
            
            cols_fill = [col for col in self.float_cols if col in df.columns]
            df[cols_fill] = df[cols_fill].fillna(0)
        return df

    def _process_chunk(self, chunk):
        
        chunk = self._lower_columns_name(chunk)

        chunk = self._clean_text_data(chunk)

        chunk = self._handle_duplicates(chunk)

        chunk = self._handle_missing_values(chunk)

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
