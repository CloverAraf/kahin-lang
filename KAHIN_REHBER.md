# 🚀 KAHİN v14.0 - KAPSAMLI KULLANIM REHBERİ

**Türkçe Programlama Dili - Başlangıçtan İleri Seviyeye**

---

## 📖 İçindekiler

1. [Giriş](#giriş)
2. [Kurulum](#kurulum)
3. [İlk Program](#ilk-program)
4. [Temel Sözdizimi](#temel-sözdizimi)
5. [Veri Türleri](#veri-türleri)
6. [Kontrol Yapıları](#kontrol-yapıları)
7. [Döngüler](#döngüler)
8. [Fonksiyonlar](#fonksiyonlar)
9. [Listeler ve Sözlükler](#listeler-ve-sözlükler)
10. [Modüller](#modüller)
11. [Hata Yakalama](#hata-yakalama)
12. [İleri Seviye](#ileri-seviye)
13. [Teknik Detaylar](#teknik-detaylar)
14. [Sık Sorulan Sorular](#sık-sorulan-sorular)

---

## 🎯 Giriş

### Kahin Nedir?

Kahin, **Türkçe anahtar kelimelerle** Python'un gücünü kullanan bir programlama dilidir.

**Özellikler:**
- ✅ Tam Türkçe sözdizimi
- ✅ Python ekosisteminin tümüne erişim
- ✅ Ultra hızlı (transpiler-based)
- ✅ Kolay öğrenme eğrisi
- ✅ Modern programlama özellikleri

### Nasıl Çalışır?

```
Kahin Kodu  →  Transpiler  →  Python Kodu  →  Python Interpreter  →  Çıktı
   (Türkçe)      (Çevirici)     (İngilizce)       (Çalıştırıcı)
```

**Transpiler Nedir?**
Kahin kodunu Python koduna çeviren akıllı program. Örnek:

```kahin
eger x > 5:
    yazdir("Büyük")
```
↓ Transpiler çevirir:
```python
if x > 5:
    print("Büyük")
```

---

## 💻 Kurulum

### Termux'ta Kurulum

Kahin zaten kurulu! Kontrol et:

```bash
kahin --versiyon
```

Çıktı:
```
KAHİN v14.0
Türkçe Programlama Dili

Python Sürümü: 3.12.12
Platform: linux
```

### Binary Konumu

```bash
which kahin
# /data/data/com.termux/files/usr/bin/kahin
```

---

## 👋 İlk Program

### Merhaba Dünya

**Dosya:** `merhaba.kahin`

```kahin
yazdir("Merhaba Dünya!")
```

**Çalıştır:**

```bash
kahin merhaba.kahin
```

**Çıktı:**
```
Merhaba Dünya!
```

### Basit Hesaplama

```kahin
// Değişkenler
sayi1 = 10
sayi2 = 20

// Toplama
toplam = sayi1 + sayi2

// Ekrana yaz
yazdir(f"Toplam: {toplam}")
```

**Çıktı:**
```
Toplam: 30
```

---

## 📝 Temel Sözdizimi

### Yorumlar

```kahin
// Tek satır yorum

// Çok satırlı yorum
// ikinci satır
// üçüncü satır
```

### Değişkenler

```kahin
// Değişken tanımlama (tip belirtmeye gerek yok)
isim = "Ahmet"
yas = 25
boy = 1.75
ogrenci_mi = dogru  // True

// f-string ile yazdırma
yazdir(f"İsim: {isim}, Yaş: {yas}")
```

### Türkçe Anahtar Kelimeler Tablosu

| Kahin (Türkçe) | Python (İngilizce) | Kullanım |
|----------------|-------------------|----------|
| `yazdir` | `print` | Ekrana yazdır |
| `girdi` | `input` | Kullanıcıdan veri al |
| `eger` | `if` | Koşul kontrolü |
| `degilse_eger` | `elif` | Alternatif koşul |
| `degilse` | `else` | Koşul değilse |
| `dondu_boyunca` | `while` | While döngüsü |
| `her_biri_icin` | `for` | For döngüsü |
| `icinde` | `in` | İçinde operatörü |
| `aralik` | `range` | Sayı aralığı |
| `tanimla` | `def` | Fonksiyon tanımla |
| `dondur` | `return` | Değer döndür |
| `dur` | `break` | Döngüyü kır |
| `devam_et` | `continue` | Sonraki iterasyon |
| `dene` | `try` | Hata yakalama |
| `yakala` | `except` | Hata işleme |
| `sonunda` | `finally` | Her durumda çalış |
| `dogru` | `True` | Doğru değeri |
| `yanlis` | `False` | Yanlış değeri |
| `hic` | `None` | Boş değer |
| `ice_aktar` | `import` | Modül içe aktar |
| `sinif` | `class` | Sınıf tanımla |

---

## 🔢 Veri Türleri

### Sayılar

```kahin
// Tam sayı
sayi = 42
yazdir(f"Tür: {tur(sayi)}")  // <class 'int'>

// Ondalıklı sayı
pi = 3.14159
yazdir(f"Tür: {tur(pi)}")  // <class 'float'>

// Matematiksel işlemler
toplam = 10 + 5      // 15
fark = 10 - 5        // 5
carpim = 10 * 5      // 50
bolum = 10 / 3       // 3.333...
tam_bolum = 10 // 3  // 3
mod = 10 % 3         // 1
us = 2 ** 3          // 8
```

### Metinler (String)

```kahin
// String tanımlama
metin1 = "Merhaba"
metin2 = 'Dünya'

// String birleştirme
tam_metin = metin1 + " " + metin2
yazdir(tam_metin)  // Merhaba Dünya

// String uzunluğu
uzunluk(metin1)  // 7

// String metodları
yazdir(metin1.upper())  // MERHABA
yazdir(metin1.lower())  // merhaba

// f-string (format string)
isim = "Ali"
yas = 25
yazdir(f"{isim}, {yas} yaşında")  // Ali, 25 yaşında
```

### Boolean (Mantıksal)

```kahin
// Boolean değerler
var_mi = dogru      // True
yok_mu = yanlis     // False

// Karşılaştırma operatörleri
10 > 5    // dogru
10 < 5    // yanlis
10 == 10  // dogru
10 != 5   // dogru
10 >= 10  // dogru
10 <= 9   // yanlis

// Mantıksal operatörler
dogru and dogru    // dogru
dogru and yanlis   // yanlis
dogru or yanlis    // dogru
not dogru          // yanlis
```

---

## 🔀 Kontrol Yapıları

### if-elif-else

```kahin
yas = 18

eger yas < 18:
    yazdir("Çocuk")
degilse_eger yas == 18:
    yazdir("Tam 18!")
degilse:
    yazdir("Yetişkin")
```

### İç İçe Koşullar

```kahin
not = 75

eger not >= 50:
    yazdir("Geçti")

    eger not >= 90:
        yazdir("Mükemmel!")
    degilse_eger not >= 70:
        yazdir("İyi")
    degilse:
        yazdir("Orta")
degilse:
    yazdir("Kaldı")
```

### Kısa Koşul (Ternary)

```kahin
yas = 20
durum = "Yetişkin" eger yas >= 18 degilse "Çocuk"
yazdir(durum)  // Yetişkin
```

---

## 🔁 Döngüler

### for Döngüsü

```kahin
// Sayı aralığı
her_biri_icin i icinde aralik(5):
    yazdir(i)
// Çıktı: 0, 1, 2, 3, 4

// Başlangıç ve bitiş
her_biri_icin i icinde aralik(1, 6):
    yazdir(i)
// Çıktı: 1, 2, 3, 4, 5

// Adım atlamalı
her_biri_icin i icinde aralik(0, 10, 2):
    yazdir(i)
// Çıktı: 0, 2, 4, 6, 8
```

### Liste Üzerinde Döngü

```kahin
meyveler = ["elma", "armut", "çilek"]

her_biri_icin meyve icinde meyveler:
    yazdir(f"Meyve: {meyve}")
```

### while Döngüsü

```kahin
sayac = 0

dondu_boyunca sayac < 5:
    yazdir(f"Sayaç: {sayac}")
    sayac = sayac + 1
```

### break ve continue

```kahin
// break - döngüyü kır
her_biri_icin i icinde aralik(10):
    eger i == 5:
        dur  // Döngü burada biter
    yazdir(i)
// Çıktı: 0, 1, 2, 3, 4

// continue - sonraki iterasyona atla
her_biri_icin i icinde aralik(5):
    eger i == 2:
        devam_et  // 2'yi atla
    yazdir(i)
// Çıktı: 0, 1, 3, 4
```

---

## ⚙️ Fonksiyonlar

### Basit Fonksiyon

```kahin
tanimla selamla():
    yazdir("Merhaba!")

// Fonksiyonu çağır
selamla()
```

### Parametreli Fonksiyon

```kahin
tanimla selamla(isim):
    yazdir(f"Merhaba {isim}!")

selamla("Ali")      // Merhaba Ali!
selamla("Ayşe")     // Merhaba Ayşe!
```

### Değer Döndüren Fonksiyon

```kahin
tanimla topla(a, b):
    sonuc = a + b
    dondur sonuc

// Kullanım
toplam = topla(10, 20)
yazdir(toplam)  // 30
```

### Varsayılan Parametreler

```kahin
tanimla selamla(isim, mesaj="Merhaba"):
    yazdir(f"{mesaj} {isim}!")

selamla("Ali")                    // Merhaba Ali!
selamla("Ali", "Günaydın")        // Günaydın Ali!
```

### Çoklu Değer Döndürme

```kahin
tanimla hesapla(a, b):
    toplam = a + b
    fark = a - b
    carpim = a * b
    dondur toplam, fark, carpim

// Kullanım
t, f, c = hesapla(10, 5)
yazdir(f"Toplam: {t}, Fark: {f}, Çarpım: {c}")
```

---

## 📚 Listeler ve Sözlükler

### Listeler

```kahin
// Liste oluşturma
sayilar = [1, 2, 3, 4, 5]
meyveler = ["elma", "armut", "çilek"]
karisik = [1, "iki", 3.0, dogru]

// Liste metodları
uzunluk(sayilar)         // 5
en_buyuk(sayilar)        // 5
en_kucuk(sayilar)        // 1
topla(sayilar)           // 15

// Eleman ekleme/çıkarma
meyveler.append("muz")   // Sona ekle
meyveler.insert(0, "üzüm")  // Başa ekle
meyveler.remove("armut") // Çıkar
meyveler.pop()           // Son elemanı çıkar

// Dilimler (slicing)
sayilar[0]       // 1 (ilk eleman)
sayilar[-1]      // 5 (son eleman)
sayilar[1:3]     // [2, 3]
sayilar[:3]      // [1, 2, 3]
sayilar[2:]      // [3, 4, 5]
```

### Sözlükler (Dictionary)

```kahin
// Sözlük oluşturma
kisi = sozluk()
kisi["ad"] = "Ahmet"
kisi["soyad"] = "Yılmaz"
kisi["yas"] = 30

// Veya direkt tanımlama
kisi = {"ad": "Ahmet", "soyad": "Yılmaz", "yas": 30}

// Erişim
yazdir(kisi["ad"])      // Ahmet
yazdir(kisi.get("ad"))  // Ahmet

// Tüm anahtarlar
yazdir(kisi.keys())     // ["ad", "soyad", "yas"]

// Tüm değerler
yazdir(kisi.values())   // ["Ahmet", "Yılmaz", 30]

// Döngü ile gezinme
her_biri_icin anahtar, deger icinde kisi.items():
    yazdir(f"{anahtar}: {deger}")
```

### Kümeler (Set)

```kahin
// Benzersiz elemanlar
sayilar = kume([1, 2, 2, 3, 3, 3])
yazdir(sayilar)  // {1, 2, 3}

// Küme işlemleri
a = kume([1, 2, 3])
b = kume([3, 4, 5])

a | b   // Birleşim: {1, 2, 3, 4, 5}
a & b   // Kesişim: {3}
a - b   // Fark: {1, 2}
```

---

## 📦 Modüller

### Modül İçe Aktarma

```kahin
// Tam modül
ice_aktar sys
yazdir(sys.version)

// Modülden belirli fonksiyon
ice_aktar sys
yazdir(sys.platform)

// Takma ad ile
ice_aktar sistem as os
yazdir(os.getcwd())
```

### Türkçe Modül İsimleri

| Kahin | Python | Açıklama |
|-------|--------|----------|
| `sistem` | `os` | İşletim sistemi |
| `zaman` | `time` | Zaman işlemleri |
| `istek` | `requests` | HTTP istekleri |
| `arayuz` | `sys` | Sistem arayüzü |

**Örnek:**

```kahin
// Sistem bilgisi
ice_aktar arayuz
yazdir(f"Python: {arayuz.version}")

// Zaman işlemleri
ice_aktar zaman
zaman.sleep(1)  // 1 saniye bekle
```

### Dosya İşlemleri

```kahin
// Dosya yazma
ile ac("dosya.txt", "w") as dosya:
    dosya.write("Merhaba Dünya!")

// Dosya okuma
ile ac("dosya.txt", "r") as dosya:
    icerik = dosya.read()
    yazdir(icerik)
```

---

## 🛡️ Hata Yakalama

### try-except

```kahin
dene:
    sayi = tam_sayi("123")
    yazdir(sayi)
yakala ValueError:
    yazdir("Geçersiz sayı!")
```

### Genel Hata Yakalama

```kahin
dene:
    sonuc = 10 / 0
yakala Exception as hata:
    yazdir(f"Hata oluştu: {hata}")
```

### finally Kullanımı

```kahin
dene:
    dosya = ac("dosya.txt", "r")
    icerik = dosya.read()
yakala FileNotFoundError:
    yazdir("Dosya bulunamadı!")
sonunda:
    dosya.close()  // Her durumda çalışır
```

---

## 🚀 İleri Seviye

### List Comprehension

```kahin
// Normal yöntem
kareler = liste()
her_biri_icin i icinde aralik(10):
    kareler.append(i ** 2)

// List comprehension (Python tarzı - desteklenir)
kareler = [i ** 2 for i in range(10)]
yazdir(kareler)
```

### Lambda Fonksiyonları

```kahin
// Lambda (anonim fonksiyon)
topla = lambda a, b: a + b
yazdir(topla(5, 3))  // 8

// Sıralama ile kullanım
kisiler = [{"ad": "Ali", "yas": 30}, {"ad": "Ayşe", "yas": 25}]
sirali = sirala(kisiler, key=lambda k: k["yas"])
```

### Sınıflar (OOP)

```kahin
sinif Kisi:
    tanimla __init__(self, ad, yas):
        self.ad = ad
        self.yas = yas

    tanimla selamla(self):
        yazdir(f"Merhaba, ben {self.ad}, {self.yas} yaşındayım")

// Kullanım
kisi1 = Kisi("Ali", 30)
kisi1.selamla()
```

### Decorator (Dekoratör)

```kahin
tanimla log_decorator(func):
    tanimla wrapper(*args, **kwargs):
        yazdir(f"Fonksiyon çağrılıyor: {func.__name__}")
        sonuc = func(*args, **kwargs)
        yazdir(f"Fonksiyon bitti")
        dondur sonuc
    dondur wrapper

@log_decorator
tanimla topla(a, b):
    dondur a + b

topla(5, 3)
```

---

## 🔧 Teknik Detaylar

### Kahin Nasıl Çalışır?

**İşlem Akışı:**

```
1. KULLANICI
   $ kahin program.kahin

2. SHELL
   Python3 başlat

3. KAHİN TRANSPİLER
   • Dosyayı oku
   • String'leri koru (literal koruması)
   • Türkçe → İngilizce (regex ile)
   • f-string içlerini çevir
   • String'leri geri yükle
   → Python kodu üret

4. PYTHON INTERPRETER
   • Kodu parse et (AST)
   • Compile et (bytecode)
   • Çalıştır (VM)

5. ÇIKTI
   Sonuç ekrana yazdırılır
```

### Transpiler Algoritması

**5 Adım:**

1. **Yorum Çevirisi**: `//` → `#`
2. **String Koruması**: Literal string'leri sakla
3. **Kelime Çevirisi**: Türkçe → İngilizce (regex)
4. **f-string İşleme**: İçindeki kod bloklarını çevir
5. **Geri Yükleme**: String'leri yerine koy

**Örnek Çeviri:**

```kahin
// Kahin kodu
eger x > 5:
    yazdir("Büyük")
```
↓ Transpiler
```python
# Python kodu
if x > 5:
    print("Büyük")
```

### Debug Modu

Transpile edilmiş kodu görmek için:

```bash
kahin program.kahin --debug
```

**Çıktı:**
```
═══════════════════════════════════
ÇEVRİLMİŞ PYTHON KODU
═══════════════════════════════════
   1 | if x > 5:
   2 |     print("Büyük")
═══════════════════════════════════
ÇIKTI
═══════════════════════════════════
Büyük
```

### Performans

**Hız:**
- Transpile: ~0.01s
- Python execution: Python kadar hızlı
- Toplam: ~0.1s

**Karşılaştırma:**
- Go-based (embed): ~2-3s (tar açma + init)
- Python-based: ~0.1s ⚡

---

## ❓ Sık Sorulan Sorular

### Kahin Python mu?

**Hayır, ama Python'a çevrilir.**

Kahin → Transpiler → Python → Çalıştır

Python ekosistemi kullanılır ama sözdizimi Türkçe.

### Python kütüphaneleri kullanılabilir mi?

**Evet, tamamen!**

```kahin
ice_aktar numpy as np
ice_aktar pandas as pd

// NumPy kullanımı
dizi = np.array([1, 2, 3])
yazdir(dizi)
```

### Hata mesajları Türkçe mi?

**Kısmen.**

- Syntax hataları: Python'dan gelir (İngilizce)
- Runtime hataları: Python'dan gelir (İngilizce)
- Kahin'in hataları: Türkçe

**Örnek:**
```bash
❌ Dosya bulunamadı: program.kahin
```

### Kahin'in kendi parser'ı var mı?

**Hayır.**

Kahin bir **transpiler**. Python'un parser'ını kullanır.

- ❌ Lexer yok
- ❌ Parser yok
- ❌ AST builder yok
- ✅ Sadece string çevirici var

### Performans nasıl?

**Python kadar hızlı!**

Transpile çok hızlı (regex), sonra Python çalışıyor.

### Binary nasıl çalışıyor?

`/usr/bin/kahin` aslında Python script:

```python
#!/usr/bin/python3
# ... Kahin transpiler kodu ...
```

Shebang sayesinde Python olarak çalışıyor.

---

## 📚 Örnek Programlar

### Hesap Makinesi

```kahin
tanimla hesap_makinesi():
    yazdir("=== HESAP MAKİNESİ ===")
    yazdir("1. Toplama")
    yazdir("2. Çıkarma")
    yazdir("3. Çarpma")
    yazdir("4. Bölme")

    secim = girdi("Seçiminiz: ")

    sayi1 = ondalik(girdi("İlk sayı: "))
    sayi2 = ondalik(girdi("İkinci sayı: "))

    eger secim == "1":
        yazdir(f"Sonuç: {sayi1 + sayi2}")
    degilse_eger secim == "2":
        yazdir(f"Sonuç: {sayi1 - sayi2}")
    degilse_eger secim == "3":
        yazdir(f"Sonuç: {sayi1 * sayi2}")
    degilse_eger secim == "4":
        eger sayi2 != 0:
            yazdir(f"Sonuç: {sayi1 / sayi2}")
        degilse:
            yazdir("Hata: Sıfıra bölme!")

hesap_makinesi()
```

### Asal Sayı Bulucu

```kahin
tanimla asal_mi(sayi):
    eger sayi < 2:
        dondur yanlis

    her_biri_icin i icinde aralik(2, sayi):
        eger sayi % i == 0:
            dondur yanlis

    dondur dogru

// Test
her_biri_icin i icinde aralik(1, 20):
    eger asal_mi(i):
        yazdir(f"{i} asal sayıdır")
```

### Dosya İşleme

```kahin
ice_aktar sistem as os

tanimla dosya_oku(yol):
    dene:
        ile ac(yol, "r", encoding="utf-8") as dosya:
            icerik = dosya.read()
            dondur icerik
    yakala FileNotFoundError:
        yazdir(f"Hata: {yol} bulunamadı")
        dondur hic

// Kullanım
icerik = dosya_oku("test.txt")
eger icerik:
    yazdir(icerik)
```

---

## 🎓 Öğrenme Yolu

### Seviye 1: Başlangıç (1-2 gün)
- ✅ Değişkenler, veri türleri
- ✅ Basit print/input
- ✅ if/else yapıları
- ✅ Basit döngüler

### Seviye 2: Orta (3-7 gün)
- ✅ Fonksiyonlar
- ✅ Listeler, sözlükler
- ✅ Dosya işlemleri
- ✅ Hata yakalama

### Seviye 3: İleri (1-2 hafta)
- ✅ OOP (sınıflar)
- ✅ Modüller
- ✅ List comprehension
- ✅ Lambda fonksiyonları

### Seviye 4: Uzman (Sürekli)
- ✅ Python kütüphaneleri
- ✅ Asenkron programlama
- ✅ Web geliştirme
- ✅ Veri bilimi

---

## 🔗 Kaynaklar

### Komutlar

```bash
# Yardım
kahin --yardim

# Versiyon
kahin --versiyon

# Normal çalıştırma
kahin program.kahin

# Debug modu
kahin program.kahin --debug
```

### Binary Konumu

```bash
/data/data/com.termux/files/usr/bin/kahin
```

### Örnek Dosyalar

```bash
~/kahin_projesi/ornekler/
```

---

## ✨ Son Notlar

### Neden Kahin?

1. **Türkçe**: Anadilinde kod yazmanın rahatlığı
2. **Python Gücü**: Tüm Python ekosistemi
3. **Kolay**: Basit ve anlaşılır sözdizimi
4. **Modern**: f-string, OOP, async destekli
5. **Hızlı**: Transpiler-based, sıfır overhead

### Katkıda Bulunun

Kahin açık kaynak bir projedir. Katkılarınızı bekliyoruz!

### İletişim

Sorularınız için:
- GitHub Issues
- E-posta
- Topluluk forumları

---

**🚀 Mutlu Kodlamalar!**

*Kahin v14.0 - Türkçe Programlama Dili*
