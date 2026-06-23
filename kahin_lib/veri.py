"""JSON veri işlemleri - Türkçe API."""
import json as _json
from pathlib import Path


def cozumle(metin):
    """JSON metni → Python nesnesi."""
    return _json.loads(metin)


def serile(nesne, girinti=2):
    """Python nesnesi → JSON metni. girinti=0 → tek satır."""
    return _json.dumps(nesne, ensure_ascii=False, indent=girinti or None)


def dosyadan_oku(yol):
    return _json.loads(Path(yol).read_text(encoding="utf-8"))


def dosyaya_yaz(yol, nesne, girinti=2):
    Path(yol).write_text(
        _json.dumps(nesne, ensure_ascii=False, indent=girinti),
        encoding="utf-8",
    )
