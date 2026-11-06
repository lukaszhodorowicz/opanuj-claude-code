"""Testy generatora strony: komentarz `<!-- analogia: … -->` pod obrazem daje rozwijany blok „Jak to sobie wyobrazić?” w ramce obrazu (na końcu linii obrazu albo w następnej linii; w innym miejscu zostaje niewidocznym komentarzem), a lekcja bez scenariusz.json składa się jako strona bez ćwiczeń (znacznik ćwiczenia albo podglądu bez scenariusza to czytelny błąd). Opis: dane/FORMAT-SCENARIUSZA.md, część „Lekcja bez scenariusza i analogia pod obrazem”."""

import json
import re
import struct
import zlib
from pathlib import Path

import pytest

from narzedzia import strona
from narzedzia.strona import main, markdown_na_html, zloz_strone

KORZEN = Path(__file__).resolve().parent.parent
BLOK = "<details><summary>Jak to sobie wyobrazić?</summary><p>{}</p></details>"


def _png() -> bytes:
    def blok(typ: bytes, dane: bytes) -> bytes:
        return struct.pack(">I", len(dane)) + typ + dane + struct.pack(">I", zlib.crc32(typ + dane))

    return b"\x89PNG\r\n\x1a\n" + blok(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)) + blok(b"IDAT", zlib.compress(b"\x00\x00\xff\x00")) + blok(b"IEND", b"")


@pytest.fixture
def katalog(tmp_path):
    (tmp_path / "obrazy").mkdir()
    (tmp_path / "obrazy" / "okno.png").write_bytes(_png())
    return tmp_path


def html(katalog, tresc):
    return markdown_na_html(tresc, katalog)


def widoczny_tekst(h):
    return re.sub(r"<[^>]+>", " ", h)


def test_analogia_na_koncu_linii_obrazu_daje_blok_pod_podpisem(katalog):
    h = html(katalog, "![Okno aplikacji](obrazy/okno.png) <!-- analogia: To jak pilot do telewizora. -->\n")
    assert BLOK.format("To jak pilot do telewizora.") in h
    assert h.index("</figcaption>") < h.index("<details>") < h.index("</figure>")
    assert h.count("<details>") == 1 and h.count("<figure") == 1


def test_analogia_w_nastepnej_linii_po_obrazie_daje_ten_sam_blok(katalog):
    h = html(katalog, "![Okno aplikacji](obrazy/okno.png)\n<!-- analogia: To jak pilot do telewizora. -->\n\nNastępny akapit.\n")
    assert BLOK.format("To jak pilot do telewizora.") in h
    assert h.index("</figcaption>") < h.index("<details>") < h.index("</figure>")
    assert "<p>Następny akapit.</p>" in h


def test_analogia_po_pustej_linii_zostaje_niewidocznym_komentarzem(katalog):
    h = html(katalog, "![Okno aplikacji](obrazy/okno.png)\n\n<!-- analogia: To jak pilot. -->\n\nAkapit.\n")
    assert "<details" not in h and "pilot" not in h


def test_analogia_w_innym_miejscu_niz_pod_obrazem_zostaje_komentarzem(katalog):
    h = html(katalog, "Akapit.\n\n<!-- analogia: Nie pod obrazem. -->\n\nTekst z komentarzem <!-- analogia: w środku --> w akapicie.\n")
    assert "<details" not in h and "Nie pod obrazem" not in widoczny_tekst(h) and "w środku" not in widoczny_tekst(h)


def test_inny_komentarz_pod_obrazem_nie_jest_analogia(katalog):
    h = html(katalog, "![Okno aplikacji](obrazy/okno.png)\n<!-- uwaga redakcji: sprawdzić -->\n")
    assert "<details" not in h and "uwaga" not in h


def test_tekst_analogii_ma_te_same_znaczniki_co_lekcja_i_jest_zabezpieczony(katalog):
    h = html(katalog, "![Okno aplikacji](obrazy/okno.png) <!-- analogia: To **pilot**, nie `telewizor` <b>x</b>. -->\n")
    assert BLOK.format("To <strong>pilot</strong>, nie <code>telewizor</code> &lt;b&gt;x&lt;/b&gt;.") in h


def test_pusta_analogia_pod_obrazem_to_blad(katalog):
    with pytest.raises(ValueError, match="analogia pod obrazem bez tekstu"):
        html(katalog, "![Okno aplikacji](obrazy/okno.png) <!-- analogia: -->\n")
    with pytest.raises(ValueError, match="analogia pod obrazem bez tekstu"):
        html(katalog, "![Okno aplikacji](obrazy/okno.png)\n<!-- analogia:   -->\n")


def test_druga_analogia_pod_tym_samym_obrazem_zostaje_komentarzem(katalog):
    h = html(katalog, "![Okno aplikacji](obrazy/okno.png) <!-- analogia: Pierwsza. -->\n<!-- analogia: Druga. -->\n")
    assert h.count("<details>") == 1 and "Pierwsza." in h and "Druga." not in h


def test_analogia_w_kilku_liniach_pod_obrazem_daje_jeden_blok_bez_pustego_akapitu(katalog):
    h = html(katalog, "![Okno aplikacji](obrazy/okno.png)\n<!-- analogia: To jak pilot do telewizora:\ntelewizor gra w salonie,\n\n a pilot tylko nim steruje. -->\n\nNastępny akapit.\n")
    assert BLOK.format("To jak pilot do telewizora: telewizor gra w salonie, a pilot tylko nim steruje.") in h
    assert h.index("</figcaption>") < h.index("<details>") < h.index("</figure>")
    assert "<p></p>" not in h and h.count("<details>") == 1 and "<!--" not in h
    assert h.rstrip().endswith("<p>Następny akapit.</p>")


def test_analogia_w_dwoch_liniach_z_zamknieciem_w_osobnej_linii(katalog):
    h = html(katalog, "![Okno aplikacji](obrazy/okno.png)\n<!-- analogia: pierwsza\ndruga\n-->\nAkapit po obrazie.\n")
    assert BLOK.format("pierwsza druga") in h and "<p>Akapit po obrazie.</p>" in h and "<p></p>" not in h


def test_analogia_w_kilku_liniach_ma_te_same_znaczniki_i_zabezpieczenie_co_jedna_linia(katalog):
    h = html(katalog, "![Okno aplikacji](obrazy/okno.png)\n<!-- analogia: To **pilot**,\nnie <b>telewizor</b>. -->\n")
    assert BLOK.format("To <strong>pilot</strong>, nie &lt;b&gt;telewizor&lt;/b&gt;.") in h


@pytest.mark.parametrize("tresc, fragment", [
    ("![Okno aplikacji](obrazy/okno.png)\n<!-- analogia: pierwsza\ndruga --> dopisek\n", "tekst po zamknięciu komentarza analogii"),
    ("![Okno aplikacji](obrazy/okno.png)\n<!-- analogia: pierwsza\ndruga\n\nAkapit bez zamknięcia.\n", "komentarz analogii pod obrazem nie ma zamknięcia -->"),
    ("![Okno aplikacji](obrazy/okno.png)\n<!-- analogia:\n-->\n", "analogia pod obrazem bez tekstu"),
])
def test_analogia_w_kilku_liniach_zle_zapisana_to_czytelny_blad(katalog, tresc, fragment):
    with pytest.raises(ValueError, match=re.escape(fragment)):
        html(katalog, tresc)


def test_obraz_bez_analogii_jest_bez_zmian(katalog):
    h = html(katalog, "![Okno aplikacji](obrazy/okno.png)\n")
    assert h.startswith('<figure class="obraz"><img') and h.endswith("</figcaption></figure>") and "<details" not in h


def test_strona_zawiera_styl_analogii_w_styl_strona_css(katalog):
    css = (KORZEN / "strona" / "styl-strona.css").read_text(encoding="utf-8")
    assert ".obraz > details" in css and "contain: inline-size" in css
    (katalog / "lekcja.md").write_text("# Lekcja\n\n![Okno aplikacji](obrazy/okno.png)\n<!-- analogia: To jak pilot. -->\n", encoding="utf-8")
    assert ".obraz > details" in zloz_strone(katalog)


def lekcja_bez_scenariusza(katalog, tresc):
    (katalog / "lekcja.md").write_text(tresc, encoding="utf-8")
    assert not (katalog / "scenariusz.json").exists()
    return katalog


def test_lekcja_bez_scenariusza_sklada_sie_jako_strona_bez_cwiczen(katalog):
    lekcja_bez_scenariusza(katalog, "# Lekcja bez ćwiczeń\n\nAkapit tekstu.\n")
    h = zloz_strone(katalog)
    assert "Akapit tekstu." in h and 'class="miejsce-cwiczenia"' not in h
    assert re.search(r'id="scenariusz">\{"cwiczenia": \[\]\}<', h)


def test_znacznik_cwiczenia_w_lekcji_bez_scenariusza_to_czytelny_blad(katalog):
    lekcja_bez_scenariusza(katalog, "# Lekcja\n\n<!-- cwiczenie: cw1 -->\n")
    with pytest.raises(ValueError, match=r"znacznik ćwiczenia <!-- cwiczenie: id -->, ale w jej katalogu nie ma scenariusz\.json") as e:
        zloz_strone(katalog)
    assert str(e.value).startswith(f"{katalog / 'lekcja.md'}: "), "komunikat podaje ścieżkę pliku lekcji"


def test_znacznik_podgladu_w_lekcji_bez_scenariusza_to_czytelny_blad(katalog):
    lekcja_bez_scenariusza(katalog, "# Lekcja\n\n<!-- podglad: cw1 t1 -->\n")
    with pytest.raises(ValueError, match=r"znacznik podglądu .*nie ma scenariusz\.json") as e:
        zloz_strone(katalog)
    assert str(e.value).startswith(f"{katalog / 'lekcja.md'}: ")


def test_scenariusz_wskazany_wprost_musi_istniec(katalog):
    lekcja_bez_scenariusza(katalog, "# Lekcja\n\nTekst.\n")
    with pytest.raises(OSError):
        zloz_strone(katalog, scenariusz=katalog / "brak.json")


def test_lekcja_ze_scenariuszem_obok_sklada_sie_jak_dotad(katalog):
    (katalog / "scenariusz.json").write_text(json.dumps({"cwiczenia": []}), encoding="utf-8")
    (katalog / "lekcja.md").write_text("# Lekcja\n\nTekst.\n", encoding="utf-8")
    assert "Tekst." in zloz_strone(katalog)


def test_wiersz_polecen_sklada_lekcje_bez_scenariusza_i_zglasza_blad_znacznika(katalog, capsys):
    lekcja_bez_scenariusza(katalog, "# Lekcja\n\nTekst.\n")
    wyjscie = katalog / "out" / "l.html"
    assert main([str(katalog), "--wyjscie", str(wyjscie)]) == 0 and wyjscie.is_file()
    (katalog / "lekcja.md").write_text("# Lekcja\n\n<!-- cwiczenie: cw1 -->\n", encoding="utf-8")
    assert main([str(katalog), "--wyjscie", str(wyjscie)]) == 1
    blad = capsys.readouterr().err
    assert "nie ma scenariusz.json" in blad and str(katalog / "lekcja.md") in blad


def test_moduly_generatora_maja_docstring_i_do_300_linii():
    for nazwa in ("strona_analogia.py", "strona.py"):
        tekst = (KORZEN / "narzedzia" / nazwa).read_text(encoding="utf-8")
        assert tekst.lstrip().startswith('"""') and len(tekst.splitlines()) <= 300, nazwa
    assert strona.analogia.NAGLOWEK == "Jak to sobie wyobrazić?"
