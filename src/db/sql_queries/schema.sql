-- Users Table
CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY
);

-- Transactions Table
CREATE TABLE transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES users(user_id) ON DELETE CASCADE,
    
    transaction_amount NUMERIC(15, 2),
    transaction_type VARCHAR(50),
    timestamp TIMESTAMP,
    account_balance NUMERIC(15, 2),
    device_type VARCHAR(50),
    location VARCHAR(100),
    merchant_category VARCHAR(100),
    
    ip_address_flag SMALLINT DEFAULT 0,
    previous_fraudulent_activity SMALLINT DEFAULT 0,
    daily_transaction_count INTEGER,
    avg_transaction_amount_7d NUMERIC(15, 2),
    failed_transaction_count_7d INTEGER,
    
    card_type VARCHAR(50),
    card_age INTEGER,
    transaction_distance NUMERIC(15, 2),
    authentication_method VARCHAR(50),
    risk_score NUMERIC(8, 4),
    
    is_weekend SMALLINT DEFAULT 0,
    fraud_label SMALLINT DEFAULT 0
);

-- INDEX
CREATE INDEX idx_txn_user_time ON transactions(user_id, timestamp);
CREATE INDEX idx_txn_device_loc ON transactions(device_type, location);
CREATE INDEX idx_txn_fraud_only ON transactions(fraud_label) WHERE fraud_label = 1;
