import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def db_engine():
    URL = os.getenv("DATABASE_URL")

    try:
        engine = create_engine(URL, pool_pre_ping=True)
        return engine
    except Exception as e:
        print(f"Error: {e}")
        raise

