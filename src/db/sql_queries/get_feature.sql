DROP VIEW IF EXISTS vw_model_features;

CREATE VIEW vw_model_features AS
SELECT 
    step,
    COALESCE(amount, 0) AS amount,
    COALESCE(oldbalance_orig, 0) AS oldbalance_orig,
    COALESCE(newbalance_orig, 0) AS newbalance_orig,
    COALESCE(oldbalance_dest, 0) AS oldbalance_dest,
    COALESCE(newbalance_dest, 0) AS newbalance_dest,
    is_fraud,
    hour_of_day,
        CASE WHEN COALESCE(amount, 0) = 0 THEN 1 ELSE 0 END AS is_amount_zero,
    (COALESCE(newbalance_orig, 0) + COALESCE(amount, 0) - COALESCE(oldbalance_orig, 0)) AS error_balance_orig,
    (COALESCE(oldbalance_dest, 0) + COALESCE(amount, 0) - COALESCE(newbalance_dest, 0)) AS error_balance_dest,
    CASE WHEN name_dest LIKE 'M%' THEN 1 ELSE 0 END AS is_merchant_dest,
    CASE WHEN type = 'CASH_OUT' THEN 1 ELSE 0 END AS type_cash_out,
    CASE WHEN type = 'DEBIT' THEN 1 ELSE 0 END AS type_debit,
    CASE WHEN type = 'PAYMENT' THEN 1 ELSE 0 END AS type_payment,
    CASE WHEN type = 'TRANSFER' THEN 1 ELSE 0 END AS type_transfer
    
    CASE WHEN COALESCE(newbalance_orig, 0) = 0 THEN 1 ELSE 0 END AS is_orig_empty_after,
    CASE WHEN COALESCE(oldbalance_dest, 0) = 0 THEN 1 ELSE 0 END AS is_dest_empty_before
FROM 
    fraud_detection;
