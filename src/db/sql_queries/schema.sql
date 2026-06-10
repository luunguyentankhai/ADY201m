DROP TABLE IF EXISTS fraud_detection CASCADE;
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
    
    hour_of_day INTEGER GENERATED ALWAYS AS (MOD(step, 24)) STORED
);

