import pandas as pd
from sqlalchemy import create_engine
import os

def get_engine():
    db_url = os.environ.get("DATABASE_URL", "postgresql://user:password@127.0.0.1:5433/investment_chatbot")
    return create_engine(db_url)

def load_table(table_name):
    engine = get_engine()
    try:
        return pd.read_sql_table(table_name, engine)
    except Exception as e:
        return pd.DataFrame()
