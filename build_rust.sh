#!/usr/bin/env bash
# Rust tokenizer derle proje köküne kahin_rs.so olarak kurun
# maturin gerekmez cargo + manuel kopya
set -e
PROJE="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJE/kahin_rs"
# --remap-path-prefix: derleme yollarini (ev dizini, cargo registry) anonimlestir
# binaryye kisisel mutlak yol gomulmesin
RUSTFLAGS="--remap-path-prefix=$HOME=~ --remap-path-prefix=$PWD=." \
  PYO3_PYTHON="$(command -v python3)" cargo build --release
cp target/release/libkahin_rs.so "$PROJE/kahin_rs.so"
echo "SO kuruldu: $PROJE/kahin_rs.so" #build alınan
python3 -c "import sys; sys.path.insert(0,'$PROJE'); import kahin_rs; print('import OK')"
