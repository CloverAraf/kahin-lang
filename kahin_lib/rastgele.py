"""Rastgele işlemleri Türkçe API random bağlayıcı"""
import random as _random


def sayi(bas, son):
    """bas ile son arası (dahil) rastgele tam sayı."""
    return _random.randint(bas, son)


def ondalik(bas=0.0, son=1.0):
    return _random.uniform(bas, son)


def sec(dizi):
    """Diziden rastgele bir öğe."""
    return _random.choice(dizi)


def ornek(dizi, adet):
    """Diziden tekrarsız k öğe."""
    return _random.sample(dizi, adet)


def karistir(dizi):
    """Diziyi yerinde karıştır."""
    _random.shuffle(dizi)
    return dizi


def tohum(deger):
    _random.seed(deger)
