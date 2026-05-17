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
| `feature_hour`                 | <!-- Write description here -->                                     |
| `feature_day_of_week`          | <!-- Write description here -->                                     |
| `transaction_type`             | Type of transaction (`Online`, `In-Store`, `ATM`, etc.)             |
| `device_type`                  | Type of device used (`Mobile`, `Desktop`, etc.)                     |
| `location`                     | Geographical location of the transaction                            |
| `merchant_category`            | Type of merchant (`Retail`, `Food`, `Travel`, etc.)                 |
| `authentication_method`        | How the user authenticated (`PIN`, `Biometric`, etc.)               |
| `target`                       | Target variable (`0 = Not Fraud`, `1 = Fraud`)                      |
