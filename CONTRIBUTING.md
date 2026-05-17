# DATABASE FETCHING GUIDE

## IMPORTANT

**`analyzer.py`**: dùng để gọi cái hàm báo cáo chính thức
**`utils.py`**: dùng để kiểm tra, debug, khám phá

## For `analyzer.py`:

### Chức Năng:

- yêu cầu phân tích: 
    - get_fraud_rate
    - get_anomalies
    - get_fraud_patterns
- kéo dữ liệu để train model:
    - get_ml_feature

### Sử dụng trong code:

```
from src.db.analyzer import FraudAnalyzer

<analyzer> = FraudAnalyzer()

<df_train> = <analyzer>.get_ml_feature()

<df_anomalies> = <analyzer>.get_anomalies()
```

## For `utils.py`:

### Chức năng:

- gọi nhanh để sử dụng mà không cần phải viết một file sql phức tạp

### Sử dụng trong code:

```
from src.db.utils import get_df

print(get_df(fraud_label, conditions=1)
```
