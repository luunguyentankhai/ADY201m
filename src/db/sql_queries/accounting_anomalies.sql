/*
 * TRUY VẤN 3: PHÁT HIỆN LỖ HỔNG KẾ TOÁN (ANOMALIES)
 * Mục tiêu: Tìm các giao dịch mà số tiền bị trừ không khớp với số tiền chuyển đi.
 * Feature hình thành: Cột `error_balance_orig`.
 */
WITH BalanceCheck AS (
    SELECT 
        id,
        step,
        type,
        amount,
        oldbalance_orig,
        newbalance_orig,
        is_fraud,
        -- Tính độ lệch: Tiền cũ - Tiền mới - Số tiền giao dịch
        ABS((oldbalance_orig - newbalance_orig) - amount) AS error_margin
    FROM fraud_detection
    WHERE type IN ('TRANSFER', 'CASH_OUT')
)
SELECT 
    id, step, type, amount, error_margin, is_fraud
FROM 
    BalanceCheck
WHERE 
    error_margin > 0 -- Chỉ lấy những dòng bị lỗi toán học
    AND is_fraud = 1
ORDER BY 
    error_margin DESC
LIMIT 100;
