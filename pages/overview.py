import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
import altair as alt

# Set the page title
st.title("NASA Geomagnetic Storm (GST) Data Explorer")

# Sidebar for user input
st.sidebar.header("Select Date Range")
default_start = (datetime.now(timezone.utc) - timedelta(days=30)).date()
default_end = datetime.now(timezone.utc).date()

start_date = st.sidebar.date_input("Start Date", default_start)
end_date = st.sidebar.date_input("End Date", default_end)

# Convert dates to strings in YYYY-MM-DD format
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

# Fetch Data Button
if st.sidebar.button("Fetch Data"):
    with st.spinner("Fetching data from NASA DONKI API..."):
        # API Endpoint
        url = f"https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/GST?startDate={start_date_str}&endDate={end_date_str}"
        
        # Make the API request
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            # Initialize events list
            events = []
            if data:
                # Process data
                for event in data:
                    gst_id = event.get("gstID")
                    start_time = event.get("startTime")
                    kp_indices = event.get("allKpIndex", [])
                    linked_events = event.get("linkedEvents", [])
                    
                    linked_event_ids = [le.get("activityID") for le in linked_events]
                    linked_event_ids_str = ", ".join(linked_event_ids) if linked_event_ids else "None"
                    
                    for kp in kp_indices:
                        observed_time = kp.get("observedTime")
                        kp_index = kp.get("kpIndex")
                        source = kp.get("source")
                        
                        events.append({
                            "GST ID": gst_id,
                            "Start Time": start_time,
                            "Observed Time": observed_time,
                            "Kp Index": kp_index,
                            "Source": source,
                            "Linked Events": linked_event_ids_str
                        })
            else:
                st.warning("No geomagnetic storm events found for the selected date range.")
            
            # Convert to DataFrame
            df = pd.DataFrame(events)
            if not df.empty:
                df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
                df['Observed Time'] = pd.to_datetime(df['Observed Time'], errors='coerce')

                # Remove timezone information from 'Observed Time'
                df['Observed Time'] = df['Observed Time'].dt.tz_localize(None)

                df['Kp Index'] = pd.to_numeric(df['Kp Index'], errors='coerce')

                # Display Data
                st.subheader("Geomagnetic Storm Events")
                st.write(f"Number of events: {len(df)}")
                st.dataframe(df)
            else:
                # Create an empty DataFrame with necessary columns
                df = pd.DataFrame(columns=['Observed Time', 'Kp Index'])
            
            # Generate date range
            date_range = pd.date_range(start=start_date, end=end_date, freq='3H')

            # Convert date_range to a DataFrame
            df_full = pd.DataFrame({'Observed Time': date_range})

            # Ensure 'Observed Time' in df_full is timezone-naive
            df_full['Observed Time'] = df_full['Observed Time'].dt.tz_localize(None)

            # Merge with the data to get Kp Index values
            df_plot = pd.merge(df_full, df[['Observed Time', 'Kp Index']], on='Observed Time', how='left')

            # Fill missing Kp Index values with zero (or you can choose another default value)
            df_plot['Kp Index'].fillna(0, inplace=True)

            # Sort the DataFrame
            df_plot = df_plot.sort_values('Observed Time')

            # Plot Kp Index over time using Altair with interactive hover dots
            st.subheader("Kp Index Time Series")

            # Define a selection that considers the nearest point along the x-axis
            nearest = alt.selection_point(nearest=True, on='mouseover', encodings=['x'], empty='none')

            # The base line chart
            line = alt.Chart(df_plot).mark_line().encode(
                x=alt.X('Observed Time:T', title='Observed Time', axis=alt.Axis(format='%Y-%m-%d %H:%M')),
                y=alt.Y('Kp Index:Q', title='Kp Index'),
                tooltip=[
                    alt.Tooltip('Observed Time:T', title='Observed Time', format='%Y-%m-%d %H:%M'),
                    alt.Tooltip('Kp Index:Q', title='Kp Index')
                ]
            )

            # Transparent selectors across the chart to capture mouseover events
            selectors = alt.Chart(df_plot).mark_rule(opacity=0).encode(
                x='Observed Time:T',
            ).add_params(
                nearest
            )

            # Points that appear on the line at the selected point
            points = line.mark_point(size=65, color='red').transform_filter(nearest)

            # Text labels near the points
            text = line.mark_text(align='left', dx=5, dy=-5).transform_filter(nearest).encode(
                text=alt.Text('Kp Index:Q', format='.2f')
            )

            # Vertical rule at the selected time
            rules = alt.Chart(df_plot).mark_rule(color='gray').encode(
                x='Observed Time:T',
            ).transform_filter(nearest)

            # Layer the chart components
            chart = alt.layer(
                line, selectors, points, rules, text
            ).interactive().properties(
                width='container',
                height=400
            )

            st.altair_chart(chart, use_container_width=True)
        else:
            st.error(f"Failed to fetch data. Status code: {response.status_code}")