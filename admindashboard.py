from PIL import Image, ImageDraw
import streamlit as st
import pandas as pd
import os
import plotly.express as px

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

def admin_dashboard_page():
    # Sidebar Navigation
    st.sidebar.title("Panda Proctor Admin Dashboard")

    # Load the image using PIL
    image_path = "C:\\Users\\mamoo\\Downloads\\PandaProctor\\assets\\images\\panda1.jpg"
    if os.path.exists(image_path):
        image = Image.open(image_path)

        # Resize and apply circular mask
        image = image.resize((120, 120), Image.Resampling.LANCZOS)
        mask = Image.new('L', (120, 120), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 120, 120), fill=255)
        image.putalpha(mask)

        # Display the image in the sidebar
        st.sidebar.image(image, use_container_width=False)

    menu = st.sidebar.radio("Navigation", ["Dashboard", "Performance", "Manage Questions", "Settings"])

    # Initialize session state for questions
    if "questions_data" not in st.session_state:
        st.session_state.questions_data = load_questions()

    # Dashboard Page
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

    # Performance Page
    elif menu == "Performance":
        st.title("Student Performance")
        selected_student = st.selectbox("Select Student", students_data["Name"])
        student_details = students_data[students_data["Name"] == selected_student].iloc[0]
        st.write(f"### Performance of {selected_student}")
        st.write(f"- **Average Score:** {student_details['Average Score']}%")
        st.write(f"- **Exams Taken:** {student_details['Exams Taken']}")

    # Manage Questions Page
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

        st.subheader("Modify or Delete Questions")
        if st.session_state.questions_data.empty:
            st.info("No questions available to modify or delete.")
        else:
            selected_id = st.selectbox("Select Question ID", st.session_state.questions_data["ID"])
            question_row = st.session_state.questions_data[st.session_state.questions_data["ID"] == selected_id].iloc[0]
            with st.form("modify_delete_form"):
                updated_text = st.text_area("Question Text", value=question_row["Text"])
                updated_options = st.text_area("Options (separate with '|')", value=question_row["Options"])
                updated_correct_answer = st.text_input("Correct Answer", value=question_row["CorrectAnswer"])
                updated_concept = st.text_input("Concept", value=question_row["Concept"])
                updated_difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"],
                                                  index=["Easy", "Medium", "Hard"].index(question_row["Difficulty"]))

                modify = st.form_submit_button("Modify Question")
                delete = st.form_submit_button("Delete Question")

                if modify:
                    st.session_state.questions_data.loc[
                        st.session_state.questions_data["ID"] == selected_id,
                        ["Text", "Options", "CorrectAnswer", "Concept", "Difficulty"],
                    ] = [updated_text, updated_options, updated_correct_answer, updated_concept, updated_difficulty]
                    save_questions(st.session_state.questions_data)
                    st.success("Question modified successfully!")

                if delete:
                    st.session_state.questions_data = st.session_state.questions_data[
                        st.session_state.questions_data["ID"] != selected_id
                    ]
                    save_questions(st.session_state.questions_data)
                    st.success("Question deleted successfully!")

    # Settings Page
    elif menu == "Settings":
        st.title("Settings")
        st.subheader("Update Dashboard Settings")
        st.text("This section can include configuration options for the system.")

    st.sidebar.markdown("---")
    st.sidebar.text("Panda Proctor © 2024")
