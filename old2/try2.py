#         # #Eğer veri boş değilse tabloyu göster
#         # #============================================================================================

#         # if not df.empty:

#         #     st.divider()
         






            



#         #     #ID İLE VERİLERİ ÇEK
#         #     #============================================================================================
#         #     satir = df[df["id"] == secili_id].iloc[0]

            
                
#         #         #ıf ile session_state kontrolü yaparak sadece id değiştiğinde formu doldur
#         #         if "Son_Id" not in st.session_state:
#         #             st.session_state.Son_Id = secili_id

#         #         if st.session_state.Son_Id != secili_id:
#         #             st.session_state.Son_Id = secili_id
                
#         #         if "Son_Ana_Kategori" not in st.session_state:
#         #             st.session_state.Son_Ana_Kategori = satir["AnaKategori"]
#         #         if st.session_state.Son_Ana_Kategori != satir["AnaKategori"]:
#         #             st.session_state.Son_Ana_Kategori = satir["AnaKategori"]
                
#         #         if "Son_Alt_Kategori" not in st.session_state:
#         #             st.session_state.Son_Alt_Kategori = satir["AltKategori"]
                
#         #         if st.session_state.Son_Alt_Kategori != satir["AltKategori"]:
#         #             st.session_state.Son_Alt_Kategori = satir["AltKategori"]
                
#         #         if "Son_Soru" not in st.session_state:
#         #             st.session_state.Son_Soru = satir["Soru"]
                
#         #         if st.session_state.Son_Soru != satir["Soru"]:
#         #             st.session_state.Son_Soru = satir["Soru"]
                
#         #         if "Son_Notlar" not in st.session_state:
#         #             st.session_state.Son_Notlar = satir["Notlar"]
                
#         #         if st.session_state.Son_Notlar != satir["Notlar"]:
#         #             st.session_state.Son_Notlar = satir["Notlar"]
                
#         #         if "Son_ResimURL" not in st.session_state:
#         #             st.session_state.Son_ResimURL = satir["ResimURL"]
                
#         #         if st.session_state.Son_ResimURL != satir["ResimURL"]:
#         #             st.session_state.Son_ResimURL = satir["ResimURL"]
                

#         #         # ===============================
#         #         # ÜST FORMU BURADA DOLDUR
#         #         # Ama ekranda yukarıda görünür
#         #         # ===============================

#         #         with form_alani:

#         #             st.subheader("Seçili Soruyu Düzenle")

#         #             col1, col2, col3, col4 = st.columns([1, 2, 2, 2])

#         #             with col1:
#         #                 t_id = st.text_input(
#         #                     "ID",
#         #                     key="MSK_edit_id",
#         #                     disabled=True,
#         #                     value=st.session_state.Son_Id
#         #                 )

#         #             with col2:
#         #                 t_ana_kategori = st.text_input(
#         #                     "Ana Kategori",
#         #                     value=st.session_state.Son_Ana_Kategori,
#         #                     key="MSK_edit_ana_kategori"
#         #                 )

#         #             with col3:
#         #                 t_alt_kategori = st.text_input(
#         #                     "Alt Kategori",
#         #                     value=st.session_state.Son_Alt_Kategori,
#         #                     key="MSK_edit_alt_kategori"
#         #                 )

#         #             with col4:
#         #                 t_pic = st.text_input(
#         #                     "Resim URL",
#         #                     value=st.session_state.Son_ResimURL,
#         #                     key="MSK_edit_pic"
#         #                 )

#         #             t_soru = st.text_area(
#         #                 "Soru",
#         #                 value=st.session_state.Son_Soru,
#         #                 key="MSK_edit_soru",
#         #                 height=120
#         #             )

#         #             t_not = st.text_area(
#         #                 "Notlar",
#         #                 value=st.session_state.Son_Notlar,
#         #                 key="MSK_edit_not",
#         #                 height=100
#         #             )
