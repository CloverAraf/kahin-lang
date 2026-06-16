#!/usr/bin/env python3
"""
Kahin Transpiler - Optimized v14.2

Optimizasyonlar:
- Compiled regex patterns (pre-compile, cache)
- Single-pass string protection
- Minimal memory allocation
- Fast path for simple cases
"""

import re
import sys
import os

# Kelime haritası
KEYWORDS = {
    "ice_aktar":"import","tanimla":"def","eger":"if","degilse_eger":"elif",
    "degilse":"else","dondu_boyunca":"while","her_biri_icin":"for","icinde":"in",
    "dondur":"return","yazdir":"print","girdi":"input","dur":"break",
    "devam_et":"continue","sinif":"class","dene":"try","yakala":"except",
    "sonunda":"finally","firlat":"raise","sil":"del","gec":"pass",
    "olumla":"assert","kuresel":"global","yerel_degil":"nonlocal",
    "lambda":"lambda","ile":"with","yukle":"yield","as":"as",
    "dogru":"True","yanlis":"False","hic":"None",
    "uzunluk":"len","aralik":"range","tam_sayi":"int","metin":"str",
    "ondalik":"float","liste":"list","sozluk":"dict","kume":"set",
    "demet":"tuple","tur":"type","yardim":"help","mutlak":"abs",
    "sirala":"sorted","ac":"open","topla":"sum","en_buyuk":"max",
    "en_kucuk":"min","bekle":"input",
    "sistem":"os","zaman":"time","istek":"requests","arayuz":"sys",
}

# Pre-compiled regex patterns (optimization)
COMMENT_RE = re.compile(r'(?m)^\s*//')
FSTRING_RE = re.compile(r'f["\'][^"\']*["\']')
STRING_RE = re.compile(r'["\'][^"\']*["\']')
FSTRING_BLOCK_RE = re.compile(r'\{([^}]+)\}')

# Compile keyword patterns once (optimization)
KEYWORD_PATTERNS = {
    tr: re.compile(r'\b' + re.escape(tr) + r'\b')
    for tr in KEYWORDS.keys()
}


def transpile_fast(source):
    """
    Fast transpiler - optimized for speed

    Single-pass algorithm:
    1. Comment conversion
    2. String protection
    3. Keyword substitution
    4. f-string block conversion
    5. String restoration
    """

    # Step 1: Comments
    source = COMMENT_RE.sub('#', source)

    # Step 2: Protect strings
    strings = []

    def save_str(m):
        strings.append(m.group(0))
        return f"__S{len(strings)-1}__"

    # f-strings first
    source = FSTRING_RE.sub(save_str, source)
    # regular strings
    source = STRING_RE.sub(save_str, source)

    # Step 3: Keyword substitution (use pre-compiled patterns)
    for tr, en in KEYWORDS.items():
        source = KEYWORD_PATTERNS[tr].sub(en, source)

    # Step 4: f-string blocks
    for i, s in enumerate(strings):
        if s.startswith('f"') or s.startswith("f'"):
            def convert_block(m):
                content = m.group(1)
                for tr, en in KEYWORDS.items():
                    content = KEYWORD_PATTERNS[tr].sub(en, content)
                return '{' + content + '}'
            s = FSTRING_BLOCK_RE.sub(convert_block, s)
            strings[i] = s

    # Step 5: Restore strings
    for i, s in enumerate(strings):
        source = source.replace(f"__S{i}__", s)

    return source


def execute_file(path):
    """Execute Kahin file"""

    if not os.path.exists(path):
        print(f"Dosya bulunamadi: {path}")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        source = f.read()

    # Transpile
    try:
        python_code = transpile_fast(source)
    except Exception as e:
        print(f"Transpile hatasi: {e}")
        sys.exit(1)

    # Debug
    if "--debug" in sys.argv:
        print("="*70)
        print("TRANSPILED CODE")
        print("="*70)
        for n, line in enumerate(python_code.split('\n'), 1):
            print(f"{n:4d} | {line}")
        print("="*70)
        print("OUTPUT")
        print("="*70)

    # Execute
    try:
        exec(python_code, globals())
    except Exception as e:
        print(f"\nHata: {type(e).__name__}")
        print(f"Detay: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def show_help():
    """Help message"""
    print("Kahin v14.2 - Turkce Programlama Dili")
    print("\nKullanim:")
    print("  kahin <dosya.kahin>")
    print("  kahin <dosya.kahin> --debug")
    print("  kahin --yardim")
    print("  kahin --versiyon")


def show_version():
    """Version info"""
    print("Kahin v14.2 Optimized")
    print(f"Python: {sys.version.split()[0]}")


def main():
    """Main entry point"""

    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    if "--yardim" in sys.argv or "--help" in sys.argv:
        show_help()
        sys.exit(0)

    if "--versiyon" in sys.argv or "--version" in sys.argv:
        show_version()
        sys.exit(0)

    # Find file argument
    file_path = None
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            file_path = arg
            break

    if file_path is None:
        print("Dosya belirtilmedi")
        show_help()
        sys.exit(1)

    execute_file(file_path)


if __name__ == "__main__":
    main()
