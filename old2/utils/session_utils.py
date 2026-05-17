import streamlit as st


def session_olustur(elemanlar: dict):
    for key, factory in elemanlar.items():
        if key not in st.session_state:
            st.session_state[key] = factory()

def session_resetle(prefix: str, elemanlar: dict):
    """
    Prefix'e göre session_state değerlerini sıfırlar (silmez, default'a çeker)

    prefix: "YE_"
    elemanlar: {"YE_x": factory}
    """
    for key, factory in elemanlar.items():
        if key.startswith(prefix):
            st.session_state[key] = factory()
            
            
def session_sil(prefix):
    for key in list(st.session_state.keys()):
        if key.startswith(prefix):
            del st.session_state[key]
            