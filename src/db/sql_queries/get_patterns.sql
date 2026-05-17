SELECT 
    merchant_category,
    transaction_type,
    authentication_method,
    device_type,
    COUNT(*) AS fraud_occurrences,
    ROUND(AVG(transaction_amount), 2) AS avg_stolen_amount
FROM transactions
WHERE fraud_label = 1
GROUP BY 
    merchant_category,
    transaction_type,
    authentication_method,
    device_type
ORDER BY fraud_occurrences DESC
LIMIT 10;
