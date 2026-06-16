# Fraud Detection in Online Payment Transactions

## INTRODUCTION

A machine learning-based fraud detection system that leverages domain-specific feature engineering and LightGBM to identify fraudulent financial transactions in the PaySim dataset.

## TECH STACK & TOOLS

- **Backend:** Python 3.11, PostgreSQL 15
- **Frontend:** React + TypeScript
- **Tools & Package Managers:**
  - `uv` (Python dependency manager)
  - Docker
  - `pnpm` (Node package manager)
  - Vite

## SETUP REQUIREMENTS

#### Python
- Ensure you have **`uv`** installed.
- Run `uv sync` to install Python dependencies.

#### Docker
- Create a `.env` file (you can use `.env.example` as a template) for Docker configuration.
- Start Docker services by running: `docker compose up -d`

#### Web
- Ensure **Node.js** is installed.
- Install **pnpm** globally by running: `npm install -g pnpm`
- Navigate to the frontend folder and install dependencies:
  ```bash
  cd web/frontend
  pnpm install
  ```

## HOW TO RUN

### Training Models
1. Ensure your `.env` file is set up and start the database:
   ```bash
   docker compose up -d
   ```
2. Run the notebook `notebooks/01_pull_and_push.ipynb` and wait for the data to be pushed into the database.
3. Once the data is successfully pushed, navigate to the `sql_queries` folder:
   ```bash
   cd src/db/sql_queries/
   ```
4. Execute the following command to extract features:
   *(Note: If you have already run this command before, you do NOT need to run it again.)*
   ```bash
   docker exec -i <container_name> psql -U <POSTGRES_USER> -d <POSTGRES_DB> < "get_feature.sql"
   ```
5. After that, run the main pipeline to start training the models:
   ```bash
   uv run src/main_pipeline.py
   ```

### Website Development Server
You have two options for running the web application:

**Option 1: Single Terminal (No backend logs)**
If you just want to run the application quickly without monitoring the backend logs, simply run:
```bash
uv run run_dev.py
```

**Option 2: Two Terminals (View frontend & backend logs separately)**
To monitor logs effectively, run the frontend and backend in separate terminals:
- **Terminal 1 (Frontend):** Navigate to `web/frontend` and start the Vite dev server using `pnpm` (it is highly recommended to use `pnpm` instead of `npm` to avoid bloating your local environment):
  ```bash
  cd web/frontend
  pnpm run dev
  ```
- **Terminal 2 (Backend):** Open a new shell, ensure you are in the root directory, and start the backend application:
  ```bash
  uv run start_app.py
  ```

## FOLDER STRUCTURE

```text
.
├── data
│   ├── processed
│   │   ├── Assets
│   │   └── Models
│   └── raw
├── docs
├── notebooks
├── preprocessing
├── src
│   ├── config
│   ├── db
│   │   └── sql_queries
│   ├── eda
│   ├── etl
│   ├── models
│   └── utils
└── web
    ├── backend
    │   ├── config
    │   ├── controllers
    │   ├── core
    │   ├── middleware
    │   ├── models
    │   ├── routes
    │   └── services
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
