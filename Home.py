import streamlit as st

CEREBRAS_API_KEY = "csk-e6pf3kwtrm8h2ejw8yhxjynpwtt3hxx3v392mjfwj6xvw298"
WEAVIATE_URL = "https://lrbzwveyrc63jrp8ndf3ma.c0.us-west3.gcp.weaviate.cloud"
WEAVIATE_API_KEY = "thFU4OaIzIAKYUdBSmmm24faJJhJRy2RI3jH"

st.set_page_config(
    layout="wide", 
    page_title="Apollo Assist",
    page_icon="🚀"
)

background_image = "https://i.ibb.co/HhrFkjR/mainpage-upscaled.png"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&display=swap');

    [data-testid="stSidebar"] {{
        display: none;
    }}
    [data-testid="stSidebarNav"] {{
        display: none;
    }}
    button[kind="expandNav"] {{
        display: none;
    }}
    .stApp {{
        background-image: url("{background_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .title {{
        font-family: 'Luckiest Guy', cursive;
        font-size: 100px;
        color: white;
        -webkit-text-stroke: 4px black;
        text-align: left;
        margin-top: 250px;
        margin-left: 5px;
        text-shadow:
            -3px -3px 0 #000,
            3px -3px 0 #000,
            -3px 3px 0 #000,
            3px 3px 0 #000;
    }}
    .button-container {{
        display: flex;
        justify-content: flex-start;
        margin-top: 25px;
        margin-left: 50px;
    }}
    .button {{
        background-color: #ffffff;
        border: none;
        color: black;
        padding: 15px 30px;
        text-align: center;
        text-decoration: none;
        font-size: 20px;
        font-weight: bold;
        border-radius: 15px;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    .button:hover {{
        background-color: #cccccc;
        transform: scale(1.05);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='title'>Apollo Assist</h1>", unsafe_allow_html=True)

st.markdown("<div class='button-container'>", unsafe_allow_html=True)
st.markdown(
    """
    <a href="/GST-Weather" target="_self">
        <button class="button">Begin</button>
    </a>
    """,
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)
