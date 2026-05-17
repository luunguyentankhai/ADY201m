SELECT 
    transaction_id,
    user_id,
    timestamp,
    transaction_amount,
    avg_transaction_amount_7d,
    daily_transaction_count,
    transaction_distance,
    fraud_label
FROM transactions
WHERE 
    transaction_amount > (avg_transaction_amount_7d * 3)
    OR daily_transaction_count > 10                     
    OR transaction_distance > 1000                      
ORDER BY timestamp DESC;
