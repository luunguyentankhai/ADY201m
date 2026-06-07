/*
 * TRUY VẤN 2: TỈ LỆ LỪA ĐẢO THEO GIỜ VÀ LOẠI GIAO DỊCH
 * Mục tiêu: Tìm ra khung giờ và hình thức thanh toán bị lợi dụng nhiều nhất.
 * Feature hình thành: Cột `hour_of_day`, `type_transfer`, `type_cash_out`.
 */
SELECT 
    hour_of_day,
    type AS transaction_type, 
    COUNT(id) AS total_transactions,
    SUM(is_fraud) AS fraud_transactions,
    ROUND((SUM(is_fraud) * 100.0) / COUNT(id), 4) AS fraud_rate_pct
FROM 
    fraud_detection
GROUP BY 
    hour_of_day,
    type
HAVING 
    SUM(is_fraud) > 0 
ORDER BY 
    fraud_rate_pct DESC,
    fraud_transactions DESC;
