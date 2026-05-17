import streamlit as st
import pandas as pd
from io import BytesIO

from v1.supabaseFonksiyon import (
    dla_ana_kategori_listesi,
    dla_alt_kategorileri_getir,
    dla_soru_ekle,
    dla_soru_sil,
    dla_sorulari_getir,
    dla_sorulari_toplu_ekle,
    dla_soru_guncelle,
)


#BAŞLIK
#============================================================================================
st.header("Dla Soru Editörü")


tab1, tab2 = st.tabs(["➕ Yeni Soru Ekle", "📋 Mevcut Sorular"])

with tab1:
    #SORU BILGILERI 
    #============================================================================================
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        with st.container(border=True,vertical_alignment="center",height="stretch"):
            Ana_kategori = st.radio(
                "Ana Kategori",
                dla_ana_kategori_listesi(),
                key="soru_ana_kategori_radio"
            )

    with col2:
        with st.container(border=True,vertical_alignment="center",height="stretch"):
            if Ana_kategori:
                
                alt_kategoriler = dla_alt_kategorileri_getir(Ana_kategori)

                Alt_kategori = st.selectbox(
                "Alt Kategori",
                alt_kategoriler,
                key="soru_alt_kategori_select"
                )
    
    with col3:
            with st.container(border=True,vertical_alignment="center",height="stretch"):
                PicPath = st.text_input(
                "Resim Yolu (Opsiyonel)",
                placeholder="Örnek: /images/question1.png",
                key="soru_picpath_input"
                )

    NewQuestion = st.text_area(
                "Soru Metni",
                placeholder="Her satıra ayrı bir soru yazın.\nÖrnek:\nWhat do you prefer, tea or coffee?\nWhat is your favorite hobby?",
                key="soru_metni_input",
                height=220
                )

    Notes = st.text_area(
                "Notlar",
                placeholder="Örnek: Bu soru tercihleri ölçmek için kullanılır.",
                key="soru_notlar_input"
                )

    #FORMU OLUŞTUR VE KAYDET BUTONU EKLE 
    #============================================================================================
    with st.form("soru_ekleme_formu", clear_on_submit=True):

        kaydet = st.form_submit_button(
            "Kaydet",
            key="dla_soru_kaydet_btn"
        )

        if kaydet:
            if not Ana_kategori.strip():
                st.warning("Ana kategori boş bırakılamaz.")
            elif not Alt_kategori.strip():
                st.warning("Alt kategori boş bırakılamaz.")
            elif not NewQuestion.strip():
                st.warning("Soru metni boş bırakılamaz.")
            else:
                sonuc = dla_sorulari_toplu_ekle(
                    Ana_kategori,
                    Alt_kategori,
                    NewQuestion.strip(),
                    Notes.strip(),
                    PicPath.strip()
                )

                eklenen_soru_sayisi = len([
                    soru for soru in NewQuestion.splitlines()
                    if soru.strip()
                ])

                st.success(f"{eklenen_soru_sayisi} soru eklendi.")

#============================================================================================
st.divider()
#============================================================================================

with tab2:
    # Mevcut Kategorileri Göster ve Düzenle
    # ============================================================================================

    rows = dla_sorulari_getir()
    df = pd.DataFrame(rows.data)

    if not df.empty:

        # Seçim kolonu ekle
        df.insert(0, "Sec", False)

        # Ekrana Yazdır
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            disabled=["id"],
            column_config={
                "Sec": st.column_config.CheckboxColumn(
                    "Seç",
                    width=None
                ),
                "id": st.column_config.NumberColumn(
                    "ID",
                    width=None
                ),
                "AnaKategori": st.column_config.TextColumn(
                    "Ana Kategori",
                    width=None
                ),
                "SubKategori": st.column_config.TextColumn(
                    "Alt Kategori",
                    width=None
                ),
                "Soru": st.column_config.TextColumn(
                    "Soru",
                    width=1000
                ),
                "ResimURL": st.column_config.TextColumn(
                    "Resim URL",
                    width=None
                ),
                "Notes": st.column_config.TextColumn(
                    "Notlar",
                    width=None
                ),
            },
            key="soru_editor"
        )

        #============================================================================================
        st.divider()
        #============================================================================================


        # Duzenleme ve Silme İşlemleri
        secili_satirlar = edited_df[edited_df["Sec"] == True]

        if len(secili_satirlar) == 1:

            selected_row = secili_satirlar.iloc[0]
            selected_id = int(selected_row["id"])

            st.info(f"Seçili ID: {selected_id}")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("💾 Seçili Satırı Güncelle", use_container_width=True):
                    dla_soru_guncelle(
                        selected_id,
                        selected_row["AnaKategori"],
                        selected_row["SubKategori"],
                        selected_row["Soru"],
                        selected_row["Notes"],
                        selected_row["ResimURL"]
                    )
                    st.success("Soru güncellendi.")
                    st.rerun()

            with col2:
                if st.button("🗑️ Seçili Satırı Sil", use_container_width=True):
                    dla_soru_sil(selected_id)
                    st.success("Soru silindi.")
                    st.rerun()

        #Seçili satır sayısına göre uyarılar
        #============================================================================================
        elif len(secili_satirlar) > 1:
            st.warning("Lütfen sadece bir satır seç.")
        else:
            st.info("İşlem yapmak için tablodan bir satır seç.")



        #excel export işlemi
        #============================================================================================

        export_df = edited_df.drop(columns=["Sec"], errors="ignore")

        excel_buffer = BytesIO()

        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            export_df.to_excel(writer, index=False, sheet_name="DlaSorular")

        st.download_button(
            label="📥 Excel Olarak İndir",
            data=excel_buffer.getvalue(),
            file_name="DlaSorular.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    else:
        st.info("Henüz kayıt yok.")