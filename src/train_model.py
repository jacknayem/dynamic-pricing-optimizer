import pandas as pd
import pickle
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

# 1. Setup Paths

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'retail.db')
MODEL_PATH = os.path.join(BASE_DIR, 'data', 'model_kmeans.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'data', 'scaler.pkl')

engine = create_engine(f'sqlite:///{DB_PATH}')

def train():
    print('Start Model Training....')
    df = pd.read_sql("SELECT * FROM transactions", engine)

    #Celan Data
    df = df.dropna(subset=['Customer ID'])
    df['Customer ID'] = df['Customer ID'].astype(str)
    df = df[df['Quantity'] > 0]
    df = df.drop_duplicates()
    df['TotalSpend'] = df['Quantity'] * df['Price']

    # Aggregated RFM
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    customers = df.groupby('Customer ID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'Invoice': 'count',
        'TotalSpend': 'sum'
    })
    customers.rename(columns={
        'InvoiceDate': 'Recency',
        'Invoice': 'Frequency',
        'TotalSpend': 'Monetary'
    }, inplace=True)

    # Pre-processing
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(customers)

    # TRAIN MODEL
    print("Training K-Means Model (3 Clusters)...")
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans.fit(scaled_data)

    # Add clusters back to our data to see who is who
    customers['Cluster'] = kmeans.labels_

    # Interpret Cluster
    cluster_summary = customers.groupby('Cluster').mean()
    print("\nCluster Profiles (Interpret this to assign discounts):")
    print(cluster_summary)

    # Save System
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(kmeans, f)
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)
    print(f'Model Saved to {MODEL_PATH}')

if __name__ == '__main__':
    train()
