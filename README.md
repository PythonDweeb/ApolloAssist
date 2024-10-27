<img src="https://github.com/PythonDweeb/ApolloAssist/blob/main/images/apolloassist.png" alt="Apollo Assist Logo" width="300"/>

# Apollo Assist 🚀
A comprehensive **Geomagnetic Weather Dashboard** for monitoring space weather events that affect Earth. Apollo Assist allows users to explore geomagnetic storms, solar flares, and coronal mass ejections, focusing on their impact on various professions and infrastructure worldwide.

## 📜 Project Overview
Basically a weather app but for geomagnetic radiation, Apollo Assist aims to provide an interactive visualization of geomagnetic disturbances and their impact across multiple domains. By utilizing real-time data from NASA's DONKI API, users can monitor and analyze key space weather metrics, track events over time, view a 3D models, and access a fast inference RAG model to perform further analysis. Built for De Anza Hacks 3.0.

## 💡 Key Features
- **Real-Time Space Weather Data**: Fetches Geomagnetic Storm (GST), Solar Flare (FLR), and Coronal Mass Ejection (CME) data from NASA’s DONKI API.
- **3D Geomagnetic Disturbance Visualization**: View an interactive heatmap of geomagnetic disturbances overlaid on a global map.
- **Impact Analysis**: Details the effect of space weather on various professions, from pilots and astronauts to satellite operators and power grid workers.
- **Dynamic Dashboard with Key Metrics**: Includes gauge charts and time series to track storm durations, Kp indices, and solar flare/cme counts.
- **Fast Inference RAG Based Voice Assistant Model**: Access a highly specialized RAG model to assist in mitigating radiation effects and help answer queries.

## ⚙️ Tech Stack
- **Frontend**: Streamlit, HTML, CSS, Javascript
- **Backend**: Python (Pandas, Requests, Numpy)
- **AI/ML**: Cerebras, Weaviate
- **Visualization**: Plotly, Pydeck, Matplotlib
- **Data Source**: NASA DONKI API, Openstreetmaps API, Supermag API

## 🖼️ Snapshots

Home Page:

<img src="https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/003/097/656/datas/original.png" alt="Apollo Assist Logo" width="600"/>

Geomagnetic Radiation Weather Dashboard:

<img src="https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/003/097/653/datas/original.png" alt="Radiation Dashboard" width="600"/>

Geomagnetic Radiation Fast-Inference AI RAG Model:

<img src="https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/003/097/869/datas/original.png" alt="RAG AI" width="600"/>

Geomagnetic Disturbance 3D Heat Map and Graphs:

<img src="https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/003/097/654/datas/original.png" alt="Visuals" width="600"/>
<img src="https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/003/097/655/datas/original.png" alt="Visuals" width="600"/>

## 🚀 Getting Started
### Prerequisites
- **Python 3.7+**
- **Streamlit** and additional libraries:
  ```bash
  pip install -r requirements.txt
- **Run:**
  ```bash
  streamlit run Home.py
