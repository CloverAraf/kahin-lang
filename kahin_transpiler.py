#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
KAHİN TRANSPİLER - KAYNAK KODU v14.0
═══════════════════════════════════════════════════════════════════════

Bu dosya Kahin dilinin ÇEKİRDEĞİDİR.
Kahin kodunu Python koduna çeviren transpiler burada.

NASIL ÇALIŞIR:
--------------
1. Kahin kodu (Türkçe) alır
2. 5 adımda Python koduna çevirir
3. Python kodunu döndürür

TRANSPİLER ALGORİTMASI:
-----------------------
ADIM 1: Yorum çevirisi (//, → #)
ADIM 2: String koruması (literal string'leri placeholder ile sakla)
ADIM 3: Kelime çevirisi (Türkçe → İngilizce, regex ile)
ADIM 4: f-string içi çevirisi (kod bloklarını çevir)
ADIM 5: String geri yükleme (placeholder'ları gerçek string'lerle değiştir)

ÖRNEK:
------
Kahin:  eger x > 5:
           yazdir("Büyük")

Python: if x > 5:
           print("Büyük")
"""

import re
import sys
import os

# ═══════════════════════════════════════════════════════════════════════
# TÜRKÇE → PYTHON KELİME HARİTASI
# ═══════════════════════════════════════════════════════════════════════

KELIME_HARITASI = {
    # ─────────────────────────────────────────────────────────────────
    # KONTROL YAPILARI (Control Flow)
    # ─────────────────────────────────────────────────────────────────
    "ice_aktar": "import",          # Modül içe aktarma
    "tanimla": "def",                # Fonksiyon tanımlama
    "eger": "if",                    # Koşul
    "degilse_eger": "elif",          # Alternatif koşul
    "degilse": "else",               # Koşul değilse
    "dondu_boyunca": "while",        # While döngüsü
    "her_biri_icin": "for",          # For döngüsü
    "icinde": "in",                  # İçinde operatörü
    "dondur": "return",              # Değer döndür
    "dur": "break",                  # Döngüyü kır
    "devam_et": "continue",          # Sonraki iterasyon
    "gec": "pass",                   # Hiçbir şey yapma
    "ile": "with",                   # Context manager
    "yukle": "yield",                # Generator yield
    "as": "as",                      # Alias

    # ─────────────────────────────────────────────────────────────────
    # HATA YAKALAMA (Exception Handling)
    # ─────────────────────────────────────────────────────────────────
    "dene": "try",                   # Hata yakalama başla
    "yakala": "except",              # Hata yakala
    "sonunda": "finally",            # Her durumda çalış
    "firlat": "raise",               # Hata fırlat
    "olumla": "assert",              # İddia et

    # ─────────────────────────────────────────────────────────────────
    # VERİ TÜRLERİ & SABİTLER (Data Types & Constants)
    # ─────────────────────────────────────────────────────────────────
    "dogru": "True",                 # Boolean True
    "yanlis": "False",               # Boolean False
    "hic": "None",                   # None değeri

    # ─────────────────────────────────────────────────────────────────
    # BUILT-IN FONKSİYONLAR (Built-in Functions)
    # ─────────────────────────────────────────────────────────────────
    "yazdir": "print",               # Ekrana yazdır
    "girdi": "input",                # Kullanıcıdan veri al
    "uzunluk": "len",                # Uzunluk
    "aralik": "range",               # Sayı aralığı
    "tam_sayi": "int",               # Integer
    "metin": "str",                  # String
    "ondalik": "float",              # Float
    "liste": "list",                 # Liste
    "sozluk": "dict",                # Sözlük
    "kume": "set",                   # Küme
    "demet": "tuple",                # Tuple
    "tur": "type",                   # Tür kontrolü
    "yardim": "help",                # Yardım
    "mutlak": "abs",                 # Mutlak değer
    "sirala": "sorted",              # Sıralama
    "ac": "open",                    # Dosya aç
    "topla": "sum",                  # Toplama
    "en_buyuk": "max",               # Maksimum
    "en_kucuk": "min",               # Minimum
    "bekle": "input",                # Input (alternatif)

    # ─────────────────────────────────────────────────────────────────
    # OOP (Object-Oriented Programming)
    # ─────────────────────────────────────────────────────────────────
    "sinif": "class",                # Sınıf tanımlama
    "sil": "del",                    # Nesne silme
    "kuresel": "global",             # Global değişken
    "yerel_degil": "nonlocal",       # Nonlocal değişken
    "lambda": "lambda",              # Lambda fonksiyon

    # ─────────────────────────────────────────────────────────────────
    # MODÜLLER (Modules - Türkçe takma adlar)
    # ─────────────────────────────────────────────────────────────────
    "sistem": "os",                  # İşletim sistemi
    "zaman": "time",                 # Zaman işlemleri
    "istek": "requests",             # HTTP istekleri
    "arayuz": "sys",                 # Sistem arayüzü
}


# ═══════════════════════════════════════════════════════════════════════
# TRANSPİLER FONKSİYONU - ANA ÇEKİRDEK
# ═══════════════════════════════════════════════════════════════════════

def metni_cevirme(kaynak_kod):
    """
    Kahin kodunu Python koduna çevirir.

    Bu fonksiyon Kahin'in KALBİDİR. Tüm çeviri işlemi burada yapılır.

    Algoritma (5 ADIM):
    -------------------
    1. Yorum Çevirisi
       Input : // Bu bir yorum
       Output: # Bu bir yorum

    2. String Koruması (Critical!)
       Input : yazdir("yanlis")
       Step  : yazdir(__STR_0__)  # "yanlis" saklandı
       Output: print(__STR_0__)   # yazdir→print, "yanlis" korundu

    3. Kelime Çevirisi (Regex)
       Input : eger x > 5:
       Regex : \beger\b → if  (\b = word boundary)
       Output: if x > 5:

    4. f-string İçi Çevirisi
       Input : f"Tür: {tur(x)}"
       Step  : {tur(x)} → {type(x)}
       Output: f"Tür: {type(x)}"

    5. String Geri Yükleme
       Input : print(__STR_0__)
       Output: print("yanlis")

    Args:
        kaynak_kod (str): Kahin kaynak kodu (Türkçe)

    Returns:
        str: Python kodu (İngilizce)

    Örnek:
        >>> kaynak = 'eger x > 5:\\n    yazdir("Büyük")'
        >>> python = metni_cevirme(kaynak)
        >>> print(python)
        if x > 5:
            print("Büyük")
    """

    # ═══════════════════════════════════════════════════════════════
    # ADIM 1: YORUM ÇEVİRİSİ (//, → #)
    # ═══════════════════════════════════════════════════════════════

    # Regex Açıklaması:
    # (?m)   : Multiline mode (her satır bağımsız)
    # ^      : Satır başı
    # \s*    : Sıfır veya daha fazla boşluk
    # //     : İki slash (yorum başlangıcı)

    kaynak_kod = re.sub(r'(?m)^\s*//', '#', kaynak_kod)

    # ═══════════════════════════════════════════════════════════════
    # ADIM 2: STRING KORUMASI (Literal Koruması)
    # ═══════════════════════════════════════════════════════════════

    # Neden gerekli?
    # --------------
    # String içindeki Türkçe kelimeler çevrilmemeli!
    # Örnek: "yanlis" → "False" OLMAMALI!

    # Strateji:
    # ---------
    # 1. Tüm string'leri bul
    # 2. Listeye ekle
    # 3. Placeholder koy (__STR_0__, __STR_1__, ...)
    # 4. Kelimeleri çevir (placeholder'lar etkilenmez)
    # 5. String'leri geri yükle

    metinler = []  # String saklama listesi

    def sakla(eslesme):
        """
        String'i sakla ve placeholder döndür.

        Callback fonksiyonu - re.sub() tarafından her eşleşme için çağrılır.
        """
        metinler.append(eslesme.group(0))
        return f"__STR_{len(metinler) - 1}__"

    # String'leri sırayla sakla
    # Önce f-string'ler, sonra normal string'ler

    # f-string: f"..." veya f'...'
    kaynak_kod = re.sub(r'f"[^"]*"', sakla, kaynak_kod)
    kaynak_kod = re.sub(r"f'[^']*'", sakla, kaynak_kod)

    # Normal string: "..." veya '...'
    kaynak_kod = re.sub(r'"[^"]*"', sakla, kaynak_kod)
    kaynak_kod = re.sub(r"'[^']*'", sakla, kaynak_kod)

    # Şimdi kaynak_kod'da tüm string'ler placeholder:
    # Örnek: yazdir(__STR_0__) eger __STR_1__ icinde ...

    # ═══════════════════════════════════════════════════════════════
    # ADIM 3: KELİME ÇEVİRİSİ (Türkçe → İngilizce)
    # ═══════════════════════════════════════════════════════════════

    # Regex Pattern Açıklaması:
    # -------------------------
    # \b        : Word boundary (kelime sınırı)
    # re.escape : Özel karakterleri escape et
    # \b        : Word boundary (kelime sonu)

    # Örnek:
    # ------
    # "eger" kelimesi:
    #   eger_test → eşleşmez (sınırda değil)
    #   eger      → eşleşir ✓
    #   test_eger → eşleşmez (sınırda değil)

    for turkce, ingilizce in KELIME_HARITASI.items():
        # Güvenli regex pattern oluştur
        regex_pattern = r'\b' + re.escape(turkce) + r'\b'

        # Türkçe kelimeyi İngilizce ile değiştir
        kaynak_kod = re.sub(regex_pattern, ingilizce, kaynak_kod)

    # Şimdi kod kısmı çevrildi ama string'ler hala placeholder:
    # Örnek: print(__STR_0__) if __STR_1__ in ...

    # ═══════════════════════════════════════════════════════════════
    # ADIM 4: f-STRING İÇİ ÇEVİRİSİ
    # ═══════════════════════════════════════════════════════════════

    # f-string'lerin içindeki {...} bloklarındaki kod da çevrilmeli!
    # Örnek: f"Tür: {tur(x)}" → f"Tür: {type(x)}"

    for indeks, metin in enumerate(metinler):
        # f-string mi kontrol et
        if metin.startswith('f"') or metin.startswith("f'"):

            def blok_cevir(blok_eslesme):
                """
                f-string içindeki {...} bloğunu çevir.

                Örnek:
                ------
                Input : {tur(x)}
                Step  : tur(x) → type(x)
                Output: {type(x)}
                """
                # Süslü parantez içindeki kodu al
                blok_icerik = blok_eslesme.group(1)

                # Blok içindeki Türkçe kelimeleri çevir
                for tr, en in KELIME_HARITASI.items():
                    blok_icerik = re.sub(
                        r'\b' + re.escape(tr) + r'\b',
                        en,
                        blok_icerik
                    )

                # Süslü parantezi geri ekle
                return '{' + blok_icerik + '}'

            # Regex: {...} bloklarını bul ve çevir
            # [^}]+ : Süslü parantez hariç herhangi bir karakter
            metin = re.sub(r'\{([^}]+)\}', blok_cevir, metin)

            # Değiştirilmiş string'i listeye geri yaz
            metinler[indeks] = metin

    # ═══════════════════════════════════════════════════════════════
    # ADIM 5: STRING GERİ YÜKLEME
    # ═══════════════════════════════════════════════════════════════

    # Placeholder'ları gerçek string'lerle değiştir
    # __STR_0__ → "yanlis"
    # __STR_1__ → f"Tür: {type(x)}"

    for indeks, metin in enumerate(metinler):
        placeholder = f"__STR_{indeks}__"
        kaynak_kod = kaynak_kod.replace(placeholder, metin)

    # ═══════════════════════════════════════════════════════════════
    # SONUÇ: Python kodu hazır!
    # ═══════════════════════════════════════════════════════════════

    return kaynak_kod


# ═══════════════════════════════════════════════════════════════════════
# TEST FONKSİYONU
# ═══════════════════════════════════════════════════════════════════════

def test_transpiler():
    """
    Transpiler'ı test et - örnek kodlarla.
    """
    print("═" * 70)
    print("KAHİN TRANSPİLER - TEST")
    print("═" * 70)

    test_kodlari = [
        # Test 1: Basit koşul
        ('eger x > 5:\n    yazdir("Büyük")', "Basit koşul"),

        # Test 2: String koruması
        ('yazdir("yanlis")', "String koruması (yanlis → False olmamalı)"),

        # Test 3: f-string
        ('yazdir(f"Tür: {tur(x)}")', "f-string içi çevirisi"),

        # Test 4: Döngü
        ('her_biri_icin i icinde aralik(5):\n    yazdir(i)', "For döngüsü"),

        # Test 5: Fonksiyon
        ('tanimla topla(a, b):\n    dondur a + b', "Fonksiyon tanımı"),
    ]

    for kahin_kod, aciklama in test_kodlari:
        print(f"\nTest: {aciklama}")
        print("-" * 70)
        print("Kahin Kodu:")
        print(kahin_kod)
        print("\nPython Kodu:")
        python_kod = metni_cevirme(kahin_kod)
        print(python_kod)
        print()


# ═══════════════════════════════════════════════════════════════════════
# MODÜL OLARAK KULLANIM
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Komut satırından çalıştırılırsa test et
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_transpiler()
    else:
        print("Kahin Transpiler Modülü")
        print("Kullanım:")
        print("  from kahin_transpiler import metni_cevirme")
        print("  python_kodu = metni_cevirme(kahin_kodu)")
        print("\nTest:")
        print("  python3 kahin_transpiler.py --test")
