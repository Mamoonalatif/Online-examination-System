import streamlit as st
import pandas as pd
import subprocess
import time
import requests
import os
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

# ----------------- PAGE CONFIGURATION ----------------
st.set_page_config(page_title="PandaProctor", page_icon="🐼", layout="centered")

# ----------------- GLOBAL VARIABLES -----------------
CSV_FILENAME = "questions.csv"
STUDENT_SCORES_FILENAME = "student_scores.csv"
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

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None


# ----------------- SAVE QUESTIONS FUNCTION -----------------
def save_questions():
    st.session_state.questions_df.to_csv(CSV_FILENAME, index=False)



# ----------------- LOGIN AND REGISTRATION PAGE -----------------
def login_page():
   
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
    st.markdown('<div class="header">🐼 Welcome to PandaProctor 🐼</div>', unsafe_allow_html=True)
    if "show_register_form" not in st.session_state:
        st.session_state.show_register_form = False

    if not st.session_state.show_register_form:
        st.markdown('<div class="subheader">Please choose your login type</div>', unsafe_allow_html=True)
        user_type = st.radio("I want to Log in as:", ["Student", "Admin"], horizontal=True)
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", placeholder="Enter password", type="password")

        if st.button("Login"):
            if username and password:
                st.success(f"Welcome {user_type}, {username}!")
                st.session_state.logged_in = True
                st.session_state.user_type = user_type
            else:
                st.error("Please enter all login details.")

        if st.button("Register"):
            st.session_state.show_register_form = True

    else:
        st.subheader("Register")
        register_user_type = st.radio("Register as:", ["Student", "Admin"], horizontal=True)
        new_username = st.text_input("New Username", placeholder="Choose a username")
        new_password = st.text_input("New Password", placeholder="Choose a password", type="password")

        if st.button("Submit Registration"):
            if new_username and new_password:
                st.success(f"Account created! You can now log in as {register_user_type}.")
                st.session_state.show_register_form = False
            else:
                st.error("Please enter all details.")

        if st.button("Back to Login"):
            st.session_state.show_register_form = False

# ----------------- ADMIN DASHBOARD -----------------
def admin_dashboard():

    st.markdown(
    """
    <style>

[data-testid="stAppViewContainer"] {
            background-image: url("https://wallpapers.com/images/high/light-lamp-minimalist-laptop-art-199o53vj2e6qmo6d.webp");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        
        }
           [data-testid="stSidebar"] {
        background-color: #1F4D36;
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
         </style>
    """,
    unsafe_allow_html=True,
)


    # Sidebar
    st.sidebar.title("Panda Proctor Admin Dashboard")
    image_path = "C:\\Users\\mamoo\\Downloads\\PandaProctor\\panda1.jpg"
    if os.path.exists(image_path):
     image = Image.open(image_path)
     image = image.resize((160, 160), Image.Resampling.LANCZOS)
     mask = Image.new('L', (160, 160), 0)
     draw = ImageDraw.Draw(mask)
     draw.ellipse((0, 0, 160, 160), fill=250)
     image.putalpha(mask)
     st.sidebar.image(image, use_container_width=False)
    
    menu = st.sidebar.radio("Navigation", ["Dashboard", "Manage Questions", "Settings", "Log Out"])
    if menu == "Dashboard":
       st.title("Student Progress")
       st.subheader("View Student Scores")
    
    
       if os.path.exists(STUDENT_SCORES_FILENAME):
         student_scores_df = pd.read_csv(STUDENT_SCORES_FILENAME)
        
        # Plotting the graph
         fig, ax = plt.subplots(figsize=(10, 6))
         ax.bar(student_scores_df["Student Name"], student_scores_df["Score"], color='skyblue')
         ax.set_xlabel('Student Name')
         ax.set_ylabel('Score')
         ax.set_title('Student Progress')
         plt.xticks(rotation=45, ha='right')

         st.pyplot(fig)  

    
    elif menu == "Manage Questions":
        st.title("Manage Questions")
        action = st.sidebar.radio("Choose Action", ["Display Questions", "Add Question", "Modify Question", "Delete Question"])

        questions_df = st.session_state.questions_df

        if action == "Display Questions":
            st.subheader("Existing Questions")
            if not questions_df.empty:
                st.dataframe(questions_df)
            else:
                st.write("No questions available.")

        elif action == "Add Question":
            st.subheader("Add New Question")
            with st.form("add_question_form"):
                question_id = st.number_input("Question ID", min_value=1, step=1)
                text = st.text_area("Question Text")
                options = st.text_area("Options (separate with '|')")
                correct_answer = st.text_input("Correct Answer")
                concept = st.text_input("Concept")
                difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
                subject = st.selectbox("Subject", course_data)
                submit = st.form_submit_button("Add Question")

                if submit:
                    if question_id in questions_df["ID"].values:
                        st.error("A question with this ID already exists.")
                    else:
                        new_data = {"ID": question_id, "Text": text, "Options": options, "CorrectAnswer": correct_answer, "Concept": concept, "Difficulty": difficulty, "Subject": subject}
                        st.session_state.questions_df = st.session_state.questions_df.append(new_data, ignore_index=True)
                        save_questions()
                        st.success("Question added successfully!")

        elif action == "Modify Question":
         st.subheader("Modify an Existing Question")
         if not questions_df.empty:
            selected_id = st.selectbox("Select Question ID", questions_df["ID"].tolist())
            selected_question = questions_df[questions_df["ID"] == selected_id].iloc[0]

            with st.form("modify_question_form"):
                updated_text = st.text_area("Question Text", value=selected_question["Text"])
                updated_options = st.text_area("Options (separate with '|')", value=selected_question["Options"])
                updated_correct_answer = st.text_input("Correct Answer", value=selected_question["CorrectAnswer"])
                updated_concept = st.text_input("Concept", value=selected_question["Concept"])
                updated_difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], index=["Easy", "Medium", "Hard"].index(selected_question["Difficulty"]))

                selected_course = selected_question["Course"]
                if selected_course not in course_data:
                    selected_course = course_data[0]  
                updated_course = st.selectbox("Course", course_data, index=course_data.index(selected_course))

                modify = st.form_submit_button("Modify Question")

                if modify:
                    st.session_state.questions_df.loc[st.session_state.questions_df["ID"] == selected_id, ["Text", "Options", "CorrectAnswer", "Concept", "Difficulty", "Course"]] = [
                        updated_text, updated_options, updated_correct_answer, updated_concept, updated_difficulty, updated_course
                    ]
                    save_questions()
                    st.success("Question modified successfully!")
         else:
            st.write("No questions available to modify.")

        elif action == "Delete Question":
            st.subheader("Delete a Question")
            if not questions_df.empty:
                question_id = st.selectbox("Select Question ID to delete", questions_df["ID"].unique())
                if st.button("Delete"):
                    st.session_state.questions_df = questions_df[questions_df["ID"] != question_id]
                    save_questions()
                    st.success("Question deleted successfully!")
            else:
                st.error("No questions available to delete.")

    elif menu == "Settings":
        st.title("Settings")
        st.write("Update your settings here!")

    elif menu == "Log Out":
        st.session_state.logged_in = False
        st.success("Logged out successfully! Returning to login page...")

# ----------------- STUDENT DASHBOARD -----------------
def is_face_detected():
    try:
        response = requests.get("http://127.0.0.1:5000/detect-face")
        if response.status_code == 200:
            return response.json().get("face_detected", False)
    except Exception as e:
        st.error("Error connecting to face detection API.")
        return False

@st.cache_resource
def load_and_process_image(image_path):
    image = Image.open(image_path).resize((160, 160), Image.Resampling.LANCZOS)
    mask = Image.new('L', (160, 160), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 160, 160), fill=250)
    image.putalpha(mask)
    return image


def student_dashboard():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        [data-testid="stSidebar"] {
            background-color: #1F4D36;
            color: white;
        }
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.title("Student Dashboard")
    image_path = "C:\\Users\\mamoo\\Downloads\\PandaProctor\\panda1.jpg"
    if os.path.exists(image_path):
        st.sidebar.image(load_and_process_image(image_path), use_container_width=False)

    menu = st.sidebar.radio("Navigation", ["Dashboard", "Take Quiz", "View Progress", "Log Out"])

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
                    question_data = subject_questions.to_dict(orient="records")
                    question_idx = st.session_state.current_question
                    if question_idx < total_questions:
                        q = question_data[question_idx]
                        st.subheader(f"Question {question_idx + 1}")
                        st.write(q["Text"])

                        options = q["Options"].split("|")
                        for i, option in enumerate(options):
                            st.write(f"{chr(65 + i)}. {option}")

                        selected_option = st.radio(
                            "Your Answer",
                            options=[chr(65 + i) for i in range(len(options))],
                            key=f"question_{question_idx}",
                        )

                        st.session_state.selected_answer = selected_option
                        if st.button("Next"):
                            if st.session_state.selected_answer:
                                if st.session_state.selected_answer == q["CorrectAnswer"]:
                                    st.session_state.student_score += 1 

                            st.session_state.current_question += 1  
                            st.session_state.selected_answer = None  

                            if st.session_state.current_question >= total_questions:
                                st.write(f"Your final score is {st.session_state.student_score}/{total_questions}")
                                st.session_state.quiz_started = False
                                st.session_state.current_question = 0  
                                st.session_state.selected_answer = None  
                            else:
                                st.rerun() 
                    else:
                        st.write(f"No questions available for {selected_subject}")

    elif menu == "View Progress":
        st.title("View Progress")
        st.write("Progress tracking coming soon!")
    elif menu == "Log Out":
        st.session_state.logged_in = False
        st.success("Logged out successfully! Returning to login page...")
    else:
        st.title("Welcome to the Student Dashboard")
        st.write("Select 'Take Quiz' to start or 'View Progress' to check your progress.")


# ----------------- MAIN FUNCTION -----------------
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_page()
    else:
        if st.session_state.user_type == "Admin":
            admin_dashboard()
        elif st.session_state.user_type == "Student":
            student_dashboard()

if __name__ == "__main__":
    main()
                                 