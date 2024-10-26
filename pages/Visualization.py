import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import matplotlib.pyplot as plt
import os

# ---------------------------
# Streamlit App Configuration
# ---------------------------

st.set_page_config(
    page_title="Geomagnetic Activity Heat Map",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🌐 Interactive 3D Geomagnetic Activity Heat Map")
st.markdown("""
This application visualizes geomagnetic activity across the Earth using ground-based magnetometer data.
Select a specific time instance from the sidebar to explore the global geomagnetic activity.
""")

# ---------------------------
# Sidebar: File Path and Time Selection
# ---------------------------

st.sidebar.header("Data Selection")

# Define the path to your CSV file
# Ensure the file '20241026-06-57-supermag.csv' is in the same directory as this script
csv_file = '20241026-06-57-supermag.csv'

# Check if the file exists
if not os.path.isfile(csv_file):
    st.error(f"CSV file '{csv_file}' not found in the current directory: {os.getcwd()}")
    st.stop()

try:
    # Load the CSV data into a Pandas DataFrame without parsing dates initially
    data = pd.read_csv(csv_file)
except Exception as e:
    st.error(f"Error loading CSV file: {e}")
    st.stop()

# Display column names for verification
st.sidebar.subheader("Dataset Columns")
st.sidebar.write(data.columns.tolist())

# Ensure essential columns are present
required_columns = ['Date_UTC', 'GEOLON', 'GEOLAT', 'dbn_geo', 'dbe_geo', 'dbz_geo']
missing_columns = [col for col in required_columns if col not in data.columns]
if missing_columns:
    st.error(f"CSV file is missing required columns: {', '.join(missing_columns)}")
    st.stop()

# Parse 'Date_UTC' as datetime
try:
    data['Date_UTC'] = pd.to_datetime(data['Date_UTC'])
except Exception as e:
    st.error(f"Error parsing 'Date_UTC' column as datetime: {e}")
    st.stop()

# Display a few rows of the data for verification
st.write("### Sample Data", data.head())

# Extract unique timestamps for selection
unique_times = data['Date_UTC'].dt.floor('T').unique()
unique_times = sorted(unique_times)

# Time Selection: Dropdown
selected_time = st.sidebar.selectbox(
    "Select Time",
    options=unique_times,
    format_func=lambda x: x.strftime("%Y-%m-%d %H:%M:%S"),
    help="Select the specific time to visualize geomagnetic activity."
)

# Filter data for the selected time
data_time = data[data['Date_UTC'] == selected_time]

if data_time.empty:
    st.warning("No data available for the selected time.")
else:
    # Calculate Total Magnetic Field Strength
    # Total_Field = |dbn_geo| + |dbe_geo| + |dbz_geo|
    data_time['Total_Field'] = data_time[['dbn_geo', 'dbe_geo', 'dbz_geo']].abs().sum(axis=1)
    
    # Prepare DataFrame for Visualization
    viz_df = data_time[['GEOLON', 'GEOLAT', 'Total_Field']].copy()
    viz_df.rename(columns={'GEOLON': 'Longitude', 'GEOLAT': 'Latitude'}, inplace=True)
    
    # Remove any rows with missing or invalid data
    viz_df.dropna(subset=['Longitude', 'Latitude', 'Total_Field'], inplace=True)
    
    # Display DataFrame Columns
    st.write("### DataFrame Columns:", viz_df.columns.tolist())
    
    # ---------------------------
    # Color Mapping Function
    # ---------------------------
    
    def get_color(value, max_val):
        """
        Map Total_Field to color.
        Blue (low) to Red (high).
        """
        normalized = value / max_val if max_val else 0
        r = int(255 * normalized)
        g = 0
        b = int(255 * (1 - normalized))
        return [r, g, b, 180]  # RGBA
    
    # Apply color mapping
    max_field = viz_df['Total_Field'].max()
    viz_df['color'] = viz_df['Total_Field'].apply(lambda x: get_color(x, max_field))
    
    # ---------------------------
    # Visualization with HexagonLayer
    # ---------------------------
    
    # Define the PyDeck HexagonLayer
    hex_layer = pdk.Layer(
        "HexagonLayer",
        data=viz_df,
        get_position=['Longitude', 'Latitude'],
        auto_highlight=True,
        radius=50000,  # 50 km radius
        elevation_scale=50,
        elevation_range=[0, 1000],
        pickable=True,
        extruded=True,
        get_fill_color='color',
        get_elevation='Total_Field',
    )
    
    # Define the initial view state
    view_state = pdk.ViewState(
        latitude=0,
        longitude=0,
        zoom=1,
        pitch=60  # Tilt the map for better 3D effect
    )
    
    # Define tooltips with correct placeholder
    tooltip = {
        "html": "<b>Total Magnetic Field:</b> {elevationValue} nT",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }
    
    # Create the Deck.gl map
    deck = pdk.Deck(
        layers=[hex_layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style=None  # Use default OpenStreetMap tiles
    )
    
    # Display the map in Streamlit
    st.pydeck_chart(deck)
    
    # ---------------------------
    # Add Color Legend
    # ---------------------------
    
    st.markdown("### Legend: Total Magnetic Field Strength (nT)")
    
    # Create a color bar using matplotlib
    fig, ax = plt.subplots(figsize=(6, 1))
    fig.subplots_adjust(bottom=0.5)
    
    cmap = plt.get_cmap('jet')
    norm = plt.Normalize(vmin=viz_df['Total_Field'].min(), vmax=viz_df['Total_Field'].max())
    cb1 = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=ax, orientation='horizontal')
    cb1.set_label('Total Magnetic Field Strength (nT)')
    
    st.pyplot(fig)

# ---------------------------
# Footer
# ---------------------------

st.markdown("""
---
**Data Source:** `20241026-06-57-supermag.csv`  
**Visualization:** [PyDeck](https://deck.gl/) & [Matplotlib](https://matplotlib.org/)  
**Built with:** [Streamlit](https://streamlit.io/)
""")
