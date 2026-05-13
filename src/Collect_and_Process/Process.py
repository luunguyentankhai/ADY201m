import config
import pandas as pd
from sklearn.preprocessing import StandardScaler

class Pre:
    def __init__(self):
        self.Data = config.Root_Data_File
        self.df = pd.read_csv(self.Data)
    
    def Read_info(self):
        print(self.df.info())
        print(self.df.head(5))
        print(self.df.tail(5))
   
    def Normalization(self):
        # Norm TimeStamp 
        self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'])

        self.df['Transaction_Hour'] = self.df['Timestamp'].dt.hour
        self.df['Transaction_DayOfWeek'] = self.df['Timestamp'].dt.dayofweek

        self.df = self.df.drop('Timestamp', axis=1)

        # Norm Device_type and Location using One-Hot Encoding
        self.df = pd.get_dummies(self.df, columns=['Device_Type','Location'], drop_first=True)

        # Norm Transaction_Amount and Daily_Transaction_Count

        scaler = StandardScaler()

        numberical_cols = ['Transaction_Amount', 'Daily_Transaction_Count']

        self.df[numberical_cols] = scaler.fit_transform(self.df[numberical_cols])

        print(self.df.head(5))

        return self.df

    def Imbalance_Check(self):
        pass


