-- ==============================================================================
-- FILE: 02_get_abnormal_tx.sql
-- YÊU CẦU: Xác định nhóm giao dịch bất thường theo giá trị cao, tần suất dày
-- CHÚ THÍCH: Lọc theo tài khoản nhận (name_dest) với tần suất >= 5 và có giao dịch >= 500.000
-- ==============================================================================

WITH receiver_stats AS (
    SELECT 
        name_dest,
        COUNT(id) AS receive_frequency,
        MAX(amount) AS max_single_amount,
        AVG(amount) AS avg_received_amount,
        SUM(amount) AS total_received_amount,
        SUM(is_fraud) AS actual_fraud_count
    FROM 
        fraud_detection
    WHERE 
        type IN ('TRANSFER', 'CASH_OUT')
    GROUP BY 
        name_dest
)

SELECT 
    name_dest,
    receive_frequency,
    max_single_amount,
    ROUND(avg_received_amount, 2) AS avg_received_amount,
    total_received_amount,
    actual_fraud_count
FROM 
    receiver_stats
WHERE 
    receive_frequency >= 5 
    AND max_single_amount >= 500000.00
ORDER BY 
    receive_frequency DESC, 
    total_received_amount DESC;
