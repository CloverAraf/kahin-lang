#!/bin/bash

cd ~/kahin_projesi

echo "Kahin Go Binary Build"
echo "====================="

# Step 1: Core archive
if [ ! -f "kahin_core.tar.gz" ]; then
    echo "[1/3] Python 3.11 core olusturuluyor..."
    python3 create_core.py
else
    echo "[1/3] Core archive mevcut"
fi

# Step 2: Go build
echo "[2/3] Go binary derleniyor..."

export CGO_ENABLED=1
export CGO_CFLAGS="-I/data/data/com.termux/files/usr/include/python3.11"
export CGO_LDFLAGS="-L/data/data/com.termux/files/usr/lib -lpython3.11"

if go build -ldflags="-s -w" -o kahin_embedded kahin.go; then
    SIZE=$(du -h kahin_embedded | cut -f1)
    echo "Derleme basarili: $SIZE"
else
    echo "Derleme hatasi"
    exit 1
fi

# Step 3: Test
echo "[3/3] Test..."
./kahin_embedded merhaba.kahin

echo ""
echo "Binary: ~/kahin_projesi/kahin_embedded"
