import json
import streamlit as st
from openai import OpenAI
from prompts import EVALUATION_PROMPT

def get_openai_client():
    api_key = st.secrets["OPENAI_API_KEY"]
    return OpenAI(api_key=api_key)

def transcribe_audio(audio_file):
    """
    Streamlit st.audio_input çıktısını OpenAI transcription API'ye gönderir.
    Geriye metin döner.
    """
    if audio is not None:
        st.audio(audio)

    client = get_openai_client()

    # Streamlit UploadedFile benzeri obje döndürüyor
    audio_bytes = audio_file.read()

    # OpenAI istemcisi dosya benzeri obje ister
    import io
    temp_audio = io.BytesIO(audio_bytes)
    temp_audio.name = "speech.wav"

    transcript = client.audio.transcriptions.create(
    model="gpt-4o-mini-transcribe",
    file=temp_audio,
    language="en"
    )

    # SDK sürümüne göre transcript.text döner
    return transcript.text.strip()

def evaluate_answer(question, category, answer):
    if not answer.strip():
        return {
            "total_score": 0,
            "grammar_score": 0,
            "fluency_score": 0,
            "relevance_score": 0,
            "vocabulary_score": 0,
            "feedback": "No answer detected.",
            "improved_answer": ""
        }

    client = get_openai_client()

    prompt = EVALUATION_PROMPT.format(
        question=question,
        category=category,
        answer=answer
    )

    response = client.responses.create(
        model="gpt-5",
        input=[
            {
                "role": "system",
                "content": "You are a strict but fair English speaking exam evaluator. Always return valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    raw_text = response.output_text.strip()

    try:
        data = json.loads(raw_text)
    except Exception:
        data = {
            "total_score": 0,
            "grammar_score": 0,
            "fluency_score": 0,
            "relevance_score": 0,
            "vocabulary_score": 0,
            "feedback": raw_text,
            "improved_answer": ""
        }

    return data