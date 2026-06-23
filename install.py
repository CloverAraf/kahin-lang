#!/usr/bin/env python3
"""
dil kurulum  ~/.local/bin/kahin launcher oluşturur
Launcher proje dizinini sys.pathe ekleyip kahin_cli.main() çagirir
"""
import os
import stat
from pathlib import Path

PROJE = Path(__file__).resolve().parent
BIN_DIZIN = Path.home() / ".local" / "bin"
HEDEF = BIN_DIZIN / "kahin"

LAUNCHER = f"""#!/usr/bin/env python3
import sys
sys.path.insert(0, {str(PROJE)!r})
from kahin_cli import main
sys.exit(main())
"""


def main():
    if not (PROJE / "kahin_cli.py").exists():
        print(f"HATA: kahin_cli.py bulunamadı: {PROJE}")
        return 1

    BIN_DIZIN.mkdir(parents=True, exist_ok=True)
    HEDEF.write_text(LAUNCHER, encoding="utf-8")
    HEDEF.chmod(HEDEF.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    print(f"Kuruldu: {HEDEF}")
    print(f"Proje:   {PROJE}")

    yollar = os.environ.get("PATH", "").split(os.pathsep)
    if str(BIN_DIZIN) not in yollar:
        print()
        print(f"UYARI: {BIN_DIZIN} PATH'te yok.")
        print("fish için ekle:")
        print(f"  fish_add_path {BIN_DIZIN}")
    else:
        print()
        print("Hazır. Dene:  kahin --versiyon")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
