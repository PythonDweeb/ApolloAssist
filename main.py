import streamlit as st

# Set the page configuration
st.set_page_config(layout="centered", page_title="Apollo Assist")

# Background image URL
background_image = "https://us-east.storage.cloudconvert.com/tasks/cb44b8c2-d965-4562-bf6b-f9d3630148ae/homepage.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241026%2Fva%2Fs3%2Faws4_request&X-Amz-Date=20241026T060023Z&X-Amz-Expires=86400&X-Amz-Signature=26563f8311392d66865395fbd46f1e915710c5e99a320bbd69852b47761df9d7&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22homepage.png%22&response-content-type=image%2Fpng&x-id=GetObject"

# Apply custom CSS for background image, text styling, and hide the sidebar
st.markdown(
    f"""
    <style>
    /* Hide the sidebar */
    [data-testid="stSidebar"] {{
        display: none;
    }}
    [data-testid="stSidebarNav"] {{
        display: none;
    }}
    button[kind="expandNav"] {{
        display: none;
    }}
    /* Background and text styles */
    .stApp {{
        background-image: url("{background_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .title {{
        font-size: 72px;
        font-weight: bold;
        color: white;
        -webkit-text-stroke: 2px black;
        text-align: center;
        margin-top: 100px;
    }}
    .button-container {{
        display: flex;
        justify-content: center;
        margin-top: 50px;
    }}
    .button {{
        background-color: #ffffff;
        border: none;
        color: black;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 24px;
        font-weight: bold;
        border-radius: 8px;
        cursor: pointer;
    }}
    .button:hover {{
        background-color: #e0e0e0;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Display the title
st.markdown("<h1 class='title'>Apollo Assist</h1>", unsafe_allow_html=True)

# Center the 'Explore Data' button as a hyperlink
st.markdown("<div class='button-container'>", unsafe_allow_html=True)
st.markdown(
    """
    <a href="/Overview" target="_self">
        <button class="button">Explore Data</button>
    </a>
    """,
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)
