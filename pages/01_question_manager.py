import streamlit as st
import pandas as pd

import io
from db import add_questions_bulk

from db import add_question, get_all_questions, delete_question, update_question
from models import CATEGORIES, DIFFICULTY_LEVELS
from utils import save_uploaded_image

st.title("🛠️ Question Manager")

tab1, tab2, tab3, tab3 , tab4 = st.tabs(["Soru Ekle", "Soruları Yönet", "oru Ekle (cvs)", "Soru Ekle (txt)"])

with tab1:
    st.subheader("Yeni soru ekle")

    category = st.selectbox("Category", CATEGORIES, key="add_category")
    subcategory = st.text_input("Subcategory", key="add_subcategory")
    question_text = st.text_area("Question Text", key="add_question_text")
    difficulty = st.selectbox("Difficulty", DIFFICULTY_LEVELS, key="add_difficulty")
    active = st.checkbox("Active", value=True, key="add_active")

    image_file = None
    if category == "Picture Description":
        image_file = st.file_uploader(
            "Upload Image",
            type=["png", "jpg", "jpeg"],
            key="add_image_file"
        )

    if st.button("Add Question", key="add_question_btn"):
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

        selected_id = st.number_input(
            "Edit/Delete Question ID",
            min_value=1,
            step=1,
            key="edit_selected_id"
        )

        selected_row = None
        for row in rows:
            if row[0] == selected_id:
                selected_row = row
                break

        if selected_row:
            st.markdown("### Edit Question")

            new_category = st.selectbox(
                "Category",
                CATEGORIES,
                index=CATEGORIES.index(selected_row[1]),
                key=f"edit_category_{selected_id}"
            )

            new_subcategory = st.text_input(
                "Subcategory",
                value=selected_row[2] or "",
                key=f"edit_subcategory_{selected_id}"
            )

            new_question_text = st.text_area(
                "Question Text",
                value=selected_row[3] or "",
                key=f"edit_question_text_{selected_id}"
            )

            new_image_path = st.text_input(
                "Image Path",
                value=selected_row[4] or "",
                key=f"edit_image_path_{selected_id}"
            )

            difficulty_index = (
                DIFFICULTY_LEVELS.index(selected_row[5])
                if selected_row[5] in DIFFICULTY_LEVELS else 0
            )

            new_difficulty = st.selectbox(
                "Difficulty",
                DIFFICULTY_LEVELS,
                index=difficulty_index,
                key=f"edit_difficulty_{selected_id}"
            )

            new_active = st.checkbox(
                "Active",
                value=bool(selected_row[6]),
                key=f"edit_active_{selected_id}"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Update Question", key=f"update_btn_{selected_id}"):
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
                if st.button("Delete Question", key=f"delete_btn_{selected_id}"):
                    delete_question(selected_id)
                    st.warning("Question deleted.")
    else:
        st.info("No questions found.")

with tab3:
    st.subheader("Toplu Soru Yükleme (CSV)")

    uploaded_csv = st.file_uploader(
        "CSV dosyası yükle",
        type=["csv"],
        key="bulk_csv_upload"
    )

    st.caption("Beklenen sütunlar: category, subcategory, question_text, image_path, difficulty, active")

    if uploaded_csv is not None:
        df = pd.read_csv(uploaded_csv)
        st.dataframe(df, use_container_width=True)

        if st.button("CSV'deki Soruları Ekle", key="bulk_insert_csv"):
            required_cols = ["category", "subcategory", "question_text", "image_path", "difficulty", "active"]
            missing_cols = [col for col in required_cols if col not in df.columns]

            if missing_cols:
                st.error(f"Eksik sütunlar var: {', '.join(missing_cols)}")
            else:
                records = []
                for _, row in df.iterrows():
                    records.append((
                        str(row["category"]) if pd.notna(row["category"]) else "",
                        str(row["subcategory"]) if pd.notna(row["subcategory"]) else "",
                        str(row["question_text"]) if pd.notna(row["question_text"]) else "",
                        str(row["image_path"]) if pd.notna(row["image_path"]) else None,
                        str(row["difficulty"]) if pd.notna(row["difficulty"]) else "Easy",
                        int(row["active"]) if pd.notna(row["active"]) else 1
                    ))

                add_questions_bulk(records)
                st.success(f"{len(records)} soru başarıyla eklendi.")

with tab4:
    st.subheader("Hızlı Toplu Soru Ekleme")

    bulk_category = st.selectbox("Category", CATEGORIES, key="bulk_category")
    bulk_subcategory = st.text_input("Subcategory", key="bulk_subcategory")
    bulk_difficulty = st.selectbox("Difficulty", DIFFICULTY_LEVELS, key="bulk_difficulty")
    bulk_active = st.checkbox("Active", value=True, key="bulk_active")

    bulk_questions = st.text_area(
        "Her satıra bir soru yaz",
        height=250,
        key="bulk_questions_text"
    )

    if st.button("Soruları Toplu Ekle", key="bulk_add_text"):
        lines = [line.strip() for line in bulk_questions.splitlines() if line.strip()]

        if not lines:
            st.warning("Eklemek için en az bir soru gir.")
        else:
            records = [
                (bulk_category, bulk_subcategory, line, None, bulk_difficulty, int(bulk_active))
                for line in lines
            ]
            add_questions_bulk(records)
            st.success(f"{len(records)} soru eklendi.")