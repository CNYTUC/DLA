# https://cnytcxtry.streamlit.app/
# 
# #py -m pip install -r requirements.txt
#streamlit run app.py
#py -m streamlit run app.py
#İCON KUTUPHANESİ https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded
# https://unicode.org/emoji/charts/full-emoji-list.html
#ÖRNEK KULLANIM: if st.button("Next Question", key=f"next_question_btn_{question_id}_{current_index}", icon=":material/home:"):


import streamlit as st

#Sayfanın Genel Yapısı
st.set_page_config(
    page_title="SINAV SİSTEMİ",
    page_icon="🎤",
    layout="wide"
)

#NAVIGASYON
#===================================================================================
pages = {
    
    "MAIN": [
        st.Page("main.py", title="Main", icon="🏠"),
        # st.Page("try.py", title="try", icon="🧪"),
        st.Page("pages/1_dla_editor.py", title="try", icon="🧪"),
        
    ],     
    "DLA SINAVLARI": [
        # st.Page("ingilizce/general.py", title="General Test", icon="🎤"),
    ],     
    "DLA EDİTÖRLERİ": [
        # st.Page("pages/dla_1_kategoriler/dla_kategoriEditor.py", title="Kategori Editörü", icon="📚"),
        # st.Page("pages/dla_2_sorular/dla_soru_editor.py", title="Soru Editörü", icon="📝"),
    ],    
}

pg = st.navigation(pages, position="top")
pg.run()
#===================================================================================