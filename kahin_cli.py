#!/usr/bin/env python3
"""
KAHİN CLI - AST hattı runner

kahin <dosya.kahin>          Çalıştır
kahin <dosya.kahin> --debug  Çevrilmiş Python kodunu göster
kahin --yardim               Yardım
kahin --versiyon             Versiyon

AST hattını kullanır (kahin_lexer + kahin_ast): optimize + yeni sözdizimi
(aralık 1..10, pipe |>, constant folding) otomatik aktif.
"""
import sys
import os
import ast

SURUM = "15.0"


def _proje_yolu():
    return os.path.dirname(os.path.abspath(__file__))


def yardim():
    print(f"Kahin v{SURUM} - Türkçe Programlama Dili")
    print()
    print("Kullanım:")
    print("  kahin <dosya.kahin>          Kahin dosyasını çalıştır")
    print("  kahin <dosya.py>             Saf Python dosyasını çalıştır")
    print("  kahin <dosya> --debug        Çevrilen/çalışan kodu göster")
    print("  kahin --yardim               Bu mesaj")
    print("  kahin --versiyon             Versiyon bilgisi")
    print()
    print("Yeni sözdizimi:")
    print("  1..10    → range(1, 10)      aralık")
    print("  1..=10   → range(1, 11)      içeren aralık")
    print("  x |> f   → f(x)              pipe (zincirlenebilir)")


def calistir(dosya_yolu, debug=False):
    if not os.path.exists(dosya_yolu):
        print(f"Hata: dosya bulunamadı: {dosya_yolu}", file=sys.stderr)
        return 1
    if os.path.isdir(dosya_yolu):
        print(f"Hata: {dosya_yolu} bir dizin", file=sys.stderr)
        return 1

    with open(dosya_yolu, 'r', encoding='utf-8') as f:
        kaynak = f.read()

    sys.path.insert(0, _proje_yolu())

    saf_python = dosya_yolu.endswith('.py')

    if saf_python:
        # Normal Python dosyasi: parser atla, dogrudan derle
        try:
            kod = compile(kaynak, dosya_yolu, 'exec')
        except SyntaxError as e:
            print(f"Sözdizimi hatası ({dosya_yolu}:{e.lineno}): {e.msg}", file=sys.stderr)
            return 1
        if debug:
            print("# --- saf Python (cevirisiz) ---")
            print(kaynak)
            print("# --- çıktı ---")
    else:
        from kahin_ast import KahinParser

        parser = KahinParser(optimize=True)
        try:
            tree = parser.parse(kaynak, dosya_adi=dosya_yolu)
        except SyntaxError as e:
            print(f"Sözdizimi hatası ({dosya_yolu}:{e.lineno}): {e.msg}", file=sys.stderr)
            return 1

        if debug:
            print("# --- çevrilen Python ---")
            print(ast.unparse(tree))
            print("# --- çıktı ---")

        try:
            kod = compile(tree, dosya_yolu, 'exec')
        except SyntaxError as e:
            print(f"Derleme hatası ({dosya_yolu}:{e.lineno}): {e.msg}", file=sys.stderr)
            return 1

    # Programın kendi __name__ == "__main__" bloğu çalışsın
    ns = {'__name__': '__main__', '__file__': dosya_yolu}
    try:
        exec(kod, ns)
    except Exception:
        import traceback
        print("Çalışma zamanı hatası:", file=sys.stderr)
        traceback.print_exc()
        return 1
    return 0


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]

    if not argv:
        yardim()
        return 1
    if "--yardim" in argv or "--help" in argv:
        yardim()
        return 0
    if "--versiyon" in argv or "--version" in argv:
        print(f"Kahin v{SURUM}")
        return 0

    debug = "--debug" in argv
    dosya = next((a for a in argv if not a.startswith("--")), None)
    if dosya is None:
        print("Hata: dosya belirtilmedi", file=sys.stderr)
        yardim()
        return 1

    return calistir(dosya, debug=debug)


if __name__ == "__main__":
    sys.exit(main())
