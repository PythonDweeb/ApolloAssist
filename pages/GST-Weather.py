import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
import plotly.graph_objects as go

st.set_page_config(
    layout="wide",
    page_title="Geomagnetic Weather Dashboard",
    page_icon="🌐",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <link
        rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
        integrity="sha512-pap3O9Dzz3d9A4nmd1zN6Ddg1pFS+XNzDqY7q5VV2+e8Btj9cEepV7Y6aM6xwG7n2vXkNv6+07KQFIBaGk/9Fg=="
        crossorigin="anonymous"
        referrerpolicy="no-referrer"
    />
    <style>
    .reportview-container {
        background-color: #1e1e1e;
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: #2c2c2c;
        color: white;
    }
    .css-1d391kg h1 {
        color: #4da6ff;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .metric-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 10px 0;
    }
    .metric-icon {
        font-size: 30px;
        margin-right: 10px;
        color: #4da6ff;
    }
    .metric-text {
        font-size: 20px;
        color: #ffffff;
        font-weight: bold;
    }
    .dataframe th {
        background-color: #2c2c2c;
        color: white;
    }
    .dataframe tbody tr td {
        background-color: #1e1e1e;
        color: white;
    }
    .separator {
        border-top: 1px solid #4da6ff;
        margin: 40px 0;
    }
    div[data-testid="stPlotlyChart"] > div {
        background: transparent !important;
        border: none !important;
    }
    div[data-testid="stPlotlyChart"] > div > div {
        padding: 0 !important;
        margin: 0 !important;
    }    
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <h1 class="custom-title">🌐 Geomagnetic Weather Dashboard</h1>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("📅 Select Date Range and Location")

default_start = (datetime.now(timezone.utc) - timedelta(days=30)).date()
default_end = datetime.now(timezone.utc).date()

start_date = st.sidebar.date_input("Start Date", default_start)
end_date = st.sidebar.date_input("End Date", default_end)

if start_date > end_date:
    st.sidebar.error("⚠️ Error: Start date must be before end date.")

if st.sidebar.button("🚀 Fetch Data"):
    api_key = "CyfJM1wo3R0Fr8JZrN4zgIs1V6b9kzd7cwN6d8cm"

    with st.spinner("📡 Fetching data from NASA DONKI API..."):
        gst_url = f"https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/GST?startDate={start_date.strftime('%Y-%m-%d')}&endDate={end_date.strftime('%Y-%m-%d')}&api_key={api_key}"
        flr_url = f"https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/FLR?startDate={start_date.strftime('%Y-%m-%d')}&endDate={end_date.strftime('%Y-%m-%d')}&api_key={api_key}"
        cme_url = f"https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/CME?startDate={start_date.strftime('%Y-%m-%d')}&endDate={end_date.strftime('%Y-%m-%d')}&api_key={api_key}"

        def fetch_data(url, data_type):
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                if not data:
                    st.warning(f"⚠️ No {data_type} events found for the selected date range.")
                return data
            except requests.exceptions.HTTPError as http_err:
                st.error(f"❌ HTTP error occurred while fetching {data_type} data: {http_err}")
            except Exception as err:
                st.error(f"❌ An error occurred while fetching {data_type} data: {err}")
            return None

        gst_data = fetch_data(gst_url, "GST")
        flr_data = fetch_data(flr_url, "Solar Flare (FLR)")
        cme_data = fetch_data(cme_url, "CME")

    num_storms = max_kp = latest_kp = total_duration = num_flares = num_cmes = 0

    if gst_data:
        events = []
        for event in gst_data:
            gst_id = event.get("gstID")
            start_time = event.get("startTime")
            kp_indices = event.get("allKpIndex", [])

            for kp in kp_indices:
                observed_time = kp.get("observedTime")
                kp_index = kp.get("kpIndex")
                source = kp.get("source")

                events.append({
                    "GST ID": gst_id,
                    "Start Time": start_time,
                    "Observed Time": observed_time,
                    "Kp Index": kp_index,
                    "Source": source
                })

        gst_df = pd.DataFrame(events)
        if not gst_df.empty:
            gst_df['Start Time'] = pd.to_datetime(gst_df['Start Time'], errors='coerce')
            gst_df['Observed Time'] = pd.to_datetime(gst_df['Observed Time'], errors='coerce')
            gst_df['Start Time'] = gst_df['Start Time'].dt.tz_convert(None).dt.tz_localize(None)
            gst_df['Observed Time'] = gst_df['Observed Time'].dt.tz_convert(None).dt.tz_localize(None)
            gst_df['Kp Index'] = pd.to_numeric(gst_df['Kp Index'], errors='coerce')
            num_storms = gst_df['GST ID'].nunique()
            max_kp = gst_df['Kp Index'].max()
            latest_kp = gst_df['Kp Index'].iloc[-1] if not gst_df.empty else 0
            gst_df['Storm Duration (hrs)'] = (gst_df['Observed Time'] - gst_df['Start Time']).dt.total_seconds() / 3600
            total_duration = gst_df['Storm Duration (hrs)'].sum()
        else:
            st.warning("⚠️ No GST events found.")
    else:
        st.warning("⚠️ GST data is unavailable.")

    if flr_data:
        num_flares = len(flr_data)
    else:
        st.warning("⚠️ FLR data is unavailable.")

    if cme_data:
        num_cmes = len(cme_data)
    else:
        st.warning("⚠️ CME data is unavailable.")

    metrics = {
        "Number of Storms": {
            "icon": "fa-bolt",
            "value": num_storms,
            "min_val": 0,
            "max_val": max(10, num_storms + 5),
            "color_low": "#ADD8E6",
            "color_mid": "#6495ED",
            "color_high": "#1E90FF"
        },
        "Maximum Kp Index": {
            "icon": "fa-chart-line",
            "value": max_kp,
            "min_val": 0,
            "max_val": 10,
            "color_low": "#ADD8E6",
            "color_mid": "#6495ED",
            "color_high": "#1E90FF"
        },
        "Total Storm Duration (hrs)": {
            "icon": "fa-clock",
            "value": round(total_duration, 2),
            "min_val": 0,
            "max_val": max(50, round(total_duration, 2) + 10),
            "color_low": "#ADD8E6",
            "color_mid": "#6495ED",
            "color_high": "#1E90FF"
        },
        "Current Kp Index": {
            "icon": "fa-sun",
            "value": latest_kp,
            "min_val": 0,
            "max_val": 10,
            "color_low": "#ADD8E6",
            "color_mid": "#6495ED",
            "color_high": "#1E90FF"
        },
        "Number of Solar Flares": {
            "icon": "fa-fire",
            "value": num_flares,
            "min_val": 0,
            "max_val": max(10, num_flares + 5),
            "color_low": "#ADD8E6",
            "color_mid": "#6495ED",
            "color_high": "#1E90FF"
        },
        "Number of CMEs": {
            "icon": "fa-cloud",
            "value": num_cmes,
            "min_val": 0,
            "max_val": max(10, num_cmes + 5),
            "color_low": "#ADD8E6",
            "color_mid": "#6495ED",
            "color_high": "#1E90FF"
        }
    }

    def create_gauge(value, min_val, max_val, color_low, color_mid, color_high):
        bar_color = "#000000"
        q1 = min_val + 0.25 * (max_val - min_val)
        q3 = min_val + 0.75 * (max_val - min_val)
        steps = []
        num_steps = 800
        step_range = max_val - min_val
        for i in range(num_steps):
            step_min = min_val + (step_range / num_steps) * i
            step_max = min_val + (step_range / num_steps) * (i + 1)
            ratio = i / num_steps
            r = int(int(color_low[1:3], 16) + (int(color_high[1:3], 16) - int(color_low[1:3], 16)) * ratio)
            g = int(int(color_low[3:5], 16) + (int(color_high[3:5], 16) - int(color_low[3:5], 16)) * ratio)
            b = int(int(color_low[5:7], 16) + (int(color_high[5:7], 16) - int(color_low[5:7], 16)) * ratio)
            color = f"rgb({r}, {g}, {b})"
            steps.append({'range': [step_min, step_max], 'color': color})

        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = value,
            gauge = {
                'axis': {
                    'range': [min_val, max_val],
                    'tickvals': [q1, q3],
                    'ticktext': [f"{q1}", f"{q3}"],
                    'tickwidth': 1,
                    'tickcolor': "white",
                    'tickfont': {'size': 14},
                    'nticks': 2
                },
                'bar': {'color': bar_color, 'thickness': 0.2},
                'steps': steps,
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': value
                }
            },
            number = {'font': {'size': 24, 'color': 'white'}},
        ))
        fig.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            height=120,
            paper_bgcolor="rgba(0,0,0,0)",
            font = {'color': "white", 'family': "Arial"}
        )
        return fig

    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
    st.subheader("🌟 Key Metrics")

    top_metrics = list(metrics.items())[:3]
    bottom_metrics = list(metrics.items())[3:]

    cols_top = st.columns(3)
    for idx, (metric, params) in enumerate(top_metrics):
        with cols_top[idx]:
            st.markdown(
                f"<div class='metric-container'>"
                f"<i class='fas {params['icon']} metric-icon'></i>"
                f"<span class='metric-text'>{metric}</span>"
                f"</div>",
                unsafe_allow_html=True
            )
            fig = create_gauge(
                value=params["value"],
                min_val=params["min_val"],
                max_val=params["max_val"],
                color_low=params["color_low"],
                color_mid=params["color_mid"],
                color_high=params["color_high"]
            )
            st.plotly_chart(fig, use_container_width=True, key=f"gauge_{metric.replace(' ', '_')}")

    cols_bottom = st.columns(3)
    for idx, (metric, params) in enumerate(bottom_metrics):
        with cols_bottom[idx]:
            st.markdown(
                f"<div class='metric-container'>"
                f"<i class='fas {params['icon']} metric-icon'></i>"
                f"<span class='metric-text'>{metric}</span>"
                f"</div>",
                unsafe_allow_html=True
            )
            st.plotly_chart(
                create_gauge(
                    value=params["value"],
                    min_val=params["min_val"],
                    max_val=params["max_val"],
                    color_low=params["color_low"],
                    color_mid=params["color_mid"],
                    color_high=params["color_high"]
                ),
                use_container_width=True,
                key=f"gauge_{metric.replace(' ', '_')}"
            )

    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)

    if gst_data and not gst_df.empty:
        table_col, graph_col = st.columns(2)

        with table_col:
            st.subheader("📊 Geomagnetic Storm Events")
            st.write(f"**Number of Events:** {num_storms}")
            st.dataframe(
                gst_df[['GST ID', 'Start Time', 'Observed Time', 'Kp Index', 'Source']].style.set_table_styles(
                    [{
                        'selector': 'th',
                        'props': [('background-color', '#2c2c2c'), ('color', 'white')]
                    },
                    {
                        'selector': 'tbody',
                        'props': [('background-color', '#1e1e1e'), ('color', 'white')]
                    }]
                )
            )

        with graph_col:
            st.subheader("📈 Kp Indices Time Series")

            kp_df = gst_df[['Observed Time', 'Kp Index']].copy()
            kp_df = kp_df.dropna()
            kp_df = kp_df.sort_values('Observed Time')

            if not kp_df.empty:
                kp_df['Time Diff'] = kp_df['Observed Time'].diff()
                mode_diff = kp_df['Time Diff'].mode()[0] if not kp_df['Time Diff'].mode().empty else timedelta(hours=1)
            else:
                mode_diff = timedelta(hours=1)

            complete_time_range = pd.date_range(start=start_date, end=end_date, freq=mode_diff)

            kp_df.set_index('Observed Time', inplace=True)

            kp_df = kp_df.reindex(complete_time_range, fill_value=0)

            kp_df = kp_df.reset_index().rename(columns={'index': 'Observed Time'})

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=kp_df['Observed Time'],
                y=kp_df['Kp Index'],
                mode='lines+markers',
                name='Kp Index',
                line=dict(color='#4da6ff'),
                marker=dict(color='#80b3ff', size=6)
            ))

            fig.update_layout(
                height=500,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                xaxis=dict(
                    title='Observed Time (UTC)',
                    tickangle=-45,
                    showgrid=False,
                    zeroline=False,
                    type='date'
                ),
                yaxis=dict(
                    title='Kp Index',
                    tickmode='linear',
                    tick0=0,
                    dtick=1,
                    showgrid=True,
                    gridcolor='lightgray',
                    zeroline=False,
                    range=[0, kp_df['Kp Index'].max() + 1]
                ),
                hovermode='x unified',
                legend=dict(x=0, y=1),
                margin=dict(l=50, r=50, t=50, b=100),
            )

            st.plotly_chart(fig, use_container_width=True, key="kp_indices_time_series")
            st.session_state['gst_data'] = gst_df if gst_data and not gst_df.empty else None
            st.session_state['metrics'] = metrics

    else:
        st.warning("⚠️ GST data is unavailable or no events found.")
