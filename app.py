import streamlit as st
from db import init_db

st.set_page_config(
    page_title="English Speaking Test App",
    page_icon="🎤",
    layout="wide"
)

init_db()

st.title("🎤 English Speaking Test App")
st.write("Bu uygulama ile soru yönetebilir ve test pratiği yapabilirsin.")

st.markdown("""
### Sayfalar
- **Question Manager** → Soru / resim ekle, düzenle, sil
- **Test Center** → Teste gir, konuşmanı yazıya döktür, AI ile puanlat
""")