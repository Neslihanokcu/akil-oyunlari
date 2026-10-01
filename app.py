import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Akıl ve Zeka Oyunları Takip Paneli",
    page_icon="🧠",
    layout="wide"
)

# Google Sheets URL
SHEET_ID = "1EFWWiyOe7kqwvEaSZeA3Kahgl9-Zy3LL6QzCpF3yt4I"

def load_data(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        df = pd.read_csv(url)
        # Boş sütun başlıklarını veya isimsiz sütunları temizle
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
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

# 2. ÖĞRENCİ LİSTESİ (SINIF VE ŞUBE FİLTRELİ)
elif sayfa == "👨‍🎓 Öğrenci Listesi":
    st.title("👨‍🎓 Öğrenci Listesi ve Sınıf Kontrolü")
    
    if not df_ogrenciler.empty:
        # Sınıf ve Şube Sütunlarını Kontrol Et
        sinif_col = "Sinif" if "Sinif" in df_ogrenciler.columns else None
        sube_col = "Sube" if "Sube" in df_ogrenciler.columns else None
        
        col_f1, col_f2 = st.columns(2)
        
        filtered_df = df_ogrenciler.copy()
        
        # Sınıf Filtresi
        if sinif_col:
            # Boş olmayan sınıfları al
            siniflar = ["Tümü"] + sorted([str(x).split('.')[0] for x in df_ogrenciler[sinif_col].dropna().unique() if str(x) != 'nan'])
            secilen_sinif = col_f1.selectbox("🎯 Sınıf Seçiniz:", siniflar)
            
            if secilen_sinif != "Tümü":
                filtered_df = filtered_df[filtered_df[sinif_col].astype(str).str.startswith(secilen_sinif)]
        
        # Şube Filtresi
        if sube_col:
            subeler = ["Tümü"] + sorted([str(x) for x in filtered_df[sube_col].dropna().unique() if str(x) != 'nan'])
            secilen_sube = col_f2.selectbox("🏢 Şube Seçiniz:", subeler)
            
            if secilen_sube != "Tümü":
                filtered_df = filtered_df[filtered_df[sube_col].astype(str) == secilen_sube]
                
        st.info(f"🔍 Toplam **{len(filtered_df)}** öğrenci listeleniyor.")
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.warning("Google Sheets üzerinde 'Ogrenciler' sayfasında kayıt bulunamadı.")

# 3. OYUNLAR
elif sayfa == "🎮 Oyunlar":
    st.title("🎮 Akıl Oyunları Kataloğu")
    if not df_oyunlar.empty:
        st.dataframe(df_oyunlar, use_container_width=True)
    else:
        st.warning("Google Sheets 'Oyunlar' sekmesinde henüz oyun tanımlanmamış.")

# 4. İKİLİ MAÇLAR
elif sayfa == "⚔️ İkili Maçlar":
    st.title("⚔️ İkili Maç Geçmişi")
    if not df_ikili.empty:
        st.dataframe(df_ikili, use_container_width=True)
    else:
        st.info("Henüz kayıtlı maç verisi yok. 'Veri Girişi Formu' üzerinden yeni maç ekleyebilirsiniz.")

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

    # İKİLİ MAÇ KAYDI
    if kayit_turu == "⚔️ İkili Maç Kaydı":
        st.subheader("⚔️ İkili Maç Bilgileri")
        
        # Tarih Seçici (Hafızada Sabit Kalır)
        secilen_tarih = st.date_input(
            "📅 Maç Tarihi:",
            value=st.session_state.selected_date,
            help="Seçtiğiniz tarih siz değiştirine kadar sonraki maç kayıtlarında sabit kalır."
        )
        st.session_state.selected_date = secilen_tarih
        
        oyun_listesi = df_oyunlar["Oyun_Adi"].dropna().tolist() if not df_oyunlar.empty and "Oyun_Adi" in df_oyunlar.columns else []
        ogrenci_listesi = df_ogrenciler["Ad_Soyad"].dropna().tolist() if not df_ogrenciler.empty and "Ad_Soyad" in df_ogrenciler.columns else []
        
        with st.form("ikili_mac_formu", clear_on_submit=False):
            if oyun_listesi:
                oyun_adi = st.selectbox("🎮 Oyun Adı:", oyun_listesi)
            else:
                oyun_adi = st.text_input("🎮 Oyun Adı:")
                
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
                st.success(f"✅ {secilen_tarih.strftime('%d.%m.%Y')} tarihli {oyun_adi} maçı kaydı alındı!")

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
            sinif = st.text_input("Sınıf (Örn: 1, 2, 3):")
            sube = st.text_input("Şube (Örn: A, B):")
            
            submitted = st.form_submit_button("💾 Öğrenciyi Kaydet")
            if submitted:
                st.success(f"✅ {ad_soyad} ({sinif}-{sube}) sisteme kaydedildi!")
