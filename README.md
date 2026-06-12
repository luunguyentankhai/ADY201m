# Fraud Detection in Online Payment Transactions

## INTRODUCTION

- A machine learning-based fraud detection system that leverages domain-specific feature engineering and LightGBM to identify fraudulent financial transactions in the PaySim dataset.

## SPEC

- Project using python version 3.11, postgresql:15 - for website project using react + ts

- Project Manager:
  - uv python
  - docker
  - pnpm
  - vite

## SETUP REQUIREMENT

#### Python

- Actually you have **uv**
- Run `uv sync` to install python libs

#### Docker

- Remember to create .env file to run docker-compose.yml
- For run **Docker** using `docker compose up -d`

#### Web

- Install **node.js** to install **_pnpm_** using command for install `npm install pnpm`
- After install **_pnpm_** moving to folder frontend and run `pnpm install`
- For run website localhost using `pnpm run dev`

## HOW TO RUN

- Training Models:
  - Create `.env`(you can see example in `.env.example`) file and run `docker compose up -d`
  - Run `notebooks/01_pull_and_push.ipynb` and wait to data push into database
  - Where data pushed into database, moving to folder **sql_queries/** `cd src/db/sql_queries/`. On **sql_queries** folder using command:

    _(Note: If you run this command before, you do need to run this command again)_

    `docker exec -i <contanier_name> psql -U <POSTGRES_USER> -d <POSTGRES_DB> < "get_feature.sql"`

  - After that, run `main_pipeline.py` to start training models

- Website (for running website you have 2 option):
  - Option 1: If you just want to run web and don't need to see log, you just run `uv run run_dev.py`
  - Option 2: For wanting see logs you need to move frontend folder `cd web/frontend` and use `pnpm run dev` - don't use `npm run dev` if you don't want many trash on machine. After that, for seeing backend logs run other shell and call `uv run start_app.py`

## FOLDER STRUCTURE

```
.
├── data
│   ├── processed
│   │   ├── Assets
│   │   └── Models
│   └── raw
├── docs
├── notebooks
├── preprocessing
├── src
│   ├── config
│   ├── db
│   │   └── sql_queries
│   ├── eda
│   ├── etl
│   ├── models
│   └── utils
└── web
    ├── backend
    │   ├── config
    │   ├── controllers
    │   ├── core
    │   ├── middleware
    │   ├── models
    │   ├── routes
    │   └── services
    └── frontend
        └── src
            ├── api
            ├── assets
            ├── components
            ├── services
            ├── types
            └── utils

34 directories
```
