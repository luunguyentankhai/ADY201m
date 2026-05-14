# Fraud Detection in Online Payment Transactions

## SPEC

- Project using python version 3.11 and postgresql:15

- Project Manager:
    - uv python
    - docker

## FOLDER STRUCTURE
```
.
├── data
│   ├── processed
│   └── raw
│       └── Data.csv
├── docker-compose.yml
├── docs
│   └── notes.md
├── main.py
├── notebooks
│   └── 01_pull_and_push.ipynb
├── pyproject.toml
├── README.md
├── src
│   ├── config
│   │   ├── db_config.py
│   │   ├── dir_config.py
│   │   └── __init__.py
│   ├── db
│   │   ├── db_manager.py
│   │   └── schema.sql
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


