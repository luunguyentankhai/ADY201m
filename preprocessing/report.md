#VIETNAMESE VERSION

# Phân tích Dataset Fraud Detection

## 1. Tổng quan Dataset

Dataset chứa hơn **6.36 triệu giao dịch**, nhưng chỉ có **8212 giao dịch fraud**, tức fraud chỉ chiếm khoảng:

\[
\frac{8212}{6362614} \approx 0.129\%
\]

Điều này cho thấy dữ liệu bị **mất cân bằng cực mạnh (extremely imbalanced)**.

Điều này rất quan trọng vì model hoàn toàn có thể đạt accuracy trên 99% nhưng vẫn detect fraud rất kém.

---

# 2. Phân tích phân phối dữ liệu

## 2.1 Các cột phân phối lệch phải mạnh

Các cột:

- `amount`
- `oldbalanceOrg`
- `newbalanceOrig`
- `oldbalanceDest`
- `newbalanceDest`

đều có phân phối lệch phải rất mạnh (right-skewed).

Điều này cho thấy:

- Phần lớn giao dịch có giá trị nhỏ
- Phần lớn khách hàng có số dư thấp
- Chỉ có một lượng rất nhỏ transaction có giá trị cực lớn

Đây là pattern rất phổ biến trong dữ liệu tài chính thực tế.

---

## 2.2 Ý nghĩa thực tế

Các phân phối này phản ánh đúng hành vi tài chính ngoài thực tế:

- Người dùng thực hiện nhiều giao dịch nhỏ mỗi ngày
- Rất ít tài khoản có số dư cực lớn
- Fraudster thường ưu tiên giao dịch nhỏ vì:
  - khó bị nghi ngờ
  - dễ vượt qua hệ thống giám sát
  - nạn nhân dễ chấp nhận hơn

Điều này phù hợp với quan sát:

> Hầu hết fraud transactions thuộc nhóm `very low amount`.

Điều đó cho thấy dataset này chủ yếu mô phỏng:

- stealth fraud
- micro-transaction fraud
- social engineering scam

thay vì các vụ trộm tiền quy mô lớn.

---

# 3. Phân tích Fraud theo loại giao dịch

Fraud chủ yếu xuất hiện trong:

- `CASH_OUT`
- `TRANSFER`

Điều này rất hợp lý về mặt nghiệp vụ.

---

## 3.1 Fraud trong CASH_OUT

`CASH_OUT` thường được dùng để chuyển tiền thành tiền có thể rút hoặc khó truy vết hơn.

Fraudster thích CASH_OUT vì:

- lấy tiền nhanh
- giảm khả năng bị trace
- hoàn tất quá trình rửa tiền

---

## 3.2 Fraud trong TRANSFER

`TRANSFER` thường được dùng để:

- chuyển tiền sang mule account
- trung gian rửa tiền
- bypass hệ thống monitoring

Đây thường là bước trước CASH_OUT.

---

## 3.3 Ý nghĩa với model

Feature `type` sẽ là feature rất mạnh.

Các transaction type như:

- `PAYMENT`
- `DEBIT`
- `CASH_IN`

ít liên quan fraud hơn nhiều.

---

# 4. Phân tích hành vi Fraud

Quan sát cho thấy:

- Một customer thường chỉ bị lừa một lần
- Fraudster tối đa lừa khoảng hai customer

Điều này cho thấy fraud mang tính targeted hơn là spam diện rộng.

Fraudster ưu tiên khả năng thành công thay vì lấy số tiền cực lớn.

---

# 5. Feature Engineering

## 5.1 Hour of Day

Feature:

\[
hour_of_day = step \mod 24
\]

được tạo để lấy giờ trong ngày từ cột `step`.

Điều này hợp lý vì fraud thường liên quan đến:

- hành vi người dùng
- thời gian monitoring
- giao dịch đêm khuya

hơn là ngày cụ thể.

---

## 5.2 Error Balance Features

### Lỗi số dư người gửi

\[
errorBalanceOrig
=
newbalanceOrig + amount - oldbalanceOrg
\]

Đối với giao dịch hợp lệ:

\[
errorBalanceOrig = 0
\]

---

### Lỗi số dư người nhận

\[
errorBalanceDest
=
oldbalanceDest + amount - newbalanceDest
\]

Đối với giao dịch hợp lệ:

\[
errorBalanceDest = 0
\]

---

## 5.3 Ý nghĩa của Error Features

Các feature này encode trực tiếp business logic vào model.

Nếu:

\[
error \neq 0
\]

thì có thể là:

- thao túng số dư
- cập nhật chậm
- lỗi hệ thống
- fraud
- laundering behavior

Đây là kiểu feature engineering rất mạnh trong fraud detection.

---

# 6. Phân tích Scatter Plot

Scatter plot so sánh:

- `errorBalanceOrig`
- `errorBalanceDest`

giữa fraud và non-fraud.

---

## Quan sát quan trọng

Fraud transactions tập trung quanh:

- `errorBalanceOrig ≈ 0`
- `errorBalanceDest > 0`

Điều này cho thấy:

- số dư sender nhìn có vẻ hợp lệ
- nhưng receiver balance có bất thường

---

## Ý nghĩa nghiệp vụ

Điều này có thể phản ánh:

- balance manipulation
- delayed update
- ghost account
- laundering behavior

Trong khi non-fraud phân bố đều hơn và thường cân bằng hoàn hảo.

---

# 7. Phân tích KDE Distribution

KDE plot của `errorBalanceDest` cho thấy:

- Fraud có tail dài hơn
- Fraud phân bố rộng hơn
- Non-fraud tập trung mạnh gần 0

Điều này chứng minh `errorBalanceDest` là feature phân biệt rất tốt.

---

# 8. Phân tích Correlation Matrix

## 8.1 Correlation mạnh

### `oldbalanceOrg ↔ newbalanceOrig = 0.803`

Điều này hợp lý vì:

\[
newbalanceOrig
=
oldbalanceOrg - amount
\]

---

### `oldbalanceDest ↔ newbalanceDest = 0.936`

Destination balances liên hệ rất mạnh do update trực tiếp sau transaction.

---

## 8.2 Correlation với Amount

### `amount ↔ oldbalanceDest = 0.595`

### `amount ↔ newbalanceDest = 0.670`

Transaction lớn thường liên quan account có số dư lớn hơn.

---

## 8.3 Correlation với Fraud rất thấp

`isFraud` có linear correlation rất thấp với đa số features:

- amount: 0.036
- oldbalanceOrg: 0.039
- errorBalanceOrig: -0.049

Điều này cho thấy fraud detection không phải bài toán tuyến tính.

---

## 8.4 Ý nghĩa với mô hình

Do fraud có pattern nonlinear nên các model tree-based sẽ phù hợp hơn:

- XGBoost
- LightGBM
- CatBoost
- Random Forest

Các model này học interaction và nonlinear boundary rất tốt.

---

# 9. Feature is_Merchant_Dest

`is_Merchant_Dest` có negative correlation mạnh với:

- amount = -0.742
- oldbalanceDest = -0.741
- newbalanceDest = -0.786

Điều này có thể cho thấy merchant transaction có rule khác customer transaction.

Feature này giúp model hiểu context transaction tốt hơn.

---

# 10. Tổng kết Insight

Fraud transactions trong dataset có đặc điểm:

- amount nhỏ
- chủ yếu CASH_OUT và TRANSFER
- receiver balance bất thường
- fraud cực hiếm
- fraud có pattern nonlinear

Các balance error feature đặc biệt mạnh vì encode trực tiếp luật tài chính vào dữ liệu.

---

# 11. Đề xuất Model

Dataset rất phù hợp với:

- LightGBM
- XGBoost
- CatBoost

vì các model này xử lý tốt:

- nonlinear relationship
- skewed distribution
- feature interaction
- imbalance classification

---

# 12. Hướng phân tích tiếp theo

## Temporal Fraud Analysis

- Phân tích giờ nào fraud xảy ra nhiều nhất

## Fraud theo Transaction Type

- So sánh CASH_OUT fraud và TRANSFER fraud

## Precision-Recall Analysis

- Accuracy gần như không có nhiều ý nghĩa

## SHAP Analysis

- Phân tích feature importance

## Threshold Optimization

- Tối ưu Recall hoặc F2-score thay vì Accuracy

---

# ENGLISH VERSION

# Fraud Detection Dataset Analysis

## 1. Dataset Overview

The dataset contains more than **6.36 million transactions**, but only **8212 fraud transactions**, meaning fraud accounts for approximately:

\[
\frac{8212}{6362614} \approx 0.129\%
\]

This indicates that the dataset is **extremely imbalanced**.

This is very important because a model can achieve more than 99% accuracy while still failing to detect fraud transactions effectively.

---

# 2. Data Distribution Analysis

## 2.1 Right-Skewed Distributions

The following features:

- `amount`
- `oldbalanceOrg`
- `newbalanceOrig`
- `oldbalanceDest`
- `newbalanceDest`

all show heavily right-skewed distributions.

This means:

- Most transactions involve small amounts
- Most customers have low account balances
- Only a very small number of transactions contain extremely large values

This pattern is very common in real-world financial transaction datasets.

---

## 2.2 Real-World Interpretation

These distributions reflect realistic financial behavior:

- Users perform many small daily transactions
- Very few accounts contain extremely high balances
- Fraudsters often prefer small transactions because:
  - they are less suspicious
  - they bypass monitoring thresholds
  - victims are more likely to approve them

This observation aligns with the finding that:

> Most fraud transactions belong to the `very low` amount category.

This suggests the dataset mainly contains:

- stealth fraud
- micro-transaction fraud
- social engineering scams

rather than massive money theft cases.

---

# 3. Fraud Analysis by Transaction Type

Fraud transactions mostly occur in:

- `CASH_OUT`
- `TRANSFER`

This makes strong business sense.

---

## 3.1 CASH_OUT Fraud

`CASH_OUT` operations are commonly used to convert digital balances into withdrawable money.

Fraudsters favor CASH_OUT because it allows them to:

- obtain money quickly
- reduce traceability
- finalize money laundering chains

---

## 3.2 TRANSFER Fraud

`TRANSFER` transactions are often used to:

- move money to mule accounts
- perform laundering operations
- bypass monitoring systems

They are commonly used before CASH_OUT operations.

---

## 3.3 Modeling Implication

The `type` feature is likely a very powerful predictive feature.

Transaction types such as:

- `PAYMENT`
- `DEBIT`
- `CASH_IN`

show little relation to fraud compared to CASH_OUT and TRANSFER.

---

# 4. Fraud Behavior Analysis

Observations show that:

- A customer is usually defrauded only once
- Fraudsters target at most two customers

This indicates localized and targeted fraud behavior rather than large-scale spam attacks.

Fraudsters appear to prioritize transaction success probability rather than stealing extremely large amounts.

---

# 5. Feature Engineering

## 5.1 Hour of Day

The feature:

\[
hour_of_day = step \mod 24
\]

was created to extract the hour from the `step` feature.

This is reasonable because fraud is often associated with:

- user activity patterns
- monitoring schedules
- suspicious late-night behavior

rather than specific calendar dates.

---

## 5.2 Error Balance Features

### Sender Balance Error

\[
errorBalanceOrig
=
newbalanceOrig + amount - oldbalanceOrg
\]

For a valid transaction:

\[
errorBalanceOrig = 0
\]

---

### Receiver Balance Error

\[
errorBalanceDest
=
oldbalanceDest + amount - newbalanceDest
\]

For a valid transaction:

\[
errorBalanceDest = 0
\]

---

## 5.3 Importance of Error Features

These features encode transaction consistency directly into the model.

If:

\[
error \neq 0
\]

it may indicate:

- balance manipulation
- delayed updates
- technical inconsistencies
- fraud attempts
- laundering behavior

This type of business-logic feature engineering is extremely valuable in fraud detection systems.

---

# 6. Scatter Plot Analysis

The scatter plot compares:

- `errorBalanceOrig`
- `errorBalanceDest`

for fraud and non-fraud transactions.

---

## Key Observation

Fraud transactions cluster around:

- `errorBalanceOrig ≈ 0`
- `errorBalanceDest > 0`

This suggests:

- sender balances appear normal
- receiver balances contain inconsistencies

---

## Business Interpretation

This may indicate:

- hidden balance manipulation
- delayed balance updates
- ghost account behavior
- laundering attempts

Non-fraud transactions are more evenly distributed and often remain perfectly balanced.

---

# 7. KDE Distribution Analysis

The KDE plot for `errorBalanceDest` shows:

- Fraud distributions have longer tails
- Fraud values are more spread out
- Non-fraud transactions concentrate near zero

This demonstrates that `errorBalanceDest` is a highly discriminative feature.

---

# 8. Correlation Matrix Analysis

## 8.1 Strong Correlations

### `oldbalanceOrg ↔ newbalanceOrig = 0.803`

This relationship is expected because:

\[
newbalanceOrig
=
oldbalanceOrg - amount
\]

---

### `oldbalanceDest ↔ newbalanceDest = 0.936`

Destination balances are strongly related because balances update directly after transactions.

---

## 8.2 Amount Correlations

### `amount ↔ oldbalanceDest = 0.595`

### `amount ↔ newbalanceDest = 0.670`

Larger transactions are associated with larger destination account balances.

---

## 8.3 Fraud Correlations are Low

`isFraud` shows weak linear correlation with most features:

- amount: 0.036
- oldbalanceOrg: 0.039
- errorBalanceOrig: -0.049

This implies fraud detection is not a simple linear problem.

---

## 8.4 Importance of Nonlinear Models

Because fraud patterns are nonlinear, tree-based models are likely to perform well:

- XGBoost
- LightGBM
- CatBoost
- Random Forest

These models can capture feature interactions and nonlinear boundaries effectively.

---

# 9. Merchant Destination Feature

`is_Merchant_Dest` shows strong negative correlations with:

- amount = -0.742
- oldbalanceDest = -0.741
- newbalanceDest = -0.786

This may indicate that merchant transactions follow different transaction rules and exhibit different balance update behaviors.

This feature helps provide transaction context to the model.

---

# 10. Key Insights

The dataset suggests that fraud transactions are characterized by:

- small transaction amounts
- CASH_OUT and TRANSFER transaction types
- suspicious destination balance inconsistencies
- highly imbalanced fraud distribution
- nonlinear fraud behavior patterns

The engineered balance error features are especially powerful because they directly encode financial consistency rules into the dataset.

---

# 11. Modeling Recommendations

The dataset is highly suitable for:

- LightGBM
- XGBoost
- CatBoost

because these models handle:

- nonlinear relationships
- skewed distributions
- feature interactions
- imbalanced classification problems

effectively.

---

# 12. Suggested Future Analysis

Further analysis could include:

## Temporal Fraud Analysis

- Identify the hours with the highest fraud frequency

## Fraud by Transaction Type

- Compare CASH_OUT fraud vs TRANSFER fraud

## Precision-Recall Evaluation

- Accuracy alone is not meaningful for this dataset

## SHAP Analysis

- Interpret feature importance

## Threshold Optimization

- Optimize Recall or F2-score instead of Accuracy
