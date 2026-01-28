import pandas as pd

def clean_data(df):
    """
    Cleans the raw transaction data:
    1. Removes rows with missing Customer ID.
    2. Converts Customer ID to string.
    3. Removes negative quantities (Returns).
    4. Calculates TotalSpend.
    """
    # Create Copy
    df = df.copy()

    # Drop missing IDs
    df = df.dropna(subset=['Customer ID'])

    # Ensure string type
    df['Customer ID'] = df['Customer ID'].astype(str)

    # Filter only positive quantities
    df = df[df['Quantity'] > 0]

    # Drop Duplicates
    df = df.drop_duplicates()
    # Calculate Total Spend
    df['TotalSpend'] = df['Quantity'] * df['Price']
    return df
