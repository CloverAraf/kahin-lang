#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
KAHİN CPYTHON-LIKE BUILD SCRIPT
═══════════════════════════════════════════════════════════════════════

Tüm modülleri birleştirip ultra fast binary oluşturur:
- kahin_lexer.py
- kahin_ast.py
- kahin_cache.py
- kahin_ultra_fast.py

ÇIKTI:
------
/usr/bin/kahin - CPython-like optimized binary
"""

import sys
from pathlib import Path


def build():
    """Tüm modülleri birleştir"""

    print("═" * 70)
    print("KAHİN CPYTHON-LIKE BUILD")
    print("═" * 70)

    project = Path.home() / "kahin_projesi"

    # Modülleri oku
    modules = {
        'lexer': project / 'kahin_lexer.py',
        'ast': project / 'kahin_ast.py',
        'cache': project / 'kahin_cache.py',
        'main': project / 'kahin_ultra_fast.py',
    }

    print("\n[1/4] Modüller kontrol ediliyor...")
    for name, path in modules.items():
        if not path.exists():
            print(f"❌ Eksik: {path}")
            sys.exit(1)
        print(f"✓ {name}: {path.name}")

    print("\n[2/4] Modüller birleştiriliyor...")

    # Shebang
    binary_kod = "#!/usr/bin/env python3\n"
    binary_kod += '"""\n'
    binary_kod += "KAHİN v14.1 - CPython-like Optimized\n"
    binary_kod += '"""\n\n'

    # Lexer ekle
    with open(modules['lexer'], 'r') as f:
        lexer_kod = f.read()
        # Shebang ve docstring'i atla
        lexer_kod = '\n'.join(lexer_kod.split('\n')[30:])  # İlk 30 satır header
        binary_kod += "# " + "="*68 + "\n"
        binary_kod += "# LEXER MODULE\n"
        binary_kod += "# " + "="*68 + "\n"
        binary_kod += lexer_kod + "\n\n"

    # AST ekle
    with open(modules['ast'], 'r') as f:
        ast_kod = f.read()
        # Import'u düzelt
        ast_kod = ast_kod.replace('from kahin_lexer import', '# from kahin_lexer import')
        ast_kod = '\n'.join(ast_kod.split('\n')[30:])
        binary_kod += "# " + "="*68 + "\n"
        binary_kod += "# AST MODULE\n"
        binary_kod += "# " + "="*68 + "\n"
        binary_kod += ast_kod + "\n\n"

    # Cache ekle
    with open(modules['cache'], 'r') as f:
        cache_kod = f.read()
        cache_kod = '\n'.join(cache_kod.split('\n')[30:])
        binary_kod += "# " + "="*68 + "\n"
        binary_kod += "# CACHE MODULE\n"
        binary_kod += "# " + "="*68 + "\n"
        binary_kod += cache_kod + "\n\n"

    # Main ekle
    with open(modules['main'], 'r') as f:
        main_kod = f.read()
        # Import'ları düzelt
        main_kod = main_kod.replace('from kahin_lexer import', '# from kahin_lexer import')
        main_kod = main_kod.replace('from kahin_ast import', '# from kahin_ast import')
        main_kod = main_kod.replace('from kahin_cache import', '# from kahin_cache import')
        main_kod = '\n'.join(main_kod.split('\n')[30:])
        binary_kod += "# " + "="*68 + "\n"
        binary_kod += "# MAIN MODULE\n"
        binary_kod += "# " + "="*68 + "\n"
        binary_kod += main_kod

    print(f"✓ Binary boyutu: {len(binary_kod)} karakter")

    print("\n[3/4] Binary yazılıyor...")

    # Geçici dosyaya yaz
    temp = project / "kahin_cpython.py"
    with open(temp, 'w', encoding='utf-8') as f:
        f.write(binary_kod)

    print(f"✓ {temp}")

    # Global konuma kopyala
    target = Path("/data/data/com.termux/files/usr/bin/kahin_fast")

    import shutil
    try:
        shutil.copy(temp, target)
        import os
        os.chmod(target, 0o755)
        print(f"✓ {target}")
    except:
        print(f"⚠️  {target} kurulamadı (izin sorunu)")
        print(f"   Manuel kur: cp {temp} {target} && chmod +x {target}")

    print("\n[4/4] Test ediliyor...")

    # Test
    import subprocess
    result = subprocess.run(
        [str(target), str(project / "merhaba.kahin"), "--benchmark"],
        capture_output=True,
        text=True,
        timeout=5
    )

    if result.returncode == 0:
        print("✓ Test başarılı!")
        print("\nÇıktı:")
        print(result.stdout)
    else:
        print("⚠️  Test hatası:")
        print(result.stderr)

    print("\n" + "═" * 70)
    print("✅ BUILD TAMAMLANDI!")
    print("═" * 70)
    print(f"\nBinary: {target}")
    print(f"Geçici: {temp}")
    print("\nKullanım:")
    print(f"  kahin_fast program.kahin")
    print(f"  kahin_fast program.kahin --benchmark")


if __name__ == "__main__":
    build()
