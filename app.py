import streamlit as st
from db import init_db

st.set_page_config(
    page_title="English Speaking Test App",
    page_icon="🎤",
    layout="wide"
)

init_db()

st.sidebar.success("Select a page above")

st.markdown("""
<h1 style='text-align:center; color:#FF4B4B;'>
🎤 AI Speaking Exam Simulator
</h1>
<p style='text-align:center; font-size:18px;'>
Practice • Speak • Get Scored • Improve
</p>
<p style='text-align:center; font-size:18px;'>
Bu uygulama ile soru yönetebilir ve test pratiği yapabilirsin.</p>

""", unsafe_allow_html=True)


st.markdown("""
### Sayfalar
- **Question Manager** → Soru / resim ekle, düzenle, sil
- **Test Center** → Teste gir, konuşmanı yazıya döktür, AI ile puanlat
""")