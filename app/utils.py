import pandas as pd

def fetch_data(filepath):
    return pd.read_csv(filepath)

def preprocess_data(df):
    # Handle missing values
    columns_to_check = df.columns.difference(['Comments'])
    df.dropna(subset=columns_to_check, inplace=True)
    # df.dropna(inplace=True)
    
    # Handle anomalies, e.g., negative values in solar irradiance
    df = df[(df['GHI'] >= 0) & (df['DNI'] >= 0) & (df['DHI'] >= 0)]
    
    return df
