#!/usr/bin/env python3
"""kahin_lib turkce stdlib testi uctan uca .kahin exec"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "kahin_lib"))

from kahin_ast import KahinParser

p = KahinParser(optimize=True)
gecti = basarisiz = 0


def kontrol(ad, kosul):
    global gecti, basarisiz
    if kosul:
        gecti += 1
        print(f"  OK   {ad}")
    else:
        basarisiz += 1
        print(f"  FAIL {ad}")


def calistir(kod):
    tree = p.parse(kod)
    ns = {'__name__': '__main__'}
    exec(compile(tree, '<test>', 'exec'), ns)
    return ns


print("=== dosya ===")
tf = os.path.join(tempfile.gettempdir(), "kahin_stdlib_test.txt")
ns = calistir(f'ice_aktar dosya\ndosya.yaz({tf!r}, "selam")\nicerik = dosya.oku({tf!r})')
kontrol("yaz + oku", ns['icerik'] == "selam")
ns = calistir(f'ice_aktar dosya\nv = dosya.var_mi({tf!r})')
kontrol("var_mi True", ns['v'] is True)
ns = calistir(f'ice_aktar dosya\ndosya.ekle({tf!r}, " dunya")\nx = dosya.oku({tf!r})')
kontrol("ekle", ns['x'] == "selam dunya")
ns = calistir(f'ice_aktar dosya\ndosya.kaldir({tf!r})\nv = dosya.var_mi({tf!r})')
kontrol("kaldir", ns['v'] is False)

print("=== veri (json) ===")
ns = calistir('ice_aktar veri\nn = veri.cozumle(\'{"a": 1, "b": [2, 3]}\')')
kontrol("cozumle", ns['n'] == {"a": 1, "b": [2, 3]})
ns = calistir('ice_aktar veri\ns = veri.serile({"x": 5}, 0)')
kontrol("serile", ns['s'] == '{"x": 5}')

print("=== zaman ===")
ns = calistir('ice_aktar zaman\nt = zaman.simdi()')
kontrol("simdi float", isinstance(ns['t'], float) and ns['t'] > 0)
ns = calistir('ice_aktar zaman\nt = zaman.tarih("%Y")')
kontrol("tarih yil", len(ns['t']) == 4 and ns['t'].isdigit())

print(f"\nSONUC: {gecti} gecti, {basarisiz} basarisiz")
sys.exit(1 if basarisiz else 0)
