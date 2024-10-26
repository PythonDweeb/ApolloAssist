import streamlit as st

# Set custom page configuration
st.set_page_config(
    page_title="Apollo Assist",
    layout="centered",
    page_icon="apolloassist.webp",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'sidebar_visible' not in st.session_state:
    st.session_state['sidebar_visible'] = False

# Function to hide the sidebar
def hide_sidebar():
    hide_streamlit_style = """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
            button[kind="expandNav"] {
                display: none;
            }
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Hide the sidebar if not visible
if not st.session_state['sidebar_visible']:
    hide_sidebar()

# Set background image
background_style = """
    <style>
    .stApp {
        background-image: "homepage.webp";
        background-size: cover;
        background-position: center;
    }
    </style>
"""
st.markdown(background_style, unsafe_allow_html=True)

# Set the page title
st.title("NASA Geomagnetic Storm Data Explorer")

# Centered input section
st.markdown("""
    <div style="text-align: center; margin-top: 100px;">
        <h2>Enter the Geomagnetic Data Query</h2>
    </div>
""", unsafe_allow_html=True)

user_input = st.text_input("", key="user_input", label_visibility="collapsed")

if st.button("Enter"):
    if user_input:
        st.write(f"You entered: {user_input}")
    else:
        st.warning("Please enter a value to proceed.")

# Button to show the sidebar
if st.button("Explore Data"):
    st.session_state['sidebar_visible'] = True
    st.rerun()
