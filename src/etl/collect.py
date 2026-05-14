import kagglehub as kg
from pathlib import Path
import pandas as pd
from src.config import dir_config
import stat
import shutil

class Data_Collection:
    def Collection(self):
        try:
            Path_Install = dir_config.Raw_Dir

            Cache_path = Path(kg.dataset_download("samayashar/fraud-detection-transactions-dataset"))

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
