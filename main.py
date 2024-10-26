import streamlit as st

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

# Set the page title
st.title("Welcome to the NASA Geomagnetic Storm Data Explorer")

st.write("This is the main page. Use the navigation on the left to explore different pages.")

# Button to show the sidebar
if st.button("Explore Data"):
    st.session_state['sidebar_visible'] = True
    st.rerun()