import streamlit as st

st.set_page_config(
    page_title="DLA Speaking Practice",
    page_icon="🎤",
    layout="wide"
)

st.sidebar.success("Select a page above")

st.markdown("""
<h1 style='text-align:center; color:#FF4B4B;'>
🎤 AI Speaking Exam Simulator
</h1>

<p style='text-align:center; font-size:18px;'>
Practice • Speak • Get Scored • Improve
</p>

<p style='text-align:center; font-size:18px;'>
Bu uygulama ile XML dosyasındaki sorular üzerinden İngilizce konuşma pratiği yapabilirsin.
</p>
""", unsafe_allow_html=True)

st.markdown("""
### Sayfalar

- **Test Center** → Soruları cevapla, konuşmanı yazıya döktür, AI ile puanlat
""")

st.info("Sorular online olarak düzenlenmez. Soruları localde `questions.xml` dosyasından güncelleyip GitHub’a yükleyebilirsin.")