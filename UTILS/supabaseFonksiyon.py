import streamlit as st
import pandas as pd
import glob

from supabase import create_client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# DLA ETİKETLERİ İÇİN FONKSİYONLAR
#============================================================================================
def dla_etiketler_DF():
    response = (
        supabase
        .table("Dla_Etiketler")
        .select("id, Etiket")
        .order("id")
        .execute()
    )
 
    # response.data bir liste döndürür. Eğer liste doluysa DF yap, boşsa kolonları hazırla.
    if response.data:
        return pd.DataFrame(response.data)
    else:
        return pd.DataFrame(columns=["id", "Etiket"])
    
def dla_Resimler_için_soru_olustur():
    
    png_sayisi = len(glob.glob('images/*.jpg')) + len(glob.glob('images/*.png'))
    for i in range(1, png_sayisi + 1):
        resim_yolu = f"/images/question{i}.png"
        supabase.table("Dla_Sorular").insert({
            "AnaKategori": "PictureDescription",
            "Soru": "Resimde ne görüyorsunuz? Resmi detaylı bir şekilde tanımlayın.",
            "Notlar": "",
            "ResimURL": resim_yolu,
            "Etiketler" : ""
        }).execute()













# def dla_etiket_guncelle(row_id, Etiket):
#     return (
#         supabase
#         .table("Dla_Etiketler")
#         .update({
#             "Etiket": Etiket
#         })
#         .eq("id", row_id)
#         .execute()
#     )








# def dla_etiket_ekle(Etiket):
#     try:
#         result = supabase.table("Dla_Etiketler").insert({
#             "Etiket": Etiket
#         }).execute()

#         return result

#     except Exception as e:
#         return str(e)



# def dla_etiket_sil(row_id):
#     return (
#         supabase
#         .table("Dla_Etiketler")
#         .delete()
#         .eq("id", row_id)
#         .execute()
#     )

# def dla_soruetiket_etikete_gore_sil(etiketid):
#     return (
#         supabase
#         .table("DlaSoru_Etiket")
#         .delete()
#         .eq("Etiket_ID", etiketid)
#         .execute()
#     )



# # DLA SORULAR İÇİN FONKSİYONLAR
# #============================================================================================

# def dla_soru_ekle(ana_kategori, soru_metni, notlar, resim_yolu):
#     return (
#         supabase
#         .table("Dla_Sorular")
#         .insert({
#             "AnaKategori": ana_kategori,
#             "Soru": soru_metni,
#             "Notlar": notlar,
#             "ResimURL": resim_yolu
#         })
#         .execute()
#     )

# def dla_sorulari_getir(ana_kategori=None):

#     # Soruguyu başlat
#     query = supabase.table("Dla_Sorular").select("id, AnaKategori, Soru, ResimURL, Notlar")

#     # 2. Filtreleme (Eğer kategori "All" değilse ve boş değilse filtre ekle)
#     if ana_kategori and ana_kategori != "All":
#         query = query.eq("AnaKategori", ana_kategori)

#     # 3. Sıralama ve Çalıştırma
#     response = query.order("id").execute()

#     # 4. DataFrame Dönüşümü
#     if response.data:
#         return pd.DataFrame(response.data)
#     else:
#         # Kolon listesini virgülle ayrılmış tek string değil, liste olarak veriyoruz
#         return pd.DataFrame(columns=["id", "AnaKategori", "Soru", "ResimURL", "Notlar"])

# def dla_soru_ve_etiket_ekle(soru_id, etiket_id):
#     try:
#         result = supabase.table("DlaSoru_Etiket").insert({
#             "Soru_ID": soru_id,
#             "Etiket_ID": etiket_id,
#         }).execute()

#         return result

#     except Exception as e:
#         return str(e)

# def dla_soruya_ait_etiketleri_getir(soru_id):
#     return (
#         supabase
#         .table("DlaSoru_Etiket")
#         .select("Etiket_ID")
#         .eq("Soru_ID", soru_id)
#         .execute()
#     )





# # def dla_soru_guncelle(row_id, category, subcategory, question, notes, pic_path):
# #     return (
# #         supabase
# #         .table("DlaSorular")
# #         .update({
# #             "AnaKategori": category,
# #             "AltKategori": subcategory,
# #             "Soru": question,
# #             "ResimURL": pic_path,
# #             "Notlar": notes
# #         })
# #         .eq("id", row_id)
# #         .execute()
# #     )

# # def dla_soru_sil(row_id):
# #     return (
# #         supabase
# #         .table("DlaSorular")
# #         .delete()
# #         .eq("id", row_id)
# #         .execute()
# #     )






















    
            



# # DLA ALT KATEGORİLERİLER İÇİN FONKSİYONLAR
# #============================================================================================

# def dla_kategorileri_getir():
#     #return supabase.table("DlaSinavKategori").select("*").order("id").execute()
#     return (
#     supabase
#     .table("DlaKategoriler")
#     .select("id,AnaKategori,AltKategori")
#     .order("id")
#     .execute()
#     )

# def dla_secili_kategorileri_getir(ana_kategori=None):

#     query = (
#         supabase
#         .table("DlaKategoriler")
#         .select("id,AnaKategori,AltKategori")
#     )

#     if ana_kategori and ana_kategori != "All":
#         query = query.eq("AnaKategori", ana_kategori)

#     return (
#         query
#         .order("id")
#         .execute()
#     )            

# def dla_alt_kategorileri_getir(selected_category):
#     rows = dla_kategorileri_getir()

#     alt_kategoriler = []

#     for kategori in rows.data:
#         ana_kategori = kategori["AnaKategori"]
#         alt_kategori = kategori["AltKategori"]

#         if selected_category and ana_kategori != selected_category:
#             continue

#         # tekrar edenleri engelle
#         if alt_kategori not in alt_kategoriler:
#             alt_kategoriler.append(alt_kategori)

#     return alt_kategoriler

# def dla_alt_kategori_ekle(category, subcategory):
#     try:
#         result = supabase.table("DlaKategoriler").insert({
#             "AnaKategori": category,
#             "AltKategori": subcategory
#         }).execute()

#         return result

#     except Exception as e:
#         return str(e)

# def dla_alt_kategori_guncelle(row_id, category, subcategory):
#     return (
#         supabase
#         .table("DlaKategoriler")
#         .update({
#             "AnaKategori": category,
#             "AltKategori": subcategory
#         })
#         .eq("id", row_id)
#         .execute()
#     )

# def dla_alt_kategori_sil(row_id):
#     return (
#         supabase
#         .table("DlaKategoriler")
#         .delete()
#         .eq("id", row_id)
#         .execute()
#     )

# # DLA SORULAR İÇİN FONKSİYONLAR
# #============================================================================================







