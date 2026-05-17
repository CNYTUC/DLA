# KUTUPHANELER
import streamlit as st
import pandas as pd
from io import BytesIO

import UTILS.ara_module as am
import UTILS.supabaseFonksiyon as SpFonk

# BAŞLIK
# ============================================================================================
st.header("D.L.A. Editörü 🤠")

# SAYFA YAPISI OLUSTUR
# ============================================================================================
Yeni_Soru, Mevcut_Soru, Mevcut_Etiketler = st.tabs(["❓ Yeni Soru", "📖 Mevcut Sorular", "🔖 Mevcut Etiketler"])    

# YENİ SORU EKLEME
# ============================================================================================
with Yeni_Soru:   
    
    # ALT BAŞLIK BELİRLE
    # ============================================================================================
    st.subheader(f"Yeni Soru Ekle ❓",divider="yellow")
        
    # DIŞ CONTAINER OLUSTUR
    # ============================================================================================
    with st.container(border=True,vertical_alignment="center",height="stretch"):
        

        # Ana kategori seçimi
        # ============================================================================================  
        with st.container(border=True, vertical_alignment="center", height="stretch"):

            # DEĞİŞKENLER
            Ana_kategoriler:list = am.DLA_Ana_Kategoriler()

            # Ana kategori seçimi
            st.radio(
                "Ana Kategori",
                options=Ana_kategoriler,
                horizontal=True,
                key="Yeni_Soru_Ana_Kategori_Radio",
            )


        # Soru metni ve notlar için geniş bir alan
        # ============================================================================================
        if st.session_state.Yeni_Soru_Ana_Kategori_Radio == "PictureDescription":
            st.session_state.Yeni_Soru_Soru_Metni = "Describe The Picture"
        else:
            with st.container(border=True, vertical_alignment="center", height="stretch"):
                st.text_area(
                    "Soru Metni",
                    placeholder="Her satıra ayrı bir soru yazın.",
                    height=100,
                    key="Yeni_Soru_Soru_Metni",
                    )


        # Etiketler girişi
        # ============================================================================================
        if not st.session_state.Yeni_Soru_Ana_Kategori_Radio == "PictureDescription":
                
            # DEĞİŞKENLER
            Vt_Etiketler: pd.DataFrame = SpFonk.dla_etiketler_DF()
            mevcut_etiketler_seti = set(Vt_Etiketler["Etiket"].dropna().unique())  
            
            with st.container(border=True, vertical_alignment="center", height="stretch"):
                
                st.multiselect(
                    "Etiketlerinizi seçin",
                    options=mevcut_etiketler_seti,
                    max_selections=20,
                    accept_new_options=True,
                    placeholder="Etiketlerinizi seçin !!!",
                    key="Yeni_Soru_Etiketler_Multiselect",
                    )
                    
                #Önerme Yaz
                Yeni_Soru_Etiketler = st.session_state.Yeni_Soru_Etiketler_Multiselect
                
                if Yeni_Soru_Etiketler:
                    st.success(am.tr_to_en_lower(" ".join(Yeni_Soru_Etiketler)))


        # Resim yolu girişi (yalnızca PictureDescription için)
        # ============================================================================================
        if st.session_state.Yeni_Soru_Ana_Kategori_Radio == "PictureDescription":
           
            with st.container(border=True, vertical_alignment="center", height="stretch"):
                                   
                st.text_input(
                "Resim Yolu",
                placeholder="Örnek: /images/question1.png",
                key="Yeni_Soru_Resim_Yolu_Input",
                )
        

        # Notlar alanı
        # ============================================================================================

        with st.container(border=True, vertical_alignment="center", height="stretch"):
            
            st.text_area(
                "Notlar (Opsiyonel)",
                placeholder="Örnek: Bu soru tercihleri ölçmek için kullanılır.",
                key="Yeni_Soru_Notlar_TextArea",
                )


        # Kontrol ve Kayıt alanı
        # ============================================================================================
        with st.container(border=True, vertical_alignment="center", height="stretch"):
            
            if st.button("Kontrol Et", key="Yeni_Soru_Kontrol_Et_Button", width="stretch", icon="✅"):
                
                # ÖNERME YAZ
                Secilen_Kategori = st.session_state.Yeni_Soru_Ana_Kategori_Radio
                st.write(f":green[Seçilen Kategori : {Secilen_Kategori}]")


                SecilenSoruSayisi = len(st.session_state.Yeni_Soru_Soru_Metni.splitlines()) if st.session_state.Yeni_Soru_Soru_Metni else 0
                if SecilenSoruSayisi > 0:
                    st.write(f":green[Girdiğiniz Soru Metni Sayısı : {SecilenSoruSayisi}]")
                else:
                    st.write(f":red[Girdiğiniz Soru Metni Sayısı : {SecilenSoruSayisi}]") 


                SecilenResimYolu = st.session_state.Yeni_Soru_Resim_Yolu_Input if st.session_state.Yeni_Soru_Ana_Kategori_Radio == "PictureDescription" else ""
                st.write(f":green[Girdiğiniz Resim Yolu : {SecilenResimYolu}]") if SecilenResimYolu else st.write(f":red[Girdiğiniz Resim Yolu : {SecilenResimYolu}]")      

                SecilenEtiketler = st.session_state.Yeni_Soru_Etiketler_Multiselect if not st.session_state.Yeni_Soru_Ana_Kategori_Radio == "PictureDescription" else ""
                st.write(f":green[Girdiğiniz Etiketler : {', '.join(SecilenEtiketler) if isinstance(SecilenEtiketler, list) else SecilenEtiketler}]")

                SecilenNotlar = st.session_state.Yeni_Soru_Notlar_TextArea if st.session_state.Yeni_Soru_Notlar_TextArea else ""
                st.write(f":green[Girdiğiniz Notlar : {SecilenNotlar}]")




                

 

            
# # MEVCUT SORULAR
# # ============================================================================================
# with Mevcut_Soru:

#     # ALT BAŞLIK BELİRLE
#     # ============================================================================================
#     st.subheader(f"Mevcut Etiketler 🔖",divider="rainbow")

#     # DIŞ CONTAINER OLUSTUR
#     # ============================================================================================
#     with st.container(border=True,vertical_alignment="center",height="stretch"):
        
#         Mevcut_Soru_Alan = st.empty()
    
# # MEVCUT ETİKETLER
# # ============================================================================================
# with Mevcut_Etiketler:

#     # ALT BAŞLIK BELİRLE
#     # ============================================================================================
#     st.subheader(f"Mevcut Sorular 📖",divider="red")

#     # DIŞ CONTAINER OLUSTUR
#     # ============================================================================================
#     with st.container(border=True,vertical_alignment="center",height="stretch"):
        
#         Mevcut_Etiket_Alan = st.empty()
