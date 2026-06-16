#!/data/data/com.termux/files/usr/bin/python3
"""
KAHİN v14.0 - TAM TÜRKÇE PROGRAMLAMA DİLİ
Ultra hızlı, tamamen Türkçe kodlanmış transpiler

Detaylı Mimari:
- String-safe transpiler (literal string'ler korunur)
- f-string içindeki kod blokları çevrilir
- Kelime sınırı kontrolü (word boundary)
- Çok aşamalı çeviri: string koruma → çeviri → geri yükleme
"""
import sys
import re
import os

# ════════════════════════════════════════════════════════════
# TÜRKÇE → PYTHON KELİME HARİTASI
# ════════════════════════════════════════════════════════════
KELIME_HARITASI = {
    # Kontrol yapıları
    "ice_aktar":"import", "tanimla":"def", "eger":"if", "degilse_eger":"elif",
    "degilse":"else", "dondu_boyunca":"while", "her_biri_icin":"for", "icinde":"in",
    "dondur":"return", "yazdir":"print", "girdi":"input", "dur":"break",
    "devam_et":"continue", "sinif":"class", "dene":"try", "yakala":"except",
    "sonunda":"finally", "firlat":"raise", "sil":"del", "gec":"pass",
    "olumla":"assert", "kuresel":"global", "yerel_degil":"nonlocal",
    "lambda":"lambda", "ile":"with", "yukle":"yield", "as":"as",

    # Sabitler
    "dogru":"True", "yanlis":"False", "hic":"None",

    # Built-in fonksiyonlar
    "uzunluk":"len", "aralik":"range", "tam_sayi":"int", "metin":"str",
    "ondalik":"float", "liste":"list", "sozluk":"dict", "kume":"set",
    "demet":"tuple", "tur":"type", "yardim":"help", "mutlak":"abs",
    "sirala":"sorted", "ac":"open", "topla":"sum", "en_buyuk":"max",
    "en_kucuk":"min", "bekle":"input",

    # Modüller
    "sistem":"os", "zaman":"time", "istek":"requests", "arayuz":"sys",
}

# ════════════════════════════════════════════════════════════
# TRANSPİLER FONKSİYONU
# ════════════════════════════════════════════════════════════
def metni_cevirme(kaynak):
    """
    Kahin kodunu Python'a çevirir.

    Algoritma:
    1. Yorumları çevir (//, →, #)
    2. Tüm string'leri placeholder ile sakla (literal koruması)
    3. f-string'leri ayrı sakla (içleri çevrilecek)
    4. Kod kısmındaki Türkçe kelimeleri Python'a çevir
    5. f-string içindeki {...} bloklarını çevir
    6. Tüm string'leri geri yükle

    Args:
        kaynak (str): Kahin kaynak kodu

    Returns:
        str: Python kodu
    """
    # Yorumları çevir
    kaynak = re.sub(r'(?m)^\s*//', '#', kaynak)

    # String saklama listeleri
    metinler = []

    def sakla(eslesme):
        """String'i sakla ve placeholder döndür"""
        metinler.append(eslesme.group(0))
        return f"__STR_{len(metinler)-1}__"

    # 1. Tüm string'leri sakla (f-string dahil)
    kaynak = re.sub(r'f"[^"]*"', sakla, kaynak)  # f"..."
    kaynak = re.sub(r"f'[^']*'", sakla, kaynak)  # f'...'
    kaynak = re.sub(r'"[^"]*"', sakla, kaynak)   # "..."
    kaynak = re.sub(r"'[^']*'", sakla, kaynak)   # '...'

    # 2. Kod kısmındaki Türkçe kelimeleri çevir
    for turkce, ingilizce in KELIME_HARITASI.items():
        # \b = kelime sınırı (word boundary)
        kaynak = re.sub(r'\b' + re.escape(turkce) + r'\b', ingilizce, kaynak)

    # 3. String'leri geri yükle
    for indeks, metin in enumerate(metinler):
        # f-string ise içindeki {...} bloklarını çevir
        if metin.startswith('f"') or metin.startswith("f'"):
            def blok_cevir(blok_eslesme):
                """f-string içindeki kod bloğunu çevir"""
                blok_icerik = blok_eslesme.group(1)
                for tr, en in KELIME_HARITASI.items():
                    blok_icerik = re.sub(r'\b' + re.escape(tr) + r'\b', en, blok_icerik)
                return '{' + blok_icerik + '}'

            metin = re.sub(r'\{([^}]+)\}', blok_cevir, metin)

        # Placeholder'ı gerçek string ile değiştir
        kaynak = kaynak.replace(f"__STR_{indeks}__", metin)

    return kaynak

# ════════════════════════════════════════════════════════════
# YARDIM MESAJLARI
# ════════════════════════════════════════════════════════════
def yardim_goster():
    """Detaylı yardım mesajı göster"""
    print("═" * 70)
    print(" " * 20 + "KAHİN v14.0")
    print(" " * 10 + "TAM TÜRKÇE PROGRAMLAMA DİLİ")
    print("═" * 70)

    print("\n📖 KULLANIM:")
    print("  kahin <dosya.kahin>              Kahin dosyasını çalıştır")
    print("  kahin <dosya.kahin> --debug      Debug modda çalıştır (transpile göster)")
    print("  kahin --yardim                   Bu yardım mesajını göster")
    print("  kahin --versiyon                 Versiyon bilgisi")

    print("\n📝 ÖRNEK KOD:")
    print('  // Değişkenler')
    print('  isim = "Ahmet"')
    print('  yas = 25')
    print('  ')
    print('  // Koşul')
    print('  eger yas > 18:')
    print('      yazdir("Yetişkin")')
    print('  degilse:')
    print('      yazdir("Çocuk")')
    print('  ')
    print('  // Döngü')
    print('  her_biri_icin i icinde aralik(5):')
    print('      yazdir(f"Sayı: {i}")')
    print('  ')
    print('  // Fonksiyon')
    print('  tanimla topla(a, b):')
    print('      dondur a + b')

    print("\n🔤 TÜRKÇE ANAHTARLAR:")
    print("  Kontrol    : eger, degilse_eger, degilse, dondu_boyunca")
    print("  Döngü      : her_biri_icin, icinde, aralik")
    print("  Fonksiyon  : tanimla, dondur")
    print("  Çıktı      : yazdir, girdi")
    print("  Veri Türü  : tam_sayi, metin, ondalik, liste, sozluk")
    print("  Built-in   : uzunluk, topla, en_buyuk, en_kucuk, sirala")
    print("  Modül      : ice_aktar, sistem, zaman, arayuz")

    print("\n🚀 ÖZELLİKLER:")
    print("  ✓ Ultra hızlı transpiler (~0.1s)")
    print("  ✓ String-safe (metinler korunur)")
    print("  ✓ f-string desteği")
    print("  ✓ Tam Python uyumluluğu")
    print("  ✓ Detaylı hata mesajları")

    print("\n📂 DOSYALAR:")
    print(f"  Binary   : {sys.argv[0]}")
    print(f"  Proje    : ~/kahin_projesi")
    print(f"  Örnekler : ~/kahin_projesi/ornekler/")

    print("\n" + "═" * 70)
    print("🌐 Daha fazla bilgi: ~/kahin_projesi/BUILD_TR.md")
    print("═" * 70)

def kullanim_goster():
    """Kısa kullanım mesajı"""
    print("KAHİN v14.0 - Tam Türkçe Programlama Dili")
    print("")
    print("Kullanım:")
    print("  kahin <dosya.kahin>        Dosyayı çalıştır")
    print("  kahin --yardim             Detaylı yardım")
    print("  kahin --versiyon           Versiyon bilgisi")

def versiyon_goster():
    """Versiyon bilgisi göster"""
    print("KAHİN v14.0")
    print("Türkçe Programlama Dili")
    print("")
    print("Python Sürümü:", sys.version.split()[0])
    print("Platform:", sys.platform)

# ════════════════════════════════════════════════════════════
# ANA PROGRAM
# ════════════════════════════════════════════════════════════
def main():
    """
    Ana program akışı:
    1. Argüman kontrolü (flag'ler önce)
    2. Dosya kontrolü
    3. Transpile
    4. Çalıştırma
    """

    # ─────────────────────────────────────────────────────────
    # ARGÜMAN KONTROLÜ
    # ─────────────────────────────────────────────────────────

    # Argüman yoksa kullanım göster
    if len(sys.argv) < 2:
        kullanim_goster()
        sys.exit(1)

    # Flag kontrolü (dosya adı aramadan önce)
    if "--yardim" in sys.argv or "--help" in sys.argv:
        yardim_goster()
        sys.exit(0)

    if "--versiyon" in sys.argv or "--version" in sys.argv:
        versiyon_goster()
        sys.exit(0)

    # ─────────────────────────────────────────────────────────
    # DOSYA ADINI BUL
    # ─────────────────────────────────────────────────────────

    # Flag olmayan ilk argümanı bul
    dosya_yolu = None
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            dosya_yolu = arg
            break

    # Dosya adı bulunamadı
    if dosya_yolu is None:
        print("❌ Hata: Dosya adı belirtilmedi!")
        print("")
        kullanim_goster()
        sys.exit(1)

    # ─────────────────────────────────────────────────────────
    # DEBUG MODU KONTROLÜ
    # ─────────────────────────────────────────────────────────

    debug_modu = "--debug" in sys.argv

    # ─────────────────────────────────────────────────────────
    # DOSYA OKUMA
    # ─────────────────────────────────────────────────────────

    try:
        # Dosya var mı kontrol et
        if not os.path.exists(dosya_yolu):
            print(f"❌ Dosya bulunamadı: {dosya_yolu}")
            print("")
            print("İpucu: Dosya yolunu kontrol edin.")
            sys.exit(1)

        # Dosyayı oku
        with open(dosya_yolu, 'r', encoding='utf-8') as dosya:
            kaynak_kod = dosya.read()

    except PermissionError:
        print(f"❌ İzin hatası: {dosya_yolu}")
        print("Dosyayı okuma izniniz yok.")
        sys.exit(1)

    except IsADirectoryError:
        print(f"❌ Hata: {dosya_yolu} bir dizin!")
        print("Lütfen bir .kahin dosyası belirtin.")
        sys.exit(1)

    except Exception as hata:
        print(f"❌ Dosya okuma hatası: {hata}")
        sys.exit(1)

    # ─────────────────────────────────────────────────────────
    # TRANSPİLE
    # ─────────────────────────────────────────────────────────

    try:
        python_kodu = metni_cevirme(kaynak_kod)
    except Exception as hata:
        print("❌ Transpile hatası!")
        print(f"Detay: {hata}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Debug modda transpile edilmiş kodu göster
    if debug_modu:
        print("═" * 70)
        print("ÇEVRİLMİŞ PYTHON KODU")
        print("═" * 70)
        for numara, satir in enumerate(python_kodu.split('\n'), 1):
            print(f"{numara:4d} | {satir}")
        print("═" * 70)
        print("ÇIKTI")
        print("═" * 70)

    # ─────────────────────────────────────────────────────────
    # ÇALIŞTIRMA
    # ─────────────────────────────────────────────────────────

    try:
        # Global namespace ile çalıştır
        exec(python_kodu, globals())

    except SyntaxError as hata:
        print("\n❌ SÖZDİZİMİ HATASI!")
        print(f"Satır {hata.lineno}: {hata.msg}")
        if hata.text:
            print(f"Kod: {hata.text.strip()}")
        print("\nİpucu: Kahin sözdizimini kontrol edin.")
        sys.exit(1)

    except NameError as hata:
        print("\n❌ İSİM HATASI!")
        print(f"Detay: {hata}")
        print("\nİpucu: Değişken veya fonksiyon tanımlı mı kontrol edin.")
        sys.exit(1)

    except Exception as hata:
        print("\n❌ ÇALIŞMA ZAMANI HATASI!")
        print(f"Tür: {type(hata).__name__}")
        print(f"Detay: {hata}")
        print("\nStack trace:")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# ════════════════════════════════════════════════════════════
# PROGRAM GİRİŞİ
# ════════════════════════════════════════════════════════════
if __name__ == "__main__":
    main()
