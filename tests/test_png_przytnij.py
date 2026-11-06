"""Sprawdza czystopythonowe przycinanie PNG: wymiary, piksele, wiersz 0, dolna krawędź, filtry wierszy i błędy."""

import struct
import zlib
from pathlib import Path

import pytest

from narzedzia.png_przytnij import (
    KANALY,
    PODPIS,
    _kawalek,
    _paeth,
    przytnij_png,
    wczytaj,
)

SZER, WYS = 7, 12


def piksel(x: int, y: int, kanaly: int) -> bytes:
    return bytes(
        [(x * 30 + 1) % 256, (y * 20 + 2) % 256, (x + y * 3) % 256, 255][:kanaly]
    )


def zakoduj(sciezka: Path, typ_koloru: int, filtr: int = 0) -> None:
    """Zapisuje obraz wzorcowy; filtr 1-4 liczy tak, jak robi to koder PNG."""
    bpp = KANALY[typ_koloru]
    surowe = [b"".join(piksel(x, y, bpp) for x in range(SZER)) for y in range(WYS)]
    wyjscie = bytearray()
    poprzedni = bytes(SZER * bpp)
    for wiersz in surowe:
        wyjscie.append(filtr)
        for i, b in enumerate(wiersz):
            a = wiersz[i - bpp] if i >= bpp else 0
            g = poprzedni[i]
            c = poprzedni[i - bpp] if i >= bpp else 0
            pred = {0: 0, 1: a, 2: g, 3: (a + g) // 2, 4: _paeth(a, g, c)}[filtr]
            wyjscie.append((b - pred) & 255)
        poprzedni = wiersz
    sciezka.write_bytes(
        PODPIS
        + _kawalek(b"IHDR", struct.pack(">IIBBBBB", SZER, WYS, 8, typ_koloru, 0, 0, 0))
        + _kawalek(b"IDAT", zlib.compress(bytes(wyjscie)))
        + _kawalek(b"IEND", b"")
    )


def sprawdz(sciezka: Path, typ_koloru: int, y: int, wys: int, szer: int) -> None:
    s, w, typ, wiersze = wczytaj(sciezka)
    bpp = KANALY[typ_koloru]
    assert (s, w, typ) == (szer, wys, typ_koloru)
    for r in range(wys):
        for x in range(szer):
            assert bytes(wiersze[r][x * bpp : (x + 1) * bpp]) == piksel(
                x, y + r, bpp
            ), (x, r)


@pytest.mark.parametrize("typ_koloru", [2, 6])
@pytest.mark.parametrize("filtr", [0, 1, 2, 3, 4])
def test_odczyt_wszystkich_filtrow(tmp_path, typ_koloru, filtr):
    plik = tmp_path / "a.png"
    zakoduj(plik, typ_koloru, filtr)
    sprawdz(plik, typ_koloru, 0, WYS, SZER)


@pytest.mark.parametrize("typ_koloru", [2, 6])
@pytest.mark.parametrize(
    ("y", "wys", "szer"), [(0, 5, 4), (3, 4, 7), (WYS - 3, 3, 5), (WYS - 1, 1, 2)]
)
def test_pas_od_wiersza_y(tmp_path, typ_koloru, y, wys, szer):
    plik = tmp_path / "a.png"
    zakoduj(plik, typ_koloru, 4)
    przytnij_png(plik, y, wys, szer)
    sprawdz(plik, typ_koloru, y, wys, szer)
    assert plik.read_bytes()[:8] == PODPIS


def test_wiersz_poza_obrazem_i_inny_format(tmp_path):
    plik = tmp_path / "a.png"
    zakoduj(plik, 2)
    with pytest.raises(ValueError):
        przytnij_png(plik, WYS, 1, 1)
    inny = tmp_path / "b.png"
    inny.write_bytes(b"GIF89a")
    with pytest.raises(ValueError):
        przytnij_png(inny, 0, 1, 1)
    szary = tmp_path / "c.png"
    szary.write_bytes(
        PODPIS
        + _kawalek(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 0, 0, 0, 0))
        + _kawalek(b"IDAT", zlib.compress(b"\x00\x00"))
        + _kawalek(b"IEND", b"")
    )
    with pytest.raises(ValueError):
        przytnij_png(szary, 0, 1, 1)


@pytest.mark.parametrize("y, wys, szer", [(8, 5, SZER), (0, 3, SZER + 1)])
def test_pas_poza_obrazem_zglasza_blad(tmp_path: Path, y: int, wys: int, szer: int) -> None:
    sciezka = tmp_path / "a.png"
    zakoduj(sciezka, 2)
    przed = sciezka.read_bytes()
    with pytest.raises(ValueError, match="wychodzi poza obraz"):
        przytnij_png(sciezka, y, wys, szer)
    assert sciezka.read_bytes() == przed
