import os
import streamlit as st
import pandas as pd
import weaviate
from langchain_weaviate import WeaviateVectorStore
from langchain_cerebras import ChatCerebras
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from datetime import datetime
import pytz

# Set API keys directly as strings
CEREBRAS_API_KEY = "csk-e6pf3kwtrm8h2ejw8yhxjynpwtt3hxx3v392mjfwj6xvw298"
WEAVIATE_URL = "https://lrbzwveyrc63jrp8ndf3ma.c0.us-west3.gcp.weaviate.cloud"
WEAVIATE_API_KEY = "thFU4OaIzIAKYUdBSmmm24faJJhJRy2RI3jH"

# Initialize Cerebras LLM using `ChatCerebras`
cerebras_llm = ChatCerebras(api_key=CEREBRAS_API_KEY, model="llama3.1-8b")

# Helper function to get geolocation and time zone for cities
def get_geolocation_and_timezone(city):
    city_data = {
        "New York": {"geolocation": (40.7128, -74.0060), "timezone": "America/New_York"},
        "San Francisco": {"geolocation": (37.7749, -122.4194), "timezone": "America/Los_Angeles"},
        "Los Angeles": {"geolocation": (34.0522, -118.2437), "timezone": "America/Los_Angeles"}
    }
    return city_data.get(city, {"geolocation": (0, 0), "timezone": "UTC"})

# Function to find nearest KP value for a given geolocation
def get_nearest_kp_value(geolocation, csv_data):
    csv_data['distance'] = ((csv_data['GEOLAT'] - geolocation[0])**2 + (csv_data['GEOLON'] - geolocation[1])**2)**0.5
    nearest_row = csv_data.loc[csv_data['distance'].idxmin()]
    return nearest_row['IGRF_DECL']

# Upload vectors to Weaviate
def upload_vectors(csv_data, embeddings, client):
    vector_store = WeaviateVectorStore(client=client, index_name="geo_data", text_key="description", embedding=embeddings)
    limited_data = csv_data.head(176)
    for i, row in limited_data.iterrows():
        vector_store.add_texts([str(row)])
    
    return vector_store

def generate_rag_report(prompt, vector_store, llm):
    retriever = vector_store.as_retriever()
    from langchain.chains.question_answering import load_qa_chain
    qa_chain = load_qa_chain(llm, chain_type="stuff")

    # Sub-prompt to encourage finding connections and focusing on related information
    refined_prompt = (
        f"Using the provided prompt: '{prompt}', please find all relevant information from the data and generate a detailed report. Even if exact data isn't directly available, attempt to provide related insights, additional context, and any inferences that can be made. Ensure the report remains friendly, clear, and encouraging to the user. When applicable, consider how the information may impact various professions:"
            "- Pilots and Airline Crew: Geomagnetic radiation can disrupt navigation systems and communication channels, posing risks during flights."
            "- Satellite Operators: Increased geomagnetic activity can damage satellite electronics and disrupt their functionality."
           " - Power Grid Operators: Geomagnetic storms can induce currents that overload power grids, leading to outages."
           " - Astronauts: Exposure to high levels of radiation can pose serious health risks to astronauts in space."
           " - Telecommunications Engineers: Geomagnetic disturbances can interfere with signal transmission and reception."
           " - Navigation Systems Engineers: Radiation can cause inaccuracies in GPS and other navigation systems."
            "- Electric Utility Workers: Maintenance and operation of power lines can become hazardous during geomagnetic events."
           " - Radio Operators: Communication can be disrupted due to ionospheric disturbances caused by geomagnetic activity."
            "- Offshore Oil Rig Workers: Equipment malfunctions due to radiation can increase safety risks on oil rigs."
            "- Railroad Operators: Signal systems may fail, affecting train schedules and safety."
            "- CIA Operatives: Communication blackouts can hinder operations, disrupt critical missions, and impact intelligence gathering."
            "- Defense System Operators: Geomagnetic events can interfere with missile defense systems, leading to potential security vulnerabilities."
           " - Data Center Managers: Geomagnetic storms can lead to data corruption and massive financial losses due to hardware malfunctions."
            "- Healthcare Providers: Radiation impacts on critical medical equipment can threaten patient safety and disrupt healthcare services."
           " - Weather Forecasters: Geomagnetic interference can affect satellite data collection, impacting weather forecasting accuracy."
            "- Financial Sector Operators: Geomagnetic events can disrupt transaction systems and impact stock exchanges relying on stable communications."
    )

    # Retrieve relevant documents
    docs = retriever.get_relevant_documents(refined_prompt)

    # Generate a response using the chain
    result = qa_chain.run(input_documents=docs, question=refined_prompt)

    # Add a friendly and confident tone to the response
    if "no direct information" in result or "not available" in result:
        result = (
            "Based on the data I found, here are some valuable insights that might help: "
            + result.replace("no direct information", "related insights")
                     .replace("not available", "connected details")
        )
    
    return result


# Streamlit App Content
st.set_page_config(page_icon="🤖", layout="wide", page_title="Cerebras with Weaviate")
st.subheader("Geolocation-Based Report Generator & Chatbot Assistant", divider="orange", anchor=False)

# Initialize session state for vector store
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None

# Directly load the specific CSV file
csv_file_path = "20241026-06-57-supermag.csv"
if not os.path.exists(csv_file_path):
    st.error("CSV file not found. Please ensure the file '20241026-06-57-supermag.csv' is present in the app directory.")
else:
    gst_data = pd.read_csv(csv_file_path)

    # Left side: City-based analysis and warning system
    col1, col2 = st.columns(2)

    with col1:
        st.title("KP-Based Analysis & Warnings")
        
        # Sidebar: Get User Input for City
        with st.sidebar:
            st.title("Settings")
            selected_city = st.selectbox("City", ["New York", "San Francisco", "Los Angeles"])

        if selected_city and st.session_state.vector_store is not None:
            city_info = get_geolocation_and_timezone(selected_city)
            nearest_kp_value = get_nearest_kp_value(city_info['geolocation'], gst_data)
            
            city_timezone = pytz.timezone(city_info['timezone'])
            current_time = datetime.now(city_timezone).strftime("%Y-%m-%d %H:%M:%S")

            st.write(f"Nearest KP Value for {selected_city}: {nearest_kp_value}")

            prompt = f"Generate a detailed report based on KP value {nearest_kp_value} near the location {city_info['geolocation']}."
            report = generate_rag_report(prompt, st.session_state.vector_store, cerebras_llm)
            
            st.write("🌟 Generated Report")
            st.markdown(report)

    with col2:
        st.title("Interactive Chatbot (RAG Model)")
        
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=WEAVIATE_URL,
            auth_credentials=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY),
            skip_init_checks=True
        )

        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        if st.session_state.vector_store is None:
            with st.spinner("Generating embeddings..."):
                st.session_state.vector_store = upload_vectors(gst_data, embeddings, client)
            st.success("Embeddings generated and stored. You can now ask questions.")
        else:
            st.info("Embeddings already generated. You can ask questions.")

        user_input = st.text_input("Ask your question:", "")
        if st.button("Send") and user_input:
            response = generate_rag_report(user_input, st.session_state.vector_store, cerebras_llm)
            st.write("**Chatbot Response:**")
            st.markdown(response)
