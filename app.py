# app.py
import sys
from pathlib import Path

# Ensure the root directory is appended to sys.path for local module resolution
sys.path.append(str(Path(__file__).resolve().parent))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium

from src.geospatial_analytics import detect_chokepoints, calculate_oil_on_water

st.set_page_config(page_title="Oil Trade Flow Tracker", layout="wide")

st.title("Oil Trade Flow & AIS Analytics Dashboard")
st.write("Real-time crude & product tanker tracking, chokepoint congestion, and Oil-on-Water monitoring.")

# Load simulated AIS dataset
@st.cache_data
def load_sample_ais():
    np.random.seed(42)
    n_vessels = 120
    data = {
        "mmsi": [f"MMSI_{1000+i}" for i in range(n_vessels)],
        "vessel_name": [f"Tanker_{i}" for i in range(n_vessels)],
        "vessel_class": np.random.choice(["VLCC", "Suezmax", "Aframax"], size=n_vessels, p=[0.4, 0.35, 0.25]),
        "latitude": np.random.uniform(15.0, 32.0, n_vessels),
        "longitude": np.random.uniform(30.0, 58.0, n_vessels),
        "dwt": np.random.choice([270000, 150000, 100000], size=n_vessels),
        "draft": np.random.uniform(12.0, 20.0, n_vessels),
        "max_draft": 20.0,
        "nav_status": np.random.choice(["Underway", "Moored / Waiting"], size=n_vessels, p=[0.75, 0.25]),
        "cargo_type": np.random.choice(["Crude Oil", "Refined Products"], size=n_vessels, p=[0.7, 0.3])
    }
    df = pd.DataFrame(data)
    return detect_chokepoints(df)

df_ais = load_sample_ais()

# Sidebar filters
st.sidebar.header("Filter Options")
selected_class = st.sidebar.multiselect(
    "Vessel Class", 
    options=["VLCC", "Suezmax", "Aframax"], 
    default=["VLCC", "Suezmax", "Aframax"]
)
selected_cargo = st.sidebar.multiselect(
    "Cargo Type", 
    options=["Crude Oil", "Refined Products"], 
    default=["Crude Oil", "Refined Products"]
)

filtered_df = df_ais[
    (df_ais['vessel_class'].isin(selected_class)) & 
    (df_ais['cargo_type'].isin(selected_cargo))
]

# Market Indicators (KPIs)
st.subheader("Market Indicators")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_oil_on_water = calculate_oil_on_water(filtered_df)
active_tankers = len(filtered_df)
waiting_tankers = len(filtered_df[filtered_df['nav_status'] == 'Moored / Waiting'])
suez_traffic = len(filtered_df[filtered_df['chokepoint'] == 'Suez_Canal'])

with kpi1:
    st.metric(label="Tracked Tankers", value=f"{active_tankers}")
with kpi2:
    st.metric(label="Oil-on-Water (MMbbl)", value=f"{total_oil_on_water:.2f} M bbl")
with kpi3:
    st.metric(label="Congestion / Waiting", value=f"{waiting_tankers} vessels")
with kpi4:
    st.metric(label="Suez Passage Traffic", value=f"{suez_traffic} vessels")

st.divider()

# Map and Chart Layout
col_map, col_chart = st.columns([2, 1])

with col_map:
    st.write("### Live Tanker Fleet Positions")
    m = folium.Map(location=[22.0, 45.0], zoom_start=4, tiles="OpenStreetMap")
    
    for _, row in filtered_df.iterrows():
        color = "red" if row['nav_status'] == 'Moored / Waiting' else "blue"
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=6 if row['vessel_class'] == 'VLCC' else 4,
            popup=f"<b>{row['vessel_name']}</b> ({row['vessel_class']})<br>Status: {row['nav_status']}<br>Cargo: {row['cargo_type']}",
            color=color,
            fill=True,
            fill_opacity=0.7
        ).add_to(m)
        
    st_folium(m, width="100%", height=450)

with col_chart:
    st.write("### Tonnage Distribution by Region")
    fig_pie = px.pie(filtered_df, names="chokepoint", title="Fleet Location Breakdown", hole=0.4)
    st.plotly_chart(fig_pie, width="stretch")