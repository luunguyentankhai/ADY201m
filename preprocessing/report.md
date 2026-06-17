
# Fraud Detection Dataset Analysis

## 1. Dataset Overview

The dataset contains more than **6.36 million transactions**, but only **8212 fraud transactions**, meaning fraud accounts for approximately:

$$
\frac{8212}{6362614} \approx 0.129\%
$$

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

$$
\text{hour\_of\_day} = step \bmod 24
$$

was created to extract the hour from the `step` feature.

This is reasonable because fraud is often associated with:

- user activity patterns
- monitoring schedules
- suspicious late-night behavior

rather than specific calendar dates.

---

## 5.2 Error Balance Features

### Sender Balance Error

$$
errorBalanceOrig
=
newbalanceOrig + amount - oldbalanceOrg
$$

For a valid transaction:

	errorBalanceOrig = 0


---

### Receiver Balance Error

$$
errorBalanceDest
=
oldbalanceDest + amount - newbalanceDest
$$

For a valid transaction:

	errorBalanceDest = 0


---

## 5.3 Importance of Error Features

These features encode transaction consistency directly into the model.

If:

$$
error \neq 0
$$

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

$$
newbalanceOrig
=
oldbalanceOrg - amount
$$

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
