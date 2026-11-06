"""Testy odwracanej karty: komentarz `<!-- wyjasnienie: obrazy/plik.png | opis -->` pod obrazem schematu daje kartę (przód rysunek, tył schemat, przycisk nad kartą), działa razem z analogią w dowolnej kolejności, a zły zapis, brak pliku i pusty opis to czytelny błąd."""

import base64
import re
import struct
import zlib
from pathlib import Path

import pytest

from narzedzia.strona import markdown_na_html, zloz_strone
from narzedzia.strona_pliki import PLIKI_CSS, PLIKI_JS

KORZEN = Path(__file__).resolve().parent.parent
OBRAZ = "![Schemat zasady](obrazy/schemat.png)\n"
KOMENTARZ = "<!-- wyjasnienie: obrazy/rysunek.png | Zasada jest jak kłódka. -->\n"
ANALOGIA = "<!-- analogia: Zasada jest jak kartka przy taśmie. -->\n"


def _png(kolor: int) -> bytes:
    def blok(typ: bytes, dane: bytes) -> bytes:
        return struct.pack(">I", len(dane)) + typ + dane + struct.pack(">I", zlib.crc32(typ + dane))

    return b"\x89PNG\r\n\x1a\n" + blok(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)) + blok(b"IDAT", zlib.compress(bytes([0, kolor, 0, 0]))) + blok(b"IEND", b"")


def _uri(kolor: int) -> str:
    return "data:image/png;base64," + base64.b64encode(_png(kolor)).decode("ascii")


@pytest.fixture
def katalog(tmp_path):
    (tmp_path / "obrazy").mkdir()
    (tmp_path / "obrazy" / "schemat.png").write_bytes(_png(10))
    (tmp_path / "obrazy" / "rysunek.png").write_bytes(_png(200))
    return tmp_path


def html(katalog, tresc):
    return markdown_na_html(tresc, katalog)


def test_komentarz_daje_karte_z_rysunkiem_z_przodu_i_schematem_z_tylu(katalog):
    h = html(katalog, OBRAZ + KOMENTARZ)
    przod, tyl = re.search(r'odwrot-przod">(.*?)</div><div class="odwrot-strona odwrot-tyl">(.*?)</div></div><button', h, re.S).groups()
    assert _uri(200) in przod and 'alt="Zasada jest jak kłódka."' in przod and "Wyjaśnienie" in przod
    assert _uri(10) in tyl and 'alt="Schemat zasady"' in tyl and "Schemat</span>" in tyl
    assert '<button type="button" class="odwrot-przycisk">' in h and "Odwróć kartę, żeby zobaczyć schemat" in h and "Wróć do wyjaśnienia" in h
    assert 'role="button" tabindex="0" aria-pressed="false"' in h
    assert "<figcaption>Schemat zasady</figcaption>" in h and "wyjasnienie" not in widoczny(h)


def widoczny(h):
    return re.sub(r"<[^>]+>", " ", h)


@pytest.mark.parametrize("kolejnosc", [KOMENTARZ + ANALOGIA, ANALOGIA + KOMENTARZ])
def test_analogia_i_wyjasnienie_pod_obrazem_w_dowolnej_kolejnosci(katalog, kolejnosc):
    h = html(katalog, OBRAZ + kolejnosc)
    assert 'class="odwrot"' in h and "<details><summary>Jak to sobie wyobrazić?</summary>" in h
    assert h.index("<figcaption>") < h.index("<details>")


def test_wielolinijkowa_analogia_i_wyjasnienie_po_niej(katalog):
    h = html(katalog, OBRAZ + "<!-- analogia: pierwsza\ndruga\n-->\n" + KOMENTARZ)
    assert 'class="odwrot"' in h and "pierwsza druga" in h


def test_obraz_bez_komentarza_zostaje_zwyklym_obrazem(katalog):
    h = html(katalog, OBRAZ)
    assert "odwrot" not in h and "<img" in h


def test_komentarz_po_akapicie_nie_robi_karty(katalog):
    h = html(katalog, OBRAZ + "\nAkapit.\n" + KOMENTARZ)
    assert 'class="odwrot"' not in h


def test_brak_pliku_rysunku_to_blad_z_nazwa_pliku(katalog):
    with pytest.raises(ValueError, match="nie ma takiego pliku"):
        html(katalog, OBRAZ + "<!-- wyjasnienie: obrazy/brak.png | Opis. -->\n")


@pytest.mark.parametrize("zapis", ["obrazy/rysunek.png |", "obrazy/rysunek.png |   "])
def test_pusty_opis_to_blad(katalog, zapis):
    with pytest.raises(ValueError, match="bez opisu rysunku"):
        html(katalog, OBRAZ + f"<!-- wyjasnienie: {zapis} -->\n")


@pytest.mark.parametrize("zapis", ["obrazy/rysunek.png", "| Opis."])
def test_zapis_bez_kreski_albo_pliku_to_blad(katalog, zapis):
    with pytest.raises(ValueError, match="bez pliku"):
        html(katalog, OBRAZ + f"<!-- wyjasnienie: {zapis} -->\n")


def test_druga_karta_pod_tym_samym_obrazem_to_blad(katalog):
    with pytest.raises(ValueError, match="jedną kartę"):
        html(katalog, OBRAZ + KOMENTARZ + KOMENTARZ)


def test_pliki_karty_sa_w_spisie_strony():
    assert "wyjasnienie.js" in PLIKI_JS and "styl-wyjasnienie.css" in PLIKI_CSS
    assert PLIKI_JS[-1] == "silnik.js"


def test_zlozona_strona_ma_karte_styl_i_skrypt(katalog):
    (katalog / "lekcja.md").write_text("# Lekcja\n\n" + OBRAZ + KOMENTARZ, encoding="utf-8")
    (katalog / "quiz.yaml").write_text("pytania: []\n", encoding="utf-8")
    (katalog / "fiszki.yaml").write_text("fiszki: []\n", encoding="utf-8")
    strona = zloz_strone(katalog)
    assert 'class="odwrot"' in strona and ".odwrot-w" in strona and 'querySelectorAll(".odwrot")' in strona


def test_niewidoczna_strona_karty_nie_rozciaga_karty():
    """Wysokość karty to wysokość widocznej strony: strona z tyłu (przed odwróceniem) i z przodu (po odwróceniu) jest absolute."""
    css = (KORZEN / "strona" / "styl-wyjasnienie.css").read_text(encoding="utf-8")
    regula = re.search(r"\.odwrot:not\(\.odwrocona\) \.odwrot-tyl,\s*\.odwrot\.odwrocona \.odwrot-przod\s*\{([^}]*)\}", css)
    assert regula and "position: absolute" in regula.group(1)
    assert re.search(r"\.odwrot-w\s*\{[^}]*position: relative", css)
    assert "overflow" not in re.search(r"\.odwrot-w\s*\{([^}]*)\}", css).group(1), "overflow na karcie spłaszcza obrót 3D"
