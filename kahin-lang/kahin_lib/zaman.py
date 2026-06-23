"""Zaman işlemleri Türkçe ApI time/datetime bağlayici"""
import time as _time
from datetime import datetime as _datetime


def simdi():
    """Şu anki zaman damgası (saniye)."""
    return _time.time()


def duraklat(saniye):
    _time.sleep(saniye)


def tarih(bicim="%Y-%m-%d %H:%M:%S"):
    """Şu anki tarihi biçimli metin olarak döndür."""
    return _datetime.now().strftime(bicim)


def gun_adi():
    return _datetime.now().strftime("%A")
