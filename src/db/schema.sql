-- Users Table
CREATE TABLE IF NOT EXISTS users (
    User_ID VARCHAR(50) PRIMARY KEY,
    Account_Balance NUMERIC(15, 2),
    Previous_Fraudulent_Activity SMALLINT DEFAULT 0
);

-- Cards Table
CREATE TABLE IF NOT EXISTS Cards (
    Card_ID SERIAL PRIMARY KEY,
    User_ID VARCHAR(50) REFERENCES users(User_ID) ON DELETE CASCADE,
    Card_Type VARCHAR(50),
    Issue_Date DATE 
);

-- Transactions Table
CREATE TABLE IF NOT EXISTS Transactions (
    Transaction_ID VARCHAR(50) PRIMARY KEY,
    User_ID VARCHAR(50) REFERENCES users(User_ID) ON DELETE CASCADE,
    Card_ID INTEGER REFERENCES cards(Card_ID) ON DELETE CASCADE,
    Transaction_Amount NUMERIC(15, 2),
    Transaction_Type VARCHAR(50),
    Timestamp TIMESTAMP,
    Device_Type VARCHAR(50),
    Location VARCHAR(100),
    Merchant_Category VARCHAR(100),
    IP_Address_Flag SMALLINT DEFAULT 0,
    Transaction_Distance NUMERIC(15, 2),
    Authentication_Method VARCHAR(50),
    Risk_Score NUMERIC(5, 4),
    Fraud_Label SMALLINT DEFAULT 0
);

-- INDEX
CREATE INDEX IF NOT EXISTS idx_txn_user_time ON transactions(User_ID, Timestamp);
CREATE INDEX IF NOT EXISTS idx_txn_device_location ON transactions(Device_Type, Location);
CREATE INDEX IF NOT EXISTS idx_txn_fraud ON transactions(Fraud_Label) WHERE Fraud_Label = 1;
