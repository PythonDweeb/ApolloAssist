import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib as mpl

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
# Sidebar: Data Selection & Configuration
# ---------------------------

st.sidebar.header("Data Selection & Configuration")

# Define the path to your CSV file
csv_file = '20241026-06-57-supermag.csv'

# Check if the file exists
if not os.path.isfile(csv_file):
    st.error(f"CSV file '{csv_file}' not found in the current directory: {os.getcwd()}")
    st.stop()

try:
    # Load the CSV data into a Pandas DataFrame
    data = pd.read_csv(csv_file)
except Exception as e:
    st.error(f"Error loading CSV file: {e}")
    st.stop()

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

# ---------------------------
# Sidebar: Heatmap Configuration
# ---------------------------

st.sidebar.header("Heatmap Configuration")

# Slider for Heatmap Intensity
intensity = st.sidebar.slider(
    "Heatmap Intensity",
    min_value=0.1,
    max_value=10.0,
    value=1.0,  # Default value set to 1
    step=0.1,
    help="Adjust the overall intensity of the heatmap."
)

# ---------------------------
# Data Processing
# ---------------------------

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
data_time = data[data['Date_UTC'] == selected_time].copy()

if data_time.empty:
    st.warning("No data available for the selected time.")
else:
    # Calculate Total Magnetic Field Strength
    # Total_Field = |dbn_geo| + |dbe_geo| + |dbz_geo|
    data_time['Total_Field'] = (data_time[['dbn_geo', 'dbe_geo', 'dbz_geo']].abs().round().sum(axis=1))

    # Prepare DataFrame for Visualization
    viz_df = data_time[['GEOLON', 'GEOLAT', 'Total_Field']].copy()
    viz_df.rename(columns={'GEOLON': 'Longitude', 'GEOLAT': 'Latitude'}, inplace=True)

    # Remove any rows with missing or invalid data
    viz_df.dropna(subset=['Longitude', 'Latitude', 'Total_Field'], inplace=True)

    # Longitude Normalization: Normalize longitude to be between -180 and 180
    viz_df['Longitude'] = viz_df['Longitude'].apply(lambda x: round(x - 360 if x > 180 else x))

    # ---------------------------
    # Define Color Gradient with 60 Colors (Yellow to Red)
    # ---------------------------

    # Get the 'YlOrRd' colormap from Matplotlib
    cmap = plt.get_cmap('YlOrRd')

    # Generate 60 evenly spaced colors from the colormap
    steps = np.linspace(0, 1, 60)
    colors = [cmap(step) for step in steps]
    # Convert RGBA from 0-1 to 0-255 scale
    color_list = [
        [int(r * 255), int(g * 255), int(b * 255), int(a * 255)]
        for r, g, b, a in colors
    ]

    # Create a gradient dictionary for PyDeck
    gradient = {
        float(step): color
        for step, color in zip(steps, color_list)
    }

    # ---------------------------
    # Visualization with HeatmapLayer
    # ---------------------------

    # Define the PyDeck HeatmapLayer
    heatmap_layer = pdk.Layer(
        "HeatmapLayer",
        data=viz_df,
        get_position=['Longitude', 'Latitude'],
        get_weight='Total_Field',
        radius=15000,        # Halved radius from 20000 to 10000 meters
        intensity=intensity,  # Adjusted intensity slider
        threshold=0.10,      # Default threshold
        aggregation='sum',   # Default aggregation method
        gradient=gradient,    # Custom 60-step gradient
    )

    # ---------------------------
    # Visualization with ColumnLayer (3D Elevation)
    # ---------------------------

    # Define the PyDeck ColumnLayer
    column_layer = pdk.Layer(
        "ColumnLayer",
        data=viz_df,
        get_position=['Longitude', 'Latitude'],
        get_elevation='Total_Field',
        elevation_scale=1000,  # Adjust scaling factor as needed
        radius=20000,          # Radius of the column base in meters
        get_fill_color=[255, 0, 0, 180],  # Red color for columns
        pickable=True,
        extruded=True,
    )

    # Define the initial view state
    view_state = pdk.ViewState(
        latitude=0,
        longitude=0,
        zoom=1,
        pitch=60  # Tilt the map for better 3D effect
    )

    # Create the Deck.gl map with HeatmapLayer and ColumnLayer
    deck = pdk.Deck(
        layers=[heatmap_layer, column_layer],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/dark-v10',  # Dark map style
        tooltip={
            "html": "<b>Latitude:</b> {Latitude}<br/><b>Longitude:</b> {Longitude}<br/><b>Total Magnetic Field:</b> {Total_Field} nT",
            "style": {
                "backgroundColor": "steelblue",
                "color": "white"
            }
        }
    )

    # Display the map in Streamlit
    st.pydeck_chart(deck, height=650)

    # # ---------------------------
    # # Add Color Legend with Numerical Labels
    # # ---------------------------

    # st.markdown("### Legend: Total Magnetic Field Strength with Intensity 1.0 and Zoom 1.0 (nT)")

    #     # Create a color bar using matplotlib
    # fig, ax = plt.subplots(figsize=(8, 1))  # Increased size for better visibility
    # # fig.patch.set_alpha(0)  # Make the figure background transparent
    # # ax.patch.set_alpha(0)   # Make the axis background transparent

    # # Create a ScalarMappable for the legend with the 'YlOrRd' colormap, setting range from 0 to 500 nT
    # norm = mpl.colors.Normalize(vmin=0, vmax=500)
    # sm = mpl.cm.ScalarMappable(cmap='YlOrRd', norm=norm)
    # sm.set_array([])

    # # Add color bar with the updated range from 0 to 500 nT
    # cb1 = plt.colorbar(sm, cax=ax, orientation='horizontal', aspect=25)
    # cb1.set_label('Total Magnetic Field Strength (nT)', fontsize=10, color='white')  # Set label color to white

    # # Set the ticks to display numbers from 0 to 500 nT with intermediate steps
    # cb1.set_ticks([0, 100, 200, 300, 400, 500])
    # cb1.ax.set_xticklabels(['0', '100', '200', '300', '400', '500'], fontsize=10, color='black')  # Set tick label color to white

    # # Adjust tick label size and color for better readability
    # cb1.ax.tick_params(labelsize=10, colors='black')  # Set tick params color to white

    # # Remove axis lines for better aesthetics
    # ax.axis('off')

    # st.pyplot(fig)