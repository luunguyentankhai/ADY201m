WITH transfer_phase AS (
    SELECT 
        step, 
        name_orig AS victim_account, 
        name_dest AS intermediate_account_1, 
        amount
    FROM fraud_detection
    WHERE is_fraud = 1 AND type = 'TRANSFER'
),
cashout_phase AS (
    SELECT 
        step, 
        name_orig AS intermediate_account_2, 
        name_dest AS final_cashout_location, 
        amount
    FROM fraud_detection
    WHERE is_fraud = 1 AND type = 'CASH_OUT'
)
SELECT 
    t.step AS original_step,
    c.step AS cashout_step,
    (c.step - t.step) AS delay_in_hours,
    t.victim_account,
    t.intermediate_account_1 AS transfer_dest,
    c.intermediate_account_2 AS cashout_orig,
    c.final_cashout_location,
    t.amount AS transfer_amount,
    c.amount AS cashout_amount
FROM transfer_phase t
JOIN cashout_phase c 
    -- ĐÃ SỬA LỖI: Khớp nối dựa trên Dấu vết Dữ liệu (Số tiền & Thời gian) thay vì ID
    ON t.amount = c.amount 
    AND t.step = c.step
ORDER BY 
    t.step ASC, 
    t.amount DESC;
