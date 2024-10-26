import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

st.set_page_config(
    page_title="Geomagnetic Activity Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🌐 Interactive Geomagnetic Activity Dashboard")
st.markdown("""
This application visualizes geomagnetic activity across the Earth using ground-based magnetometer data.
Select a time and location to explore global geomagnetic disturbances and view a timeline of magnetic intensity.
""")

st.sidebar.header("Data Selection & Configuration")

csv_file = '20241026-06-57-supermag.csv'

if not os.path.isfile(csv_file):
    st.error(f"CSV file '{csv_file}' not found in the current directory: {os.getcwd()}")
    st.stop()

try:
    data = pd.read_csv(csv_file)
except Exception as e:
    st.error(f"Error loading CSV file: {e}")
    st.stop()

required_columns = ['Date_UTC', 'GEOLON', 'GEOLAT', 'dbn_geo', 'dbe_geo', 'dbz_geo']
missing_columns = [col for col in required_columns if col not in data.columns]
if missing_columns:
    st.error(f"CSV file is missing required columns: {', '.join(missing_columns)}")
    st.stop()

try:
    data['Date_UTC'] = pd.to_datetime(data['Date_UTC'])
except Exception as e:
    st.error(f"Error parsing 'Date_UTC' column as datetime: {e}")
    st.stop()

unique_times = data['Date_UTC'].dt.floor('T').unique()
unique_times = sorted(unique_times)

selected_time = st.sidebar.selectbox(
    "Select Time",
    options=unique_times,
    format_func=lambda x: x.strftime("%Y-%m-%d %H:%M:%S"),
    help="Select the specific time to visualize geomagnetic activity."
)

data_time = data[data['Date_UTC'] == selected_time].copy()

location_options = data[['GEOLON', 'GEOLAT']].drop_duplicates().reset_index(drop=True)
location_selection = st.sidebar.selectbox(
    "Select Location for Intensity Timeline",
    options=location_options.index,
    format_func=lambda x: f"Longitude: {location_options.iloc[x]['GEOLON']}, Latitude: {location_options.iloc[x]['GEOLAT']}",
    help="Select a location to view its magnetic intensity timeline."
)

selected_location = location_options.iloc[location_selection]
longitude = selected_location['GEOLON']
latitude = selected_location['GEOLAT']

if data_time.empty:
    st.warning("No data available for the selected time.")
else:
    data_time['Total_Field'] = data_time[['dbn_geo', 'dbe_geo', 'dbz_geo']].abs().sum(axis=1)

    viz_df = data_time[['GEOLON', 'GEOLAT', 'Total_Field']].copy()
    viz_df.rename(columns={'GEOLON': 'Longitude', 'GEOLAT': 'Latitude'}, inplace=True)
    viz_df.dropna(subset=['Longitude', 'Latitude', 'Total_Field'], inplace=True)
    viz_df['Longitude'] = viz_df['Longitude'].apply(lambda x: round(x - 360 if x > 180 else x))

    st.subheader("3D Geomagnetic Disturbance Heatmap")

    heatmap_layer = pdk.Layer(
        "HeatmapLayer",
        data=viz_df,
        get_position=['Longitude', 'Latitude'],
        get_weight='Total_Field',
        radius=15000,
        threshold=0.2,
        aggregation='sum',
    )

    column_layer = pdk.Layer(
        "ColumnLayer",
        data=viz_df,
        get_position=['Longitude', 'Latitude'],
        get_elevation='Total_Field',
        elevation_scale=500,
        radius=20000,
        get_fill_color=[255, 0, 0, 180],
        pickable=True,
        extruded=True,
    )

    view_state = pdk.ViewState(
        latitude=0,
        longitude=0,
        zoom=1,
        pitch=60
    )

    deck = pdk.Deck(
        layers=[heatmap_layer, column_layer],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/dark-v10',
        tooltip={
            "html": "<b>Latitude:</b> {Latitude}<br/><b>Longitude:</b> {Longitude}<br/><b>Total Magnetic Field:</b> {Total_Field} nT",
            "style": {
                "backgroundColor": "steelblue",
                "color": "white"
            }
        }
    )

    st.pydeck_chart(deck, height=650)

st.subheader(f"Magnetic Disturbance Intensity Timeline")

location_data = data[(data['GEOLON'] == longitude) & (data['GEOLAT'] == latitude)].copy()

location_data['Total_Field'] = location_data[['dbn_geo', 'dbe_geo', 'dbz_geo']].abs().sum(axis=1)

fig, ax = plt.subplots(figsize=(10, 4))
fig.patch.set_facecolor('#101414')
ax.set_facecolor('#101414')

ax.plot(location_data['Date_UTC'], location_data['Total_Field'], color='#FFA500', marker='o', linestyle='-', linewidth=1.5, markersize=5)

ax.set_xlabel("Time (UTC)", color='white', fontsize=12)
ax.set_ylabel("Magnetic Field Intensity (nT)", color='white', fontsize=12)
ax.set_title(f"Longitude: {longitude}, Latitude: {latitude}", color='white', fontsize=14)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('gray')
ax.spines['bottom'].set_color('gray')
ax.tick_params(axis='x', colors='gray', labelsize=10)
ax.tick_params(axis='y', colors='gray', labelsize=10)
ax.grid(color='#444444', linestyle='--', linewidth=0.5)

st.pyplot(fig)
