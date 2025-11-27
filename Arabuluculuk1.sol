// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ArabuluculukSistemi {

    // Anlaşma yapısı (Veri Modeli)
    struct Anlasma {
        string dosyaNo;
        string anlasmaHash; // Tutanağın parmak izi
        bool tarafA_Imzaladi;
        bool tarafB_Imzaladi;
        bool arabulucu_Imzaladi;
        bool tescilEdildi;
        string mahkemeSerhKodu; // Yarı otomatik icra için
    }

    // Dosya Numarasına göre anlaşmaları saklayan defter
    mapping(string => Anlasma) public anlasmalar;

    // Olaylar (Blockchain üzerinde log tutmak için - ispat)
    event AnlasmaOlusturuldu(string dosyaNo, string hash);
    event ImzaAtildi(string dosyaNo, string imzalayan);
    event TescilTamamlandi(string dosyaNo);
    event IcraBaslatildi(string dosyaNo, string serhKodu);

    // 1. Arabulucu Anlaşmayı Sisteme Yükler
    function anlasmaOlustur(string memory _dosyaNo, string memory _anlasmaHash) public {
        anlasmalar[_dosyaNo] = Anlasma(_dosyaNo, _anlasmaHash, false, false, false, false, "");
        emit AnlasmaOlusturuldu(_dosyaNo, _anlasmaHash);
    }

    // 2. İmza Atma Fonksiyonu
    // Cüzdan adresi kontrolü yerine simülasyona uygun şekilde kontrol basitleştirildi.
    function imzaAt(string memory _dosyaNo, string memory _kisi) public {
        Anlasma storage a = anlasmalar[_dosyaNo];
        
        
        if (keccak256(bytes(_kisi)) == keccak256(bytes("TarafA"))) {
            a.tarafA_Imzaladi = true;
        } else if (keccak256(bytes(_kisi)) == keccak256(bytes("TarafB"))) {
            a.tarafB_Imzaladi = true;
        } else if (keccak256(bytes(_kisi)) == keccak256(bytes("Arabulucu"))) {
            a.arabulucu_Imzaladi = true;
        }

        emit ImzaAtildi(_dosyaNo, _kisi);

        // 3 imza tamamlandığının kontrol edilmesi
        if (a.tarafA_Imzaladi && a.tarafB_Imzaladi && a.arabulucu_Imzaladi) {
            a.tescilEdildi = true;
            emit TescilTamamlandi(_dosyaNo);
        }
    }

    // 3. Yarı Otomatik İcra (Mahkeme Onayı)
    function icraBaslat(string memory _dosyaNo, string memory _serhKodu) public {
        Anlasma storage a = anlasmalar[_dosyaNo];
        
        require(a.tescilEdildi, "HATA: Once tum imzalar tamamlanmali.");
        
        // Temsili gösterim için mahkemenin onayı ile birlikte UYAP'tan gönderilecek onay kodu yerine "UYAP_OK" onayı tanımlanmıştır.
        if (keccak256(bytes(_serhKodu)) == keccak256(bytes("UYAP_OK"))) {
            a.mahkemeSerhKodu = _serhKodu;
            emit IcraBaslatildi(_dosyaNo, "Otomatik Icra Islemi Basladi");
        }
    }
}