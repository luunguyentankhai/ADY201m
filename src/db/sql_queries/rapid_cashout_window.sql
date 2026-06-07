/*
 * TRUY VẤN 4: HÀNH VI CHUYỂN TIỀN QUÁ KHẢ NĂNG TÀI CHÍNH
 * Mục tiêu: Xếp hạng các giao dịch lừa đảo có giá trị lớn nhất trong từng khung giờ.
 * Kỹ thuật: Sử dụng RANK() kết hợp phân vùng OVER(PARTITION BY).
 */
SELECT 
    step,
    hour_of_day,
    type,
    amount,
    name_orig,
    is_fraud,
    RANK() OVER(PARTITION BY hour_of_day ORDER BY amount DESC) as amount_rank_in_hour
FROM 
    fraud_detection
WHERE 
    is_fraud = 1
ORDER BY 
    hour_of_day ASC, 
    amount_rank_in_hour ASC;
