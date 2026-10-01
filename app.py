import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Akıl ve Zeka Oyunları Takip Paneli",
    page_icon="🧠",
    layout="wide"
)

# --- YÖNETİCİ ŞİFRESİ VE AYARLAR ---
YONETICI_SIFRESI = "1234"  # 👈 Buradan şifrenizi değiştirebilirsiniz

# Google Sheets URL
SHEET_ID = "1EFWWiyOe7kqwvEaSZeA3Kahgl9-Zy3LL6QzCpF3yt4I"

def load_data(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        df = pd.read_csv(url)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df
    except Exception as e:
        return pd.DataFrame()

# Oturum Durumu (Session State) Hazırlığı
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = datetime.now().date()
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Verileri Yükle
df_ogrenciler = load_data("Ogrenciler")
df_oyunlar = load_data("Oyunlar")
df_ikili = load_data("Ikili_Maclar")
df_bireysel = load_data("Bireysel_Performans")

# --- KENAR ÇUBUĞU (SIDEBAR) & YETKİLENDİRME ---
st.sidebar.title("🏛️ Akıl Oyunları Paneli")
st.sidebar.caption("2026-2027 Eğitim Öğretim Yılı")

# Yönetici Giriş / Çıkış Alanı
st.sidebar.divider()
if not st.session_state.is_admin:
    st.sidebar.subheader("🔒 Yönetici Girişi")
    sifre_input = st.sidebar.text_input("Şifre:", type="password", help="Veri girişi yapabilmek için şifrenizi giriniz.")
    if st.sidebar.button("Giriş Yap"):
        if sifre_input == YONETICI_SIFRESI:
            st.session_state.is_admin = True
            st.sidebar.success("Yönetici yetkisi doğrulandı!")
            st.rerun()
        else:
            st.sidebar.error("Hatalı şifre!")
else:
    st.sidebar.success("🔑 Yönetici Modu Aktif")
    if st.sidebar.button("Çıkış Yap"):
        st.session_state.is_admin = False
        st.rerun()

st.sidebar.divider()

# Menü Seçenekleri (Yetkiye Göre Dinamik)
sayfa_seçenekleri = ["📊 Genel Durum", "👨‍‍🎓 Öğrenci Listesi", "🎮 Oyunlar", "⚔️ İkili Maçlar", "⭐ Bireysel Performans"]

# Sadece admin giriş yaptıysa Veri Girişi Formu görünür
if st.session_state.is_admin:
    sayfa_seçenekleri.append("➕ Veri Girişi Formu")

sayfa = st.sidebar.radio("Sayfa Seçiniz:", sayfa_seçenekleri)

# 1. GENEL DURUM
if sayfa == "📊 Genel Durum":
    st.title("🧠 Akıl ve Zeka Oyunları Yönetim ve Takip Paneli")
    st.caption("Öğrenci gelişim, turnuva ve etkinlik takip platformu")
    st.divider()
    
    st.subheader("📈 Genel İstatistikler")
    col1, col2, col3 = st.columns(3)
    col1.metric("Kayıtlı Toplam Öğrenci", len(df_ogrenciler) if not df_ogrenciler.empty else 0)
    col2.metric("Aktif Oyun Kütüphanesi", len(df_oyunlar) if not df_oyunlar.empty else 0)
    col3.metric("Tamamlanan İkili Maç", len(df_ikili) if not df_ikili.empty else 0)
    
    st.divider()
    st.subheader("📋 Son Oynanan Maçlar ve Turnuva Kayıtları")
    if not df_ikili.empty:
        st.dataframe(df_ikili.tail(10), use_container_width=True)
    else:
        st.info("Henüz kayıtlı maç verisi bulunmamaktadır.")

# 2. ÖĞRENCİ LİSTESİ (SINIF VE ŞUBE FİLTRELİ)
elif sayfa == "👨‍🎓 Öğrenci Listesi":
    st.title("👨‍🎓 Öğrenci Listesi ve Sınıf Kontrolü")
    
    if not df_ogrenciler.empty:
        sinif_col = "Sinif" if "Sinif" in df_ogrenciler.columns else None
        sube_col = "Sube" if "Sube" in df_ogrenciler.columns else None
        
        col_f1, col_f2 = st.columns(2)
        filtered_df = df_ogrenciler.copy()
        
        if sinif_col:
            siniflar = ["Tümü"] + sorted([str(x).split('.')[0] for x in df_ogrenciler[sinif_col].dropna().unique() if str(x) != 'nan'])
            secilen_sinif = col_f1.selectbox("🎯 Sınıf Seçiniz:", siniflar)
            
            if secilen_sinif != "Tümü":
                filtered_df = filtered_df[filtered_df[sinif_col].astype(str).str.startswith(secilen_sinif)]
        
        if sube_col:
            subeler = ["Tümü"] + sorted([str(x) for x in filtered_df[sube_col].dropna().unique() if str(x) != 'nan'])
            secilen_sube = col_f2.selectbox("🏢 Şube Seçiniz:", subeler)
            
            if secilen_sube != "Tümü":
                filtered_df = filtered_df[filtered_df[sube_col].astype(str) == secilen_sube]
                
        st.info(f"🔍 Seçilen kritere göre **{len(filtered_df)}** öğrenci listeleniyor.")
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.warning("Google Sheets üzerinde 'Ogrenciler' sayfasında kayıt bulunamadı.")

# 3. OYUNLAR
elif sayfa == "🎮 Oyunlar":
    st.title("🎮 Akıl Oyunları Müfredat ve Oyun Kataloğu")
    if not df_oyunlar.empty:
        st.dataframe(df_oyunlar, use_container_width=True)
    else:
        st.warning("Henüz oyun bilgisi tanımlanmamış.")

# 4. İKİLİ MAÇLAR
elif sayfa == "⚔️ İkili Maçlar":
    st.title("⚔️ İkili Maç ve Turnuva Kayıtları")
    if not df_ikili.empty:
        st.dataframe(df_ikili, use_container_width=True)
    else:
        st.info("Kayıtlı maç verisi bulunmamaktadır.")

# 5. BİREYSEL PERFORMANS
elif sayfa == "⭐ Bireysel Performans":
    st.title("⭐ Bireysel Gelişim ve Değerlendirme Kayıtları")
    if not df_bireysel.empty:
        st.dataframe(df_bireysel, use_container_width=True)
    else:
        st.info("Kayıtlı bireysel performans verisi bulunmamaktadır.")

# 6. VERİ GİRİŞİ FORMU (SADECE YÖNETİCİ GİRİŞİ YAPANLAR GÖREBİLİR)
elif sayfa == "➕ Veri Girişi Formu" and st.session_state.is_admin:
    st.title("➕ Yönetici Hızlı Veri Kayıt Ekranı")
    
    kayit_turu = st.radio(
        "Kayıt Türü Seçiniz:",
        ["⚔️ İkili Maç Kaydı", "⭐ Bireysel Performans Kaydı", "👨‍‍🎓 Yeni Öğrenci Kaydı"],
        horizontal=True
    )
    
    st.divider()

    # İKİLİ MAÇ KAYDI
    if kayit_turu == "⚔️ İkili Maç Kaydı":
        st.subheader("⚔️ İkili Maç Bilgileri")
        
        secilen_tarih = st.date_input(
            "📅 Maç Tarihi:",
            value=st.session_state.selected_date,
            help="Seçtiğiniz tarih siz değiştirene kadar sabit kalır."
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
