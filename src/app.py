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

st.write("### Created by Abu Nayem")
st.markdown("""
    <a href="https://github.com/jacknayem" target="_blank">GitHub</a> | 
    <a href="https://www.linkedin.com/in/jacknayem/" target="_blank">LinkedIn</a> | 
    <a href="https://jacknayem.medium.com/" target="_blank">Medium</a>
    """, unsafe_allow_html=True)
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
    st.write("Upload a raw Excel file to automatically calculate RFM and segments for ALL customers.")

    # --- DEMO FILE DOWNLOADER ---
    DEMO_FILE_PATH = os.path.join(BASE_DIR, 'data', 'test_data.xlsx')
    if os.path.exists(DEMO_FILE_PATH):
        with open(DEMO_FILE_PATH, "rb") as file:
            btn = st.download_button(
                label="Download Demo Excel File",
                data=file,
                file_name= "test_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.warning(f"Demo file not found at: {DEMO_FILE_PATH}")
        st.write("Please commit a file named 'test_data.xlsx' to your 'data' folder in GitHub.")
    st.markdown("---")
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'])
    
    if uploaded_file and st.button("Process Batch"):
        with st.spinner("Processing Thousands of Rows..."):
            # Read and Clean
            df_raw = pd.read_excel(uploaded_file, sheet_name='Year 2009-2010', dtype={'Customer ID':str})
            df_clean = clean_data(df_raw)

            # Calculate RFM for every Customer automatically
            snapshot_date = df_clean['InvoiceDate'].max() + pd.Timedelta(days=1)

            rfm_table = df_clean.groupby('Customer ID').agg({
                'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
                'Invoice': 'count',
                'TotalSpend': 'sum'
            })

            rfm_table.rename(columns={'InvoiceDate': 'Recency', 'Invoice': 'Frequency', 'TotalSpend': 'Monetary'}, inplace=True)

            rfm_scaled = scaler.transform(rfm_table)
            rfm_table['Cluster'] = model.predict(rfm_scaled)
            
            # 4. Add Business Logic Column
            def get_action(cluster):
                if cluster == 0: return "Send 15% Coupon"
                elif cluster == 2: return "Upsell (VIP)"
                else: return "Standard"

            rfm_table['Recommendation'] = rfm_table['Cluster'].apply(get_action)

            # 5. Show Results
            st.success(f"Processed {len(rfm_table)} Customers!")
            st.dataframe(rfm_table.style.applymap(lambda x: 'background-color: #ffcccc' if x == 'Send 15% Coupon' else '', subset=['Recommendation']))

            # 6. Download Button
            csv = rfm_table.to_csv().encode('utf-8')
            st.download_button(
                label= "Download Results CSV",
                data = csv,
                file_name= 'customer_segmentation_results.csv',
                mime= 'text/csv'
            )
