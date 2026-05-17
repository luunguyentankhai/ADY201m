SELECT
    device_type,
    location,
    COUNT(*) AS total_txns,
    SUM(fraud_label) AS fraud_txns,
    ROUND(AVG(fraud_label) * 100,2) AS fraud_rate_percentage
FROM transactions
GROUP BY device_type, location
HAVING COUNT(*) > 10
ORDER BY fraud_rate_percentage DESC;
