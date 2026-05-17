import time
import re
import streamlit as st



################################### 
# Metinleri yavaş yazdırma 
###################################    

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  

def slow_print(text: str, CharMode: bool = False, delay: float = 0.02):
    
    if CharMode == "char":
        generator = (char for char in text)
    else:
        generator = (word + " " for word in text.split())

    def stream():
        for item in generator:
            yield item
            time.sleep(delay)

    st.write_stream(stream())

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  

###################################
# Metinleri kısaltma
###################################

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  

def trim_text(text, max_length):
    if len(text) > max_length:
        st.write(text[:max_length])

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  

###################################
# Metinleri kısaltma ve ... ekleme.
###################################

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  

def trim_text_3points(text, max_length):
    if len(text) > max_length:
        st.write(text[:max_length] + "...")

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  


###################################
# Turkce metinleri ingilizce metine cevirme
###################################

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  

def tr_to_en_lower(text: str) -> str:
    if not text:
        return ""

    ceviri_tablosu = str.maketrans({
        "Ü": "u", "ü": "u",
        "Ğ": "g", "ğ": "g",
        "İ": "i", "ı": "i",
        "Ş": "s", "ş": "s",
        "Ç": "c", "ç": "c",
        "Ö": "o", "ö": "o",
    })

    text = text.translate(ceviri_tablosu)

    # boşlukları düzenle
    text = re.sub(r"\s+", "-", text.strip())

    return text.lower()

def ilk_harf_buyuk(text: str) -> str:
    if not text.split():
        return ""

    return text[0].upper() + text[1:]

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  
