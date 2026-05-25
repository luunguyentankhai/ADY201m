import pandas as pd
import numpy as np
from src.config.dir_config import Process_Dir
from src.config.logs_config import setup_log, auto_logger

logger = setup_log(name="EDA", filename="app")

class EDA:
    def __init__(self):
        self.df = pd.read_csv(Process_Dir / "Cleaned_Data.csv")
        self.df = self.df.drop(columns= "isflaggedfraud")
        self.df['type'] = self.df['type'].astype('category')

    @auto_logger(logger)
    def Pre_Read(self):

        print(f"{'='*50}")
    
        print(self.df.head(10))
    
        print(f"{'='*50}")
    
        print(self.df.tail(10))
    
        print(f"{'='*50}")
    
        print(self.df.info())

        print(f"{'='*50}")

    @auto_logger(logger)
    def Describe(self):

        print(self.df.describe(include= [np.number]).T) 
    
        print(f"{'='*50}")

        print(self.df.describe(include= ['str', 'category']).T)

        print(f"{'='*50}")


    @auto_logger(logger)
    def value_count(self):
    
        print(self.df['name_orig'].value_counts())

        print(f"{'='*50}")
    
        print(self.df['name_dest'].value_counts())

        print(f"{'='*50}")
    
        for i in self.df.select_dtypes(include= "category").columns:
            print(self.df[i].value_counts())

        print(f"{'='*50}")

    


    


