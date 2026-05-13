from pathlib import Path

Base_Dir = Path(__file__).resolve().parent

Data_Dir = Base_Dir / "data"

Data_Dir.mkdir(parents=True, exist_ok=True)

Root_Data_File = Data_Dir / "Data.csv"
