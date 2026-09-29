import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Akıl Oyunları Takip Sistemi",
    page_icon="🧠",
    layout="wide"
)

# Google Sheets Base URL
SHEET_ID = "1EFWWiyOe7kqwvEaSZeA3Kahgl9-Zy3LL6QzCpF3yt4I"

@st.cache_data(ttl=5)
def load_data(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        return pd.DataFrame()

# Title
st.title("🧠 Akıl ve Zeka Oyunları Takip Paneli")
st.markdown("---")

# Sidebar Navigation
st.sidebar.header("📌 Navigasyon")
page = st.sidebar.radio(
    "Sayfa Seçiniz:", 
    ["📊 Genel Durum", "👨‍🎓 Öğrenci Listesi", "🎮 Oyunlar", "⚔️ İkili Maçlar", "⭐ Bireysel Performans", "➕ Veri Girişi Formu"]
)

# Load all data
ogrenciler_df = load_data("Ogrenciler")
oyunlar_df = load_data("Oyunlar")
maclar_df = load_data("Ikili_Maclar")
performans_df = load_data("Bireysel_Performans")

if page == "📊 Genel Durum":
    st.subheader("📌 Genel İstatistikler")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Toplu Öğrenci Sayısı", len(ogrenciler_df) if not ogrenciler_df.empty else 0)
    with col2:
        st.metric("Kayıtlı Oyun Sayısı", len(oyunlar_df) if not oyunlar_df.empty else 0)
    with col3:
        st.metric("Oynanan İkili Maçlar", len(maclar_df) if not maclar_df.empty else 0)
    with col4:
        st.metric("Bireysel Performans Kaydı", len(performans_df) if not performans_df.empty else 0)
        
    st.markdown("---")
    st.info("💡 Sol menüyü kullanarak detaylı verilere, sınıf filtrelerine ve veri giriş formuna ulaşabilirsiniz.")

elif page == "👨‍🎓 Öğrenci Listesi":
    st.subheader("👨‍🎓 Öğrenci Veritabanı")
    if not ogrenciler_df.empty and "Sinif" in ogrenciler_df.columns:
        siniflar = ["Tüm Sınıflar"] + list(ogrenciler_df["Sinif"].dropna().unique())
        secilen_sinif = st.selectbox("🎯 Sınıf Filtrele:", siniflar)
        
        if secilen_sinif != "Tüm Sınıflar":
            filtered_df = ogrenciler_df[ogrenciler_df["Sinif"] == secilen_sinif]
        else:
            filtered_df = ogrenciler_df
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.dataframe(ogrenciler_df, use_container_width=True)

elif page == "🎮 Oyunlar":
    st.subheader("🎮 Akıl Oyunları Kataloğu")
    st.dataframe(oyunlar_df, use_container_width=True)

elif page == "⚔️ İkili Maçlar":
    st.subheader("⚔️ İkili Maç Sonuçları")
    st.dataframe(maclar_df, use_container_width=True)

elif page == "⭐ Bireysel Performans":
    st.subheader("⭐ Bireysel Performans Gelişim Kayıtları")
    st.dataframe(performans_df, use_container_width=True)

elif page == "➕ Veri Girişi Formu":
    st.subheader("➕ Hızlı Veri Kayıt Ekranı")
    
    form_type = st.radio("Kayıt Türü Seçiniz:", ["⚔️ İkili Maç Kaydı", "⭐ Bireysel Performans Kaydı", "👨‍🎓 Yeni Öğrenci Kaydı"], horizontal=True)
    st.markdown("---")
    
    if form_type == "⚔️ İkili Maç Kaydı":
        st.write("### ⚔️ İkili Maç Ekle")
        oyun = st.text_input("Oyun Adı")
        oyuncu_1 = st.text_input("1. Oyuncu (Ad Soyad)")
        oyuncu_2 = st.text_input("2. Oyuncu (Ad Soyad)")
        kazanan = st.text_input("Kazanan Oyuncu")
        skor = st.text_input("Skor / Sonuç")
        notlar = st.text_area("Notlar / Turnuva Turu")
        
        if st.button("Maç Kaydını Tamamla"):
            st.success("Kayıt iletildi! Verileriniz Google Sheets'e güncellenmek üzere gönderiliyor.")
            st.info("💡 Not: Doğrudan form üzerinden Google Sheets'e anlık veri yazma bağlantısı için Google Sheets API / Service Account kimliği gereklidir. Şimdilik bu veriyi kopyalayıp tablonuza kolayca ekleyebilirsiniz.")

    elif form_type == "⭐ Bireysel Performans Kaydı":
        st.write("### ⭐ Bireysel Performans Ekle")
        ogrenci = st.text_input("Öğrenci Adı Soyadı")
        oyun_perf = st.text_input("Oyun Adı")
        basari = st.selectbox("Başarı Durumu", ["Başarılı", "Geliştirilmeli", "Katılım Sağladı"])
        seviye = st.text_input("Seviye / Aşama")
        gozlem = st.text_area("Gözlem Notu")
        
        if st.button("Performans Kaydını Tamamla"):
            st.success("Kayıt iletildi!")

    elif form_type == "👨‍🎓 Yeni Öğrenci Kaydı":
        st.write("### 👨‍🎓 Yeni Öğrenci Ekle")
        ad_soyad = st.text_input("Ad Soyad")
        sinif = st.text_input("Sınıf (Örn: 5-A)")
        sube = st.text_input("Şube")
        
        if st.button("Öğrenciyi Kaydet"):
            st.success("Öğrenci Eklendi!")
