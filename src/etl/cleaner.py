import pandas as pd
import numpy as np

def lower_columns_name(df):
    
    df.columns = df.columns.str.lower().str.replace(' ','_')
    return df

def format_datetime(df):
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    return df

def clean_text_data(df):

    str_cols = df.select_dtypes(include=["object", "string"]).columns

    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()

    return df

def fix_check_missing(df):
    
    if df.isnull().sum().sum() == 0:
        print("Data Clear")
        return df

    print("Data have missing values")

    crit_cols = ['transaction_id', 'user_id', 'timestamp']

    cols_check = [cols for cols in crit_cols if col in df.columns]

    before_drop = len(df)
    df = df.dropna(subset=cols_check)

    if len(df) < before_drop:
        print("Missing at Critical Columns")

    for col in df.columns:
        if df[col].isnull().any():

            # Numberic

            if pd.api.types.is_numeric_dtype(df[col]):
                median_val = df[col].median()

                df[col] = df[col].fillna(median_val)

                print(f"Fixed: filling {median_val} of {col}")

            # String/Category/Boolean

            else:

                df[col] = df[col].fillna("Unknow")

                print(f"Fixed: filling 'Unknow' of {col}")

    print("Done process missing data")
    return df

