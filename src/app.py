import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# Setup Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'data', 'model_kmeans.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'data', 'scaler.pkl')

#Load Brain
@st.cache_resource
def load_model():
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler

model, scaler = load_model()

#User Inputs
col1, col2, col3 = st.columns(3)
with col1:
    recency = st.number_input("Days Since Last Purchase", min_value=0, value=200)
with col2:
    frequency = st.number_input("Total Transactions", min_value=1, value=5)
with col3:
    monetary = st.number_input("Total Spend ($)", min_value=0.0, value=500.0)

## The "Predict" Button
if st.button("Run Model"):
    input_data = pd.DataFrame({
        'Recency': [recency],
        'Frequency': [frequency],
        'Monetary': [monetary]
    })
    input_scaled = scaler.transform(input_data)
    
    cluster = model.predict(input_scaled)[0]

    if cluster == 0:
        st.error(f"Customer belong to Cluster {cluster}(At Risk)")
        st.success("RECOMMENDATION: Send 15% Discount Coupon!")
    elif cluster == 2:
        st.balloons()
        st.info(f"Customer belongs to Cluster {cluster} (VIP).")
        st.warning("RECOMMENDATION: No Discount. Upsell Premium items.")
    else:
        st.info(f"Customer belongs to Cluster {cluster} (Regular).")
        st.warning("RECOMMENDATION: No Discount needed.")