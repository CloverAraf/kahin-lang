#!/usr/bin/env python3
"""
Kahin hata mesajları - Python traceback'i Türkçeleştirir.

Çalışma zamanı hatalarında ham İngilizce traceback yerine, hatanın olduğu
.kahin satırını ve Türkçe hata tipini gösterir.
"""
import traceback

EXCEPTION_MAP = {
    'NameError': 'Tanımsız isim',
    'TypeError': 'Tür hatası',
    'ValueError': 'Geçersiz değer',
    'ZeroDivisionError': 'Sıfıra bölme',
    'IndexError': 'Geçersiz indis',
    'KeyError': 'Bulunamayan anahtar',
    'AttributeError': 'Geçersiz öznitelik',
    'ImportError': 'Modül bulunamadı',
    'ModuleNotFoundError': 'Modül bulunamadı',
    'FileNotFoundError': 'Dosya bulunamadı',
    'IndentationError': 'Girinti hatası',
    'RecursionError': 'Çok derin özyineleme',
    'OverflowError': 'Sayı taşması',
    'StopIteration': 'Yineleme bitti',
    'AssertionError': 'Olumlama başarısız',
    'RuntimeError': 'Çalışma zamanı hatası',
    'NotImplementedError': 'Henüz uygulanmadı',
    'PermissionError': 'İzin yok',
    'OSError': 'İşletim sistemi hatası',
}

# En yaygın SyntaxError mesaj parçaları
SYNTAX_MAP = {
    'invalid syntax': 'geçersiz sözdizimi',
    "expected ':'": "':' bekleniyordu",
    'unexpected EOF': 'beklenmeyen dosya sonu',
    'unexpected indent': 'beklenmeyen girinti',
    'expected an indented block': 'girintili blok bekleniyordu',
    'was never closed': 'kapatılmamış',
    'invalid character': 'geçersiz karakter',
}


def _son_kullanici_frame(tb):
    """Kullanıcı koduna ait son frame'i bul (stdlib iç dosyalarını atla)."""
    import os
    stdlib = os.path.dirname(os.__file__)
    son = None
    for frame, lineno in traceback.walk_tb(tb):
        ad = frame.f_code.co_filename
        if ad in ('<input>', '<kahin>', '<string>'):
            son = (ad, lineno)
        elif ad.endswith(('.kahin', '.py')) and not ad.startswith(stdlib):
            son = (ad, lineno)
    return son


def turkcelestir(exc_type, exc_value, tb) -> str:
    """Çalışma zamanı exception'ını Türkçe tek bloğa çevir."""
    tip = exc_type.__name__
    tr_tip = EXCEPTION_MAP.get(tip, tip)
    mesaj = str(exc_value)

    konum = _son_kullanici_frame(tb)
    satirlar = ["Çalışma zamanı hatası:"]
    if konum and konum[0] != '<input>':
        dosya, lineno = konum
        satirlar.append(f"  {dosya}:{lineno} satırında")
    if mesaj:
        satirlar.append(f"  {tr_tip}: {mesaj}")
    else:
        satirlar.append(f"  {tr_tip}")
    return "\n".join(satirlar)


def syntax_turkcelestir(msg: str) -> str:
    """SyntaxError mesajındaki yaygın İngilizce parçaları çevir."""
    if not msg:
        return msg
    dusuk = msg.lower()
    for ing, tr in SYNTAX_MAP.items():
        if ing in dusuk:
            return tr
    return msg
