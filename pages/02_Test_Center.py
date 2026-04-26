import streamlit as st
from PIL import Image

from db_xml import get_active_questions
from models import CATEGORIES
from ai import transcribe_audio, evaluate_answer

st.title("🎯 Test Center")

col1, col2 = st.columns([2, 1])

with col1:
    category = st.selectbox("Category", ["All"] + CATEGORIES, key="test_category")

with col2:
    subcategory = st.text_input("Subcategory", placeholder="e.g. prefer", key="test_subcategory")

if st.button("Load Questions", key="load_questions_btn"):

    # Eski test verilerini temizle
    st.session_state.pop("questions", None)
    st.session_state.pop("current_index", None)

    selected_category = None if category == "All" else category
    questions = get_active_questions(
        category=selected_category,
        subcategory=subcategory or None
    )

    if questions:
        st.session_state["questions"] = questions
        st.session_state["current_index"] = 0
        st.rerun()
    else:
        st.warning("No active questions found.")

questions = st.session_state.get("questions", [])
current_index = st.session_state.get("current_index", 0)

if questions and current_index < len(questions):
    q = questions[current_index]

    question_id = q.get("id", "")
    q_category = q.get("category", "")
    q_subcategory = q.get("subcategory", "")
    question_text = q.get("question_text", "")
    image_path = q.get("image_path", "")

    st.markdown(
        f"""
        <p style='text-align:center; font-size:18px;'>
        Id: {question_id} |
        Category: {q_category} |
        Subcategory: {q_subcategory}
        </p>
        """,
        unsafe_allow_html=True
    )

    if q_category == "Picture Description" and image_path:
        try:
            img = Image.open(image_path)
            st.image(img, caption="Picture Description", width=450)
        except Exception:
            st.error("Image could not be loaded.")

    if question_text:
        st.markdown(
            f"""
            <p style='text-align:left; font-size:22px;'>
            {question_text}
            </p>
            """,
            unsafe_allow_html=True
        )

    audio = st.audio_input(
        "Record your answer",
        key=f"audio_{question_id}_{current_index}"
    )


    if st.button("Next Question", key=f"next_question_btn_{question_id}_{current_index}"):
        st.session_state["current_index"] += 1
        st.rerun()
        
    if st.button("Evaluate Answer", key=f"evaluate_answer_btn_{question_id}_{current_index}"):

        if audio is None:
            st.warning("Please record your answer first.")
        else:
            with st.spinner("Transcribing audio..."):
                transcript = transcribe_audio(audio)

            if not transcript:
                st.warning("No speech detected. Please record your answer again.")
            else:
                st.markdown("### Transcript")
                st.write(transcript)

                with st.spinner("Evaluating answer..."):
                    result = evaluate_answer(
                        question=question_text,
                        category=q_category,
                        answer=transcript
                    )

                st.markdown("### Evaluation")
                st.write(f"**Total Score:** {result['total_score']}/100")
                st.write(f"**Grammar:** {result['grammar_score']}/25")
                st.write(f"**Fluency:** {result['fluency_score']}/25")
                st.write(f"**Relevance:** {result['relevance_score']}/25")
                st.write(f"**Vocabulary:** {result['vocabulary_score']}/25")

                st.markdown("### Feedback")
                st.write(result["feedback"])

                st.markdown("### Improved Answer")
                st.write(result["improved_answer"])


elif questions and current_index >= len(questions):
    st.success("Test completed.")
else:
    st.info("Load questions to start the test.")