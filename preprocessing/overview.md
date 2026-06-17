# 1. Feature-by-Feature Analysis

## General Dataset Information

- **Number of rows:**  `6,362,620`
    
- **Number of columns:** `10`
    
- **Target column:** `isFraud`
    
- **Problem type:** Binary Classification

---

# Feature Analysis

## 1. `step`

- **Data type:** Numeric (integer)
    
- **Distribution:** Likely uniform or periodic (represents time steps)
    
- **Skewness:** Minimal
    
- **Outliers:** Not expected
    
- **Missing values:** Not indicated
    
- **Cardinality:** High (many unique values)
    
- **Quality issues:** None apparent

---

## 2. `type`

- **Data type:** Categorical (`CASH_IN`, `CASH_OUT`, `DEBIT`, `PAYMENT`, `TRANSFER`)
    
- **Distribution:** Imbalanced (`PAYMENT`, `CASH_OUT`, and `CASH_IN` dominate; `DEBIT` is rare)
    
- **Skewness:** High
    
- **Outliers:** Not applicable
    
- **Missing values:** Not indicated
    
- **Cardinality:** Low (5 categories)
    
- **Quality issues:** None apparent

---

## 3. `amount`

- **Data type:** Numeric (float)
    
- **Distribution:** Highly right-skewed (long tail, most transactions are small)
    
- **Skewness:** Severe positive skew
    
- **Outliers:** Many (as shown in boxplots)
    
- **Missing values:** Not indicated
    
- **Cardinality:** High
    
- **Quality issues:** Extreme values may require capping

---

## 4. `oldbalanceOrg` / `newbalanceOrg` / `oldbalanceDest` / `newbalanceDest`

- **Data type:** Numeric (float)
    
- **Distribution:** Highly right-skewed with long tails
    
- **Skewness:** Severe positive skew
    
- **Outliers:** Many (visible in boxplots)
    
- **Missing values:** Not indicated
    
- **Cardinality:** High
    
- **Quality issues:** Check for zero, negative, or inconsistent balances

---

## 5. `isFraud` (Target)

- **Data type:** Binary (0/1)
    
- **Distribution:** Extremely imbalanced (majority class = 0)
    
- **Skewness:** High
    
- **Outliers:** Not applicable
    
- **Missing values:** Not indicated
    
- **Cardinality:** 2
    
- **Quality issues:** None

---

# 2. Feature–Target Relationships

## `type` vs `isFraud`

- **Strength:** Only `TRANSFER` and `CASH_OUT` contain fraud cases.
    
- **Correlation:** Strong categorical relationship; `type` is highly predictive.
    
- **Trend:** Non-linear (fraud only appears in specific transaction types).
    
- **Predictive utility:** Very high
    
- **Leakage risk:** Low
    
- **Statistical importance:** High

---

## `amount` vs `isFraud`

- **Strength:** Fraudulent transactions often involve larger amounts.
    
- **Correlation:** Weak linear relationship but possible non-linear threshold effect.
    
- **Trend:** Transactions in the right tail are more likely to be fraudulent.
    
- **Predictive utility:** Moderate to high
    
- **Leakage risk:** Low
    
- **Statistical importance:** Moderate

---

## Balance Features vs `isFraud`

- **Strength:** Some fraud patterns exist in balance-related features.
    
- **Correlation:** Weak linear correlation with possible non-linear effects.
    
- **Trend:** Extreme balance values may indicate fraud.
    
- **Predictive utility:** Moderate
    
- **Leakage risk:** Low
    
- **Statistical importance:** Moderate
    

---

## `step` vs `isFraud`

- **Strength:** Certain time steps contain more fraud cases.
    
- **Correlation:** Weak overall correlation.
    
- **Trend:** Non-linear and potentially periodic.
    
- **Predictive utility:** Low to moderate
    
- **Leakage risk:** Low
    
- **Statistical importance:** Low

---

# 3. Feature–Feature Relationships

- **Correlation matrix:** Most features are weakly correlated. `newbalanceDest` and `oldbalanceDest` are highly correlated (0.936).
    
- **Multicollinearity:** High correlation exists between old and new balances for the same entity.
    
- **Redundancy:** Some balance features may be redundant.
    
- **Strong interactions:** Strong interactions may exist between `amount` and balances, or between `type` and `amount`.

---

# 4. Class Imbalance

- **Severity:** Fraud cases account for less than 0.2% of all transactions.
    
- **Risks:** Models may ignore the minority fraud class.
    
- **Recommended metrics:** Precision, Recall, F1-score, ROC-AUC, and PR-AUC.
    
- **Resampling:** Use SMOTE, undersampling, or class weighting.

---

# 5. Preprocessing Requirements

- **Encoding:** Apply one-hot encoding to the `type` feature.
    
- **Scaling:** Use `RobustScaler` or log transformation for highly skewed numerical features.
    
- **Log transformations:** Strongly recommended for `amount` and balance-related features.
    
- **Outlier treatment:** Cap or transform extreme values.
    
- **Feature engineering:** Create ratio-based, flag-based, aggregated, and time-based features.

---

# 6. Machine Learning Recommendations

- **Best models:** `Random Forest`, `XGBoost`, and `LightGBM` are strong candidates.
    
- **Most important features:** `type`, `amount`, and balance-related features.
    
- **Features that may harm performance:** Highly collinear balance features.
    
- **Feature engineering:** Modify column `step` and add new columns to check error of **balance** in a transaction.
    
- **Validation strategy:** Use Stratified K-Fold Cross-Validation.


---

# FINE-TUNING PARAMETERS

## Logistic Regression

|Parameter|Description|
|---|---|
|`C`|Regularization strength|
|`penalty`|L1 / L2 regularization|
|`solver`|Optimization algorithm|
|`class_weight`|Class imbalance handling|
|`max_iter`|Maximum training iterations|

---

## Random Forest

|Parameter|Description|
|---|---|
|`n_estimators`|Number of trees|
|`max_depth`|Maximum tree depth|
|`min_samples_split`|Minimum samples required to split|
|`min_samples_leaf`|Minimum samples per leaf|
|`max_features`|Number of features considered at each split|
|`class_weight`|Class imbalance handling|

---

## XGBoost

|Parameter|Description|
|---|---|
|`n_estimators`|Number of boosting rounds|
|`learning_rate`|Learning rate|
|`max_depth`|Tree depth|
|`subsample`|Row sampling ratio|
|`colsample_bytree`|Feature sampling ratio|
|`gamma`|Split regularization parameter|
|`min_child_weight`|Minimum child weight|
|`scale_pos_weight`|Class imbalance handling|

---

## LightGBM

|Parameter|Description|
|---|---|
|`n_estimators`|Number of trees|
|`learning_rate`|Learning rate|
|`num_leaves`|Number of leaves|
|`max_depth`|Maximum tree depth|
|`min_child_samples`|Minimum child samples|
|`subsample`|Row sampling ratio|
|`colsample_bytree`|Feature sampling ratio|
|`reg_alpha`|L1 regularization|
|`reg_lambda`|L2 regularization|

---

## CatBoost

|Parameter|Description|
|---|---|
|`iterations`|Number of boosting rounds|
|`learning_rate`|Learning rate|
|`depth`|Tree depth|
|`l2_leaf_reg`|Regularization parameter|
|`bagging_temperature`|Randomness control|
|`border_count`|Number of split points|
|`auto_class_weights`|Class imbalance handling|