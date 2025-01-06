import streamlit as st
import pandas as pd
import requests
import time
import os
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
SCORE_FILENAME = "student_scores.csv"

def is_face_detected():
    try:
        response = requests.get("http://127.0.0.1:5000/detect-face")
        if response.status_code == 200:
            return response.json().get("face_detected", False)
    except Exception as e:
        st.error("Error connecting to face detection API.")
        return False

CSV_FILENAME = "questions.csv"
course_data = ["DSA", "OOP", "PF"]

if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "student_score" not in st.session_state:
    st.session_state.student_score = 0
if "questions_df" not in st.session_state:
    if os.path.exists(CSV_FILENAME):
        st.session_state.questions_df = pd.read_csv(CSV_FILENAME)
    else:
        st.session_state.questions_df = pd.DataFrame(columns=["ID", "Text", "Options", "CorrectAnswer", "Concept", "Difficulty", "Course"])

if "student_score" not in st.session_state:
    st.session_state.student_score = {}

if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None

def save_questions():
    st.session_state.questions_df.to_csv(CSV_FILENAME, index=False)

def save_student_score():
    score_data = {
        "Student Name": [st.session_state.student_name],
        "Score": [st.session_state.student_score[st.session_state.student_name]]
    }
    score_df = pd.DataFrame(score_data)
    if os.path.exists(SCORE_FILENAME):
        score_df.to_csv(SCORE_FILENAME, mode='a', header=False, index=False)
    else:
        score_df.to_csv(SCORE_FILENAME, index=False)

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

questions_df = st.session_state.questions_df

if menu == "Take Quiz":
    st.title("Take a Quiz")

    if not st.session_state.quiz_started:
        student_name = st.text_input("Enter Your Name")
        selected_subject = st.selectbox("Select course", course_data)

        if student_name and selected_subject:
            st.session_state.quiz_started = True
            st.session_state.current_question = 0
            st.session_state.student_name = student_name
            st.session_state.selected_subject = selected_subject
            st.session_state.student_score = 0
    else:
        
        st.write("Keep your face visible in the frame to continue the quiz.")
        st.warning("If no face is detected, the quiz will stop.")

        student_name = st.session_state.student_name
        selected_subject = st.session_state.selected_subject
        
        face_detected = is_face_detected()
        if not face_detected:
            st.error("Cheating detected! The quiz has been stopped.")
            st.session_state.quiz_started = False
        else:
            subject_questions = questions_df[questions_df["Course"] == selected_subject]
            if not subject_questions.empty:
              total_questions = len(subject_questions)
              question_data = subject_questions.to_dict(orient='records')
            question_idx = st.session_state.current_question
            if question_idx < total_questions:
               q = question_data[question_idx]
               st.subheader(f"Question {question_idx + 1}")
               st.write(q["Text"])

               options = q["Options"].split('|')
               for i, option in enumerate(options):
                st.write(f"{chr(65 + i)}. {option}")

               selected_option = st.radio("Your Answer", options=[chr(65 + i) for i in range(len(options))], key=f"question_{question_idx}")

               st.session_state.selected_answer = selected_option
               if st.button("Next"):
                if st.session_state.selected_answer:
                    if st.session_state.selected_answer == q["CorrectAnswer"]:
                        st.session_state.student_score[student_name] += 1  

                st.session_state.current_question += 1  
                st.session_state.selected_answer = None  

                if st.session_state.current_question >= total_questions:
                    st.write(f"Your final score is {st.session_state.student_score[student_name]}/{total_questions}")
                    save_student_score()
                    st.session_state.quiz_started = False
                    st.session_state.current_question = 0  
                    st.session_state.selected_answer = None  
                else:
                    st.rerun()  
            else:
             st.write(f"No questions available for {selected_subject}")

elif menu == "View Progress":
    st.title("View Progress")
    if os.path.exists(SCORE_FILENAME):
        scores_df = pd.read_csv(SCORE_FILENAME)
        student_name = st.selectbox("Select Student", scores_df["Student Name"].tolist())

        if student_name:
            student_score = scores_df[scores_df["Student Name"] == student_name]["Score"].iloc[0]
            
            fig, ax = plt.subplots()
            ax.bar(scores_df["Student Name"], scores_df["Score"], color='green')
            ax.set_xlabel('Students')
            ax.set_ylabel('Scores')
            ax.set_title('Student Progress')
            st.pyplot(fig)
    else:
        st.write("No progress data available.")
    st.write("Progress tracking coming soon!")
else:
    st.title("Welcome to the Student Dashboard")
    st.write("Select 'Take Quiz' to start or 'View Progress' to check your progress.")