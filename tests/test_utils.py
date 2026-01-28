import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils import clean_data

def test_clean_data_removes_negative_quantity():
    # 1. ARRANGE (Create fake dirty data)
    # We create a dataframe with 2 rows: one "Good" sale, one "Bad" return (-5)
    raw_data = pd.DataFrame({
        'Customer ID': ['123', '456'],
        'Quantity': [10, -5],
        'Price': [5.0, 5.0]
    })

    cleaned_df = clean_data(raw_data)

    # Check A: Did it remove the negative row?
    assert len(cleaned_df) == 1, "Failled to Remove the negative quantity row!"

    # Check B: Is the remaining row the correct one? (Customer 123)
    assert cleaned_df.iloc[0]['Customer ID'] == '123', 'Wrong row remained!'

    # Check C: Did it calculate TotalSpend correctly? (10 * 5.0 = 50.0)
    assert cleaned_df.iloc[0]['TotalSpend'] == 50.0, "TotalSpend Calcualtion is wrong!"

def test_clean_data_removes_missing_id():
    # 1. ARRANGE
    raw_data = pd.DataFrame({
        'Customer ID': ['123', None],
        'Quantity': [10, 10],
        'Price': [5.0, 5.0]
    })

    # 2. ACT
    cleaned_df = clean_data(raw_data)

    # 3. ASSERT
    assert len(cleaned_df) == 1, "Failed to drop the missing Customer ID!"



