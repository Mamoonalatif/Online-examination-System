import streamlit as st
import pandas as pd
import os
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
            background-image: url("https://wallpapers.com/images/featured/cute-laptop-background-wskgbnazlfkt4h30.jpg");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Constants
CSV_FILENAME = "questions.csv"
course_data = ["DSA", "OOP", "PF"]

# Initialize session state for questions and progress
if "questions_df" not in st.session_state:
    if os.path.exists(CSV_FILENAME):
        st.session_state.questions_df = pd.read_csv(CSV_FILENAME)
    else:
        st.session_state.questions_df = pd.DataFrame(columns=["ID", "Text", "Options", "CorrectAnswer", "Concept", "Difficulty", "Course"])

if "student_score" not in st.session_state:
    st.session_state.student_score = {}

# Save questions to CSV
def save_questions():
    st.session_state.questions_df.to_csv(CSV_FILENAME, index=False)

# Sidebar customization
st.markdown(
    """<style>
    [data-testid="stSidebar"] {
        background-color: #1F4D36;
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    </style>""",
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.title("Student Dashboard")
image_path = "C:\\Users\\mamoo\\Downloads\\PandaProctor\\panda1.jpg"
if os.path.exists(image_path):
    image = Image.open(image_path)
    image = image.resize((160, 160), Image.Resampling.LANCZOS)
    mask = Image.new('L', (160, 160), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 160, 160), fill=250)
    image.putalpha(mask)
    st.sidebar.image(image, use_container_width=False)

menu = st.sidebar.radio("Navigation", ["Dashboard", "Take Quiz", "View Progress"])

# Load the questions from session state
questions_df = st.session_state.questions_df

if menu == "Take Quiz":
    st.title("Take a Quiz")
    
    # Student name and course selection (initial page)
    if "quiz_started" not in st.session_state:
        student_name = st.text_input("Enter Your Name")
        selected_subject = st.selectbox("Select course", course_data)
        
        if student_name and selected_subject:
            # Store student name and selected course in session state
            st.session_state.student_name = student_name
            st.session_state.selected_subject = selected_subject
            st.session_state.quiz_started = True
            st.session_state.current_question = 0  # Start from the first question
            st.session_state.student_score[student_name] = 0  # Initialize score to 0
            # Move to the quiz section after submission
            st.experimental_rerun()  # This should be replaced with st.experimental_rerun() if needed
    else:
        # Proceed to quiz if already started
        student_name = st.session_state.student_name
        selected_subject = st.session_state.selected_subject
        
        # Filter questions based on the selected subject
        subject_questions = questions_df[questions_df["Course"] == selected_subject]

        if not subject_questions.empty:
            score = st.session_state.student_score[student_name]
            total_questions = len(subject_questions)
            question_data = subject_questions.to_dict(orient='records')

            # Show current score at the top
            st.subheader(f"Your Score: {score}/{total_questions}")

            # Show first question
            if "current_question" not in st.session_state:
                st.session_state.current_question = 0

            question_idx = st.session_state.current_question
            if question_idx < total_questions:
                q = question_data[question_idx]
                st.subheader(f"Question {question_idx + 1}")
                st.write(q["Text"])

                options = q["Options"].split('|')
                selected_option = st.radio("Your Answer", options=[chr(65 + i) for i in range(len(options))])
                
                # Store selected answer in session state
                if selected_option:
                    st.session_state.selected_option = selected_option
                
                # Handle user answer when "Next" button is clicked
                if st.button("Next"):
                    if st.session_state.selected_option == q["CorrectAnswer"]:
                        score += 1
                    st.session_state.student_score[student_name] = score

                    # Move to next question
                    st.session_state.current_question += 1
                    if st.session_state.current_question >= total_questions:
                        st.write(f"Your final score is {score}/{total_questions}")
                        st.session_state.quiz_started = False
                        st.session_state.current_question = 0
                    st.experimental_rerun()  # After button click, refresh page with updated state
        else:
            st.write(f"No questions available for {selected_subject}")

elif menu == "View Progress":
    st.title("Your Progress")

    if st.session_state.student_score:
        student_name = st.selectbox("Select Student", list(st.session_state.student_score.keys()))
        
        if student_name:
            score = st.session_state.student_score[student_name]
            st.write(f"Score for {student_name}: {score}")
            
            # Plotting progress
            scores = list(st.session_state.student_score.values())
            students = list(st.session_state.student_score.keys())
            fig, ax = plt.subplots()
            ax.bar(students, scores, color='green')
            ax.set_xlabel('Students')
            ax.set_ylabel('Scores')
            ax.set_title('Student Progress')
            st.pyplot(fig)
    else:
        st.write("No progress data available.")

else:
    st.title("Welcome to the Student Dashboard")
    st.write("Select 'Take Quiz' to start a quiz or 'View Progress' to check your progress.")
