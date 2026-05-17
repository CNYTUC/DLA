import streamlit as st
import pandas as pd
from io import BytesIO
from kategoriler import DLA_ANA_KATEGORI_LISTESI, DLA_ALT_KATEGORILERI_LISTESI

from v1.supabaseFonksiyon import (
    dla_soru_ekle,
    dla_sorulari_getir,
    dla_soru_guncelle,
    dla_soru_sil
)

#BAŞLIK
#============================================================================================
st.header("Dla Soru Editörü")


#Yenı Soru Ekleme Formu
#============================================================================================
st.subheader("➕ Yeni Soru Ekle")


# Soru seçimi oluştur.
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    with st.container(border=True,vertical_alignment="center",height="stretch"):
        Ana_kategori = st.radio(
            "Ana Kategori",
            DLA_ANA_KATEGORI_LISTESI,
            key="ana_kategori_radio"
        )

with col2:
    with st.container(border=True,vertical_alignment="center",height="stretch"):
        if Ana_kategori:
            
            alt_kategoriler = DLA_ALT_KATEGORILERI_LISTESI(Ana_kategori)

            Alt_kategori = st.selectbox(
            "Alt Kategori",
            alt_kategoriler,
            key="alt_kategori_select"
            )
    
with col3:
        with st.container(border=True,vertical_alignment="center",height="stretch"):
            PicPath = st.text_input(
            "Resim Yolu (Opsiyonel)",
            placeholder="Örnek: /images/question1.png"
            )

NewQuestion = st.text_input(
                "Soru Metni",
                placeholder="Örnek: What do you prefer, tea or coffee?"
                )

Notes = st.text_input(
                "Notlar",
                placeholder="Örnek: Bu soru tercihleri ölçmek için kullanılır."
                )

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
            dla_soru_ekle(
                Ana_kategori,
                Alt_kategori,
                NewQuestion.strip(),
                Notes.strip(),
                PicPath.strip()
            )
            st.success("Yeni soru eklendi.")
            st.rerun()

st.divider()

# Mevcut Kategorileri Göster ve Düzenle
# ============================================================================================

st.subheader("📋 Mevcut Kategoriler")

rows = dla_sorulari_getir()
df = pd.DataFrame(rows.data)

if not df.empty:

    # Seçim kolonu ekle
    df.insert(0, "Sec", False)

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
                width=550
            ),
            "SubKategori": st.column_config.TextColumn(
                "Alt Kategori",
                width=550
            ),
            "Soru": st.column_config.TextColumn(
                "Soru",
                width=550
            ),
            "ResimURL": st.column_config.TextColumn(
                "Resim URL",
                width=550
            ),
            "Notes": st.column_config.TextColumn(
                "Notlar",
                width=550
            ),
        },
        key="soru_editor"
    )

    st.divider()

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

    elif len(secili_satirlar) > 1:
        st.warning("Lütfen sadece bir satır seç.")
    else:
        st.info("İşlem yapmak için tablodan bir satır seç.")


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