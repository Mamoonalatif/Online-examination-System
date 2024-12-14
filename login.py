import streamlit as st
import subprocess

# Set page configuration
st.set_page_config(
    page_title="PandaProctor Login",
    page_icon="🐼",
    layout="centered"
)

st.markdown(
    """
    <style>
        [data-testid="stAppViewContainer"] {
            background-image: url("https://t4.ftcdn.net/jpg/07/79/02/19/360_F_779021987_LFIvUS11mfSUnoo9kk8YDBGra4a14hPw.jpg");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        .stButton button {
            background-color: #1F4D36; 
            color: white;
            border-radius: 5px;
            border: 2px solid #1F4D36;
            font-size: 16px;
            font-weight: bold;
            padding: 10px 20px;
            margin: 10px auto;
            display: block;
        }
        .stButton button:hover {
            background-color: #FFFFFF;
            color: #1F4D36;
            border: 2px solid #1F4D36;
        }
        .header {
            font-size: 36px;
            font-weight: bold;
            color: #1F4D36;
            text-align: center; 
            margin: 20px 0;
        }
        .subheader {
            font-size: 20px;
            font-weight: bold;
            color: #333;
            text-align: center;
            margin: 10px 0;
        }
        .stRadio label, .stTextInput label {
            color: black !important; /* Set the text color for labels */
        }
        .stRadio div {
            display: flex;
            justify-content: center;
        }
        
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to handle login and registration pages
def login_page():
    if "show_register_form" not in st.session_state:
        st.session_state.show_register_form = False  # Initially, show login form

    # Header
    st.markdown('<div class="header">🐼 Welcome to PandaProctor 🐼</div>', unsafe_allow_html=True)

    if not st.session_state.show_register_form:
        # Login form
        st.markdown('<div class="subheader">Please choose your login type</div>', unsafe_allow_html=True)
        user_type = st.radio("I want to log in as:", ("Student", "Admin"), horizontal=True)

        st.text_input("Username", placeholder="Enter your username", key="login_username")
        st.text_input("Password", placeholder="Enter your password", type="password", key="login_password")

        if st.button("Login"):
            username = st.session_state.login_username
            password = st.session_state.login_password
            if username and password:
                try:
                    result = subprocess.run(
                        ['./login', 'login', user_type, username, password],
                        capture_output=True, text=True, check=True
                    )
                    st.success(result.stdout)
                except subprocess.CalledProcessError as e:
                    st.error(f"Error: {e.stderr}")
            else:
                st.error("Please enter both username and password.")

        if st.button("Register Now"):
            st.session_state.show_register_form = True  # Switch to registration form
    else:
        # Registration form
        st.markdown('<div class="subheader">Create a new account</div>', unsafe_allow_html=True)
        register_user_type = st.radio("Register as:", ("Student", "Admin"), horizontal=True)

        st.text_input("New Username", placeholder="Enter your username", key="register_username")
        st.text_input("New Password", placeholder="Enter your password", type="password", key="register_password")

        if st.button("Register"):
            register_username = st.session_state.register_username
            register_password = st.session_state.register_password
            if register_username and register_password:
                try:
                    result = subprocess.run(
                        ['./login', 'register', register_user_type, register_username, register_password],
                        capture_output=True, text=True, check=True
                    )
                    st.success("Registration successful! You can now log in.")
                    st.session_state.show_register_form = False  # Switch back to login form
                except subprocess.CalledProcessError as e:
                    st.error(f"Error: {e.stderr}")
            else:
                st.error("Please enter both username and password.")

        if st.button("Back to Login"):
            st.session_state.show_register_form = False  # Switch back to login form

# Run the login page function
login_page()
