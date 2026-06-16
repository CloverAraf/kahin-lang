#!/usr/bin/env python3
"""
Kahin modül entegrasyon testi
Tüm modüllerin birlikte çalıştığını doğrula
"""

import sys
from pathlib import Path

def test_transpiler():
    """Basit transpiler test"""
    print("Test 1: kahin_transpiler")

    try:
        from kahin_transpiler import metni_cevirme

        kahin = 'eger x > 5:\n    yazdir("test")'
        python = metni_cevirme(kahin)

        assert 'if x > 5:' in python
        assert 'print("test")' in python

        print("  OK: Transpiler calisiyor")
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False

def test_lexer():
    """Lexer test"""
    print("\nTest 2: kahin_lexer")

    try:
        from kahin_lexer import KahinLexer

        lexer = KahinLexer()
        tokens = lexer.tokenize('eger x > 5:\n    yazdir("test")')

        assert len(tokens) > 0

        # Token'ları Python koduna çevir
        python_kod = lexer.tokens_to_code(tokens)
        assert 'if' in python_kod

        print("  OK: Lexer calisiyor")
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ast():
    """AST parser test"""
    print("\nTest 3: kahin_ast")

    try:
        from kahin_ast import KahinParser

        parser = KahinParser(optimize=True)
        tree = parser.parse('x = 2 + 3')

        assert tree is not None

        print("  OK: AST parser calisiyor")
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cache():
    """Cache test"""
    print("\nTest 4: kahin_cache")

    try:
        from kahin_cache import KahinCache

        cache = KahinCache()
        stats = cache.get_stats()

        assert 'count' in stats

        print("  OK: Cache sistemi calisiyor")
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("="*70)
    print("KAHIN MODUL ENTEGRASYON TESTI")
    print("="*70)
    print()

    results = []
    results.append(test_transpiler())
    results.append(test_lexer())
    results.append(test_ast())
    results.append(test_cache())

    print("\n" + "="*70)
    passed = sum(results)
    total = len(results)
    print(f"SONUC: {passed}/{total} test basarili")

    if passed == total:
        print("Tum moduller calisir durumda")
        return 0
    else:
        print("Bazi moduller calismadi, duzeltme gerekli")
        return 1

if __name__ == "__main__":
    sys.exit(main())
