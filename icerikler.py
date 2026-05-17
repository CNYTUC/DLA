# KUTUPHANELER
import streamlit as st
import pandas as pd
from io import BytesIO

# UTILS import
import UTILS.session_utils as SsnFonk
import UTILS.supabaseFonksiyon as SpFonk
import UTILS.text_utils as TxtFonk
import UTILS.time_utils as TimeFonk

# YENİ SORU DÜZENLEME ALANINI DOLDUR
#============================================================================================
def Yeni_Soru_Alan_Doldur(alan):
    

    Ana_kategoriler = st.session_state.Ana_kategoriler_list

    with alan:
    

        Secilen_ana_kategori: str = ""


        # Ana kategori seçimi
        # ============================================================================================  
        # with st.container(border=True, vertical_alignment="center", height="stretch"):


        Secilen_ana_kategori = st.radio(
            "Ana Kategori",
            options=Ana_kategoriler,
            key="YSK_ana_kategori",
            horizontal=True
        )

        #Önerme Yaz
        if Secilen_ana_kategori == "PictureDescription":
            st.write("Gereklilikler: En az 1 Etiket, Sadece 1 Soru metni ve 1 Resim yolu.")
        else:
            st.write("Gereklilikler: En az 1 Etiket, Soru metni.")

        # st.write(Secilen_ana_kategori)


        # Etiketler girişi
        # ============================================================================================

        VT_ETIKETLER = SpFonk.dla_etiketler_DF()
        mevcut_etiketler_seti = set(VT_ETIKETLER["Etiket"].dropna().unique())
        YS_ETIKETLER: list = []
        
        # 1. Etiketler seçme
        # with st.container(border=True, vertical_alignment="center", height="stretch"):
            
        YS_ETIKETLER = st.multiselect(
            "Etiketlerinizi seçin",
            options=mevcut_etiketler_seti,
            max_selections=20,
            accept_new_options=True,
            placeholder="Etiketlerinizi seçin !!!",
            key="YSK_etiketler0",
            )
                
        # Etiketleri yazdır
        st.write(TxtFonk.tr_to_en_lower(", ".join(YS_ETIKETLER)))



# # YENİ ETİKET EKLEME ALANINI DOLDUR
# #============================================================================================
# def Yeni_Etiket_Alan_Doldur(alan):
        
    
#     with alan:
              
#         #ETİKETLERİ GETIR
#         vt_etiketler: pd.DataFrame = st.session_state.YE_YeniEtiketler_list
        
#         #EĞER KAYIT YOKSA BILGI VER
#         if vt_etiketler.empty:
#             st.info("Herhangi bir etiket bulunamadı.")           
#             st.stop()
        
        
        
#         #EĞER KAYIT VARSA DEVAM ET
#         st.write(len(vt_etiketler), "tane etiket bulundu.")
        
#         # Kolonları olustur
#         # ============================================================================================
#         col1,col2 = st.columns([1,1])
        
#         with col1:
                
#                 # COL1 CONTAINER OLUSTUR
#                 # ============================================================================================
#                 with st.container(border=True,vertical_alignment="center",height="stretch"):    
                    
#                     # Arama alanı
#                     # ============================================================================================
#                     search_text = st.text_input("🔍 Etiket Ara", placeholder="Etiket gir...")
#                     search_text = TxtFonk.tr_to_en_lower(search_text.strip())
                    
#                     filtered_df = vt_etiketler.copy()

#                     if search_text:
#                         filtered_df = filtered_df[
#                             filtered_df["Etiket"].str.contains(search_text, case=False, na=False)
#                         ]
        
#                     # ETİKET ALANI
#                     # ============================================================================================

#                     # Seçim kolonu ekle
#                     if "sec" not in vt_etiketler.columns:
#                         filtered_df.insert(0, "sec", False)


#                     edited_df = st.data_editor(
#                         filtered_df,
#                         use_container_width=False,
#                         hide_index=True,
#                         row_height=42,
#                         height=300,
                        
#                         column_config={
                            
#                             "sec": st.column_config.CheckboxColumn("SEC", width=100),
#                             "id": None,  # 👈 BU SATIR KOLONU GİZLER
#                             "Etiket": st.column_config.TextColumn("ETİKET", width=1000),
                            
#                         },
                        
#                         key="MEK_etiket_editor"
#                     )
                    
#                     # Excel olarak indirme butonu
#                     #============================================================================================

#                     export_df = edited_df.drop(columns=["Sec"], errors="ignore")
                    
#                     excel_buffer = BytesIO()

#                     with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
#                         export_df.to_excel(writer, index=False, sheet_name="DlaKategoriler")

#                     st.download_button(
#                         label="📥 Excel Olarak İndir",
#                         data=excel_buffer.getvalue(),
#                         file_name="DlaEtiketler.xlsx",
#                         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#                         use_container_width=True
#                     )

#         with col2:
            
#             #seçili satırları al
#             secili_satirlar = edited_df[edited_df["sec"] == True] 
            
#             updated_tag = ""
            
#             # COL2 CONTAINER OLUSTUR
#             # ============================================================================================
#             with st.container(border=True,vertical_alignment="center",height="stretch"):
        
#                     # SINAMA 1
#                 # ============================================================================================
#                 if len(secili_satirlar) > 1:
#                     st.warning("Lütfen sadece bir satır seç.", icon="⚠️")
                
#                 # SINAMA 2
#                 # ============================================================================================    
#                 elif len(secili_satirlar) < 1:
#                     st.info("İşlem yapmak için tablodan bir satır seç.", icon="ℹ️")
                
#                 # İŞLEM
#                 # ============================================================================================
#                 else:
                    
#                     # Tanımalamaları yap
#                     #============================================================================================
#                     selected_row = secili_satirlar.iloc[0]
#                     selected_id = int(selected_row["id"])
#                     selected_tag = TxtFonk.tr_to_en_lower(selected_row["Etiket"])

#                     #Seçilen ID ve Etiketi yazdır
#                     st.info(f"Seçili ID: {selected_id}", icon="ℹ️")
                    
#                     updated_tag = st.text_input(
#                         "Seçili Etiket",
#                         value=selected_tag,
#                         disabled=False,
#                         width="stretch"
#                     )
                    
#                     #  GUNCELLE BUTONU
#                     if st.button("💾 Seçili Etiketi Güncelle", use_container_width=True):
#                         SpFonk.dla_etiket_guncelle(
#                             selected_id,
#                             TxtFonk.tr_to_en_lower(updated_tag),
#                         )
                        
#                         st.success("Etiket güncellendi.", icon="✅")
                        
#                         # RESET
#                         SsnFonk.session_resetle("ME_", SsnFonk.ssElamanlar)
                        
                    