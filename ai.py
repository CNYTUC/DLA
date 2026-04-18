import json
from prompts import EVALUATION_PROMPT

def transcribe_audio(audio_file):
    """
    Buraya speech-to-text entegrasyonu gelecek.
    Şimdilik örnek dönüş yapıyoruz.
    """
    if audio_file is None:
        return ""

    return "This is a sample transcription. Replace this with real speech-to-text output."

def evaluate_answer(question, category, answer):
    """
    Buraya LLM değerlendirme entegrasyonu gelecek.
    Şimdilik sahte veri döndürüyoruz.
    """
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

    prompt = EVALUATION_PROMPT.format(
        question=question,
        category=category,
        answer=answer
    )

    # Burada daha sonra OpenAI API çağrısı yapılacak.
    # Şimdilik örnek bir sonuç:
    return {
        "total_score": 78,
        "grammar_score": 20,
        "fluency_score": 18,
        "relevance_score": 21,
        "vocabulary_score": 19,
        "feedback": "Your answer is relevant and understandable. However, some grammar and fluency issues reduce clarity.",
        "improved_answer": "In my opinion, this topic is very important because it affects daily life. I would try to answer clearly and calmly. Also, I think being organized and confident can make a big difference in such situations."
    }