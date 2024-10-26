# Apollo Assist 🚀
A comprehensive **Geomagnetic Weather Dashboard** for monitoring space weather events that affect Earth. Apollo Assist allows users to explore geomagnetic storms, solar flares, and coronal mass ejections, focusing on their impact on various professions and infrastructure worldwide.

![Apollo Assist Logo]([https://path-to-your-logo.png](https://i.ibb.co/5cP5Pq4/apolloassist.webp))

## 📜 Project Overview
Similar to Apple's weather app, Apollo Assist aims to provide an interactive visualization of geomagnetic disturbances and their impact across multiple domains. By utilizing real-time data from NASA's DONKI API, users can monitor and analyze key space weather metrics, track events over time, view a 3D models, and access a fast inference RAG model to perform further analysis.

## 💡 Key Features
- **Real-Time Space Weather Data**: Fetches Geomagnetic Storm (GST), Solar Flare (FLR), and Coronal Mass Ejection (CME) data from NASA’s DONKI API.
- **3D Geomagnetic Disturbance Visualization**: View an interactive heatmap of geomagnetic disturbances overlaid on a global map.
- **Impact Analysis**: Details the effect of space weather on various professions, from pilots and astronauts to satellite operators and power grid workers.
- **Dynamic Dashboard with Key Metrics**: Includes gauge charts and time series to track storm durations, Kp indices, and solar flare/cme counts.
- **Fast Inference RAG Based Voice Assistant Model**: Access a highly specialized RAG model to assist in mitigating radiation effects and general queries.

## ⚙️ Tech Stack
- **Frontend**: Streamlit, HTML, CSS, Javascript
- **Backend**: Python (Pandas, Requests, Numpy)
- **AI/ML**: Cerebras, Weaviate, Cartesia, Deegram
- **Visualization**: Plotly, Pydeck, Matplotlib, Godot
- **Data Source**: NASA DONKI API, Openstreetmaps API, Supermag API

## 🚀 Getting Started
### Prerequisites
- **Python 3.7+**
- **Streamlit** and additional libraries:
  ```bash
  pip install streamlit pandas plotly pydeck requests numpy
