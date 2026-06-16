#!/usr/bin/env bash
# Rust tokenizer derle + proje köküne kahin_rs.so olarak kur.
# maturin gerekmez; cargo + manuel kopya.
set -e
PROJE="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJE/kahin_rs"
PYO3_PYTHON="$(command -v python3)" cargo build --release
cp target/release/libkahin_rs.so "$PROJE/kahin_rs.so"
echo "Kuruldu: $PROJE/kahin_rs.so"
python3 -c "import sys; sys.path.insert(0,'$PROJE'); import kahin_rs; print('import OK')"
