import streamlit as st
from PIL import Image

from db import get_active_questions, save_test_result
from models import CATEGORIES
from ai import transcribe_audio, evaluate_answer

st.title("🎯 Test Center")

category = st.selectbox("Choose Category", ["All"] + CATEGORIES)
subcategory = st.text_input("Optional Subcategory Filter")

if st.button("Load Questions"):
    selected_category = None if category == "All" else category
    questions = get_active_questions(category=selected_category, subcategory=subcategory or None)

    if questions:
        st.session_state["questions"] = questions
        st.session_state["current_index"] = 0
    else:
        st.warning("No active questions found.")

questions = st.session_state.get("questions", [])
current_index = st.session_state.get("current_index", 0)

if questions and current_index < len(questions):
    q = questions[current_index]
    question_id, q_category, q_subcategory, question_text, image_path, difficulty, active = q


    st.markdown("<p style='text-align:center; font-size:18px;'>"&
                
                "No:" & {current_index + 1} & 
                ", Category:" & {q_category + 1} & 
                ", Subcategory:" & {q_subcategory + 1} & 
                ", Difficulty:" & {difficulty + 1} & 
                
                "</p>", unsafe_allow_html=True)


    # st.markdown(f"### Question {current_index + 1}")
    # st.write(f"**Category:** {q_category}")
    # st.write(f"**Subcategory:** {q_subcategory}")
    # st.write(f"**Difficulty:** {difficulty}")

    if q_category == "Picture Description" and image_path:
        try:
            img = Image.open(image_path)
            st.image(img, caption="Picture Description", use_container_width=True)
        except Exception:
            st.error("Image could not be loaded.")

    if question_text:
        st.write(f"**Question:** {question_text}")

    audio = st.audio_input("Record your answer")

    manual_text = st.text_area("Or type your answer manually")

    if st.button("Evaluate Answer"):
        transcript = manual_text.strip()

        if not transcript and audio is not None:
            transcript = transcribe_audio(audio)

        st.markdown("### Transcript")
        st.write(transcript)

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

        save_test_result(
            question_id=question_id,
            transcript=transcript,
            total_score=result["total_score"],
            grammar_score=result["grammar_score"],
            fluency_score=result["fluency_score"],
            relevance_score=result["relevance_score"],
            vocabulary_score=result["vocabulary_score"],
            feedback=result["feedback"],
            improved_answer=result["improved_answer"]
        )

    if st.button("Next Question"):
        st.session_state["current_index"] += 1
        st.rerun()

elif questions and current_index >= len(questions):
    st.success("Test completed.")
else:
    st.info("Load questions to start the test.")