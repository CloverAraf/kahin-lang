#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
KAHİN FULL BUILD SCRIPT v14.0
═══════════════════════════════════════════════════════════════════════

Bu script transpiler'ı ve yardımcı modülleri birleştirip
tek bir executable binary oluşturur.

NASIL ÇALIŞIR:
--------------
1. kahin_transpiler.py'yi oku
2. Ana kahin binary'sini oluştur (transpiler + CLI)
3. /usr/bin/kahin konumuna kur
4. Executable yap

ÇIKTI:
------
/usr/bin/kahin - Çalışabilir Kahin binary'si
"""

import os
import sys
import shutil
from pathlib import Path


def build_binary():
    """Ana binary'i oluştur ve kur"""

    print("═" * 70)
    print("KAHİN FULL BUILD v14.0")
    print("═" * 70)

    # ─────────────────────────────────────────────────────────────────
    # ADIM 1: Transpiler'ı oku
    # ─────────────────────────────────────────────────────────────────

    print("\n[1/5] Transpiler modülü okunuyor...")

    transpiler_path = Path.home() / "kahin_projesi" / "kahin_transpiler.py"

    if not transpiler_path.exists():
        print(f"❌ Hata: {transpiler_path} bulunamadı!")
        print("Önce kahin_transpiler.py oluşturulmalı.")
        sys.exit(1)

    with open(transpiler_path, 'r', encoding='utf-8') as f:
        transpiler_kod = f.read()

    print(f"✓ Transpiler okundu: {len(transpiler_kod)} karakter")

    # ─────────────────────────────────────────────────────────────────
    # ADIM 2: Ana CLI kodunu ekle
    # ─────────────────────────────────────────────────────────────────

    print("\n[2/5] CLI kodu ekleniyor...")

    # CLI kodu (argüman parse, dosya okuma, exec)
    cli_kod = '''

# ═══════════════════════════════════════════════════════════════════════
# YARDIM MESAJLARI
# ═══════════════════════════════════════════════════════════════════════

def yardim_goster():
    """Detaylı yardım mesajı"""
    print("═" * 70)
    print(" " * 20 + "KAHİN v14.0")
    print(" " * 10 + "TAM TÜRKÇE PROGRAMLAMA DİLİ")
    print("═" * 70)
    print("\\n📖 KULLANIM:")
    print("  kahin <dosya.kahin>              Dosyayı çalıştır")
    print("  kahin <dosya.kahin> --debug      Debug modu")
    print("  kahin --yardim                   Yardım")
    print("  kahin --versiyon                 Versiyon")
    print("\\n🚀 Kaynak: ~/kahin_projesi/")
    print("═" * 70)

def kullanim_goster():
    """Kısa kullanım"""
    print("KAHİN v14.0 - Türkçe Programlama Dili")
    print("\\nKullanım:")
    print("  kahin <dosya.kahin>")
    print("  kahin --yardim")

def versiyon_goster():
    """Versiyon bilgisi"""
    print("KAHİN v14.0")
    print("Türkçe Programlama Dili")
    print(f"\\nPython: {sys.version.split()[0]}")


# ═══════════════════════════════════════════════════════════════════════
# ANA PROGRAM
# ═══════════════════════════════════════════════════════════════════════

def main():
    """Ana CLI"""

    # Argüman yoksa
    if len(sys.argv) < 2:
        kullanim_goster()
        sys.exit(1)

    # Flag'leri kontrol et
    if "--yardim" in sys.argv or "--help" in sys.argv:
        yardim_goster()
        sys.exit(0)

    if "--versiyon" in sys.argv or "--version" in sys.argv:
        versiyon_goster()
        sys.exit(0)

    # Dosya adını bul
    dosya_yolu = None
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            dosya_yolu = arg
            break

    if dosya_yolu is None:
        print("❌ Dosya adı belirtilmedi!")
        kullanim_goster()
        sys.exit(1)

    # Debug modu
    debug = "--debug" in sys.argv

    # Dosyayı oku
    try:
        if not os.path.exists(dosya_yolu):
            print(f"❌ Dosya bulunamadı: {dosya_yolu}")
            sys.exit(1)

        with open(dosya_yolu, 'r', encoding='utf-8') as f:
            kahin_kod = f.read()

    except Exception as e:
        print(f"❌ Dosya okuma hatası: {e}")
        sys.exit(1)

    # Transpile et
    try:
        python_kod = metni_cevirme(kahin_kod)
    except Exception as e:
        print(f"❌ Transpile hatası: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Debug
    if debug:
        print("═" * 70)
        print("ÇEVRİLMİŞ PYTHON KODU")
        print("═" * 70)
        for n, line in enumerate(python_kod.split('\\n'), 1):
            print(f"{n:4d} | {line}")
        print("═" * 70)
        print("ÇIKTI")
        print("═" * 70)

    # Çalıştır
    try:
        exec(python_kod, globals())
    except Exception as e:
        print(f"\\n❌ Çalışma Hatası: {type(e).__name__}")
        print(f"Detay: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
'''

    # ─────────────────────────────────────────────────────────────────
    # ADIM 3: Binary'i birleştir
    # ─────────────────────────────────────────────────────────────────

    print("\n[3/5] Binary birleştiriliyor...")

    # Shebang + transpiler + CLI
    binary_icerik = (
        "#!/usr/bin/env python3\n"
        + transpiler_kod
        + cli_kod
    )

    # Geçici dosyaya yaz
    temp_binary = Path.home() / "kahin_projesi" / "kahin_temp.py"
    with open(temp_binary, 'w', encoding='utf-8') as f:
        f.write(binary_icerik)

    print(f"✓ Binary oluşturuldu: {len(binary_icerik)} karakter")

    # ─────────────────────────────────────────────────────────────────
    # ADIM 4: Global konuma kopyala
    # ─────────────────────────────────────────────────────────────────

    print("\n[4/5] Global konuma kuruluyor...")

    target = "/data/data/com.termux/files/usr/bin/kahin"

    try:
        shutil.copy(temp_binary, target)
        print(f"✓ Kopyalandı: {target}")
    except PermissionError:
        print("❌ İzin hatası!")
        sys.exit(1)

    # ─────────────────────────────────────────────────────────────────
    # ADIM 5: Executable yap
    # ─────────────────────────────────────────────────────────────────

    print("\n[5/5] Yetkilendiriliyor...")

    os.chmod(target, 0o755)
    print("✓ Executable yapıldı")

    # Temp dosyayı sil
    temp_binary.unlink()

    # ─────────────────────────────────────────────────────────────────
    # SONUÇ
    # ─────────────────────────────────────────────────────────────────

    print("\n" + "═" * 70)
    print("✅ BUILD BAŞARILI!")
    print("═" * 70)
    print(f"\nBinary: {target}")
    print(f"Boyut: {os.path.getsize(target) / 1024:.1f} KB")
    print("\nTest:")
    print("  kahin --versiyon")
    print("  kahin merhaba.kahin")


if __name__ == "__main__":
    build_binary()
