"""Dosya işlemleri - Türkçe API (pathlib/os sarmalayıcı)."""
from pathlib import Path


def oku(yol, kodlama="utf-8"):
    return Path(yol).read_text(encoding=kodlama)


def yaz(yol, icerik, kodlama="utf-8"):
    Path(yol).write_text(icerik, encoding=kodlama)


def ekle(yol, icerik, kodlama="utf-8"):
    with open(yol, "a", encoding=kodlama) as f:
        f.write(icerik)


def satirlar(yol, kodlama="utf-8"):
    return Path(yol).read_text(encoding=kodlama).splitlines()


def var_mi(yol):
    return Path(yol).exists()


def kaldir(yol):
    Path(yol).unlink(missing_ok=True)


def listele(yol="."):
    return [p.name for p in Path(yol).iterdir()]
