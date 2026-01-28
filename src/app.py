import streamlit as st
import pandas as pd
import pickle
import os
from utils import clean_data

# Setup Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'data', 'model_kmeans.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'data', 'scaler.pkl')

#Load Brain
@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        st.error("Model file not found. Run train_model.py first.")
        return None, None
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler

model, scaler = load_model()

#User Inputs
st.title("AI Discount Optimizer")
# --- CREATE TABS FOR DIFFERENT MODES ---
tab1, tab2 = st.tabs(["Single Simulation", "Batch Processing (Real Data)"])
# =========================================
# TAB 1: Single User Simulation
# =========================================
with tab1:
    st.header("Simulate a Customer")
    col1, col2, col3 = st.columns(3)
    with col1:
        recency = st.number_input("Day Since Last Purchase", min_value=0, value=200)
    with col2:
        frequency = st.number_input("Total Transactions", min_value=1, value=5)
    with col3:
        monetary = st.number_input("Total Spend ($)", min_value=0.0, value=500.0)

    if st.button("Predict Single User"):
        input_data = pd.DataFrame({
            'Recency': [recency],
            'Frequency': [frequency],
            'Monetary':[monetary]
        })

        input_scaled = scaler.transform(input_data)
        cluster = model.predict(input_scaled)[0]

        if cluster == 0:
            st.error(f"At-Risk (Cluster {cluster}) -> Send 15% Coupon")
        elif cluster == 2:
            st.balloons()
            st.success(f"VIP (Cluster {cluster}) -> No Discount Needed")
        else:
            st.info(f"Regular (Cluster {cluster}) -> Standard Marketing")
with tab2:
    st.header("Upload Raw Sales Data")