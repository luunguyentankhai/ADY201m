SELECT 
    day_of_month,
    hour_of_day,
    type AS transaction_type, 
    COUNT(id) AS total_transactions,
    SUM(is_fraud) AS fraud_transactions,
    ROUND((SUM(is_fraud) * 100.0) / COUNT(id), 4) AS fraud_rate_pct

FROM 
    fraud_detection

GROUP BY 
    day_of_month,
    hour_of_day,
    type

ORDER BY 
    fraud_rate_pct DESC,
    fraud_transactions DESC;
