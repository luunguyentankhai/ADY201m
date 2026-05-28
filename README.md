# Fraud Detection in Online Payment Transactions

## NOTE

- All team members must log the completion time of each task into the `notes.md` file inside the `docs/` folder immediately upon finishing

## SPEC

- Project using python version 3.11, postgresql:15 - for website project using react + ts

- Project Manager:
    - uv python
    - docker
    - pnpm
    - vite

## FOLDER STRUCTURE
```
.
├── CONTRIBUTING.md
├── data <-- Data storage directory (Git-ignored to optimize repository size)
│   ├── processed <-- Processed data, evaluation charts, and output artifacts
│   │   ├── 7_models_benchmark.csv
│   │   ├── Assets 
│   │   │   ├── dist_log_amount.png
│   │   │   ├── ...
│   │   ├── Cleaned_Data.csv
│   │   ├── LightGBM_Feature_Importance.csv
│   │   └── Models <-- Storage for trained Machine Learning models (.pkl)
│   │       ├── CatBoost.pkl
│   │       ├── ...
│   └── raw <-- Original raw data
│       └── Data.csv
├── docker-compose.yml
├── docs <-- Project documentation directory
│   └── notes.md
├── logs <-- System runtime logs
│   ├── app.log
│   ├── DataBase.log
│   ├── Models.log
│   └── utils.log
├── main_pipeline.py
├── notebooks <-- Jupyter Notebooks for research and experimentation
│   ├── 01_pull_and_push.ipynb
│   ├── ...
├── preprocessing <-- Documentation and reports related to data cleaning
│   ├── data_cleaning.ipynb
│   ├── ...
├── pyproject.toml
├── README.md
├── src <-- Main source code directory (Core AI Engine)
│   ├── config <-- System configuration variables and path settings
│   │   ├── db_config.py
│   │   ├── ...
│   ├── db <-- Database connections, management, and operations
│   │   ├── analyzer.py
│   │   ├── ...
│   │   ├── sql_queries <-- Directory containing SQL query files (.sql)
│   │   │   ├── get_anomalies.sql
│   │   │   ├── ...
│   ├── eda <-- Scripts for automated Exploratory Data Analysis
│   │   ├── distribution_plt.py
│   │   ├── ...
│   ├── etl <-- Extract, Transform, Load processes (Data pipeline)
│   │   ├── cleaner.py
│   │   ├── ...
│   ├── models <-- Model training, optimization, and evaluation
│   │   ├── evaluator.py
│   │   ├── ...
│   └── utils <-- Shared utility functions for the system
│       ├── file_helpers.py
│       ├── ...
├── start_app.py 
├── uv.lock
└── web <-- Full-stack web application directory
    ├── backend <-- API server system (FastAPI)
    └── frontend <-- User interface system (React/Vite)
        ├── eslint.config.js
        ├── index.html 
        ├── package.json 
        ├── pnpm-lock.yaml
        ├── public <-- Static assets directory
        │   ├── favicon.svg 
        │   └── icons.svg
        ├── README.md 
        ├── src <-- Main user interface source code
        │   ├── App.css 
        │   ├── App.tsx 
        │   ├── assets <-- Images and resources used directly in the UI
        │   │   ├── hero.png
        │   │   ├── react.svg 
        │   │   └── vite.svg 
        │   ├── index.css 
        │   └── main.tsx 
        ├── tsconfig.app.json
        ├── tsconfig.json
        ├── tsconfig.node.json
        └── vite.config.ts
```

## SETUP REQUIREMENT

#### Python
- Actually you have **uv**
- Run `uv sync` to install python libs

#### Docker
- Remember to create .env file to run docker-compose.yml
- For run **Docker** using `docker compose up -d`

#### Web
- Install **node.js** to install ***pnpm*** using command for install `npm install pnpm`
- After install ***pnpm*** moving to folder frontend and run `pnpm install`
- For run website localhost using `pnpm run dev`


