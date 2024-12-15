import streamlit as st
import pandas as pd
import os
from PIL import Image, ImageDraw
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
subjects_data = ["DSA", "OOP", "PF"]

# Initialize session state for questions
if "questions_df" not in st.session_state:
    if os.path.exists(CSV_FILENAME):
        st.session_state.questions_df = pd.read_csv(CSV_FILENAME)
    else:
        st.session_state.questions_df = pd.DataFrame(columns=["ID", "Text", "Options", "CorrectAnswer", "Concept", "Difficulty", "Subject"])

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

menu = st.sidebar.radio("Navigation", ["Dashboard", "Manage Questions", "Settings"])

# Load the questions from session state
questions_df = st.session_state.questions_df

if menu == "Manage Questions":
    st.title("Manage Questions")

    # Sidebar options for Manage Questions
    manage_questions_option = st.sidebar.radio("Select an Action", ["Display Questions", "Add Question", "Modify Question", "Delete Question"])

    if manage_questions_option == "Display Questions":
        st.subheader("Existing Questions")
        if not questions_df.empty:
            st.dataframe(questions_df)
        else:
            st.write("No questions available.")

    elif manage_questions_option == "Add Question":
        st.subheader("Add New Question")
        with st.form("add_question_form"):
            question_id = st.number_input("Question ID", min_value=1, step=1)
            text = st.text_area("Question Text")
            options = st.text_area("Options (separate with '|')")
            correct_answer = st.text_input("Correct Answer")
            concept = st.text_input("Concept")
            difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
            subject = st.selectbox("Subject", subjects_data)
            submit_add = st.form_submit_button("Add Question")

            if submit_add:
                if not questions_df[questions_df["ID"] == question_id].empty:
                    st.error("A question with this ID already exists.")
                else:
                    new_question = {
                        "ID": question_id,
                        "Text": text,
                        "Options": options,
                        "CorrectAnswer": correct_answer,
                        "Concept": concept,
                        "Difficulty": difficulty,
                        "Subject": subject
                    }
                    st.session_state.questions_df = questions_df.append(new_question, ignore_index=True)
                    save_questions()
                    st.success("Question added successfully!")

    elif manage_questions_option == "Modify Question":
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

                selected_subject = selected_question["Subject"]
                if selected_subject not in subjects_data:
                    selected_subject = subjects_data[0]  # Default to first subject if not found
                updated_subject = st.selectbox("Subject", subjects_data, index=subjects_data.index(selected_subject))

                modify = st.form_submit_button("Modify Question")

                if modify:
                    st.session_state.questions_df.loc[st.session_state.questions_df["ID"] == selected_id, ["Text", "Options", "CorrectAnswer", "Concept", "Difficulty", "Subject"]] = [
                        updated_text, updated_options, updated_correct_answer, updated_concept, updated_difficulty, updated_subject
                    ]
                    save_questions()
                    st.success("Question modified successfully!")
        else:
            st.write("No questions available to modify.")

    elif manage_questions_option == "Delete Question":
        st.subheader("Delete an Existing Question")
        if not questions_df.empty:
            selected_id = st.selectbox("Select Question ID", questions_df["ID"].tolist())
            selected_question = questions_df[questions_df["ID"] == selected_id].iloc[0]

            delete = st.button("Delete Question")

            if delete:
                st.session_state.questions_df = st.session_state.questions_df[st.session_state.questions_df["ID"] != selected_id]
                save_questions()
                st.success("Question deleted successfully!")
        else:
            st.write("No questions available to delete.")

elif menu == "Settings":
    st.title("Settings")
    st.subheader("Update Dashboard Settings")
    st.text("This section can include configuration options for the system.")

st.sidebar.markdown("---")
st.sidebar.text("Panda Proctor © 2024")
