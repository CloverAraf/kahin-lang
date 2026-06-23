"""Matematik işlemleri Türkçe API math bağlayıcı"""
import math as _math

pi = _math.pi
e = _math.e
sonsuz = _math.inf


def karekok(x):
    return _math.sqrt(x)


def us(taban, kuvvet):
    return _math.pow(taban, kuvvet)


def mutlak(x):
    return _math.fabs(x)


def taban(x):
    return _math.floor(x)


def tavan(x):
    return _math.ceil(x)


def yuvarla(x, basamak=0):
    return round(x, basamak)


def log(x, taban=_math.e):
    return _math.log(x, taban)


def log10(x):
    return _math.log10(x)


def faktoriyel(n):
    return _math.factorial(n)


def obeb(a, b):
    return _math.gcd(a, b)


def okek(a, b):
    return _math.lcm(a, b)


def sin(x):
    return _math.sin(x)


def cos(x):
    return _math.cos(x)


def tan(x):
    return _math.tan(x)


def radyan(derece):
    return _math.radians(derece)


def derece(radyan):
    return _math.degrees(radyan)
