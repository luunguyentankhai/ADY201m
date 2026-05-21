import kagglehub as kg
from pathlib import Path
import pandas as pd
from src.config import dir_config
from src.config.logs_config import setup_log, auto_logger
import stat
import shutil

logger = setup_log()

class Data_Collection:
    @auto_logger(logger)
    def Collection(self):
        try:
            Path_Install = dir_config.Raw_Dir

            Cache_path = Path(kg.dataset_download("rupakroy/online-payments-fraud-detection-dataset"))

            for csv_file in Cache_path.rglob('*.csv'):
                target = Path_Install / "Data.csv"

                if target.exists():
                    target.chmod(target.stat().st_mode | stat.S_IWRITE)

                shutil.copyfile(csv_file, target)
                target.chmod(target.stat().st_mode | stat.S_IWRITE)

        except Exception as e:
            print(f"Error : {e}")
        finally:
            pass
