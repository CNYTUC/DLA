# https://cnytcxtry.streamlit.app/
# 
# #py -m pip install -r requirements.txt
#streamlit run app.py
#py -m streamlit run app.py
#İCON KUTUPHANESİ https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded
# https://unicode.org/emoji/charts/full-emoji-list.html
#ÖRNEK KULLANIM: if st.button("Next Question", key=f"next_question_btn_{question_id}_{current_index}", icon=":material/home:"):


# KÜTÜPHANELER
import streamlit as st
import pandas as pd

# UTILS
import UTILS.ara_module as am
  

#Sayfanın Genel Yapısı
#============================================================================================

st.set_page_config(
    page_title="SINAV SİSTEMİ",
    page_icon="🎤",
    layout="wide"
)

#============================================================================================

# NAVIGASYON
am.navigasyonOlustur()

