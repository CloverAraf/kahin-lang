#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
REGEX TEST & AÇIKLAMA - Kahin Transpiler'da Regex Kullanımı
═══════════════════════════════════════════════════════════════════════

Bu dosya Kahin transpiler'ında kullanılan REGEX pattern'lerini
test eder ve açıklar.
"""

import re


def test_word_boundary():
    """
    Word Boundary (\\b) Testi

    \\b : Kelime sınırını işaret eder
          - Harf/rakam ile harf/rakam-olmayan karakter arası
          - String başı/sonu

    NEDEN ÖNEMLİ:
    -------------
    "eger" kelimesini değiştirirken "eger_test" değişmemeli!
    """

    print("═" * 70)
    print("WORD BOUNDARY (\\b) TESTİ")
    print("═" * 70)

    test_metni = "eger_test eger test_eger egerlik bir_eger eger"

    print(f"Orijinal metin:")
    print(f"  {test_metni}")
    print()

    # ─────────────────────────────────────────────────────────────────
    # Test 1: \\b OLMADAN (YANLIŞ!)
    # ─────────────────────────────────────────────────────────────────

    yanlis = re.sub("eger", "if", test_metni)

    print("Test 1: \\b OLMADAN (YANLIŞ!)")
    print(f"  Pattern: \"eger\"")
    print(f"  Sonuç  : {yanlis}")
    print(f"  ❌ SORUN: eger_test → if_test (yanlış!)")
    print()

    # ─────────────────────────────────────────────────────────────────
    # Test 2: \\b İLE (DOĞRU!)
    # ─────────────────────────────────────────────────────────────────

    dogru = re.sub(r"\\beger\\b", "if", test_metni)

    print("Test 2: \\b İLE (DOĞRU!)")
    print(f"  Pattern: r\"\\beger\\b\"")
    print(f"  Sonuç  : {dogru}")
    print(f"  ✓ DOĞRU: Sadece bağımsız 'eger' değişti")
    print()

    # ─────────────────────────────────────────────────────────────────
    # Açıklama
    # ─────────────────────────────────────────────────────────────────

    print("Detaylı Açıklama:")
    print("  eger_test   → Eşleşmez (öncesinde '_' var, kelime sınırı değil)")
    print("  eger        → Eşleşir ✓ (kelime sınırında)")
    print("  test_eger   → Eşleşmez (sonrasında '_' var)")
    print("  egerlik     → Eşleşmez (sonrasında harf var)")


def test_string_protection():
    """
    String Koruması Testi

    SORUN:
    ------
    String içindeki "yanlis" kelimesi "False" olmamalı!

    ÇÖZÜM:
    ------
    1. String'leri sakla (placeholder)
    2. Kelimeleri değiştir
    3. String'leri geri yükle
    """

    print("\\n" + "═" * 70)
    print("STRING KORUMASI TESTİ")
    print("═" * 70)

    kaynak = 'yazdir("yanlis") eger yanlis:'

    print(f"Orijinal kod:")
    print(f"  {kaynak}")
    print()

    # ─────────────────────────────────────────────────────────────────
    # YANLIŞ YÖNTEM: Direkt değiştirme
    # ─────────────────────────────────────────────────────────────────

    yanlis_yontem = kaynak.replace("yanlis", "False")
    yanlis_yontem = yanlis_yontem.replace("yazdir", "print")

    print("YANLIŞ YÖNTEM (Direkt değiştirme):")
    print(f"  {yanlis_yontem}")
    print(f"  ❌ SORUN: String içindeki 'yanlis' → 'False' oldu!")
    print()

    # ─────────────────────────────────────────────────────────────────
    # DOĞRU YÖNTEM: String koruması
    # ─────────────────────────────────────────────────────────────────

    print("DOĞRU YÖNTEM (String koruması):")

    # Adım 1: String'i sakla
    metinler = []

    def sakla(m):
        metinler.append(m.group(0))
        return f"__STR_{len(metinler)-1}__"

    adim1 = re.sub(r'"[^"]*"', sakla, kaynak)
    print(f"  Adım 1 (String sakla): {adim1}")
    print(f"          Saklanan     : {metinler}")

    # Adım 2: Kelimeleri değiştir
    adim2 = adim1.replace("yanlis", "False")
    adim2 = adim2.replace("yazdir", "print")
    print(f"  Adım 2 (Kelime değiştir): {adim2}")

    # Adım 3: String'i geri yükle
    for i, metin in enumerate(metinler):
        adim2 = adim2.replace(f"__STR_{i}__", metin)

    print(f"  Adım 3 (Geri yükle)     : {adim2}")
    print(f"  ✓ DOĞRU: String içindeki 'yanlis' korundu!")


def test_fstring_içi():
    """
    f-string İçi Çevirisi

    SORUN:
    ------
    f"Tür: {tur(x)}" içindeki "tur" çevrilmeli!

    ÇÖZÜM:
    ------
    {...} bloklarını bul ve içlerini çevir
    """

    print("\\n" + "═" * 70)
    print("f-STRING İÇİ ÇEVİRİSİ TESTİ")
    print("═" * 70)

    f_string = 'f"Tür: {tur(x)}, Uzunluk: {uzunluk(liste)}"'

    print(f"Orijinal:")
    print(f"  {f_string}")
    print()

    # {...} bloklarını bul ve çevir
    def blok_cevir(m):
        icerik = m.group(1)  # Süslü parantez içindeki kod
        icerik = icerik.replace("tur", "type")
        icerik = icerik.replace("uzunluk", "len")
        return '{' + icerik + '}'

    sonuc = re.sub(r'\\{([^}]+)\\}', blok_cevir, f_string)

    print("Sonuç:")
    print(f"  {sonuc}")
    print()

    print("Açıklama:")
    print("  Regex: r'\\{([^}]+)\\}'")
    print("    \\{       : Açılış süslü parantezi")
    print("    ([^}]+) : Süslü parantez olmayan karakterler (capture group)")
    print("    \\}       : Kapanış süslü parantezi")


def test_multiline_comment():
    """
    Çok Satırlı Yorum Çevirisi

    //, → #
    """

    print("\\n" + "═" * 70)
    print("ÇOK SATIRLI YORUM ÇEVİRİSİ")
    print("═" * 70)

    kod = """// Bu bir yorum
sayi = 10
    // Girintili yorum
eger sayi > 5:
    yazdir("Büyük")
// Son yorum"""

    print("Orijinal:")
    print(kod)
    print()

    # Regex: Her satır başındaki // → #
    sonuc = re.sub(r'(?m)^\\s*//', '#', kod)

    print("Sonuç:")
    print(sonuc)
    print()

    print("Regex Açıklaması:")
    print("  (?m)  : Multiline mode (her satır bağımsız)")
    print("  ^     : Satır başı")
    print("  \\s*   : Sıfır veya daha fazla boşluk")
    print("  //    : İki slash")


def main():
    """Tüm testleri çalıştır"""

    print("\\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "KAHİN REGEX TEST SÜİTİ" + " " * 31 + "║")
    print("╚" + "═" * 68 + "╝")
    print()

    test_word_boundary()
    test_string_protection()
    test_fstring_içi()
    test_multiline_comment()

    print("\\n" + "═" * 70)
    print("✅ TÜM TESTLER TAMAMLANDI")
    print("═" * 70)


if __name__ == "__main__":
    main()
