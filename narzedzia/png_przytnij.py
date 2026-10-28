"""Wycina z pliku PNG pas od wskazanego wiersza i lewej krawędzi, czystym Pythonem (bez sips i bez bibliotek obrazów).

Czyta PNG 8 bit w kolorach RGB albo RGBA bez przeplotu (tak zapisuje zrzuty Chrome), odwraca filtry wierszy 0-4,
przycina i zapisuje ten sam typ koloru z filtrem 0. Inny format kończy się `ValueError`.
"""

import struct
import zlib
from pathlib import Path

PODPIS = b"\x89PNG\r\n\x1a\n"
KANALY = {2: 3, 6: 4}  # typ koloru PNG -> liczba bajtów na piksel przy 8 bitach


def _kawalki(dane: bytes):
    """Zwraca kolejno (typ, zawartość) kawałków PNG po sprawdzeniu podpisu."""
    if dane[:8] != PODPIS:
        raise ValueError("To nie jest plik PNG.")
    i = 8
    while i + 8 <= len(dane):
        dlugosc, typ = struct.unpack(">I4s", dane[i : i + 8])
        yield typ, dane[i + 8 : i + 8 + dlugosc]
        i += 12 + dlugosc


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def _odwroc_filtr(
    filtr: int, wiersz: bytearray, poprzedni: bytearray, bpp: int
) -> None:
    """Zamienia wiersz po filtrze na surowe bajty (w miejscu); `poprzedni` to wiersz już odfiltrowany."""
    if filtr == 0:
        return
    for i in range(len(wiersz)):
        a = wiersz[i - bpp] if i >= bpp else 0
        b = poprzedni[i]
        if filtr == 1:
            pred = a
        elif filtr == 2:
            pred = b
        elif filtr == 3:
            pred = (a + b) // 2
        elif filtr == 4:
            pred = _paeth(a, b, poprzedni[i - bpp] if i >= bpp else 0)
        else:
            raise ValueError(f"Nieznany filtr wiersza PNG: {filtr}.")
        wiersz[i] = (wiersz[i] + pred) & 255


def wczytaj(sciezka: Path) -> tuple[int, int, int, list[bytearray]]:
    """Zwraca (szerokość, wysokość, typ koloru, surowe wiersze bez filtrów)."""
    szer = wys = typ_koloru = 0
    idat = []
    for typ, tresc in _kawalki(Path(sciezka).read_bytes()):
        if typ == b"IHDR":
            szer, wys, glebia, typ_koloru, _, _, przeplot = struct.unpack(
                ">IIBBBBB", tresc
            )
            if glebia != 8 or typ_koloru not in KANALY or przeplot != 0:
                raise ValueError(
                    "Obsługiwany jest tylko PNG 8 bit, RGB albo RGBA, bez przeplotu."
                )
        elif typ == b"IDAT":
            idat.append(tresc)
        elif typ == b"IEND":
            break
    if not szer or not idat:
        raise ValueError("Plik PNG jest uszkodzony.")
    bpp = KANALY[typ_koloru]
    dlugosc = szer * bpp
    surowe = zlib.decompress(b"".join(idat))
    if len(surowe) < wys * (dlugosc + 1):
        raise ValueError("Plik PNG jest za krótki.")
    wiersze: list[bytearray] = []
    poprzedni = bytearray(dlugosc)
    for r in range(wys):
        start = r * (dlugosc + 1)
        wiersz = bytearray(surowe[start + 1 : start + 1 + dlugosc])
        _odwroc_filtr(surowe[start], wiersz, poprzedni, bpp)
        wiersze.append(wiersz)
        poprzedni = wiersz
    return szer, wys, typ_koloru, wiersze


def _kawalek(typ: bytes, tresc: bytes) -> bytes:
    return (
        struct.pack(">I", len(tresc))
        + typ
        + tresc
        + struct.pack(">I", zlib.crc32(typ + tresc))
    )


def zapisz(
    sciezka: Path, szer: int, wys: int, typ_koloru: int, wiersze: list[bytearray]
) -> None:
    """Zapisuje PNG 8 bit z filtrem 0 w każdym wierszu."""
    surowe = b"".join(b"\x00" + bytes(w) for w in wiersze)
    Path(sciezka).write_bytes(
        PODPIS
        + _kawalek(b"IHDR", struct.pack(">IIBBBBB", szer, wys, 8, typ_koloru, 0, 0, 0))
        + _kawalek(b"IDAT", zlib.compress(surowe, 6))
        + _kawalek(b"IEND", b"")
    )


def przytnij_png(sciezka: Path, y: int, wys: int, szer: int) -> None:
    """Zastępuje plik pasem `wys` x `szer` od wiersza `y` i kolumny 0; pas nie wychodzi poza obraz."""
    szer_obrazu, wys_obrazu, typ_koloru, wiersze = wczytaj(sciezka)
    if y < 0 or y >= wys_obrazu:
        raise ValueError(f"Wiersz {y} leży poza obrazem o wysokości {wys_obrazu}.")
    if y + wys > wys_obrazu or szer > szer_obrazu:
        raise ValueError(
            f"Pas {wys}x{szer} od wiersza {y} wychodzi poza obraz {szer_obrazu}x{wys_obrazu}."
        )
    bajty = szer * KANALY[typ_koloru]
    pas = [w[:bajty] for w in wiersze[y : y + wys]]
    zapisz(sciezka, bajty // KANALY[typ_koloru], len(pas), typ_koloru, pas)
