import streamlit as st
import pandas as pd
import plotly.express as px

# Sample Data
students_data = pd.DataFrame({
    "Student ID": [1, 2, 3, 4],
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Average Score": [85, 76, 90, 65],
    "Exams Taken": [5, 4, 6, 3]
})

subjects_data = ["Math", "Science", "History", "English"]
questions_data = pd.DataFrame({
    "Question ID": [1, 2, 3],
    "Subject": ["Math", "Science", "History"],
    "Concept": ["Algebra", "Physics Basics", "World War II"],
    "Question Text": ["What is 2 + 2?", "Define gravity.", "When did WWII end?"],
    "Answer": ["4", "Force that attracts bodies", "1945"]
})

# Streamlit Layout
st.set_page_config(page_title="Panda Proctor Admin Dashboard", layout="wide")

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

    /* Sidebar Image Roundness */
    .sidebar img {
        border-radius: 50%; /* Make the image circular */
        width: 150px; /* Adjust the size of the image */
        height: 150px; /* Ensure the image remains square for circular cropping */
        object-fit: cover; /* Maintain aspect ratio and avoid stretching */
        margin: 0 auto; /* Center the image horizontally */
        display: block; /* Center the image properly */
    }

    /* Headers and Subheaders */
    h1, h2, h3, h4, h5, h6 {
        color: #1F4D36; /* New Dark Green */
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

# Sidebar Navigation
st.sidebar.title("Panda Proctor")
st.sidebar.image("C:\\Users\\LENOVO\\Downloads\\panda proctor\\assets\\panda1.jpg", 
                 caption="Admin Dashboard", use_container_width=True)

st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigation", ["Dashboard", "Performance", "Manage Questions", "Settings"])

# Dashboard Page
if menu == "Dashboard":
    st.title("Admin Dashboard")
    col1, col2 = st.columns(2)
    col1.metric("Total Students", len(students_data))
    col2.metric("Total Questions", len(questions_data))

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
    st.write("### Existing Questions")
    st.write(questions_data)

    st.subheader("Add New Question")
    with st.form("add_question_form"):
        subject = st.selectbox("Subject", subjects_data)
        concept = st.text_input("Concept")
        question_text = st.text_area("Question Text")
        answer = st.text_input("Answer")
        if st.form_submit_button("Add Question"):
            new_question = {
                "Question ID": len(questions_data) + 1,
                "Subject": subject,
                "Concept": concept,
                "Question Text": question_text,
                "Answer": answer
            }
            questions_data = questions_data.append(new_question, ignore_index=True)
            st.success("Question added successfully!")

    st.subheader("Modify or Delete Questions")
    selected_question = st.selectbox("Select Question to Modify/Delete", questions_data["Question Text"])
    question_details = questions_data[questions_data["Question Text"] == selected_question].iloc[0]
    with st.form("modify_delete_form"):
        updated_subject = st.selectbox("Subject", subjects_data, index=subjects_data.index(question_details["Subject"]))
        updated_concept = st.text_input("Concept", value=question_details["Concept"])
        updated_question_text = st.text_area("Question Text", value=question_details["Question Text"])
        updated_answer = st.text_input("Answer", value=question_details["Answer"])
        modify = st.form_submit_button("Modify Question")
        delete = st.form_submit_button("Delete Question")

        if modify:
            questions_data.loc[questions_data["Question ID"] == question_details["Question ID"], 
                               ["Subject", "Concept", "Question Text", "Answer"]] = [updated_subject, updated_concept, updated_question_text, updated_answer]
            st.success("Question updated successfully!")
        if delete:
            questions_data = questions_data[questions_data["Question ID"] != question_details["Question ID"]]
            st.success("Question deleted successfully!")

# Settings Page
elif menu == "Settings":
    st.title("Settings")
    st.subheader("Update Dashboard Settings")
    st.text("This section can include configuration options for the system.")

st.sidebar.markdown("---")
st.sidebar.text("Panda Proctor © 2024")
