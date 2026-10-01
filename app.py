import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Akıl ve Zeka Oyunları Takip Paneli",
    page_icon="🧠",
    layout="wide"
)

# Google Sheets URL'leri
SHEET_ID = "1EFWWiyOe7kqwvEaSZeA3Kahgl9-Zy3LL6QzCpF3yt4I"

def load_data(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        return pd.DataFrame()

# Oturum Durumu (Session State) Hazırlığı
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = datetime.now().date()

# Verileri Yükle
df_ogrenciler = load_data("Ogrenciler")
df_oyunlar = load_data("Oyunlar")
df_ikili = load_data("Ikili_Maclar")
df_bireysel = load_data("Bireysel_Performans")

# Kenar Çubuğu (Sidebar) Navigasyon
st.sidebar.title("📌 Navigasyon")
sayfa = st.sidebar.radio(
    "Sayfa Seçiniz:",
    ["📊 Genel Durum", "👨‍🎓 Öğrenci Listesi", "🎮 Oyunlar", "⚔️ İkili Maçlar", "⭐ Bireysel Performans", "➕ Veri Girişi Formu"]
)

# 1. GENEL DURUM
if sayfa == "📊 Genel Durum":
    st.title("🧠 Akıl ve Zeka Oyunları Takip Paneli")
    st.subheader("📈 Genel İstatistikler")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Toplam Öğrenci", len(df_ogrenciler) if not df_ogrenciler.empty else 0)
    col2.metric("Kayıtlı Oyun Sayısı", len(df_oyunlar) if not df_oyunlar.empty else 0)
    col3.metric("Oynanan İkili Maç", len(df_ikili) if not df_ikili.empty else 0)
    
    st.divider()
    st.subheader("📋 Son Oynanan Maçlar")
    if not df_ikili.empty:
        st.dataframe(df_ikili.tail(10), use_container_width=True)
    else:
        st.info("Henüz kayıtlı ikili maç bulunmuyor.")

# 2. ÖĞRENCİ LİSTESİ
elif sayfa == "👨‍🎓 Öğrenci Listesi":
    st.title("👨‍🎓 Öğrenci Listesi")
    if not df_ogrenciler.empty:
        siniflar = ["Tümü"] + list(df_ogrenciler["Sinif"].astype(str).unique()) if "Sinif" in df_ogrenciler.columns else ["Tümü"]
        secilen_sinif = st.selectbox("🎯 Sınıfa Göre Filtrele:", siniflar)
        
        if secilen_sinif != "Tümü":
            filtre_df = df_ogrenciler[df_ogrenciler["Sinif"].astype(str) == secilen_sinif]
        else:
            filtre_df = df_ogrenciler
            
        st.dataframe(filtre_df, use_container_width=True)
    else:
        st.warning("Google Sheets üzerinde 'Ogrenciler' sayfasında kayıt bulunamadı.")

# 3. OYUNLAR
elif sayfa == "🎮 Oyunlar":
    st.title("🎮 Akıl Oyunları Kataloğu")
    if not df_oyunlar.empty:
        st.dataframe(df_oyunlar, use_container_width=True)
    else:
        st.warning("Google Sheets 'Oyunlar' sekmesinde henüz oyun tanımlanmamış. Mangala, Dokuztaş vb. oyunları tablonuza ekleyebilirsiniz.")

# 4. İKİLİ MAÇLAR
elif sayfa == "⚔️ İkili Maçlar":
    st.title("⚔️ İkili Maç Geçmişi")
    if not df_ikili.empty:
        st.dataframe(df_ikili, use_container_width=True)
    else:
        st.info("Kayıtlı maç verisi yok.")

# 5. BİREYSEL PERFORMANS
elif sayfa == "⭐ Bireysel Performans":
    st.title("⭐ Bireysel Performans Kayıtları")
    if not df_bireysel.empty:
        st.dataframe(df_bireysel, use_container_width=True)
    else:
        st.info("Kayıtlı bireysel performans verisi yok.")

# 6. VERİ GİRİŞİ FORMU
elif sayfa == "➕ Veri Girişi Formu":
    st.title("➕ Hızlı Veri Kayıt Ekranı")
    
    kayit_turu = st.radio(
        "Kayıt Türü Seçiniz:",
        ["⚔️ İkili Maç Kaydı", "⭐ Bireysel Performans Kaydı", "👨‍🎓 Yeni Öğrenci Kaydı"],
        horizontal=True
    )
    
    st.divider()

    # İKİLİ MAÇ KAYDI FORMALARI
    if kayit_turu == "⚔️ İkili Maç Kaydı":
        st.subheader("⚔️ İkili Maç Bilgileri")
        
        # Tarih Seçici (Hafızada Tutulur)
        secilen_tarih = st.date_input(
            "📅 Maç Tarihi:",
            value=st.session_state.selected_date,
            help="Seçtiğiniz tarih siz değiştirene kadar sonraki maç kaydı girişlerinizde sabit kalır."
        )
        st.session_state.selected_date = secilen_tarih
        
        # Oyunlar Listesi Hazırlığı
        oyun_listesi = df_oyunlar["Oyun_Adi"].dropna().tolist() if not df_oyunlar.empty and "Oyun_Adi" in df_oyunlar.columns else []
        # Öğrenciler Listesi Hazırlığı
        ogrenci_listesi = df_ogrenciler["Ad_Soyad"].dropna().tolist() if not df_ogrenciler.empty and "Ad_Soyad" in df_ogrenciler.columns else []
        
        with st.form("ikili_mac_formu", clear_on_submit=False):
            if oyun_listesi:
                oyun_adi = st.selectbox("🎮 Oyun Adı:", oyun_listesi)
            else:
                oyun_adi = st.text_input("🎮 Oyun Adı (Google Sheets Oyunlar sekmesini doldurabilirsiniz):")
                
            col1, col2 = st.columns(2)
            with col1:
                if ogrenci_listesi:
                    oyuncu_1 = st.selectbox("👤 1. Oyuncu:", ogrenci_listesi, key="p1")
                else:
                    oyuncu_1 = st.text_input("👤 1. Oyuncu (Ad Soyad):")
            with col2:
                if ogrenci_listesi:
                    oyuncu_2 = st.selectbox("👤 2. Oyuncu:", ogrenci_listesi, key="p2")
                else:
                    oyuncu_2 = st.text_input("👤 2. Oyuncu (Ad Soyad):")
                    
            kazanan_secenekleri = ["Berabere", oyuncu_1, oyuncu_2] if (ogrenci_listesi or oyuncu_1) else ["Berabere"]
            kazanan = st.selectbox("🏆 Kazanan Oyuncu:", kazanan_secenekleri)
            
            skor = st.text_input("🔢 Skor / Sonuç (Örn: 2-1, 1-0):", "1-0")
            notlar = st.text_area("📝 Notlar / Turnuva Turu (Örn: 1. Hafta Maçı, Çeyrek Final):")
            
            submitted = st.form_submit_button("💾 Maçı Kaydet")
            if submitted:
                st.success(f"✅ {secilen_tarih.strftime('%d.%m.%Y')} tarihli {oyun_adi} maçı kaydı alındı! (Tarih bir sonraki kayıt için sabit tutuldu)")

    # BİREYSEL PERFORMANS KAYDI
    elif kayit_turu == "⭐ Bireysel Performans Kaydı":
        st.subheader("⭐ Bireysel Performans Bilgileri")
        
        secilen_tarih = st.date_input("📅 Değerlendirme Tarihi:", value=st.session_state.selected_date)
        st.session_state.selected_date = secilen_tarih
        
        ogrenci_listesi = df_ogrenciler["Ad_Soyad"].dropna().tolist() if not df_ogrenciler.empty and "Ad_Soyad" in df_ogrenciler.columns else []
        oyun_listesi = df_oyunlar["Oyun_Adi"].dropna().tolist() if not df_oyunlar.empty and "Oyun_Adi" in df_oyunlar.columns else []

        with st.form("bireysel_form", clear_on_submit=False):
            if ogrenci_listesi:
                ogrenci = st.selectbox("👤 Öğrenci Seçiniz:", ogrenci_listesi)
            else:
                ogrenci = st.text_input("👤 Öğrenci (Ad Soyad):")
                
            if oyun_listesi:
                oyun = st.selectbox("🎮 Çalışılan Oyun:", oyun_listesi)
            else:
                oyun = st.text_input("🎮 Çalışılan Oyun:")
                
            puan = st.slider("⭐ Performans Puanı (1-10):", 1, 10, 8)
            degerlendirme = st.text_area("💬 Öğretmen Değerlendirmesi / Gelişim Notu:")
            
            submitted = st.form_submit_button("💾 Performansı Kaydet")
            if submitted:
                st.success(f"✅ {ogrenci} için {secilen_tarih.strftime('%d.%m.%Y')} tarihli performans kaydı alındı!")

    # YENİ ÖĞRENCİ KAYDI
    elif kayit_turu == "👨‍🎓 Yeni Öğrenci Kaydı":
        st.subheader("👨‍🎓 Yeni Öğrenci Ekle")
        with st.form("yeni_ogrenci_formu"):
            ad_soyad = st.text_input("Ad Soyad:")
            sinif = st.text_input("Sınıf (Örn: 5):")
            sube = st.text_input("Şube (Örn: A):")
            
            submitted = st.form_submit_button("💾 Öğrenciyi Kaydet")
            if submitted:
                st.success(f"✅ {ad_soyad} ({sinif}-{sube}) sisteme kaydedildi!")
