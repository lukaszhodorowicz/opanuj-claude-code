"""Robi obraz lekcji z ćwiczenia: zrzut narzędziem silnika bez znacznika i bez luki (bez_luki), przycięty do okna aplikacji.

Wywołanie z korzenia repozytorium, po złożeniu strony lekcji do build/<lekcja>.html (bez zewnętrznego flock, skrypt bierze blokadę sam):
`env PYTHONPATH=. python3 moduly/powtarzalna-praca/wtyczki/obrazy/zrodla/kadr-z-cwiczenia.py <katalog lekcji> <plik.png> <x0> <y0> <x1> <y1> '<ujęcie JSON>'`.
Ujęcie ma pola jak w zrzuty.json (szer, wys, budzet, polecenie, do, klik); kadr liczy się w pikselach zrzutu, który zaczyna się 12 px nad ćwiczeniem.
Znacznik „kliknij tutaj” i obwódkę celu chowa narzędzie silnika (`bez_luki`, polecenie nadzoru 27.10.2026); skrypt dokłada tylko kadr okna.
"""

import fcntl
import json
import sys
from pathlib import Path

from PIL import Image

from narzedzia.zrzuty import zrob


def main() -> None:
    katalog, obraz = Path(sys.argv[1]), Path(sys.argv[2])
    kadr = tuple(int(x) for x in sys.argv[3:7])
    ujecie = {**json.loads(sys.argv[7]), "bez_luki": True}
    wyjscie = (Path("build/zrzuty") / f"{katalog.name}-kadr").resolve()
    wyjscie.mkdir(parents=True, exist_ok=True)
    strona = Path("build") / f"{katalog.name}.html"
    with open("/tmp/przewodnik-chrome.lock", "w") as blokada:
        fcntl.flock(blokada, fcntl.LOCK_EX)
        png = zrob(obraz.stem, ujecie, strona.resolve(), wyjscie)
    Image.open(png).crop(kadr).save(katalog / obraz)
    print(katalog / obraz)


if __name__ == "__main__":
    main()
