#!/usr/bin/env python3
"""
Kahin tek-binary derleme (Nuitka onefile).

Çıktı: dist/kahin  — tek dosya, Python kurulu OLMAYAN makinede çalışır.
kahin_lib (Türkçe stdlib) + kahin_rs (Rust hızlandırıcı) gömülür.

Çalıştır:  python build_nuitka.py
Gereksinim: pip install --user --break-system-packages nuitka, gcc, patchelf
Not: C derlemesi RAM yer (~2-3GB). LTO kapalı, jobs=2 — düşük RAM için.
"""
import os
import subprocess
import sys
from pathlib import Path

PROJE = Path(__file__).resolve().parent
KAHIN_LIB = PROJE / "kahin_lib"
DIST = PROJE / "dist"

# Lazy/dinamik import edilen tüm modüller — Nuitka statik analizle göremez,
# açıkça gömülmeli. kahin_cli içindeki fonksiyon-içi import'lar + kahin_lib.
GOMULECEK = [
    "kahin_lexer", "kahin_ast", "kahin_cache", "kahin_hata", "kahin_repl",
    "kahin_rs",          # Rust .so hızlandırıcı
    "dosya", "veri", "zaman",  # kahin_lib Türkçe stdlib (ice_aktar X)
]


def main():
    # kahin_lib modüllerinin (dosya/veri/zaman) derleme sırasında bulunması için
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(
        [str(KAHIN_LIB), env.get("PYTHONPATH", "")]
    ).rstrip(os.pathsep)

    # patchelf 0.18.0 (Arch repo) buggy — Nuitka reddediyor. pip sürümü (~0.17)
    # ~/.local/bin'de; onu PATH'in başına al.
    local_bin = str(Path.home() / ".local" / "bin")
    env["PATH"] = local_bin + os.pathsep + env.get("PATH", "")

    cmd = [
        sys.executable, "-m", "nuitka",
        "--onefile",
        "--standalone",
        "--output-dir=" + str(DIST),
        "--output-filename=kahin",
        "--assume-yes-for-downloads",
        "--lto=no",          # düşük RAM: LTO kapalı
        "--jobs=2",
        "--remove-output",   # ara .build dizinini temizle
        "--company-name=Kahin",
        "--product-name=Kahin",
        "--product-version=16.0",
    ]
    cmd += [f"--include-module={m}" for m in GOMULECEK]
    cmd.append(str(PROJE / "kahin_cli.py"))

    print("Derleme başlıyor (RAM yoğun, birkaç dakika)...")
    print(" ".join(cmd))
    r = subprocess.run(cmd, env=env)
    if r.returncode != 0:
        print("HATA: derleme başarısız", file=sys.stderr)
        return r.returncode

    cikti = DIST / "kahin"
    print(f"\nTamam: {cikti}")
    print("Taşı: tek dosya, Python gerekmez (Linux x86-64).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
