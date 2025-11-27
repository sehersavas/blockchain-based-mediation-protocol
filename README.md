# blockchain-based-mediation-protocol
Türk Hukukunda arabuluculuk süreçleri için blok zinciri tabanlı tescil ve yarı-otomatik icra protokolü.
# ⚖️ Blok Zinciri Tabanlı Arabuluculuk Tutanaklarının Kriptografik Tescil Protokolü

![License](https://img.shields.io/badge/license-MIT-blue) ![Solidity](https://img.shields.io/badge/Solidity-%5E0.8.0-363636) ![Python](https://img.shields.io/badge/Python-3.8%2B-yellow) ![Status](https://img.shields.io/badge/Status-Prototype-green)

## Proje Özeti
Bu proje, Türk Hukuku'ndaki arabuluculuk süreçlerinde karşılaşılan "ıslak imza zorunluluğu" ve "fiziksel tescil" problemlerini çözmek amacıyla geliştirilmiş hibrit bir **LegalTech** projesidir.

**Temel Amaç:** Avukatı olmayan vatandaşların uzaktan (online) katıldığı arabuluculuk süreçlerinde,  anlaşma tutanaklarının **Blok Zinciri (Blockchain)** üzerinde değiştirilemez ve inkâr edilemez (Non-repudiation) şekilde tescil edilmesini sağlamaktır.

---

## Çözülen Problem ve Yaklaşım

| Sorun Alanı | Mevcut Durum (Geleneksel) | Projenin Çözümü (Blockchain) |
| :--- | :--- | :--- |
| **İmza** | Arabuluculuk sürecinde taraflardan en az biri avukat ile temsil edilmediği ve e-imzaya sahip olmadığı takdirde ıslak imza atılması gerekmektedir. E-imza vatandaş için yaygın şekilde kullanımda olmadığı gibi belirli periyotlarla yenilenmesi gerekmekte ve külfet oluşturmaktadır. | **Kriptografik İmza:** Özel anahtar ile atılan dijital imza (5070 s. Kanun uyumlu) ile e-imza sahibi olmayan vatandaşların da fiziksel olarak imza atmasına gerek kalmadan güvenle tutanağı imzalamasına olanak sağlanmaktadır. |
| **Güven** | Tutanakların kaybolma riski. | **Değişmezlik (Immutability):** Belge Hash'inin blok zincirine kazınması. |
| **İcra** | Kanunda sayılan belli durumlarda arabuluculuk tutanağının ilam niteliği kazanabilmesi için icra edilebilirlik şerhi alınması gerekmektedir, bu süreç sulh hukuk mahkemesinde bir dava açılması ve sonuçlanmasını beklemeyi içerir ve bu süreç iş gücü ve bekleme süresi gerektirir. | **Yarı-Otomatik İcra:** Akıllı sözleşme ile resmi onayın (UYAP) otomatik işlenmesi ile usul ekonomisi adına kazanım sağlanır. |

---

##  Mimari: Hukuki-Teknik Eşleştirme

| Adım | Akıllı Sözleşme Fonksiyonu (Solidity) | Hukuki Karşılık (Legal Context) |
| :--- | :--- | :--- |
| **1** | `anlasmaOlustur(dosyaNo, hash)` | **Son Tutanağın Düzenlenmesi:** Arabulucu metni hazırlar, değişmezliği Hash ile sabitlenir. |
| **2** | `imzaAt(kisi)` | **İrade Beyanı:** Taraflar kriptografik anahtarlarıyla "Kabul Ediyorum" beyanını sunar. |
| **3** | `if (imzaSayisi == 3)` | **İlam Niteliği (HUAK Md. 18):** Taraflar ve arabulucunun (3 imza) tamamlanmasıyla belge mahkeme hükmü vasfını kazanır. |
| **4** | `event TescilTamamlandi` | **Resmi Sicil:** İşlem, dağıtık defterde zaman damgasıyla silinemez şekilde arşivlenir. |
| **5** | `icraBaslat(serhKodu)` | **Yarı-Otomatik İcra:** Taşınmaz devri gibi işlemlerde Mahkeme/UYAP onayı ile süreç tetiklenir. |

---

##  Teknoloji Yığını

* **Smart Contract:** Solidity (Ethereum Sanal Makinesi)
* **Simülasyon:** Python (Mantıksal akış prototipi)
* **Geliştirme Ortamı:** Remix IDE
* **Kriptografi:** SHA-256 Hashing, ECDSA İmza Mantığı

---

## Kurulum ve Test

Bu proje **Remix IDE** üzerinden tarayıcıda çalıştırılabilir.

1. [Remix Ethereum](https://remix.ethereum.org/) adresine gidin.
2. `Arabuluculuk.sol` dosyasını yükleyin.
3. **Compile** ve **Deploy** edin.
4. `imzaAt` ve `icraBaslat` fonksiyonları ile süreci test edin.

### Test Kanıtı (Proof of Concept)
![Remix Test Sonucu](remix_proof.png)

---

## Hukuki Dayanaklar
1. **6325 Sayılı Hukuk Uyuşmazlıklarında Arabuluculuk Kanunu (Md. 18):** İlam niteliğinde belge şartları.
2. **5070 Sayılı Elektronik İmza Kanunu (Md. 4):** Güvenli elektronik imzanın elle atılan imza ile eşdeğerliği.

---
## Metodoloji ve AI Kullanımı
Bu projenin hukuki mimarisi, iş akış şemaları ve çözüm modeli şahsıma aittir. 

Teknik prototipleme aşamasında (Solidity Akıllı Sözleşme kodlarının yazımı ve Python simülasyonu), kod verimliliğini artırmak ve hata ayıklamak amacıyla **Üretken Yapay Zeka (Generative AI)** araçlarından asistan desteği alınmıştır. Proje, insan denetimli (Human-in-the-loop) bir yaklaşımla geliştirilmiştir.

---
**Geliştirici:** Seher Savaş
*Avukat & Akdeniz Üniversitesi Veri Analitiği ve Yönetimi Yüksek Lisans Öğrencisi*
