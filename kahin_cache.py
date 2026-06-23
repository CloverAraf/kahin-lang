#!/usr/bin/env python3
"""
CPython’un `.pyc` sistemi gibi çalışır.
Derlenmiş bytecode’u cache’ler ve tekrar compile etmeyi önler.

## .pyc NEDİR:

Python Compiled Bytecode – CPython’un derlenmiş cache formatıdır.

Örnek:
program.py  → **pycache**/program.cpython-312.pyc

## KAHİN’DE:

```
program.kahin  → __kahin_cache__/program.kahc
```

## PERFORMANS KAZANCI:

* İlk çalıştırma: Parse + Compile (~5ms)
* Cache’den okuma: sadece load (~0.5ms)
* Yaklaşık 10x hızlanma sağlar

## FORMAT:

.kahc dosyası:

```
[4 byte] Magic number (Kahin versiyonu)  
[4 byte] Timestamp (dosya değişiklik zamanı)  
[4 byte] Source size (kaynak dosya boyutu)  
[?????] Marshalled code object (bytecode)  
```

Bu yapı sayesinde sistem, kaynak kod değişmediyse yeniden derleme yapmadan doğrudan önbellekten çalıştırır.

"""

import marshal
import os
import struct
import time
import hashlib
from pathlib import Path
from typing import Optional, Any


# ═══════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════

# Magic number - Kahin versiyonu
# Her Kahin versiyonunda değiştir ki eski cache'ler geçersiz olsun
KAHIN_MAGIC = b'KAHN'  # 4 byte
KAHIN_VERSION = 16  # v16.0

# Cache dizini
CACHE_DIR = Path.home() / ".kahin_cache"


# ═══════════════════════════════════════════════════════════════════════
# CACHE MANAGER
# ═══════════════════════════════════════════════════════════════════════

class KahinCache:
    """
    Bytecode Cache Manager - .pyc benzeri

    CPython'un imp/importlib cache sistemi gibi.
    """

    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, kaynak_dosya: str) -> Path:
        """
        Kaynak dosya için cache dosyası yolu.
        Anahtar = tam yol hash'i; farklı dizinlerdeki aynı adlı dosyalar çakışmaz.
        """
        tam_yol = os.path.abspath(kaynak_dosya)
        yol_hash = hashlib.md5(tam_yol.encode('utf-8')).hexdigest()[:12]
        dosya_adi = Path(kaynak_dosya).stem
        return self.cache_dir / f"{dosya_adi}.{yol_hash}.kahc"

    def _get_source_hash(self, kaynak_dosya: str) -> bytes:
        """
        Kaynak dosyanın hash'i (değişiklik kontrolü için)
        """
        with open(kaynak_dosya, 'rb') as f:
            return hashlib.md5(f.read()).digest()

    def load(self, kaynak_dosya: str) -> Optional[Any]:
        """
        Cache'den bytecode yükle

        Args:
            kaynak_dosya: Kaynak .kahin dosyası

        Returns:
            Code object (bytecode) veya None (cache yoksa/geçersizse)
        """

        cache_path = self._get_cache_path(kaynak_dosya)

        # Cache yoksa
        if not cache_path.exists():
            return None

        # Kaynak dosya yoksa cache geçersiz
        if not os.path.exists(kaynak_dosya):
            return None

        try:
            # Cache dosyasını oku
            with open(cache_path, 'rb') as f:
                # HEADER: Magic + Version + Timestamp + Size + Hash
                magic = f.read(4)
                version = struct.unpack('I', f.read(4))[0]
                cache_timestamp = struct.unpack('d', f.read(8))[0]
                cache_size = struct.unpack('Q', f.read(8))[0]
                cache_hash = f.read(16)  # MD5 hash

                # Magic number kontrolü
                if magic != KAHIN_MAGIC:
                    return None

                # Versiyon kontrolü
                if version != KAHIN_VERSION:
                    return None

                # Kaynak dosya bilgileri
                source_stat = os.stat(kaynak_dosya)
                source_timestamp = source_stat.st_mtime
                source_size = source_stat.st_size
                source_hash = self._get_source_hash(kaynak_dosya)

                # Timestamp kontrolü
                if cache_timestamp < source_timestamp:
                    return None  # Kaynak güncellenmiş

                # Size kontrolü
                if cache_size != source_size:
                    return None  # Boyut değişmiş

                # Hash kontrolü (en güvenilir)
                if cache_hash != source_hash:
                    return None  # İçerik değişmiş

                # Bytecode'u unmarshall et
                code = marshal.load(f)

                return code

        except Exception:
            # Hata olursa cache'i sil
            try:
                cache_path.unlink()
            except:
                pass
            return None

    def save(self, kaynak_dosya: str, code: Any):
        """
        Bytecode'u cache'e kaydet

        Args:
            kaynak_dosya: Kaynak .kahin dosyası
            code: Code object (bytecode)
        """

        cache_path = self._get_cache_path(kaynak_dosya)

        try:
            # Kaynak dosya bilgileri
            source_stat = os.stat(kaynak_dosya)
            source_timestamp = source_stat.st_mtime
            source_size = source_stat.st_size
            source_hash = self._get_source_hash(kaynak_dosya)

            # Cache dosyasına yaz
            with open(cache_path, 'wb') as f:
                # HEADER yaz
                f.write(KAHIN_MAGIC)  # 4 byte
                f.write(struct.pack('I', KAHIN_VERSION))  # 4 byte
                f.write(struct.pack('d', source_timestamp))  # 8 byte
                f.write(struct.pack('Q', source_size))  # 8 byte
                f.write(source_hash)  # 16 byte (MD5)

                # Bytecode'u marshall et
                marshal.dump(code, f)

        except Exception as e:
            # Hata olursa sessizce devam et
            pass

    def clear(self):
        """Tüm cache'i temizle"""
        for cache_file in self.cache_dir.glob("*.kahc"):
            try:
                cache_file.unlink()
            except:
                pass

    def get_stats(self) -> dict:
        """Cache istatistikleri"""
        cache_files = list(self.cache_dir.glob("*.kahc"))
        total_size = sum(f.stat().st_size for f in cache_files)

        return {
            'count': len(cache_files),
            'total_size': total_size,
            'cache_dir': str(self.cache_dir),
        }


# ═══════════════════════════════════════════════════════════════════════
# TEST & BENCHMARK
# ═══════════════════════════════════════════════════════════════════════

def test_cache():
    """Cache test"""

    print("═" * 70)
    print("KAHİN BYTECODE CACHE - .pyc benzeri")
    print("═" * 70)

    # Test dosyası oluştur
    test_file = Path.home() / "test_cache.kahin"
    test_file.write_text('''
tanimla test():
    yazdir("Cache test")
    dondur 42

sonuc = test()
yazdir(f"Sonuç: {sonuc}")
''')

    print(f"\nTest dosyası: {test_file}")

    # Cache manager
    cache = KahinCache()

    # İlk yükleme - cache yok
    print("\n[1] İlk yükleme (cache yok):")
    import time
    start = time.perf_counter()
    code = cache.load(str(test_file))
    elapsed = time.perf_counter() - start

    if code is None:
        print(f"  Cache yok (beklenen)")

        # Compile et
        from kahin_ast import KahinParser
        parser = KahinParser()
        kaynak = test_file.read_text()

        start = time.perf_counter()
        code = parser.parse_and_compile(kaynak, str(test_file))
        compile_time = time.perf_counter() - start

        print(f"  Compile süresi: {compile_time*1000:.3f} ms")

        # Cache'e kaydet
        cache.save(str(test_file), code)
        print(f"  Cache'e kaydedildi ✓")

    # İkinci yükleme - cache'den
    print("\n[2] İkinci yükleme (cache'den):")
    start = time.perf_counter()
    code = cache.load(str(test_file))
    cache_time = time.perf_counter() - start

    if code:
        print(f"  Cache'den yüklendi ✓")
        print(f"  Yükleme süresi: {cache_time*1000:.3f} ms")
        print(f"  Hızlanma: {compile_time/cache_time:.1f}x")

    # Cache stats
    stats = cache.get_stats()
    print(f"\n[3] Cache İstatistikleri:")
    print(f"  Dosya sayısı: {stats['count']}")
    print(f"  Toplam boyut: {stats['total_size']/1024:.1f} KB")
    print(f"  Cache dizini: {stats['cache_dir']}")

    # Çalıştır
    print("\n[4] Bytecode Çalıştır:")
    print("-" * 70)
    exec(code)

    # Temizle
    test_file.unlink()
    print("\n✓ Test tamamlandı")


if __name__ == "__main__":
    test_cache()
