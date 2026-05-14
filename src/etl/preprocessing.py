# TODO: sửa lại cái file preprocessing nha cái này để tạm thôi

def Normalization(self):
        self.NA_Check()
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
