# Table of features

The below column reference:

- **step**: represents a unit of time where 1 step equals 1 hour
- **type**: type of online transaction
- **amount**: the amount of the transaction
- **nameOrig**: customer starting the transaction
- **oldbalanceOrg**: balance before the transaction
- **newbalanceOrig**: balance after the transaction
- **nameDest**: recipient of the transaction
- **oldbalanceDest**: initial balance of recipient before the transaction
- **newbalanceDest**: the new balance of recipient after the transaction
- **isFraud**: fraud transaction

# 1. Feature-by-Feature Analysis

# 1. Phân tích từng đặc trưng

## General Dataset Info

## Thông tin tổng quan về tập dữ liệu

- **Number of rows:** [INSERT]  
  **Số lượng hàng:** [INSERT]

- **Number of columns:** [INSERT]  
  **Số lượng cột:** [INSERT]

- **Target column:** `isFraud`  
  **Cột mục tiêu:** `isFraud`

- **Problem type:** Binary Classification  
  **Loại bài toán:** Phân loại nhị phân

---

# Feature Analysis

# Phân tích đặc trưng

## 1. `step`

- **Data type:** Numeric (integer)  
  **Kiểu dữ liệu:** Số nguyên

- **Distribution:** Likely uniform or periodic (represents time steps)  
  **Phân phối:** Có thể đồng đều hoặc mang tính chu kỳ (đại diện cho các bước thời gian)

- **Skewness:** Minimal  
  **Độ lệch:** Ít lệch

- **Outliers:** Not expected  
  **Ngoại lệ:** Không đáng kể

- **Missing values:** Not indicated  
  **Giá trị thiếu:** Không được ghi nhận

- **Cardinality:** High (many unique values)  
  **Cardinality:** Cao (nhiều giá trị duy nhất)

- **Quality issues:** None apparent  
  **Vấn đề chất lượng:** Không có vấn đề rõ ràng

---

## 2. `type`

- **Data type:** Categorical (`CASH_IN`, `CASH_OUT`, `DEBIT`, `PAYMENT`, `TRANSFER`)  
  **Kiểu dữ liệu:** Phân loại (`CASH_IN`, `CASH_OUT`, `DEBIT`, `PAYMENT`, `TRANSFER`)

- **Distribution:** Imbalanced (`PAYMENT`, `CASH_OUT`, and `CASH_IN` dominate; `DEBIT` is rare)  
  **Phân phối:** Mất cân bằng (`PAYMENT`, `CASH_OUT`, và `CASH_IN` chiếm ưu thế; `DEBIT` hiếm)

- **Skewness:** High  
  **Độ lệch:** Cao

- **Outliers:** Not applicable  
  **Ngoại lệ:** Không áp dụng

- **Missing values:** Not indicated  
  **Giá trị thiếu:** Không được ghi nhận

- **Cardinality:** Low (5 categories)  
  **Cardinality:** Thấp (5 nhóm giá trị)

- **Quality issues:** None apparent  
  **Vấn đề chất lượng:** Không có vấn đề rõ ràng

---

## 3. `amount`

- **Data type:** Numeric (float)  
  **Kiểu dữ liệu:** Số thực

- **Distribution:** Highly right-skewed (long tail, most transactions are small)  
  **Phân phối:** Lệch phải mạnh (đuôi dài, phần lớn giao dịch có giá trị nhỏ)

- **Skewness:** Severe positive skew  
  **Độ lệch:** Lệch dương nghiêm trọng

- **Outliers:** Many (as seen in boxplots)  
  **Ngoại lệ:** Nhiều ngoại lệ (thể hiện qua boxplot)

- **Missing values:** Not indicated  
  **Giá trị thiếu:** Không được ghi nhận

- **Cardinality:** High  
  **Cardinality:** Cao

- **Quality issues:** Extreme values may need capping  
  **Vấn đề chất lượng:** Các giá trị cực lớn có thể cần được giới hạn

---

## 4. `oldbalanceOrg` / `newbalanceOrg` / `oldbalanceDest` / `newbalanceDest`

- **Data type:** Numeric (float)  
  **Kiểu dữ liệu:** Số thực

- **Distribution:** Highly right-skewed with long tails  
  **Phân phối:** Lệch phải mạnh với đuôi dài

- **Skewness:** Severe positive skew  
  **Độ lệch:** Lệch dương nghiêm trọng

- **Outliers:** Many (visible in boxplots)  
  **Ngoại lệ:** Nhiều ngoại lệ (thể hiện trong boxplot)

- **Missing values:** Not indicated  
  **Giá trị thiếu:** Không được ghi nhận

- **Cardinality:** High  
  **Cardinality:** Cao

- **Quality issues:** Check for zero, negative, or inconsistent balances  
  **Vấn đề chất lượng:** Cần kiểm tra số dư bằng 0, âm hoặc không nhất quán

---

## 5. `isFraud` (Target)

- **Data type:** Binary (0/1)  
  **Kiểu dữ liệu:** Nhị phân (0/1)

- **Distribution:** Extremely imbalanced (majority class = 0)  
  **Phân phối:** Mất cân bằng nghiêm trọng (đa số thuộc lớp 0)

- **Skewness:** High  
  **Độ lệch:** Cao

- **Outliers:** Not applicable  
  **Ngoại lệ:** Không áp dụng

- **Missing values:** Not indicated  
  **Giá trị thiếu:** Không được ghi nhận

- **Cardinality:** 2  
  **Cardinality:** 2 giá trị

- **Quality issues:** None  
  **Vấn đề chất lượng:** Không có

---

# 2. Feature–Target Relationships

# 2. Mối quan hệ giữa đặc trưng và biến mục tiêu

## `type` vs `isFraud`

- **Strength:** Only `TRANSFER` and `CASH_OUT` contain fraud cases.  
  **Độ mạnh:** Chỉ `TRANSFER` và `CASH_OUT` chứa các trường hợp gian lận.

- **Correlation:** Strong categorical relationship; `type` is highly predictive.  
  **Tương quan:** Quan hệ phân loại mạnh; `type` có khả năng dự đoán cao.

- **Trend:** Non-linear (fraud only appears in specific transaction types).  
  **Xu hướng:** Phi tuyến (gian lận chỉ xuất hiện ở một số loại giao dịch cụ thể).

- **Predictive utility:** Very high  
  **Khả năng dự đoán:** Rất cao

- **Leakage risk:** Low  
  **Rủi ro rò rỉ dữ liệu:** Thấp

- **Statistical importance:** High  
  **Tầm quan trọng thống kê:** Cao

---

## `amount` vs `isFraud`

- **Strength:** Fraudulent transactions often involve larger amounts.  
  **Độ mạnh:** Các giao dịch gian lận thường có giá trị lớn hơn.

- **Correlation:** Weak linear relationship but possible non-linear threshold effect.  
  **Tương quan:** Quan hệ tuyến tính yếu nhưng có thể tồn tại ngưỡng phi tuyến.

- **Trend:** Transactions in the right tail are more likely fraudulent.  
  **Xu hướng:** Các giao dịch ở đuôi phải có khả năng gian lận cao hơn.

- **Predictive utility:** Moderate to high  
  **Khả năng dự đoán:** Trung bình đến cao

- **Leakage risk:** Low  
  **Rủi ro rò rỉ dữ liệu:** Thấp

- **Statistical importance:** Moderate  
  **Tầm quan trọng thống kê:** Trung bình

---

## Balance Features vs `isFraud`

- **Strength:** Some fraud patterns exist in balance-related features.  
  **Độ mạnh:** Có một số mẫu gian lận liên quan đến các đặc trưng số dư.

- **Correlation:** Weak linear correlation with possible non-linear effects.  
  **Tương quan:** Tương quan tuyến tính yếu nhưng có thể có hiệu ứng phi tuyến.

- **Trend:** Extreme balance values may indicate fraud.  
  **Xu hướng:** Các giá trị số dư cực đoan có thể liên quan đến gian lận.

- **Predictive utility:** Moderate  
  **Khả năng dự đoán:** Trung bình

- **Leakage risk:** Low  
  **Rủi ro rò rỉ dữ liệu:** Thấp

- **Statistical importance:** Moderate  
  **Tầm quan trọng thống kê:** Trung bình

---

## `step` vs `isFraud`

- **Strength:** Certain time steps contain more fraud cases.  
  **Độ mạnh:** Một số bước thời gian chứa nhiều giao dịch gian lận hơn.

- **Correlation:** Weak overall correlation.  
  **Tương quan:** Tương quan tổng thể yếu.

- **Trend:** Non-linear and potentially periodic.  
  **Xu hướng:** Phi tuyến và có thể mang tính chu kỳ.

- **Predictive utility:** Low to moderate  
  **Khả năng dự đoán:** Thấp đến trung bình

- **Leakage risk:** Low  
  **Rủi ro rò rỉ dữ liệu:** Thấp

- **Statistical importance:** Low  
  **Tầm quan trọng thống kê:** Thấp

---

# 3. Feature–Feature Relationships

# 3. Mối quan hệ giữa các đặc trưng

- **Correlation matrix:** Most features are weakly correlated. `newbalanceDest` and `oldbalanceDest` are highly correlated (0.936).  
  **Ma trận tương quan:** Phần lớn các đặc trưng có tương quan yếu. `newbalanceDest` và `oldbalanceDest` có tương quan rất cao (0.936).

- **Multicollinearity:** High correlation exists between old and new balances for the same entity.  
  **Đa cộng tuyến:** Có tương quan cao giữa số dư cũ và mới của cùng một đối tượng.

- **Redundancy:** Some balance features may be redundant.  
  **Dư thừa:** Một số đặc trưng số dư có thể dư thừa.

- **Strong interactions:** Strong interactions may exist between `amount` and balances, or between `type` and `amount`.  
  **Tương tác mạnh:** Có thể tồn tại tương tác mạnh giữa `amount` và số dư, hoặc giữa `type` và `amount`.

---

# 4. Class Imbalance

# 4. Mất cân bằng lớp

- **Severity:** Fraud cases account for less than 0.2% of all transactions.  
  **Mức độ:** Các giao dịch gian lận chiếm dưới 0.2% tổng số giao dịch.

- **Risks:** Models may ignore the minority fraud class.  
  **Rủi ro:** Mô hình có thể bỏ qua lớp gian lận thiểu số.

- **Recommended metrics:** Precision, recall, F1-score, ROC-AUC, and PR-AUC.  
  **Chỉ số đánh giá khuyến nghị:** Precision, recall, F1-score, ROC-AUC và PR-AUC.

- **Resampling:** Use SMOTE, undersampling, or class weighting.  
  **Cân bằng dữ liệu:** Sử dụng SMOTE, undersampling hoặc class weighting.

---

# 5. Preprocessing Needs

# 5. Nhu cầu tiền xử lý

- **Encoding:** One-hot encode the `type` feature.  
  **Mã hóa:** One-hot encode cho đặc trưng `type`.

- **Scaling:** Use `RobustScaler` or log transformation for skewed numerical features.  
  **Chuẩn hóa:** Sử dụng `RobustScaler` hoặc biến đổi log cho các đặc trưng lệch mạnh.

- **Log transformations:** Strongly recommended for `amount` and balance features.  
  **Biến đổi log:** Được khuyến nghị mạnh cho `amount` và các đặc trưng số dư.

- **Outlier treatment:** Cap or transform extreme values.  
  **Xử lý ngoại lệ:** Giới hạn hoặc biến đổi các giá trị cực đoan.

- **Feature engineering:** Create ratio, flag, aggregate, and time-based features.  
  **Feature engineering:** Tạo các đặc trưng dạng tỷ lệ, cờ đánh dấu, tổng hợp và theo thời gian.

---

# 6. ML Recommendations

# 6. Đề xuất Machine Learning

- **Best models:** Random Forest, XGBoost, and LightGBM are strong candidates.  
  **Mô hình phù hợp:** Random Forest, XGBoost và LightGBM là các lựa chọn mạnh.

- **Most important features:** `type`, `amount`, and balance-related features.  
  **Đặc trưng quan trọng nhất:** `type`, `amount` và các đặc trưng liên quan đến số dư.

- **Features that may harm performance:** Highly collinear balance features.  
  **Đặc trưng có thể gây hại:** Các đặc trưng số dư có đa cộng tuyến cao.

- **Feature engineering:** Add interaction terms and anomaly-based features.  
  **Feature engineering:** Thêm interaction terms và đặc trưng dựa trên bất thường.

- **Validation strategy:** Use Stratified K-Fold cross-validation.  
  **Chiến lược validation:** Sử dụng Stratified K-Fold cross-validation.

---

# 7. Findings & Business Implications

# 7. Kết luận và tác động kinh doanh

- **Transaction type is the strongest predictor of fraud.**  
  **Loại giao dịch là yếu tố dự đoán gian lận mạnh nhất.**

- **Amounts and balances are highly skewed; outlier handling is critical.**  
  **Số tiền và số dư bị lệch mạnh; việc xử lý ngoại lệ là rất quan trọng.**

- **Extreme class imbalance makes accuracy misleading.**  
  **Mất cân bằng lớp nghiêm trọng khiến accuracy trở nên gây hiểu nhầm.**

- **High correlations between balance features suggest redundancy.**  
  **Tương quan cao giữa các đặc trưng số dư cho thấy khả năng dư thừa dữ liệu.**

- **Monitoring high-risk transaction types and large transactions can improve fraud detection.**  
  **Theo dõi các loại giao dịch rủi ro cao và giao dịch giá trị lớn có thể cải thiện khả năng phát hiện gian lận.**

---

# FINE-TUNING PARAMETERS

## Logistic Regression

| Tham số        | Ý nghĩa                |
| -------------- | ---------------------- |
| `C`            | Độ regularization      |
| `penalty`      | Regularization L1 / L2 |
| `solver`       | Thuật toán tối ưu      |
| `class_weight` | Xử lý imbalance        |
| `max_iter`     | Số vòng lặp train      |

---

## Random Forest

| Tham số             | Ý nghĩa              |
| ------------------- | -------------------- |
| `n_estimators`      | Số lượng cây         |
| `max_depth`         | Độ sâu tối đa        |
| `min_samples_split` | Minimum split        |
| `min_samples_leaf`  | Minimum leaf         |
| `max_features`      | Số feature mỗi split |
| `class_weight`      | Xử lý imbalance      |

---

## XGBoost

| Tham số            | Ý nghĩa              |
| ------------------ | -------------------- |
| `n_estimators`     | Số boosting rounds   |
| `learning_rate`    | Tốc độ học           |
| `max_depth`        | Độ sâu cây           |
| `subsample`        | Sampling dòng        |
| `colsample_bytree` | Sampling feature     |
| `gamma`            | Regularization split |
| `min_child_weight` | Minimum child weight |
| `scale_pos_weight` | Xử lý imbalance      |

---

## LightGBM

| Tham số             | Ý nghĩa               |
| ------------------- | --------------------- |
| `n_estimators`      | Số cây                |
| `learning_rate`     | Tốc độ học            |
| `num_leaves`        | Số leaf               |
| `max_depth`         | Độ sâu cây            |
| `min_child_samples` | Minimum child samples |
| `subsample`         | Sampling dòng         |
| `colsample_bytree`  | Sampling feature      |
| `reg_alpha`         | Regularization L1     |
| `reg_lambda`        | Regularization L2     |

---

## CatBoost

| Tham số               | Ý nghĩa            |
| --------------------- | ------------------ |
| `iterations`          | Số boosting rounds |
| `learning_rate`       | Tốc độ học         |
| `depth`               | Độ sâu cây         |
| `l2_leaf_reg`         | Regularization     |
| `bagging_temperature` | Độ ngẫu nhiên      |
| `border_count`        | Số split           |
| `auto_class_weights`  | Xử lý imbalance    |
