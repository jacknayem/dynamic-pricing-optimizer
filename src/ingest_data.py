import pandas as pd
from sqlalchemy import create_engine
import os

# Define Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw_data.xlsx')
DB_PATH = os.path.join(BASE_DIR, 'data', 'retail.db')

def ingest_data():
    print('Loading data....')

    # Read the excel file
    df = pd.read_excel(DATA_PATH, sheet_name='Year 2010-2011', dtype={'Customer ID': str})
    print(f'Data Loaded: {df.shape[0]} rows found')

    # Create a local SQLite database engine
    engine = create_engine(f'sqlite:///{DB_PATH}')
    print('Writing to SQLite database...')
    df.to_sql('transactions', engine, index=False, if_exists='replace')
    print("Success! Data is now inside 'data/retail.db' in table 'transactions'.")

if __name__ == "__main__":
    ingest_data()