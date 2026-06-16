# 🚀 KAHİN v14.0

**Türkçe Programlama Dili - Proje Dizini**

---

## 📁 Proje Yapısı

```
kahin_projesi/
├── KAHIN_REHBER.md        # Kapsamlı kullanım rehberi (957 satır)
├── README.md              # Bu dosya
├── kahin_binary.py        # Kahin transpiler binary (kaynak)
├── build.py               # Build script (binary'i kur)
├── merhaba.kahin          # Basit örnek
├── test.kahin             # Test dosyası
└── ornekler/
    ├── hizli_test.kahin   # Hızlı test
    └── tam_turkce_test.kahin  # Kapsamlı test
```

---

## 🎯 Dosya Açıklamaları

### Çekirdek Dosyalar

| Dosya | Açıklama | Boyut |
|-------|----------|-------|
| `kahin_binary.py` | **ÇEKİRDEK** - Kahin transpiler (Python script) | 14 KB |
| `build.py` | Binary'i `/usr/bin/kahin` konumuna kurar | 1 KB |

### Dokümantasyon

| Dosya | Açıklama | Boyut |
|-------|----------|-------|
| `KAHIN_REHBER.md` | Başlangıçtan ileri seviyeye tam rehber | 20 KB |
| `README.md` | Bu dosya - proje yapısı | 2 KB |

### Örnekler

| Dosya | Açıklama |
|-------|----------|
| `merhaba.kahin` | Merhaba Dünya örneği |
| `test.kahin` | Basit test |
| `ornekler/hizli_test.kahin` | Hızlı özellik testi |
| `ornekler/tam_turkce_test.kahin` | Kapsamlı test |

---

## ⚙️ Kurulum

### Binary Zaten Kurulu

Kahin binary `/usr/bin/kahin` konumunda:

```bash
which kahin
# /data/data/com.termux/files/usr/bin/kahin

kahin --versiyon
# KAHİN v14.0
```

### Binary'i Yeniden Kurmak

Eğer binary silinmişse veya güncellenmişse:

```bash
cd ~/kahin_projesi
python3 build.py
```

---

## 🚀 Hızlı Başlangıç

### 1. İlk Program

```bash
cd ~/kahin_projesi
kahin merhaba.kahin
```

**Çıktı:**
```
Merhaba Kahin!
...
```

### 2. Test Dosyası

```bash
kahin test.kahin
```

### 3. Kapsamlı Test

```bash
kahin ornekler/hizli_test.kahin
```

### 4. Kendi Programını Yaz

```bash
nano program.kahin
# Kodunu yaz, kaydet

kahin program.kahin
```

---

## 📖 Öğrenme

**Kapsamlı rehber:**
```bash
cat KAHIN_REHBER.md
# veya
less KAHIN_REHBER.md
```

**İçindekiler:**
- Temel sözdizimi
- Veri türleri
- Kontrol yapıları
- Döngüler
- Fonksiyonlar
- Listeler ve sözlükler
- Modüller
- Hata yakalama
- İleri seviye (OOP, lambda, decorator)
- Teknik detaylar (transpiler nasıl çalışır)
- SSS

---

## 🔧 Teknik Bilgiler

### Kahin Binary Nedir?

`kahin_binary.py` bir **Python script**:
- Kahin kodunu Python'a çeviren transpiler
- String-safe (literal koruması)
- f-string desteği
- 5 adımlı çeviri algoritması

### Nasıl Çalışır?

```
Kahin Kodu → Transpiler → Python Kodu → Python VM → Çıktı
```

**Transpiler Adımları:**
1. Yorum çevirisi (`//` → `#`)
2. String koruması (placeholder)
3. Kelime çevirisi (Türkçe → İngilizce, regex)
4. f-string içi işleme
5. String geri yükleme

Detaylar için: `KAHIN_REHBER.md` → Teknik Detaylar

---

## 🔨 Geliştirme

### Binary'i Düzenle

```bash
nano kahin_binary.py
# Değişiklik yap, kaydet

# Global konuma kur
python3 build.py

# Test et
kahin test.kahin
```

### Yeni Anahtar Kelime Ekle

`kahin_binary.py` içinde `KELIME_HARITASI` sözlüğünü düzenle:

```python
KELIME_HARITASI = {
    # Mevcut kelimeler...
    "yeni_kelime": "python_karsiligi",
}
```

Sonra:
```bash
python3 build.py
```

---

## 🐛 Sorun Giderme

### Binary Çalışmıyor

**Kontrol et:**
```bash
which kahin
file $(which kahin)
kahin --versiyon
```

**Yeniden kur:**
```bash
cd ~/kahin_projesi
python3 build.py
```

### Dosya Bulunamadı Hatası

```bash
❌ Dosya bulunamadı: program.kahin
```

**Çözüm:** Dosya yolunu kontrol et:
```bash
ls -la program.kahin
# veya tam yol kullan
kahin /tam/yol/program.kahin
```

### Syntax Hatası

```bash
❌ SÖZDİZİMİ HATASI!
```

**Debug modu ile çalıştır:**
```bash
kahin program.kahin --debug
```

Transpile edilmiş Python kodunu göreceksin.

---

## 📊 İstatistikler

**Proje Boyutu:** ~40 KB (sadece text dosyalar)

**Binary:** 14 KB (Python script)

**Dokümantasyon:** 20 KB (957 satır)

**Örnekler:** 6 KB

---

## ✨ Özellikler

- ✅ Tam Türkçe sözdizimi
- ✅ Python ekosistemi
- ✅ Ultra hızlı (~0.1s)
- ✅ String-safe transpiler
- ✅ f-string desteği
- ✅ Debug modu
- ✅ Detaylı hata mesajları
- ✅ OOP, lambda, decorator desteği
- ✅ Tüm Python kütüphaneleri kullanılabilir

---

## 🔗 Komutlar

```bash
# Versiyon
kahin --versiyon

# Yardım
kahin --yardim

# Normal çalıştırma
kahin program.kahin

# Debug modu
kahin program.kahin --debug
```

---

## 📞 Destek

**Sorun mu var?**
1. `KAHIN_REHBER.md` → SSS bölümünü oku
2. `kahin --yardim` komutunu çalıştır
3. Debug modu ile test et: `kahin program.kahin --debug`

---

**🚀 Mutlu Kodlamalar!**

*Kahin v14.0 - Türkçe Programlama Dili*
