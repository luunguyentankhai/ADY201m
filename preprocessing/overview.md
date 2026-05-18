# Table of features

| Column Name                    | Description                                                         |
| ------------------------------ | ------------------------------------------------------------------- |
| `transaction_amount`           | Amount of money involved in the transaction                         |
| `account_balance`              | User's current account balance before the transaction               |
| `daily_transaction_count`      | Number of transactions made by the user that day                    |
| `avg_transaction_amount_7d`    | User's average transaction amount in the past 7 days                |
| `failed_transaction_count_7d`  | Count of failed transactions in the past 7 days                     |
| `card_age`                     | Age of the card in months                                           |
| `transaction_distance`         | Distance between the user's usual location and transaction location |
| `risk_score`                   | Fraud risk score computed for the transaction                       |
| `ip_address_flag`              | Whether the IP address was flagged as suspicious (`0` or `1`)       |
| `previous_fraudulent_activity` | Number of past fraudulent activities by the user                    |
| `is_weekend`                   | Whether the transaction occurred on a weekend (`0` or `1`)          |
| `feature_hour`                 | Time the transaction occured                                        |
| `feature_day_of_week`          | Day of week (Monday to Sunday)                                      |
| `transaction_type`             | Type of transaction (`Online`, `In-Store`, `ATM`, etc.)             |
| `device_type`                  | Type of device used (`Mobile`, `Desktop`, etc.)                     |
| `location`                     | Geographical location of the transaction                            |
| `merchant_category`            | Type of merchant (`Retail`, `Food`, `Travel`, etc.)                 |
| `authentication_method`        | How the user authenticated (`PIN`, `Biometric`, etc.)               |
| `target`                       | Target variable (`0 = Not Fraud`, `1 = Fraud`)                      |

---

# 1. Feature Distributions & Trends

- **transaction_amount**: Highly right-skewed, with most transactions being small and a few large outliers. Boxplot confirms many outliers.
- **transaction_amount**: Phân phối lệch phải mạnh, với hầu hết các giao dịch có giá trị nhỏ và chỉ có một số ít ngoại lệ có giá trị rất lớn. Biểu đồ Boxplot xác nhận có nhiều giá trị ngoại lệ.

- **account_balance, card_age, transaction_distance, avg_transaction_amount_7d, risk_score**: All show relatively uniform or broad distributions, with some outliers.
- **account_balance, card_age, transaction_distance, avg_transaction_amount_7d, risk_score**: Tất cả đều cho thấy phân phối tương đối đồng đều hoặc rộng, cùng với một số giá trị ngoại lệ.

- **daily_transaction_count, failed_transaction_count_7d, feature_hour, feature_day_of_week**: Discrete, nearly uniform or cyclical distributions.
- **daily_transaction_count, failed_transaction_count_7d, feature_hour, feature_day_of_week**: Có dạng dữ liệu rời rạc, với phân phối gần như đồng đều hoặc mang tính chu kỳ.

- **Categorical features (transaction_type, device_type, location, merchant_category, authentication_method)**: All categories are well represented, with no major imbalance.
- **Các đặc trưng phân loại (transaction_type, device_type, location, merchant_category, authentication_method)**: Tất cả các nhóm dữ liệu đều được biểu diễn đầy đủ, không có sự mất cân bằng lớn.

- **ip_address_flag, previous_fraudulent_activity, is_weekend, target**: Mostly binary, with a majority of zeros and a minority of ones.
- **ip_address_flag, previous_fraudulent_activity, is_weekend, target**: Chủ yếu là dữ liệu nhị phân, với phần lớn là giá trị 0 và một phần nhỏ là giá trị 1.

---

# 2. Relationships Between Features

## Correlation Matrix

- The strongest correlation with the target is **avg_transaction_amount_7d (0.51)** and **risk_score (0.39)**.
- Tương quan mạnh nhất với biến mục tiêu là **avg_transaction_amount_7d (0.51)** và **risk_score (0.39)**.

- Most other features have very low correlation with the target and with each other.
- Hầu hết các đặc trưng khác có mức tương quan rất thấp với biến mục tiêu cũng như với nhau.

- This suggests that **avg_transaction_amount_7d** and **risk_score** are likely the most predictive features for fraud.
- Điều này cho thấy rằng **avg_transaction_amount_7d** và **risk_score** có khả năng là các đặc trưng dự đoán gian lận quan trọng nhất.

---

# 3. Feature Importance (Based on Correlation & Distribution)

## Most Important Features

- **avg_transaction_amount_7d**: Strongest correlation with the target. Likely, recent average transaction size is a key fraud indicator.
- **avg_transaction_amount_7d**: Có tương quan mạnh nhất với biến mục tiêu. Giá trị giao dịch trung bình gần đây có khả năng là một chỉ báo quan trọng của gian lận.

- **risk_score**: Also highly correlated with the target, as expected for a risk metric.
- **risk_score**: Cũng có mức tương quan cao với biến mục tiêu, điều này phù hợp với vai trò của một chỉ số rủi ro.

- **previous_fraudulent_activity** and **ip_address_flag**: While not highly correlated, these are classic fraud indicators and may be important in non-linear models.
- **previous_fraudulent_activity** và **ip_address_flag**: Mặc dù không có tương quan quá cao, đây là các chỉ báo gian lận điển hình và có thể quan trọng trong các mô hình phi tuyến.

## Other Features

- **transaction_amount** itself is not highly correlated with the target, but its outliers may still be important for detecting fraud.
- Bản thân **transaction_amount** không có tương quan cao với biến mục tiêu, nhưng các giá trị ngoại lệ của nó vẫn có thể quan trọng trong việc phát hiện gian lận.

- Categorical features (like **transaction_type, device_type**, etc.) are balanced and may provide value when combined with other features.
- Các đặc trưng phân loại (như **transaction_type, device_type**, v.v.) có sự cân bằng tốt và có thể mang lại giá trị khi kết hợp với các đặc trưng khác.

---

# 4. Comparing Feature Values

## Range & Outliers

- Some features (like **transaction_amount, account_balance, transaction_distance**) have wide ranges and outliers, suggesting normalization or transformation may help.
- Một số đặc trưng (như **transaction_amount, account_balance, transaction_distance**) có khoảng giá trị rộng và nhiều ngoại lệ, cho thấy việc chuẩn hóa hoặc biến đổi dữ liệu có thể hữu ích.

## Binary Features

- Features like **ip_address_flag, previous_fraudulent_activity, and is_weekend** are mostly zeros, so their predictive power may be limited unless the minority class is highly indicative of fraud.
- Các đặc trưng như **ip_address_flag, previous_fraudulent_activity, và is_weekend** chủ yếu chứa giá trị 0, vì vậy khả năng dự đoán của chúng có thể bị hạn chế trừ khi lớp thiểu số mang tính chỉ báo gian lận rất cao.

---

# 5. Ideas & Recommendations

## Feature Engineering

- Consider creating interaction features (e.g., **transaction_amount × risk_score**).
- Hãy cân nhắc tạo các đặc trưng tương tác (ví dụ: **transaction_amount × risk_score**).

- Normalize or log-transform highly skewed features like **transaction_amount**.
- Chuẩn hóa hoặc áp dụng log-transform cho các đặc trưng lệch mạnh như **transaction_amount**.

## Modeling

- Use tree-based models (e.g., **Random Forest, XGBoost**) to capture non-linear relationships and feature interactions.
- Sử dụng các mô hình dựa trên cây (ví dụ: **Random Forest, XGBoost**) để nắm bắt các mối quan hệ phi tuyến và sự tương tác giữa các đặc trưng.

- Use feature selection techniques to confirm importance (e.g., permutation importance, SHAP values).
- Sử dụng các kỹ thuật chọn đặc trưng để xác nhận mức độ quan trọng (ví dụ: permutation importance, SHAP values).

## Data Imbalance

- The target is imbalanced (more non-fraud than fraud). Consider resampling or using class weights in your model.
- Biến mục tiêu bị mất cân bằng (số lượng giao dịch không gian lận nhiều hơn giao dịch gian lận). Hãy cân nhắc sử dụng resampling hoặc class weights trong mô hình.

## Further Analysis

- Explore time-based patterns (e.g., fraud by hour or day).
- Khám phá các mẫu dữ liệu theo thời gian (ví dụ: gian lận theo giờ hoặc theo ngày).

- Analyze the effect of categorical features in combination with numeric ones.
- Phân tích ảnh hưởng của các đặc trưng phân loại khi kết hợp với các đặc trưng số.

---

# Summary Table: Key Features

| Feature                      | Trend/Distribution     | Correlation with Target | Notes/Importance                |
| ---------------------------- | ---------------------- | ----------------------- | ------------------------------- |
| avg_transaction_amount_7d    | Uniform, wide range    | 0.51                    | Most important, strong signal   |
| risk_score                   | Uniform, wide range    | 0.39                    | Very important, as expected     |
| transaction_amount           | Right-skewed, outliers | ~0                      | Outliers may be important       |
| previous_fraudulent_activity | Mostly 0, some 1s      | ~0                      | Classic fraud indicator         |
| ip_address_flag              | Mostly 0, some 1s      | ~0                      | Useful for rare event detection |
| Categorical features         | Balanced               | N/A                     | Useful for model interactions   |
