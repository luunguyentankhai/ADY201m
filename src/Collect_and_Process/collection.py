import kagglehub as kg
from pathlib import Path
import pandas as pd
import config
import stat
import shutil

class Data_Collection:
    def Collection(self):
        try:
            Path_Install = config.Data_Dir
            Path_Install.mkdir(parents=True, exist_ok=True)

            Cache_path = Path(kg.dataset_download("samayashar/fraud-detection-transactions-dataset"))

            for csv_file in Cache_path.rglob('*.csv'):
                target = Path_Install / csv_file.name

                if target.exists():
                    target.chmod(target.stat().st_mode | stat.S_IWRITE)

                shutil.copyfile(csv_file, target)
                target.chmod(target.stat().st_mode | stat.S_IWRITE)

        except Exception as e:
            print(f"Error : {e}")
        finally:
            pass
