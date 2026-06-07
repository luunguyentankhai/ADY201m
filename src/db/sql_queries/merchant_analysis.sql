/*
 * TRUY VẤN 1: SÀNG LỌC ĐỐI TƯỢNG TÌNH NGHI
 * Mục tiêu: Kiểm tra xem các tài khoản Thương gia (bắt đầu bằng 'M') có bao giờ dính líu đến lừa đảo không.
 * Feature hình thành: Cột `is_merchant_dest` trong View.
 */
SELECT 
    name_dest AS merchant_account,
    type AS transaction_type,
    amount,
    oldbalance_dest,
    newbalance_dest,
    is_fraud
FROM 
    fraud_detection
WHERE 
    name_dest LIKE 'M%' 
    AND is_fraud = 1;
