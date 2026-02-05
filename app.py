import streamlit as st
import pandas as pd
import requests
import time
import os

# --- CONFIGURATION ---
CSV_FILE = "network_traffic.csv"
CHUNK_SIZE = 10000 

st.set_page_config(page_title="Network Traffic Visualizer", layout="wide")

# --- 1. DATA INGESTION PIPELINE (The "Engineered" Part) ---
@st.cache_data
def load_and_aggregate_data():
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame()

    aggregated_data = {}

    try:
        for chunk in pd.read_csv(CSV_FILE, chunksize=CHUNK_SIZE):
            chunk_agg = chunk.groupby('source_ip')['bytes_sent'].sum()
            for ip, total_bytes in chunk_agg.items():
                aggregated_data[ip] = aggregated_data.get(ip, 0) + total_bytes

        df_agg = pd.DataFrame(list(aggregated_data.items()), columns=['source_ip', 'total_bytes'])
        return df_agg.sort_values(by='total_bytes', ascending=False)
    
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return pd.DataFrame()

# --- 2. API ENRICHMENT (The "Microservices" Part) ---
def get_ip_location(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    try:
        response = requests.get(url)
        data = response.json()
        if data['status'] == 'success':
            return data['lat'], data['lon'], data['country']
    except Exception as e:
        pass # Silently fail for demo purposes
    return None, None, None

# --- 3. THE DASHBOARD UI ---
st.title("🛡️ Network Traffic Log Visualizer")
st.markdown("Processing large logs to visualize high-bandwidth sources.")

# Load Data
df = load_and_aggregate_data()

if df.empty:
    st.warning(f"Data not found. Please run 'python generate_logs.py' first to create '{CSV_FILE}'.")
else:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Top High-Bandwidth IPs")
        st.dataframe(df.head(10))
        
        if st.button("Enrich Top 10 IPs (API Call)"):
            st.info("Fetching location data via REST API...")
            
            # Take top 10 IPs to avoid hitting API rate limits during demo
            top_ips = df.head(10).copy()
            
            lats, lons, countries = [], [], []
            
            progress_bar = st.progress(0)
            for i, (index, row) in enumerate(top_ips.iterrows()):
                lat, lon, country = get_ip_location(row['source_ip'])
                lats.append(lat)
                lons.append(lon)
                countries.append(country)
                
                progress_bar.progress((i + 1) / 10)
            
            top_ips['lat'] = lats
            top_ips['lon'] = lons
            top_ips['country'] = countries
            top_ips = top_ips.dropna(subset=['lat', 'lon'])
            
            st.success("Enrichment Complete!")
            
            # --- 4. VISUALIZATION ---
            if not top_ips.empty:
                st.subheader("Traffic Origin Map")
                st.map(top_ips[['lat', 'lon']])
                
                st.subheader("Traffic by Country")
                st.bar_chart(top_ips.set_index('country')['total_bytes'])
            else:
                st.error("Could not retrieve location data. The API might be blocking requests.")

    with col2:
        st.info("👈 Click the button to query the API and generate the map.")
        st.code("""
# Code Snippet: Ingestion Logic
# Chunking handles files larger than RAM
for chunk in pd.read_csv(file, chunksize=10000):
    process(chunk)
    aggregate_results()
        """, language="python")