import streamlit as st
import pandas as pd

# KÜTÜPHANELER
import UTILS.session_utils as SsnFonk
import UTILS.supabaseFonksiyon as SpFonk
import UTILS.text_utils as TxtFonk

# Veri Tabanından Çağırılanlar
def DLA_Ana_Kategoriler():
    #dondur
    return ["General", "Scenario", "PictureDescription"]


#====================================================================================
# NAVIGATION OLUŞTUR
#============================================================================================

def navigasyonOlustur():

    pages = {
    
    "MAIN": [
        st.Page("main.py", title="Main", icon="🏠")
        
    ],     
    "DLA KATEGORİSİ": [
        st.Page("PAGES/01_DLA_EDITOR.py", title="D.L.A. Editör", icon="📝"),
        st.Page("PAGES/02_DLA_EXAM.py", title="D.L.A. Exam", icon="🎤")

    ],     
    "REC KATEGORİSİ": [
        st.Page("PAGES/03_REC_EDITOR.py", title="R.E.C. Editör", icon="📝"),
        st.Page("PAGES/04_REC_EXAM.py", title="R.E.C. Exam", icon="📚")

    ],    
    }

    pg = st.navigation(pages, position="top")
    pg.run()


#====================================================================================
# TEXT DÜZENLEME FONKSİYONLARI
#============================================================================================

def tr_to_en_lower(text):
    return TxtFonk.tr_to_en_lower(text)