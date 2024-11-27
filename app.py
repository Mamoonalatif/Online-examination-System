import streamlit as st
import subprocess

# Set page configuration (only once at the start)
st.set_page_config(page_title="Login Page", page_icon="🐼", layout="centered")

st.markdown(
    """
    <style>
    body {
        background-color: #FFFFF; 
        color: #FFFFF; 
        text-align: center;  
    }
    .stButton button {
        background-color: #1F4D36; 
        color: white;
        border-radius: 5px;
        border: 2px solid #1F4D36;
        font-size: 16px;
        font-weight: bold;
        padding: 10px;
        display: inline-block;
        margin: 10px 0; 
    }
    .stButton button:hover {
        background-color: #FFFFFF;
        color: #1F4D36;
        border: 2px solid #1F4D36;
    }
    .header, .subheader {
        font-size: 36px;
        font-weight: bold;
        color: #1F4D36;
        padding: 10px;
        text-align: center; 
        margin-top: 20px;
    }
    .subheader {
        font-size: 20px;
        font-weight: bold;
        color: #333;
        padding: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Check session state for toggling between login and register
if "show_register_form" not in st.session_state:
    st.session_state.show_register_form = False  # Initially, show login form

# Header
st.markdown('<div class="header">🐼 Welcome to PandaProctor🐼</div>', unsafe_allow_html=True)

# Form toggle logic
if not st.session_state.show_register_form:
    # Login form
    st.markdown('<div class="subheader">Please choose your login type</div>', unsafe_allow_html=True)

    user_type = st.radio(
        "I want to log in as:", 
        ("Student", "Admin"), 
        horizontal=True, 
        label_visibility="collapsed"
    )

    st.markdown(f"### Login as {user_type}")
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", placeholder="Enter your password", type="password")

    # Handle login functionality
    if st.button("Login"):
        if username and password:
            try:
                result = subprocess.run(
                    ['./main', 'login', user_type, username, password],
                    capture_output=True, text=True, check=True
                )
                st.success(result.stdout)
            except subprocess.CalledProcessError as e:
                st.error(f"Error: {e.stderr}")
        else:
            st.error("Please enter both username and password.")

    # Show Register Now button
    st.markdown("### Don't have an account?")
    if st.button("Register Now"):
        st.session_state.show_register_form = True  # Switch to registration form

else:
    # Registration form
    st.markdown('<div class="subheader">Create a new account</div>', unsafe_allow_html=True)

    register_user_type = st.radio(
        "Register as:", 
        ("Student", "Admin"), 
        horizontal=True
    )

    register_username = st.text_input("Username", placeholder="Enter your username")
    register_password = st.text_input("Password", placeholder="Enter your password", type="password")

    # Handle registration functionality
    if st.button("Register"):
        if register_username and register_password:
            try:
                result = subprocess.run(
                    ['./main', 'register', register_user_type, register_username, register_password],
                    capture_output=True, text=True, check=True
                )
                st.success(result.stdout)
                st.session_state.show_register_form = False  # Switch back to login form after successful registration
            except subprocess.CalledProcessError as e:
                st.error(f"Error: {e.stderr}")
        else:
            st.error("Please enter both username and password.")
    
    # Go back to login form
    if st.button("Back to Login"):
        st.session_state.show_register_form = False
