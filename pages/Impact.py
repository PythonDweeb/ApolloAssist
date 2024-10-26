import streamlit as st
from datetime import datetime, timedelta, timezone

st.set_page_config(
    layout="wide",
    page_title="Impact",
    page_icon="🌎",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <h1 class="custom-title">🌎 Impact</h1>
    """,
    unsafe_allow_html=True
)

professions = {
    "Pilots and Airline Crew": "Geomagnetic radiation can disrupt navigation systems and communication channels, posing risks during flights.",
    "Satellite Operators": "Increased geomagnetic activity can damage satellite electronics and disrupt their functionality.",
    "Power Grid Operators": "Geomagnetic storms can induce currents that overload power grids, leading to outages.",
    "Astronauts": "Exposure to high levels of radiation can pose serious health risks to astronauts in space.",
    "Telecommunications Engineers": "Geomagnetic disturbances can interfere with signal transmission and reception.",
    "Navigation Systems Engineers": "Radiation can cause inaccuracies in GPS and other navigation systems.",
    "Electric Utility Workers": "Maintenance and operation of power lines can become hazardous during geomagnetic events.",
    "Radio Operators": "Communication can be disrupted due to ionospheric disturbances caused by geomagnetic activity.",
    "Offshore Oil Rig Workers": "Equipment malfunctions due to radiation can increase safety risks on oil rigs.",
    "Railroad Operators": "Signal systems may fail, affecting train schedules and safety.",
}

left_col, right_col = st.columns([1, 1])

# this is just to see it, remove it later but this is how u can access the data
if 'gst_data' in st.session_state:
    st.write("📊 Geomagnetic Storm Events Data:")
    st.dataframe(st.session_state['gst_data'])

with left_col:
    for profession, impact in professions.items():
        with st.expander(profession):
            st.write(impact)

# temp text but 
with right_col:
    st.write("🌟 Metrics Overview")
    for metric, params in st.session_state['metrics'].items():
        st.write(f"{metric}: {params['value']}")