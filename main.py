import streamlit as st
import subprocess
import pandas as pd
import os
import plotly.express as px
from PIL import Image, ImageDraw

# Custom CSS for theme styling
st.markdown(
    """
    <style>
    /* Background and text colors */
    body {
        background-color: white; /* Background */
        color: black; /* Default Text */
    }

    /* Sidebar customization */
    .css-1d391kg {
        background-color: #1F4D36;  /* New Dark Green */
        color: white;  /* Sidebar Text */
    }

    .sidebar .sidebar-content {
        color: white;
    }

    /* Headers and Subheaders */
    h1, h2, h3, h4, h5, h6 {
        color: #1F4D36; /* New Dark Green */
        font-weight: bold; /* Make the text bold */
    }

    /* Streamlit widget labels */
    .stTextInput label,
    .stSelectbox label,
    .stMetric label {
        color: black; /* Widget Labels in Black */
    }

    /* Metric value styling */
    .stMetric-value {
        color: #1F4D36; /* New Dark Green */
    }

    /* Button styling */
    .stButton button {
        background-color: #1F4D36;  /* New Dark Green */
        color: white;
        border: none;
    }

    /* Input and select fields */
    .stTextInput input, .stSelectbox select {
        background-color: white;
        color: black;
    }

    /* Data table styling */
    .dataframe {
        color: black; /* Black Text in Tables */
    }
    </style>
    """, unsafe_allow_html=True)

# Constants
CSV_FILENAME = "questions.csv"

# Sample Data for Students
students_data = pd.DataFrame({
    "Student ID": [1, 2, 3, 4],
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Average Score": [85, 76, 90, 65],
    "Exams Taken": [5, 4, 6, 3]
})

# Load Questions from CSV
@st.cache_data
def load_questions():
    if not os.path.exists(CSV_FILENAME):
        return pd.DataFrame(columns=["ID", "Text", "Options", "CorrectAnswer", "Concept", "Difficulty"])
    return pd.read_csv(CSV_FILENAME)

# Save Questions to CSV
def save_questions(df):
    df.to_csv(CSV_FILENAME, index=False)

# Login Page
def login_page():
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

    if "show_register_form" not in st.session_state:
        st.session_state.show_register_form = False  # Initially, show login form

    st.markdown('<div class="header">🐼 Welcome to PandaProctor 🐼</div>', unsafe_allow_html=True)

    if not st.session_state.show_register_form:
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

        if st.button("Login"):
            if username and password:
                try:
                    result = subprocess.run(
                        ['./login', 'login', user_type, username, password],
                        capture_output=True, text=True, check=True
                    )
                    st.success(result.stdout)
                    st.session_state.logged_in = True
                except subprocess.CalledProcessError as e:
                    st.error(f"Error: {e.stderr}")
            else:
                st.error("Please enter both username and password.")

        st.markdown("### Don't have an account?")
        if st.button("Register Now"):
            st.session_state.show_register_form = True  # Switch to registration form
    else:
        st.markdown('<div class="subheader">Create a new account</div>', unsafe_allow_html=True)

        register_user_type = st.radio(
            "Register as:", 
            ("Student", "Admin"), 
            horizontal=True
        )

        register_username = st.text_input("New Username", placeholder="Enter your username")
        register_password = st.text_input("New Password", placeholder="Enter your password", type="password")

        if st.button("Register"):
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

# Admin Dashboard Page
def admin_dashboard_page():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        login_page()
        return

    st.sidebar.title("Panda Proctor Admin Dashboard")

    image_path = "C:\\Users\\mamoo\\Downloads\\PandaProctor\\assets\\images\\panda1.jpg"
    if os.path.exists(image_path):
        image = Image.open(image_path)

        image = image.resize((120, 120), Image.Resampling.LANCZOS)
        mask = Image.new('L', (120, 120), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 120, 120), fill=255)
        image.putalpha(mask)

        st.sidebar.image(image, use_container_width=False)

    menu = st.sidebar.radio("Navigation", ["Dashboard", "Performance", "Manage Questions", "Settings", "Logout"])

    if menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.show_register_form = False  # Reset registration form state
        st.sidebar.empty()  # Remove the sidebar
        st.rerun()  # Refresh the page to reflect the changes

    # Initialize session state for questions
    if "questions_data" not in st.session_state:
        st.session_state.questions_data = load_questions()

    if menu == "Dashboard":
        st.title("Admin Dashboard")
        col1, col2 = st.columns(2)
        col1.metric("Total Students", len(students_data))
        col2.metric("Total Questions", len(st.session_state.questions_data))

        st.subheader("Student Performance Overview")
        fig = px.bar(
            students_data, x="Name", y="Average Score", color="Exams Taken",
            title="Performance Overview",
            color_discrete_map={5: '#1F4D36', 4: 'black', 6: '#1F4D36', 3: 'black'}
        )
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "Performance":
        st.title("Student Performance")
        selected_student = st.selectbox("Select Student", students_data["Name"])
        student_details = students_data[students_data["Name"] == selected_student].iloc[0]
        st.write(f"### Performance of {selected_student}")
        st.write(f"- **Average Score:** {student_details['Average Score']}%")
        st.write(f"- **Exams Taken:** {student_details['Exams Taken']}")

    elif menu == "Manage Questions":
        st.title("Manage Questions")
        st.subheader("Existing Questions")
        if st.session_state.questions_data.empty:
            st.info("No questions available. Add some questions to get started!")
        else:
            st.write(st.session_state.questions_data)

        st.subheader("Add New Question")
        with st.form("add_question_form"):
            question_id = st.number_input("Question ID", min_value=1, step=1, value=len(st.session_state.questions_data) + 1)
            text = st.text_area("Question Text")
            options = st.text_area("Options (separate with '|')")
            correct_answer = st.text_input("Correct Answer")
            concept = st.text_input("Concept")
            difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
            if st.form_submit_button("Add Question"):
                new_row = {
                    "ID": question_id,
                    "Text": text,
                    "Options": options,
                    "CorrectAnswer": correct_answer,
                    "Concept": concept,
                    "Difficulty": difficulty,
                }
                st.session_state.questions_data = pd.concat(
                    [st.session_state.questions_data, pd.DataFrame([new_row])], ignore_index=True
                )
                save_questions(st.session_state.questions_data)
                st.success("Question added successfully!")

    elif menu == "Settings":
        st.title("Settings")
        st.subheader("Update Dashboard Settings")
        st.text("This section can include configuration options for the system.")

    st.sidebar.markdown("---")
    st.sidebar.text("Panda Proctor © 2024")

if __name__ == "__main__":
    admin_dashboard_page()
