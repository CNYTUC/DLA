import streamlit as st
import pandas as pd

from db import add_question, get_all_questions, delete_question, update_question
from models import CATEGORIES, DIFFICULTY_LEVELS
from utils import save_uploaded_image

st.title("🛠️ Question Manager")

tab1, tab2 = st.tabs(["Add Question", "Manage Questions"])

with tab1:
    st.subheader("Yeni soru ekle")

    category = st.selectbox("Category", CATEGORIES)
    subcategory = st.text_input("Subcategory")
    question_text = st.text_area("Question Text")
    difficulty = st.selectbox("Difficulty", DIFFICULTY_LEVELS)
    active = st.checkbox("Active", value=True)

    image_file = None
    if category == "Picture Description":
        image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if st.button("Add Question"):
        image_path = save_uploaded_image(image_file) if image_file else None
        add_question(
            category=category,
            subcategory=subcategory,
            question_text=question_text,
            image_path=image_path,
            difficulty=difficulty,
            active=active
        )
        st.success("Question added successfully.")

with tab2:
    st.subheader("Mevcut sorular")

    rows = get_all_questions()

    if rows:
        df = pd.DataFrame(rows, columns=[
            "ID", "Category", "Subcategory", "Question", "Image", "Difficulty", "Active", "Created At"
        ])
        st.dataframe(df, use_container_width=True)

        selected_id = st.number_input("Edit/Delete Question ID", min_value=1, step=1)

        selected_row = None
        for row in rows:
            if row[0] == selected_id:
                selected_row = row
                break

        if selected_row:
            st.markdown("### Edit Question")

            new_category = st.selectbox("Category", CATEGORIES, index=CATEGORIES.index(selected_row[1]))
            new_subcategory = st.text_input("Subcategory", value=selected_row[2] or "")
            new_question_text = st.text_area("Question Text", value=selected_row[3] or "")
            new_image_path = st.text_input("Image Path", value=selected_row[4] or "")
            new_difficulty = st.selectbox(
                "Difficulty",
                DIFFICULTY_LEVELS,
                index=DIFFICULTY_LEVELS.index(selected_row[5]) if selected_row[5] in DIFFICULTY_LEVELS else 0
            )
            new_active = st.checkbox("Active", value=bool(selected_row[6]))

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Update Question"):
                    update_question(
                        question_id=selected_id,
                        category=new_category,
                        subcategory=new_subcategory,
                        question_text=new_question_text,
                        image_path=new_image_path,
                        difficulty=new_difficulty,
                        active=new_active
                    )
                    st.success("Question updated.")

            with col2:
                if st.button("Delete Question"):
                    delete_question(selected_id)
                    st.warning("Question deleted.")
    else:
        st.info("No questions found.")