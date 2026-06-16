#!/usr/bin/env python3
"""
KAHİN BUILD SCRIPT
Binary'i global konuma kopyalar
"""
import shutil
import os
import sys

def build():
    print("═" * 60)
    print("KAHİN v14.0 - BUILD SCRIPT")
    print("═" * 60)

    source = os.path.expanduser("~/kahin_projesi/kahin_binary.py")
    target = "/data/data/com.termux/files/usr/bin/kahin"

    print(f"\n[1/3] Kaynak kontrol ediliyor...")
    if not os.path.exists(source):
        print(f"❌ Hata: {source} bulunamadı!")
        sys.exit(1)
    print(f"✓ Kaynak mevcut: {source}")

    print(f"\n[2/3] Binary kopyalanıyor...")
    try:
        shutil.copy(source, target)
        print(f"✓ Kopyalandı: {target}")
    except PermissionError:
        print("❌ İzin hatası! 'pkg install python' deneyin")
        sys.exit(1)

    print(f"\n[3/3] Yetkilendiriliyor...")
    os.chmod(target, 0o755)
    print(f"✓ Executable yapıldı")

    print("\n" + "═" * 60)
    print("✅ BUILD BAŞARILI!")
    print("═" * 60)
    print(f"\nKullanım:")
    print(f"  kahin --versiyon")
    print(f"  kahin program.kahin")

if __name__ == "__main__":
    build()
