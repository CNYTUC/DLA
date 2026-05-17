# IMPORTLAR
# ============================================================================================
import streamlit as st
import pandas as pd
from io import BytesIO
#text
from v1.utils.text_utils import tr_to_en_lower
from v1.utils.text_utils import ilk_harf_buyuk
#zaman
from v1.utils.time_utils import wait
#session
from v1.utils.session_utils import session_olustur
from v1.utils.session_utils import session_resetle

#supabase
from v1.supabaseFonksiyon import (
    dla_ana_kategori_listesi,
    dla_etiket_ekle,
    dla_etiketler_getir,
    dla_etiket_guncelle,
    dla_etiket_sil,
    
    dla_soruetiket_etikete_gore_sil,

    dla_soru_ekle,
    dla_sorulari_getir,
    dla_soru_ve_etiket_ekle,
    dla_soruya_ait_etiketleri_getir,
)
# ============================================================================================


# BAŞLIK
# ============================================================================================
st.header("D.L.A. Editörü 🤠")
 

# TAB PANEL OLUSTUR
# ============================================================================================
tab1, tab2, tab3, tab4 = st.tabs(["🏷️ Yeni Etiket", "🔖 Mevcut Etiketler", "❓ Yeni Soru", "📖 Mevcut Sorular"])    
    

# TEKRAR EDEN FONKSIYONLAR
# ============================================================================================
def VeriTabaniEtiketler_doldur():

    # Kayıtları Getir       
    # ===========================================           
    Kayitlar = dla_etiketler_getir()
    st.session_state.VT_Etiketler_df = pd.DataFrame(Kayitlar)

def VeriTabaniSorular_doldur():

    # Kayıtları Getir       
    # ===========================================           
    Kayitlar = dla_sorulari_getir()
    st.session_state.VT_Sorular_df = pd.DataFrame(Kayitlar)

# Session State Oluştur
# ============================================================================================  
ssElamanlar = {
        "VT_Etiketler_df": pd.DataFrame,
        "VT_Sorular_df": pd.DataFrame,
        "VT_ana_kategoriler_list": list,

        # TAB1 : YENI ETIKETLER
        "YE_YeniEtiketler_list": list,

        # TAB 3 : YENİ SORU EKLEME
        "YS_etiketler_listesi": list,
        "YS_secilen_ana_Kategori": str,
        "YS_resim_yolu": str,
        "YS_soru_metni": str,
        "YS_notlar": str,

        # TAB 4 : MEVCUT SORULAR
        "MS_secilen_ana_kategori": str,
        "MS_secilen_etiketler": list,
        # "MS_secilen_alt_kategori": str,
        # "MS_soru_metni": str,
        # "MS_resim_yolu": str,
        # "MS_notlar": str,
        # "MS_Etiketler": list,
        # "MS_son_ana_kategori": str,
        # "MS_son_alt_kategori": str,
        "MS_soru_listelensin_mi": bool

    }

session_olustur(ssElamanlar)

# VT_ana_kategoriler_list = ["General","Scenario","PictureDescription"]
VT_ana_kategoriler_list = dla_ana_kategori_listesi()


with tab1:
         
    # TAB1.BAŞLIK BELİRLE
    # ============================================================================================
    st.subheader(f"Yeni Etiket Ekle 🏷️",divider="green")

    # ETİKET EKLEME FORMU OLUSTUR
    # ============================================================================================
    with st.form("Etiket_ekleme_formu", clear_on_submit=True):
        
        
        # KOLONLARI OLUSTUR
        # ===========================================
        col1, col2 = st.columns([5, 1])

        with col1:
            


            # # SADECE ETIKET LISTESI OLUSTUR
            # # ===========================================      
            # sadece_etiket_listesi:list = []       
            # if not vt_etiketler.empty:
            #     sadece_etiket_listesi = vt_etiketler["Etiket"].dropna().unique().tolist()


            # YENI ETIKET ICIN *** MULTISELECT *** OLUSTUR
            # ===========================================
            with st.container(border=True,vertical_alignment="center",height="stretch"):
                st.session_state.YE_YeniEtiketler_list = st.multiselect(
                    "Etiket Adı",
                    options=[],
                    max_selections=20,
                    accept_new_options=True,
                    placeholder="Henüz etiket yok...",
                    key="YEK_etiket_input"
                    )
        
        with col2:
            
            # YENI ETIKET ICIN *** KAYDET BUTTON *** OLUSTUR
            # ===========================================
            with st.container(border=True,vertical_alignment="center",height="stretch"):
                kaydet = st.form_submit_button("Kaydet")


        # KAYDET BUTONA BASILIRSA
        # ===========================================
        if kaydet:

            Islenecek_Etiketler = st.session_state.YE_YeniEtiketler_list.copy()

            # etiketler boş bırakılamaz
            if not Islenecek_Etiketler:
                st.warning("Etiket / Etiketler boş bırakılamaz.")
                st.stop()

            # ETİKETLERİ GETİR VE SESSION ATAMASI
            # ============================================================================================      

            # 1. Mevcut etiketleri bir kez çek ve hız için bir "set" (küme) yapısına dönüştür
            VeriTabaniEtiketler_doldur() 
            mevcut_etiketler_seti = set(st.session_state.VT_Etiketler_df["Etiket"].dropna().unique())

            # 2. İşlenecek etiketleri benzersiz hale getir (liste içinde aynı isim varsa elenir)
            benzersiz_yeni_etiketler = set(tr_to_en_lower(e) for e in Islenecek_Etiketler)

            # info
            yeni_etiket_sayisi = 0
            ayni_etiket_sayisi = 0

            for etiket in benzersiz_yeni_etiketler:
                # 3. Sadece veritabanında gerçekten yoksa ekle
                if etiket not in mevcut_etiketler_seti:
                    dla_etiket_ekle(etiket)
                    # 4. (Opsiyonel) Eklenen etiketi sete ekle ki aynı döngüde tekrar kontrol edilmesin
                    mevcut_etiketler_seti.add(etiket)
                    yeni_etiket_sayisi += 1
                else:
                    ayni_etiket_sayisi += 1


            # mesaj
            if yeni_etiket_sayisi > 0: st.success(f"Eklenen etiketler: {yeni_etiket_sayisi}", icon="✅")
            if ayni_etiket_sayisi > 0: st.error(f"Eklenmeyen!!! sistemdeki etiketler: {ayni_etiket_sayisi}", icon="🚨")

            # Formu temizle
            session_resetle("YE_", ssElamanlar)
        
                


with tab2: 
    

    # TAB2.BAŞLIK BELİRLE
    # ============================================================================================
    st.subheader(f"Mevcut Etiketler 🔖",divider="rainbow")
    
    
    # Kayıtları Getir       
    # =========================================== 
    VeriTabaniEtiketler_doldur() 
    vt_etiketler = st.session_state.VT_Etiketler_df.copy()
    
    
    # DIŞ CONTAINER OLUSTUR
    # ============================================================================================
    with st.container(border=True,vertical_alignment="center",height="stretch"):
        
        #EĞER KAYIT YOKSA BILGI VER
        if vt_etiketler.empty:
            st.info("Herhangi bir etiket bulunamadı.")
        else:

            st.write(len(vt_etiketler), "tane etiket bulundu." )
    
            # Kolonları olustur
            # ============================================================================================
            col1,col2 = st.columns([1,1])
            
            with col1:
                
                # COL1 CONTAINER OLUSTUR
                # ============================================================================================
                with st.container(border=True,vertical_alignment="center",height="stretch"):    
               


                    # Arama alanı
                    # ============================================================================================
                    search_text = st.text_input("🔍 Etiket Ara", placeholder="Etiket gir...")
                    search_text = tr_to_en_lower(search_text.strip())
                    
                    filtered_df = vt_etiketler.copy()

                    if search_text:
                        filtered_df = filtered_df[
                            filtered_df["Etiket"].str.contains(search_text, case=False, na=False)
                        ]



                    # ETİKET ALANI
                    # ============================================================================================

                    # Seçim kolonu ekle
                    if "sec" not in vt_etiketler.columns:
                        filtered_df.insert(0, "sec", False)


                    edited_df = st.data_editor(
                        filtered_df,
                        use_container_width=False,
                        hide_index=True,
                        row_height=42,
                        height=300,
                        
                        column_config={
                            
                            "sec": st.column_config.CheckboxColumn("SEC", width=100),
                            "id": None,  # 👈 BU SATIR KOLONU GİZLER
                            "Etiket": st.column_config.TextColumn("ETİKET", width=1000),
                            
                        },
                        
                        key="MEK_etiket_editor"
                    )



                    # Excel olarak indirme butonu
                    #============================================================================================

                    export_df = edited_df.drop(columns=["Sec"], errors="ignore")
                    
                    excel_buffer = BytesIO()

                    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                        export_df.to_excel(writer, index=False, sheet_name="DlaKategoriler")

                    st.download_button(
                        label="📥 Excel Olarak İndir",
                        data=excel_buffer.getvalue(),
                        file_name="DlaEtiketler.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )


            with col2:
        
                #seçili satırları al
                secili_satirlar = edited_df[edited_df["sec"] == True] 
                
                
                updated_tag = ""

                # COL2 CONTAINER OLUSTUR
                # ============================================================================================
                with st.container(border=True,vertical_alignment="center",height="stretch"):    
                                       
                    # SINAMA 1
                    # ============================================================================================
                    if len(secili_satirlar) > 1:
                        st.warning("Lütfen sadece bir satır seç.", icon="⚠️")
                    
                    # SINAMA 2
                    # ============================================================================================    
                    elif len(secili_satirlar) < 1:
                        st.info("İşlem yapmak için tablodan bir satır seç.", icon="ℹ️")
                    
                    # İŞLEM
                    # ============================================================================================
                    else:
                        
                        # Tanımalamaları yap
                        #============================================================================================
                        selected_row = secili_satirlar.iloc[0]
                        selected_id = int(selected_row["id"])
                        selected_tag = tr_to_en_lower(selected_row["Etiket"])

                        #Seçilen ID ve Etiketi yazdır
                        st.info(f"Seçili ID: {selected_id}", icon="ℹ️")
                        
                        updated_tag = st.text_input(
                            "Seçili Etiket",
                            value=selected_tag,
                            disabled=False,
                            width="stretch"
                        )
                        
                        col1, col2 = st.columns(2)
                                
                        with col1:
                            
                            
                            #  GUNCELLE BUTONU
                            if st.button("💾 Seçili Etiketi Güncelle", use_container_width=True):
                                dla_etiket_guncelle(
                                    selected_id,
                                    tr_to_en_lower(updated_tag),
                                )
                                
                                st.success("Etiket güncellendi.", icon="✅")
                                
                                # RESET
                                session_resetle("ME_", ssElamanlar)

                        with col2:

                            #  SIL BUTONU
                            if st.button("🗑️ Seçili Satırı Sil", use_container_width=True):
                                dla_etiket_sil(selected_id)

                                #Dla Soru Etiket listesinden de sil
                                dla_soruetiket_etikete_gore_sil(selected_id)
                                st.warning("Etiket silindi.", icon="⚠️")
                                
                                # RESET
                                session_resetle("ME_", ssElamanlar)
                     



with tab3:
    

    # TAB3.BAŞLIK BELİRLE
    # ============================================================================================
    st.subheader(f"Yeni Soru Ekle ❓",divider="yellow")


    # COL1 CONTAINER OLUSTUR
    # ============================================================================================
    with st.container(border=True, vertical_alignment="center", height="stretch"):
            
        
        # Ana kategori seçimi
        # ============================================================================================  
        with st.container(border=True, vertical_alignment="center", height="stretch"):
            
            AK = st.radio(
                "Ana Kategori",
                VT_ana_kategoriler_list,
                key="YSK_ana_kategori",
                horizontal=True
            )

            #Önerme Yaz
            if AK == "PictureDescription":
                st.write("Gereklilikler: En az 1 Etiket, Sadece 1 Soru metni ve 1 Resim yolu.")
            else:
                st.write("Gereklilikler: En az 1 Etiket, Soru metni.")

            st.session_state.YS_secilen_ana_Kategori = AK


        # Etiketler girişi
        # ============================================================================================
             
        # Kayıtları Getir       
        # =========================================== 
        # 1. Mevcut etiketleri bir kez çek ve hız için bir "set" (küme) yapısına dönüştür
        VeriTabaniEtiketler_doldur() 
        mevcut_etiketler_seti = set(st.session_state.VT_Etiketler_df["Etiket"].dropna().unique())

        # 2. Etiketler seçme
        with st.container(border=True, vertical_alignment="center", height="stretch"):
            
            tags = st.multiselect(
                "Etiketlerinizi seçin",
                options=mevcut_etiketler_seti,
                max_selections=20,
                accept_new_options=True,
                placeholder="Etiketlerinizi seçin !!!",
                key="YSK_etiketler0",
                )
                    
            st.session_state.YS_etiketler_listesi = tags
            
            # Etiketleri yazdır
            st.write(tr_to_en_lower(", ".join(st.session_state.YS_etiketler_listesi)))



        # RESİM YOLU GİRİŞİ
        # ============================================================================================
        if st.session_state.YS_secilen_ana_Kategori == "PictureDescription":
            
            with st.container(border=True, vertical_alignment="center", height="stretch"):
                
                st.session_state.YS_resim_yolu = st.text_input(
                "Resim Yolu",
                placeholder="Örnek: /images/question1.png",
                key="YSK_resim_yolu",
                )

        else:
            
            st.session_state.YS_resim_yolu = "" 


        # Soru metni ve notlar için geniş bir alan
        # ============================================================================================

        with st.container(border=True, vertical_alignment="center", height="stretch"):
            
            st.session_state.YS_soru_metni = st.text_area(
                "Soru Metni",
                placeholder="Her satıra ayrı bir soru yazın.",
                height=100,
                key="YSK_soru_metni",
                )
            
            
        # Notlar alanı
        # ============================================================================================

        with st.container(border=True, vertical_alignment="center", height="stretch"):
            
            st.session_state.YS_notlar = st.text_area(
                "Notlar (Opsiyonel)",
                placeholder="Örnek: Bu soru tercihleri ölçmek için kullanılır.",
                key="YSK_notlar",
                )


        # Kaydet butonu ve doğrulama
        # ============================================================================================
        # ============================================================================================
        # ============================================================================================
        # ============================================================================================
        # ============================================================================================
        if st.button("Kaydet", key="YSK_kaydet_buton"):

            # Etiketler yoksa
            if not st.session_state.YS_etiketler_listesi:
                st.warning(f"{st.session_state.YS_secilen_ana_Kategori} kategorisinde en az bir etiket seçmelisiniz.", icon="⚠️")
                st.stop()

            # Soru metni yoksa
            if not st.session_state.YS_soru_metni:
                st.warning(f"{st.session_state.YS_secilen_ana_Kategori} kategorisinde soru metni yazmalısınız.", icon="⚠️")
                st.stop()

            # Resim yolu boşsa
            if st.session_state.YS_secilen_ana_Kategori == "PictureDescription" and not st.session_state.YS_resim_yolu.split(): 
                st.warning(f"{st.session_state.YS_secilen_ana_Kategori} kategorisinde resim yolu boş bırakılamaz.", icon="⚠️") 
                st.stop()

            # Resim Soru Metni 
            if st.session_state.YS_secilen_ana_Kategori == "PictureDescription" and len(st.session_state.YS_soru_metni.splitlines()) != 1:          
                st.warning(f"{st.session_state.YS_secilen_ana_Kategori} kategorisinde bir tane soru metni olmalıdır.") 
                st.stop()
            

            # Soru Ekle
            # ============================================================================================
            # ============================================================================================
            # ============================================================================================
            # 1. Mevcut soruları bir kez çek ve hız için bir "set" (küme) yapısına dönüştür
            VeriTabaniSorular_doldur() 
            mevcut_sorular_seti = set(st.session_state.VT_Sorular_df["Soru"].dropna().unique())
            df_sorular = st.session_state.VT_Sorular_df


            #Yeni Soruların Idleri
            # ===========================================
            Eklenen_secilen_soru_id_listesi: list = []


            # Yeni Soruların Metnleri
            # ===========================================
            for soru in st.session_state.YS_soru_metni.splitlines():

                # Soruyu formatla
                soru = ilk_harf_buyuk(tr_to_en_lower(soru.strip()))


                # Soru boşsa
                if soru == "": continue

                if soru not in mevcut_sorular_seti:

                    yeni_soru = dla_soru_ekle(
                        st.session_state.YS_secilen_ana_Kategori,
                        soru,
                        st.session_state.YS_notlar,
                        st.session_state.YS_resim_yolu
                    )
                    
                    if yeni_soru.data:
                        
                        # Yeni ID al

                        for row in yeni_soru.data:
                            Eklenen_secilen_soru_id_listesi.append(row["id"])

                        mevcut_sorular_seti.add(soru)
                    
                    else:
                    
                        st.error(yeni_soru.error)

                else:

                    Eklenen_secilen_soru_id_listesi.append(df_sorular[df_sorular["Soru"] == soru]["id"].iloc[0]) 



            st.success(f"{len(Eklenen_secilen_soru_id_listesi)} soru işlendi.", icon="✅")
            st.write("Soru ID Listesi: " + ", ".join(map(str, Eklenen_secilen_soru_id_listesi)))


            # Etiket Ekle
            # ============================================================================================
            # ============================================================================================
            # ============================================================================================
            # 1. Mevcut soruları bir kez çek ve hız için bir "set" (küme) yapısına dönüştür
            VeriTabaniEtiketler_doldur() 
            mevcut_etiketler_seti = set(st.session_state.VT_Etiketler_df["Etiket"].dropna().unique())
            df_etiketler = st.session_state.VT_Etiketler_df


            #Yeni Etikertlerin Idleri
            # ===========================================
            Eklenen_secilen_etiket_id_listesi: list = []


            # Yeni Etiketler
            # ===========================================
            for etiket in st.session_state.YS_etiketler_listesi:

                # Etiketi formatla
                etiket = tr_to_en_lower(etiket)

                # Etiket boşsa
                if etiket == "": continue

                if etiket not in mevcut_etiketler_seti:

                    yeni_etiket = dla_etiket_ekle(etiket)

                    if yeni_etiket.data:

                        # Yeni ID al
                        for row in yeni_etiket.data:
                            Eklenen_secilen_etiket_id_listesi.append(row["id"])

                        mevcut_etiketler_seti.add(etiket)

                    else:

                        st.error("Soru eklenirken bir hata oluştu veya ID dönmedi.")

                else:

                    Eklenen_secilen_etiket_id_listesi.append(df_etiketler[df_etiketler["Etiket"] == etiket]["id"].iloc[0])  


            st.success(f"{len(Eklenen_secilen_etiket_id_listesi)} etiket işlendi.", icon="✅")
            st.write("Etiket ID Listesi: " + ", ".join(map(str, Eklenen_secilen_etiket_id_listesi)))




            # Sorular ile Etiketleri Ekle
            # ============================================================================================
            # ============================================================================================
            # ============================================================================================

            for soruID in Eklenen_secilen_soru_id_listesi:
                
                if soruID in [None, ""]:
                    continue

                for etiketID in Eklenen_secilen_etiket_id_listesi:
                    
                    if etiketID in [None, ""]:
                        continue
                
                    dla_soru_ve_etiket_ekle(soruID, etiketID)


            st.success(f"{len(Eklenen_secilen_etiket_id_listesi)} etiket ile {len(Eklenen_secilen_soru_id_listesi)} soru işlendi.", icon="✅")

            # Formu temizle
            session_resetle("YS_", ssElamanlar)




with tab4:
    
    # TAB4.BAŞLIK BELİRLE
    # ============================================================================================
    st.subheader(f"Mevcut Sorular 📖",divider="red")

    
    # Kategori seçim alanları için kolon düzeni
    # ============================================================================================
    col1, col2 , col3 = st.columns([1, 1, 1])
    

    # Ana kategori seçimi
    # ============================================================================================
    with col1: 

        with st.container(border=True, vertical_alignment="center", height="stretch"):
            st.session_state.MS_secilen_ana_kategori = st.radio(
                "Ana Kategori",
                ["All"] + VT_ana_kategoriler_list,
                key="MSK_ana_kategori_radio",
            )


        if not st.session_state.MS_secilen_ana_kategori:
            st.session_state.MS_secilen_ana_kategori = "All"


    # Etiket seçimi
    # ============================================================================================
    with col2:
        VeriTabaniEtiketler_doldur()

        with st.container(border=True, vertical_alignment="center", height="stretch"):
            st.session_state.MS_secilen_etiketler = st.multiselect(
                "Etiket",
                st.session_state.VT_Etiketler_df["Etiket"].dropna().unique().tolist(),
                max_selections=5,
                accept_new_options=False,
                key="MSK_etiket_radio",
            )

        if st.session_state.MS_secilen_etiketler == []:
            st.session_state.MS_secilen_etiketler.append("All")



    #Soruları Getir
    # ============================================================================================

    with col3:
        with st.container(border=True, vertical_alignment="center", height="stretch"):
            # Butona basıldığında state'i True yap
            if st.button("Soruları Getir", key="MSK_soru_getir_btn"):
                st.session_state.MS_soru_listelensin_mi = True

    bilgi_kutusu = st.empty()


    def sorulari_getir(sonuc_alani):
        
        VeriTabaniSorular_doldur()
        Vt_Sorular_df = st.session_state.VT_Sorular_df.copy()

        kategori = st.session_state.MS_secilen_ana_kategori
        etiketler = st.session_state.MS_secilen_etiketler # Liste formatında olduğunu varsayıyoruz

        # 1. Aşama: Kategori Filtrelemesi (Hızlıca ana tabloyu daraltalım)
        if kategori:
            Gosterilecek_sorular = Vt_Sorular_df[Vt_Sorular_df["AnaKategori"] == kategori].copy()
        else:
            Gosterilecek_sorular = Vt_Sorular_df.copy()

        # 2. Aşama: Etiket Filtrelemesi
        def etiket_kontrol(soru_id):
            # Veritabanından o soruya ait etiketleri çek
            response = dla_soruya_ait_etiketleri_getir(soru_id)
            soru_etiket_listesi = [str(item["Etiket_ID"]) for item in response.data]
            
            # Seçilen tüm etiketler, sorunun etiket listesinde var mı? (Hepsi olmalı derseniz 'all')
            # Eğer "herhangi biri olsa yeter" derseniz 'any' kullanabilirsiniz.
            return all(etiket in soru_etiket_listesi for etiket in etiketler)

        if etiketler:
            # 'apply' metodunu kullanarak her satır için fonksiyonu çalıştırıyoruz
            maske = Gosterilecek_sorular["id"].apply(etiket_kontrol)
            Gosterilecek_sorular = Gosterilecek_sorular[maske]
 



        # Gosterilecek kolonları belirle
        #============================================================================================
        if st.session_state.MS_secilen_ana_kategori == "All":
            gosterilecek_kolonlar = ["id", "AnaKategori", "Soru", "Notlar", "ResimURL"]

        if st.session_state.MS_secilen_ana_kategori == "General":
            gosterilecek_kolonlar = ["id", "Soru"]

        if st.session_state.MS_secilen_ana_kategori == "Scenario":
            gosterilecek_kolonlar = ["id", "Soru"]

        if st.session_state.MS_secilen_ana_kategori == "PictureDescription":
            gosterilecek_kolonlar = ["id", "ResimURL"]


        with sonuc_alani.container(border=True, vertical_alignment="center", height="stretch"):
    
            event = st.dataframe(
                Gosterilecek_sorular[gosterilecek_kolonlar],
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row",
                column_config={
                    "id": st.column_config.NumberColumn("ID", width=20),
                    }
                )


            secili_id = 0
            if event.selection.rows:
                secili_index = event.selection.rows[0]
                secili_satir = Vt_Sorular_df.iloc[secili_index]
                secili_id = secili_satir["id"]

            st.write(f"Seçilen ID: {secili_id}")






    if st.session_state.MS_soru_listelensin_mi:
        sorulari_getir(bilgi_kutusu)
            






