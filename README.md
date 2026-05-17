# Fraud Detection in Online Payment Transactions

## SPEC

- Project using python version 3.11 and postgresql:15

- Project Manager:
    - uv python
    - docker

## FOLDER STRUCTURE
```
.
├── CONTRIBUTING.md
├── data
│   ├── processed
│   └── raw
│       └── Data.csv
├── docker-compose.yml
├── docs
│   └── notes.md
├── main.py
├── notebooks
│   ├── 01_pull_and_push.ipynb
│   └── 02_sql_and_eda.ipynb
├── pyproject.toml
├── README.md
├── src
│   ├── config
│   │   ├── db_config.py
│   │   ├── dir_config.py
│   │   └── __init__.py
│   ├── db
│   │   ├── analyzer.py
│   │   ├── db_manager.py
│   │   ├── sql_queries
│   │   │   ├── get_anomalies.sql
│   │   │   ├── get_feature.sql
│   │   │   ├── get_fraud_rate.sql
│   │   │   ├── get_patterns.sql
│   │   │   └── schema.sql
│   │   └── utils.py
│   ├── etl
│   │   ├── cleaner.py
│   │   ├── collect.py
│   │   ├── __init__.py
│   │   ├── pipeline.py
│   │   └── preprocessing.py
│   ├── __init__.py
│   └── models
└── uv.lock
```

## SETUP REQUIREMENT

#### Python
- Actually you have **uv**
- Run `uv sync` to install python libs

#### Docker
- Remember to create .env file to run docker-compose.yml
- For run **Docker** using `docker compose up -d`


