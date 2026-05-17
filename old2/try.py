# import streamlit as st
# import pandas as pd
# from io import BytesIO

# from supabaseFonksiyon import (
#     dla_ana_kategori_listesi,
#     dla_alt_kategorileri_getir,
#     dla_sorulari_getir,
#     dla_sorulari_toplu_ekle,
#     dla_soru_guncelle,
#     dla_soru_sil,
# )

# st.header("Dla Soru Editörü")

# tab1, tab2 = st.tabs(["➕ Yeni Soru Ekle", "📋 Mevcut Sorular"])


# # ============================================================================================
# # TAB 1 - YENİ SORU EKLE
# # ============================================================================================
# with tab1:

#     col1, col2, col3 = st.columns([1, 1, 2])

#     with col1:
#         with st.container(border=True, vertical_alignment="center", height="stretch"):
#             Ana_kategori = st.radio(
#                 "Ana Kategori",
#                 dla_ana_kategori_listesi(),
#                 key="soru_ana_kategori_radio"
#             )

#     with col2:
#         with st.container(border=True, vertical_alignment="center", height="stretch"):
#             alt_kategoriler = dla_alt_kategorileri_getir(Ana_kategori)

#             Alt_kategori = st.selectbox(
#                 "Alt Kategori",
#                 alt_kategoriler,
#                 key="soru_alt_kategori_select"
#             )

#     with col3:
#         with st.container(border=True, vertical_alignment="center", height="stretch"):
#             PicPath = st.text_input(
#                 "Resim Yolu (Opsiyonel)",
#                 placeholder="Örnek: /images/question1.png",
#                 key="soru_picpath_input"
#             )

#     NewQuestion = st.text_area(
#         "Soru Metni",
#         placeholder="Her satıra ayrı bir soru yazın.",
#         key="soru_metni_input",
#         height=220
#     )

#     Notes = st.text_area(
#         "Notlar",
#         placeholder="Örnek: Bu soru tercihleri ölçmek için kullanılır.",
#         key="soru_notlar_input"
#     )

#     if st.button("Kaydet", key="dla_soru_kaydet_btn"):

#         if not Ana_kategori.strip():
#             st.warning("Ana kategori boş bırakılamaz.")

#         elif not Alt_kategori.strip():
#             st.warning("Alt kategori boş bırakılamaz.")

#         elif not NewQuestion.strip():
#             st.warning("Soru metni boş bırakılamaz.")

#         else:
#             dla_sorulari_toplu_ekle(
#                 Ana_kategori.strip(),
#                 Alt_kategori.strip(),
#                 NewQuestion.strip(),
#                 Notes.strip(),
#                 PicPath.strip()
#             )

#             eklenen_soru_sayisi = len([
#                 soru for soru in NewQuestion.splitlines()
#                 if soru.strip()
#             ])

#             st.success(f"{eklenen_soru_sayisi} soru eklendi.")




# # ============================================================================================
# # TAB 2 - MEVCUT SORULAR
# # ============================================================================================
# with tab2:

#     # Üst form için yer ayır
#     col1, col2 , col3 = st.columns([1, 1, 1])
#     with col1:
#         with st.container(border=True, vertical_alignment="center", height="stretch"):
#             Ana_kategori1 = st.radio(
#                 "Ana Kategori",
#                 ["All"] + dla_ana_kategori_listesi(),
#                 key="soru_ana_kategori_radio1"
#             )

#     with col2:
#         with st.container(border=True, vertical_alignment="center", height="stretch"):
#             alt_kategoriler1 = dla_alt_kategorileri_getir(Ana_kategori1)
    
#             if Ana_kategori1 == "ALL":
#                 Alt_kategori1 = st.selectbox(
#                 "Alt Kategori",
#                 ["All"],
#                 key="soru_alt_kategori_select1"
#                 )
#             else:
#                 Alt_kategori1 = st.selectbox(
#                 "Alt Kategori",
#                 ["All"] + alt_kategoriler1,
#                 key="soru_alt_kategori_select1"
#                 )

#     if "son_ana_kategori" not in st.session_state:
#         st.session_state.son_ana_kategori = Ana_kategori1

#     if "son_alt_kategori" not in st.session_state:
#         st.session_state.son_alt_kategori = Alt_kategori1

#     if (
#         st.session_state.son_ana_kategori != Ana_kategori1
#         or st.session_state.son_alt_kategori != Alt_kategori1
#     ):
#         st.session_state.sorular_gosterilsin = False
#         st.session_state.son_ana_kategori = Ana_kategori1
#         st.session_state.son_alt_kategori = Alt_kategori1

#     with col3:
#         with st.container(border=True, vertical_alignment="center", height="stretch"):
#             sorugetir = st.button("Soruları Getir", key="soru_getir_btn")

#     if "sorular_gosterilsin" not in st.session_state:
#         st.session_state.sorular_gosterilsin = False
    
#     if sorugetir:
#         st.session_state.sorular_gosterilsin = True

#     if st.session_state.sorular_gosterilsin:

#         form_alani = st.container()

#         # ===============================
#         # VERİ ÇEK
#         # ===============================
#         rows = dla_sorulari_getir(ana_kategori=Ana_kategori1, alt_kategori=Alt_kategori1)
#         df = pd.DataFrame(rows.data)

#         if not df.empty:

#             st.divider()

           
#             # Önce tabloyu sadece göster
#             if Ana_kategori1 == "All":
#                 gosterilecek_kolonlar = ["id", "AnaKategori", "AltKategori", "Soru", "Notlar", "ResimURL"]

#             if Ana_kategori1 == "General":
#                 gosterilecek_kolonlar = ["id", "Soru"]

#             if Ana_kategori1 == "Scenario":
#                 gosterilecek_kolonlar = ["id", "Soru"]

#             if Ana_kategori1 == "PictureDescription":
#                 gosterilecek_kolonlar = ["id", "ResimURL"]

#             event = st.dataframe(
#                 df[gosterilecek_kolonlar],
#                 use_container_width=True,
#                 hide_index=True,
#                 on_select="rerun",
#                 selection_mode="single-row",
#                 column_config={
#                     "id": st.column_config.NumberColumn("ID", width=20),
#                     }
#                 )
            
#             if event.selection.rows:
#                 secili_index = event.selection.rows[0]
#                 secili_satir = df.iloc[secili_index]
#                 secili_id = secili_satir["id"]

#                 # st.write("Seçilen ID:", secili_id)
                

#                 #ID İLE VERİLERİ ÇEK
#                 satir = df[df["id"] == secili_id].iloc[0]
                
#                 #ıf ile session_state kontrolü yaparak sadece id değiştiğinde formu doldur
#                 if "Son_Id" not in st.session_state:
#                     st.session_state.Son_Id = secili_id

#                 if st.session_state.Son_Id != secili_id:
#                     st.session_state.Son_Id = secili_id
                
#                 if "Son_Ana_Kategori" not in st.session_state:
#                     st.session_state.Son_Ana_Kategori = satir["AnaKategori"]
#                 if st.session_state.Son_Ana_Kategori != satir["AnaKategori"]:
#                     st.session_state.Son_Ana_Kategori = satir["AnaKategori"]
                
#                 if "Son_Alt_Kategori" not in st.session_state:
#                     st.session_state.Son_Alt_Kategori = satir["AltKategori"]
                
#                 if st.session_state.Son_Alt_Kategori != satir["AltKategori"]:
#                     st.session_state.Son_Alt_Kategori = satir["AltKategori"]
                
#                 if "Son_Soru" not in st.session_state:
#                     st.session_state.Son_Soru = satir["Soru"]
                
#                 if st.session_state.Son_Soru != satir["Soru"]:
#                     st.session_state.Son_Soru = satir["Soru"]
                
#                 if "Son_Notlar" not in st.session_state:
#                     st.session_state.Son_Notlar = satir["Notlar"]
                
#                 if st.session_state.Son_Notlar != satir["Notlar"]:
#                     st.session_state.Son_Notlar = satir["Notlar"]
                
#                 if "Son_ResimURL" not in st.session_state:
#                     st.session_state.Son_ResimURL = satir["ResimURL"]
                
#                 if st.session_state.Son_ResimURL != satir["ResimURL"]:
#                     st.session_state.Son_ResimURL = satir["ResimURL"]
                

#                 # ===============================
#                 # ÜST FORMU BURADA DOLDUR
#                 # Ama ekranda yukarıda görünür
#                 # ===============================

#                 with form_alani:

#                     st.subheader("Seçili Soruyu Düzenle")

#                     col1, col2, col3, col4 = st.columns([1, 2, 2, 2])

#                     with col1:
#                         t_id = st.text_input(
#                             "ID",
#                             key="edit_id",
#                             disabled=True,
#                             value=st.session_state.Son_Id
#                         )

#                     with col2:
#                         t_ana_kategori = st.text_input(
#                             "Ana Kategori",
#                             value=st.session_state.Son_Ana_Kategori,
#                             key="edit_ana_kategori"
#                         )

#                     with col3:
#                         t_alt_kategori = st.text_input(
#                             "Alt Kategori",
#                             value=st.session_state.Son_Alt_Kategori,
#                             key="edit_alt_kategori"
#                         )

#                     with col4:
#                         t_pic = st.text_input(
#                             "Resim URL",
#                             value=st.session_state.Son_ResimURL,
#                             key="edit_pic"
#                         )

#                     t_soru = st.text_area(
#                         "Soru",
#                         value=st.session_state.Son_Soru,
#                         key="edit_soru",
#                         height=120
#                     )

#                     t_not = st.text_area(
#                         "Notlar",
#                         value=st.session_state.Son_Notlar,
#                         key="edit_not",
#                         height=100
#                     )


                

                


#     #     secili_satirlar = edited_df[edited_df["Sec"] == True]

#     #     if len(secili_satirlar) == 1:

#     #         selected_row = secili_satirlar.iloc[0]
#     #         selected_id = int(selected_row["id"])

#     #         if st.session_state.son_secili_id != selected_id:

#     #             st.session_state.son_secili_id = selected_id
#     #             st.session_state.edit_id = str(selected_row["id"])
#     #             st.session_state.edit_ana_kategori = str(selected_row["AnaKategori"])
#     #             st.session_state.edit_alt_kategori = str(selected_row["SubKategori"])
#     #             st.session_state.edit_soru = str(selected_row["Soru"])

#     #             st.session_state.edit_pic = (
#     #                 "" if pd.isna(selected_row["ResimURL"])
#     #                 else str(selected_row["ResimURL"])
#     #             )

#     #             st.session_state.edit_not = (
#     #                 "" if pd.isna(selected_row["Notes"])
#     #                 else str(selected_row["Notes"])
#     #             )

#     #             st.rerun()

#     #     elif len(secili_satirlar) > 1:
#     #         st.warning("Lütfen sadece bir satır seç.")

#     #     else:
#     #         st.info("İşlem yapmak için tablodan bir satır seç.")

#     #     # ===============================
#     #     # ÜST FORMU BURADA DOLDUR
#     #     # Ama ekranda yukarıda görünür
#     #     # ===============================
#     #     with form_alani:

#     #         st.subheader("Seçili Soruyu Düzenle")

#     #         col1, col2, col3, col4 = st.columns([1, 2, 2, 2])

#     #         with col1:
#     #             t_id = st.text_input(
#     #                 "ID",
#     #                 key="edit_id",
#     #                 disabled=True
#     #             )

#     #         with col2:
#     #             t_ana_kategori = st.text_input(
#     #                 "Ana Kategori",
#     #                 key="edit_ana_kategori"
#     #             )

#     #         with col3:
#     #             t_alt_kategori = st.text_input(
#     #                 "Alt Kategori",
#     #                 key="edit_alt_kategori"
#     #             )

#     #         with col4:
#     #             t_pic = st.text_input(
#     #                 "Resim URL",
#     #                 key="edit_pic"
#     #             )

#     #         t_soru = st.text_area(
#     #             "Soru",
#     #             key="edit_soru",
#     #             height=120
#     #         )

#     #         t_not = st.text_area(
#     #             "Notlar",
#     #             key="edit_not",
#     #             height=100
#     #         )

#     #         col1, col2, col3 = st.columns(3)

#     #         with col1:
#     #             if st.button("💾 Güncelle", use_container_width=True):

#     #                 if not st.session_state.edit_id:
#     #                     st.warning("Önce bir satır seçmelisin.")

#     #                 else:
#     #                     dla_soru_guncelle(
#     #                         int(st.session_state.edit_id),
#     #                         st.session_state.edit_ana_kategori.strip(),
#     #                         st.session_state.edit_alt_kategori.strip(),
#     #                         st.session_state.edit_soru.strip(),
#     #                         st.session_state.edit_not.strip(),
#     #                         st.session_state.edit_pic.strip()
#     #                     )

#     #                     st.success("Soru güncellendi.")
#     #                     st.rerun()

#     #         with col2:
#     #             if st.button("🗑️ Sil", use_container_width=True):

#     #                 if not st.session_state.edit_id:
#     #                     st.warning("Önce bir satır seçmelisin.")

#     #                 else:
#     #                     dla_soru_sil(int(st.session_state.edit_id))
#     #                     st.success("Soru silindi.")
#     #                     st.rerun()

#     #         with col3:
#     #             if st.button("🧹 Temizle", use_container_width=True):

#     #                 st.session_state.edit_id = ""
#     #                 st.session_state.edit_ana_kategori = ""
#     #                 st.session_state.edit_alt_kategori = ""
#     #                 st.session_state.edit_pic = ""
#     #                 st.session_state.edit_soru = ""
#     #                 st.session_state.edit_not = ""
#     #                 st.session_state.son_secili_id = None

#     #                 st.rerun()

#     # else:
#     #     st.info("Henüz kayıt yok.")
        
#     # st.divider()

#     # ============================================================================================
#     # EXCEL EXPORT
#     # ============================================================================================

#     # export_df = edited_df.drop(columns=["Sec"], errors="ignore")

#     # excel_buffer = BytesIO()

#     # with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
#     #     export_df.to_excel(writer, index=False, sheet_name="DlaSorular")

#     # st.download_button(
#     #     label="📥 Excel Olarak İndir",
#     #     data=excel_buffer.getvalue(),
#     #     file_name="DlaSorular.xlsx",
#     #     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#     #     use_container_width=True
#     # )



#     # col1, col2, col3, col4, col5 = st.columns([1, 1,1,1,1])
    
#     # with col1:
#     #     container = st.container(border=True,height=100, vertical_alignment="center")
#     #     container.write("ID")
#     # with col2:
#     #     container = st.container(border=True,height=100, vertical_alignment="center")
#     #     container.write("ID2")
#     # with col3:
#     #     container = st.container(border=True,height=100, vertical_alignment="center")
#     #     container.write("ID3")
#     # with col4:
#     #     container = st.container(border=True,height=100, vertical_alignment="center")
#     #     container.write("ID4")
#     # with col5:
#     #     container = st.container(border=True,height=100, vertical_alignment="center")
#     #     container.write("ID5")