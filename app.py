import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Akıl Oyunları Takip Sistemi",
    page_icon="🧠",
    layout="wide"
)

# Google Sheets Base URL
SHEET_ID = "1EFWWiyOe7kqwvEaSZeA3Kahgl9-Zy3LL6QzCpF3yt4I"

@st.cache_data(ttl=60)
def load_data(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Veri yüklenirken hata oluştu ({sheet_name}): {e}")
        return pd.DataFrame()

# Title
st.title("🧠 Akıl ve Zeka Oyunları Takip Paneli")
st.markdown("---")

# Sidebar Navigation
st.sidebar.header("📌 Navigasyon")
page = st.sidebar.radio("Sayfa Seçiniz:", ["📊 Genel Durum", "👨‍🎓 Öğrenci Listesi", "🎮 Oyunlar", "⚔️ İkili Maçlar", "⭐ Bireysel Performans"])

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
    st.info("💡 Sol menüyü kullanarak detaylı verilere ve kayıtlara ulaşabilirsiniz.")

elif page == "👨‍🎓 Öğrenci Listesi":
    st.subheader("👨‍🎓 Öğrenci Veritabanı")
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
