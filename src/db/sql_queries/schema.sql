DROP TABLE IF EXISTS fraud_detection;
CREATE TABLE fraud_detection (
    id BIGSERIAL PRIMARY KEY,
    
    step INTEGER NOT NULL,
    type VARCHAR(20) NOT NULL,
    amount NUMERIC(15, 2) CHECK (amount >= 0), 
    
    name_orig VARCHAR(50),
    oldbalance_orig NUMERIC(15, 2),
    newbalance_orig NUMERIC(15, 2),
    
    name_dest VARCHAR(50),
    oldbalance_dest NUMERIC(15, 2),
    newbalance_dest NUMERIC(15, 2),
    
    is_fraud INTEGER CHECK (is_fraud IN (0, 1)),
    
    isflaggedfraud INTEGER CHECK (isflaggedfraud IN (0, 1)),
    
    hour_of_day INTEGER GENERATED ALWAYS AS (MOD(step, 24)) STORED,
    day_of_month INTEGER GENERATED ALWAYS AS ((step / 24) + 1) STORED
);

CREATE INDEX idx_transactions_type ON fraud_detection(type);
CREATE INDEX idx_transactions_name_dest ON fraud_detection(name_dest);
CREATE INDEX idx_transactions_is_fraud ON fraud_detection(is_fraud);
