#!/usr/bin/env python3
import tarfile
import subprocess
import os
from pathlib import Path

os.chdir(Path.home() / "kahin_projesi")

# Step 1: Create core archive
print("[1/2] Python 3.11 core olusturuluyor...")
python_lib = Path("/data/data/com.termux/files/usr/lib/python3.11")

if not python_lib.exists():
    print("HATA: Python 3.11 bulunamadi")
    exit(1)

with tarfile.open("kahin_core.tar.gz", "w:gz") as tar:
    tar.add(python_lib, arcname="lib/python3.11")

size = Path("kahin_core.tar.gz").stat().st_size / (1024*1024)
print(f"  Tamam: {size:.1f} MB")

# Step 2: Go build
print("[2/2] Go binary derleniyor...")

env = os.environ.copy()
env["CGO_ENABLED"] = "1"
env["CGO_CFLAGS"] = "-I/data/data/com.termux/files/usr/include/python3.11"
env["CGO_LDFLAGS"] = "-L/data/data/com.termux/files/usr/lib -lpython3.11"

result = subprocess.run(
    ["go", "build", "-ldflags", "-s -w", "-o", "kahin_embedded", "kahin.go"],
    env=env,
    capture_output=True,
    text=True
)

if result.returncode == 0:
    size = Path("kahin_embedded").stat().st_size / (1024*1024)
    print(f"  Basarili: {size:.1f} MB")
    os.chmod("kahin_embedded", 0o755)
    print("\nBinary: ~/kahin_projesi/kahin_embedded")
    print("Test: ./kahin_embedded merhaba.kahin")
else:
    print("HATA:")
    print(result.stderr)
    exit(1)
