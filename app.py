import streamlit as st
import streamlit.components.v1 as components
import hashlib
import json
import datetime
import time
import base64

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Dijital Arabuluculuk Projesi Simülasyonu", page_icon="⚖️", layout="wide")

# --- OTURUM HAFIZASI (SESSION STATE) ---
if 'sira' not in st.session_state:
    st.session_state.sira = "Arabulucu"
if 'imzalar' not in st.session_state:
    st.session_state.imzalar = [] 
if 'tescil_durumu' not in st.session_state:
    st.session_state.tescil_durumu = False
if 'belge_hash' not in st.session_state:
    st.session_state.belge_hash = None
if 'dosya_adi' not in st.session_state:
    st.session_state.dosya_adi = None
if 'mahkeme_karari' not in st.session_state:
    st.session_state.mahkeme_karari = None

# --- YARDIMCI FONKSİYONLAR ---
def dosya_hash_hesapla(uploaded_file):
    uploaded_file.seek(0)
    bytes_data = uploaded_file.getvalue()
    return hashlib.sha256(bytes_data).hexdigest()

def pdf_goster(byte_data):
    """PDF dosyasını tarayıcıda gömmek için HTML iframe oluşturur."""
    base64_pdf = base64.b64encode(byte_data).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="900" type="application/pdf"></iframe>'
    return pdf_display

def belge_olustur_html(dosya_adi, hash_degeri, imzalar, mahkeme_karari=None):
    """Resmi görünümlü HTML belgesi üretir (Yasal Uyarı ile)."""
    

    ornek_damgasi = '<div style="position: absolute; top: 40px; right: 40px; opacity: 0.5; transform: rotate(-10deg); border: 5px double red; color: red; padding: 10px 20px; font-size: 30px; font-weight: bold; border-radius: 10px; z-index: 1000;">ÖRNEKTİR</div>'
    mahkeme_damgasi = "" 
    mahkeme_html = ""

    # İmza Listesi HTML
    imza_html = ""
    for imza in imzalar:
        imza_html += f"""
        <div style="border-bottom: 1px solid #ddd; padding: 10px; display: flex; justify-content: space-between;">
            <span>🖊️ <b>{imza['kim']}</b></span>
            <span style="font-family: monospace; color: #555;">{imza['zaman']}</span>
        </div>
        """

    # Mahkeme Kararı Varsa HTML'i Hazırla
    if mahkeme_karari:
        mahkeme_html = f"""
        <div style="margin-top: 30px; border: 2px solid #d9534f; padding: 20px; background-color: #fdf7f7;">
            <h3 style="color: #d9534f; margin-top: 0; text-align: center;">⚖️ İCRA EDİLEBİLİRLİK ŞERHİ</h3>
            <p><b>Mahkeme:</b> {mahkeme_karari['Mahkeme']}</p>
            <p><b>Karar Tarihi:</b> {mahkeme_karari['Tarih']} - <b>Saat:</b> {datetime.datetime.now().strftime("%H:%M:%S")}</p>
            <p><b>Karar Sonucu:</b> İşbu belge, 6325 Sayılı Kanun'un 18. maddesi uyarınca incelenmiş ve <b>İCRA EDİLEBİLİRLİĞİNE</b> karar verilmiştir.(Usulen yazılmıştır, hukuki geçerliliği yoktur)</p>
            <p style="font-family: monospace; background: #fff; padding: 5px; border: 1px dashed #d9534f;">Doğrulama Kodu: {mahkeme_karari['UYAP_Dogrulama_Kodu']}</p>
        </div>
        """
        mahkeme_damgasi = '<div style="position: absolute; bottom: 120px; right: 50px; opacity: 0.8; transform: rotate(-15deg); border: 3px solid red; color: red; padding: 10px; font-size: 24px; font-weight: bold; border-radius: 10px;">MAHKEME ONAYLI</div>'

    # Ana HTML Şablonu
    html_content = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: 'Times New Roman', serif; padding: 40px; background-color: #f9f9f9; }}
            .container {{ background-color: white; padding: 50px; box-shadow: 0 0 15px rgba(0,0,0,0.1); max-width: 800px; margin: auto; position: relative; }}
            h1 {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; }}
            .hash-box {{ background-color: #eee; padding: 10px; font-family: monospace; font-size: 12px; word-break: break-all; margin-bottom: 30px; }}
            .qr-code {{ text-align: center; margin-top: 40px; }}
            .footer {{ text-align: center; font-size: 10px; color: #777; margin-top: 50px; border-top: 1px solid #ccc; padding-top: 10px; }}
            .disclaimer {{ color: red; font-weight: bold; font-size: 11px; margin-top: 10px; border: 1px solid red; padding: 5px; background-color: #fff0f0; }}
        </style>
    </head>
    <body>
        <div class="container">
            {ornek_damgasi}
            {mahkeme_damgasi}
            <h1>DİJİTAL TESCİL BELGESİ</h1>
            <p><b>Dosya Adı:</b> {dosya_adi}</p>
            <p><b>Tescil Tarihi:</b> {datetime.datetime.now().strftime("%d.%m.%Y")}</p>
            <div class="hash-box">
                <b>BELGE HASH DEĞERİ (SHA-256):</b><br>
                {hash_degeri}
            </div>
            <h3>✍️ İMZA VE ZAMAN DAMGASI LOGLARI</h3>
            <div style="border: 1px solid #ccc; border-radius: 5px;">
                {imza_html}
            </div>
            {mahkeme_html}
            <div class="qr-code">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={hash_degeri}" alt="Dogrulama QR">
                <p>Belge Doğrulama QR Kodu</p>
            </div>
            <div class="footer">
                Bu belge Blok Zinciri teknolojisi ile tescil edilmiş olup, simülasyon gereği 5070 Sayılı Elektronik İmza Kanunu uyarınca kesin delil niteliğindedir.(Örnektir,hukuki geçerliliği yoktur.)<br>
                xxx Bakanlığı Dijital Arabuluculuk Simülasyonu
                <div class="disclaimer">
                    ⚠️ UYARI: İşbu belge yüksek lisans projesi kapsamında oluşturulan simülasyon tarafından yapay zeka yardımı ile üretilmiştir, gerçek kişi, kurum ve olaylar ile bağlantısı bulunmamaktadır, hiçbir hukuki geçerliliği yoktur.
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

# --- YAN MENÜ ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Seal_of_the_Ministry_of_Justice_%28Turkey%29.svg/1200px-Seal_of_the_Ministry_of_Justice_%28Turkey%29.svg.png", width=80)
    st.title("Giriş Paneli")
    aktif_rol = st.radio("Kullanıcı Seçiniz:", ["Arabulucu", "Taraf A ", "Taraf B "])
    st.divider()
    
    # Durum Bilgisi (Sidebar)
    st.caption("📢 SİSTEM DURUMU")
    if st.session_state.sira == "Arabulucu": st.warning("Sıra: ARABULUCU")
    elif st.session_state.sira == "Taraf A ": st.warning("Sıra: TARAF A")
    elif st.session_state.sira == "Taraf B ": st.warning("Sıra: TARAF B")
    elif st.session_state.sira == "Tamamlandi": st.success("Süreç: TESCİLLENDİ")

    st.divider()
    ozel_anahtar = st.text_input("Özel Anahtar (Private Key)", type="password", placeholder="Şifreniz...")

# --- ANA EKRAN ---
st.title("⚖️ Blok Zinciri Tabanlı Tescil Platformu")

# İlerleme Çubuğu
adımlar = ["Arabulucu", "Taraf A", "Taraf B", "Tescil"]
simdiki_adim = 0
if st.session_state.sira == "Taraf A ": simdiki_adim = 1
if st.session_state.sira == "Taraf B ": simdiki_adim = 2
if st.session_state.sira == "Tamamlandi": simdiki_adim = 3

st.progress(simdiki_adim / 3, text=f"Süreç Durumu: {st.session_state.sira}")

col1, col2 = st.columns([1, 1])

# --- SOL KOLON ---
with col1:
    st.subheader("📂 Belge Paneli")
    
    if aktif_rol == "Arabulucu" and st.session_state.sira == "Arabulucu":
        yuklenen_dosya = st.file_uploader("Anlaşma Tutanağını Yükleyin (PDF)", type=["pdf", "docx"])
        if yuklenen_dosya is not None:
            st.session_state.belge_hash = dosya_hash_hesapla(yuklenen_dosya)
            st.session_state.dosya_adi = yuklenen_dosya.name

            # Dosya içeriğini okuyup hafızaya alıyoruz (Önizleme için)
            yuklenen_dosya.seek(0)
            st.session_state.dosya_icerigi = yuklenen_dosya.getvalue()
            st.success("Dosya Hazırlandı.")
            
    elif st.session_state.dosya_adi is not None:
        st.info(f"📄 Dosya: **{st.session_state.dosya_adi}**")
        st.code(st.session_state.belge_hash, language="text")
        st.caption("👆 Dijital Parmak İzi (Hash)")
    else:
        st.info("Henüz sisteme dosya yüklenmedi.")

    # İmza Listesi
    st.write("---")
    st.write("📊 **İmza Kütüğü**")
    for imza in st.session_state.imzalar:
        st.text(f"✅ {imza['kim']} - {imza['zaman']}")

# --- SAĞ KOLON ---
with col2:
    st.subheader(f"✍️ İşlem Paneli: {aktif_rol}")

    # İMZA FONKSİYONU
    def imza_at(rol, sonraki_adim, tescil_tamamla=False):
        if ozel_anahtar:
            zaman_damgasi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.imzalar.append({'kim': rol, 'zaman': zaman_damgasi})
            st.session_state.sira = sonraki_adim
            
            if tescil_tamamla:
                st.session_state.tescil_durumu = True
                
            st.success("İmza Blok Zincirine İşlendi!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Özel Anahtar Girilmedi!")

    # AKIŞ KONTROLÜ
    if aktif_rol == "Arabulucu":
        if st.session_state.sira == "Arabulucu":
            if st.session_state.dosya_adi:
                
                st.write("Belgeyi inceleyip imzalayınız:")
                with st.expander("👀 Yüklenen Dosyayı Oku (İçerik)", expanded=True):
                    if st.session_state.dosya_adi.endswith(".pdf") and st.session_state.dosya_icerigi:
                        st.markdown(pdf_goster(st.session_state.dosya_icerigi), unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ Tarayıcı önizlemesi için lütfen PDF dosyası yükleyiniz. (Şu anki dosya: .docx veya başka format)")
                        st.info("Not: Simülasyonun tam çalışması için Word dosyanızı PDF olarak kaydedip yüklemenizi öneririz.")
              
                
                if st.button("İmzala ve Taraf A'ya Gönder", type="primary"):
                    imza_at("Arabulucu", "Taraf A ")
            else:
                st.warning("Lütfen önce belge yükleyiniz.")
        elif st.session_state.sira != "Tamamlandi":
            st.info("Arabulucu işlemi tamamlandı. Sıra taraflarda.")
        elif st.session_state.sira == "Tamamlandi":
            st.success("Tüm imzalar tamamlandı.")
            st.info("⬇️ Lütfen aşağı kaydırın. Belge indirme ve İcra Şerhi işlemleri alt kısımda aktif edilmiştir.")

    elif aktif_rol == "Taraf A ":
        if st.session_state.sira == "Taraf A ":
            st.write("Arabulucu dosyayı gönderdi.")
            # --- ÖNİZLEME (Taraf A için) ---
            with st.expander("👀 Anlaşma Metnini Oku (İçerik)", expanded=True):
                if st.session_state.dosya_adi.endswith(".pdf") and st.session_state.dosya_icerigi:
                    st.markdown(pdf_goster(st.session_state.dosya_icerigi), unsafe_allow_html=True)
                else:
                    st.warning("⚠️ PDF formatında olmayan dosyalar önizlenemez. Arabulucunuzun PDF yüklemesi önerilir.")
            # -------------------------------
            if st.button("İmzala ve Taraf B'ye Gönder", type="primary"):
                imza_at("Taraf A ", "Taraf B ")
        elif st.session_state.sira == "Arabulucu":
            st.warning("⚠️ Henüz sıra size gelmedi. Arabulucunun belgeyi yükleyip göndermesi bekleniyor.")
        elif st.session_state.sira == "Tamamlandi":
            st.success("Tüm imzalar tamamlandı.")
            st.info("⬇️ Lütfen aşağı kaydırın. Belge indirme ve İcra Şerhi işlemleri alt kısımda aktif edilmiştir.")
        else:
            st.success("Siz imzanızı attınız.")

    elif aktif_rol == "Taraf B ":
        if st.session_state.sira == "Taraf B ":
            st.write("Taraf A imzaladı. Son imza ve tescil için sıra sizde.")
            # --- ÖNİZLEME (Taraf B için) ---
            with st.expander("👀 Anlaşma Metnini Oku (İçerik)", expanded=True):
                if st.session_state.dosya_adi.endswith(".pdf") and st.session_state.dosya_icerigi:
                    st.markdown(pdf_goster(st.session_state.dosya_icerigi), unsafe_allow_html=True)
                else:
                    st.warning("⚠️ PDF formatında olmayan dosyalar önizlenemez.")
            # -------------------------------
            if st.button("İmzala ve Tescili Tamamla", type="primary"):
                # Burada 3. parametreyi True gönderiyoruz
                imza_at("Taraf B ", "Tamamlandi", tescil_tamamla=True)
        elif st.session_state.sira != "Tamamlandi":
            st.warning("⚠️ Henüz sıra size gelmedi. Önce Taraf A'nın imzalaması gerekiyor.")
        elif st.session_state.sira == "Tamamlandi":
            st.success("Tüm işlemler başarıyla tamamlandı.")
            st.info("⬇️ Lütfen sayfanın **en altına** kaydırın. Belge indirme ve İcra Şerhi işlemleri alt kısımda aktif edilmiştir.")

# --- FİNAL: İNDİRME VE İCRA ---
if st.session_state.tescil_durumu or st.session_state.sira == "Tamamlandi":
    st.divider()
    st.header("✅ İŞLEM SONUÇLANDI")
    
    col_final1, col_final2 = st.columns(2)
    
    # 1. KOLON: İNDİRME VE ÖNİZLEME
    with col_final1:
        html_belge = belge_olustur_html(st.session_state.dosya_adi, st.session_state.belge_hash, st.session_state.imzalar, st.session_state.mahkeme_karari)
        
        btn_label = "📄 Tescil Belgesini İndir"
        if st.session_state.mahkeme_karari:
            btn_label = "⚖️ Mahkeme Onaylı Belgeyi İndir"
            
        st.download_button(
            label=btn_label,
            data=html_belge.encode('utf-8'),
            file_name="Dijital_Tescil_Belgesi.html",
            mime="text/html"
        )

       
        with st.expander("👀 Nihai Belgeyi Görüntüle", expanded=False):
             if st.session_state.dosya_adi.endswith(".pdf") and st.session_state.dosya_icerigi:
                 st.markdown(pdf_goster(st.session_state.dosya_icerigi), unsafe_allow_html=True)
             else:
                 st.info("Dosya PDF olmadığı için önizleme yapılamıyor.")
                 
        # 2. KOLON: İCRA BUTONU
    with col_final2:
        if st.session_state.mahkeme_karari is None:
            if st.button("🏛️ İcra Edilebilirlik Şerhi Talep Et"):
                with st.status("UYAP Entegrasyonu...", expanded=True):
                    time.sleep(1)
                    st.write("Mahkeme kararı sorgulanıyor...")
                    time.sleep(1)
                    
                    st.write("Şerh Kodu alındı: UYAP-ANK-2025-OK")
                
                st.session_state.mahkeme_karari = {
                    "Mahkeme": "Ankara 1086. Sulh Hukuk Mahkemesi",
                    "Tarih": datetime.datetime.now().strftime("%d.%m.%Y"),
                    "UYAP_Dogrulama_Kodu": "UYAP-ANK-1086SHM-2025-X92"
                }
                st.rerun()
        else:
            st.success("Şerh Alındı. Soldaki butondan güncel belgeyi indirebilirsiniz.")
