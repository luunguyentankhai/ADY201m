/*
 * TRUY VẤN 5: TRUY VẾT TÀI KHOẢN CON LA (DỰA TRÊN DẤU VẾT HÀNH VI)
 * Mục tiêu: Phát hiện kịch bản TRANSFER -> CASH_OUT liền mạch để tẩu tán tiền.
 * Kỹ thuật: Heuristic JOIN (Khớp nối theo hành vi thay vì ID)
 */
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
    t.step AS execution_step,
    t.victim_account,
    t.intermediate_account_1 AS transfer_dest,
    c.intermediate_account_2 AS cashout_orig,
    c.final_cashout_location,
    t.amount AS stolen_amount
FROM transfer_phase t
INNER JOIN cashout_phase c 
    ON t.amount = c.amount 
    AND t.step = c.step
ORDER BY 
    t.step ASC, 
    t.amount DESC;
