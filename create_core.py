#!/usr/bin/env python3
"""
Python 3.11 core archive olusturucu
"""

import tarfile
import sys
from pathlib import Path

python_lib = Path("/data/data/com.termux/files/usr/lib/python3.11")
output = Path.home() / "kahin_projesi" / "kahin_core.tar.gz"

if not python_lib.exists():
    print(f"Hata: {python_lib} bulunamadi")
    print("Python 3.11 kurulu degil")
    sys.exit(1)

print(f"Python 3.11 paketleniyor...")
print(f"Kaynak: {python_lib}")
print(f"Hedef: {output}")

with tarfile.open(output, "w:gz") as tar:
    tar.add(python_lib, arcname="lib/python3.11")

size_mb = output.stat().st_size / (1024 * 1024)
print(f"Tamam: {size_mb:.1f} MB")
