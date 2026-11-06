"""Testy stopki źródeł na stronie lekcji (D-2026-10-26-54, skutek s1): część `## Źródła` z lekcja.md stoi na końcu strony, po quizie i fiszkach, a nie w treści lekcji."""

import json
import re
from pathlib import Path

from narzedzia.strona import zloz_strone

# Kontrakt dla kodera (skutek s1, stopka źródeł):
# - `narzedzia/strona.py` odcina z lekcja.md część `## Źródła`: od linii `## Źródła` (nagłówek drugiego stopnia,
#   dokładnie to słowo) do następnego nagłówka `## ` albo do końca pliku. `### Źródła` to zwykły nagłówek treści.
# - Odcięta część nie trafia do treści lekcji (HTML między `<div class="strona">` a `id="sekcja-quiz"`).
#   Reszta treści jest taka sama jak w tej samej lekcji bez części `## Źródła`.
# - Odcięta część, zamieniona na HTML tym samym konwerterem co treść (linki `<a href="…">`), stoi w jednym elemencie
#   `<footer class="… stopka-zrodel …" id="zrodla">` (klasa `stopka-zrodel` obowiązkowa, może mieć inne klasy obok,
#   np. `tekst`). Stopka stoi w HTML strony PO `id="sekcja-quiz"`, `id="sekcja-fiszki"` i `id="fiszki-lista"`,
#   a przed danymi `<script type="application/json" id="scenariusz">`. W `strona/szablon.html` miejsce na nią
#   (np. `{{ZRODLA}}`) po `<div class="fiszki" id="fiszki-lista"></div>`.
# - Lekcja bez `## Źródła`: na stronie nie ma żadnego `<footer`, a w HTML nie zostaje znacznik szablonu `{{…}}`.

KORZEN = Path(__file__).resolve().parent.parent
# Lekcja straznik-zamiast-pytan zamrożona w tests/dane (wersja sprzed commita 516201c, który napisał ją od nowa),
# żeby stopka nie zmieniała się razem z kursem.
LEKCJA_STRAZNIK = Path(__file__).resolve().parent / "dane" / "lekcja-stopka-straznik"
SCEN = {"lekcja": "x", "folder_startowy": [], "cwiczenia": [{"id": "cw1", "rodzaj": "przelacznik", "tytul": "x"}]}
WSTEP = "# Próba\n\nWstęp lekcji.\n\n<!-- cwiczenie: cw1 -->\n\n## Jak to działa\n\nTekst części.\n"
ZRODLA = (
    "## Źródła\n\nDokumentacja Claude Code:\n\n"
    "- [Choose a permission mode](https://code.claude.com/docs/en/permission-modes)\n"
    "- [Desktop application](https://code.claude.com/docs/en/desktop)\n\n"
    "Sprawdzone 25.10.2026, Claude Code 2.1.310.\n"
)
LINK = '<a href="https://code.claude.com/docs/en/permission-modes">Choose a permission mode</a>'


def _strona(tmp_path, lekcja):
    (tmp_path / "lekcja.md").write_text(lekcja, encoding="utf-8")
    (tmp_path / "scenariusz.json").write_text(json.dumps(SCEN), encoding="utf-8")
    return zloz_strone(tmp_path)


def _tresc(strona):
    """HTML treści lekcji: od `<div class="strona">` do sekcji quizu."""
    m = re.search(r'<div class="strona">(.*?)<div class="tekst" id="sekcja-quiz">', strona, re.S)
    assert m, "brak treści lekcji przed sekcją quizu"
    return m.group(1)


def _stopki(strona):
    return re.findall(r"<footer\b([^>]*)>(.*?)</footer>", strona, re.S)


def test_s1_zrodla_w_stopce_po_quizie_i_fiszkach(tmp_path):
    strona = _strona(tmp_path, WSTEP + "\n" + ZRODLA)
    stopki = _stopki(strona)
    assert len(stopki) == 1, f"oczekiwana jedna stopka <footer>, jest {len(stopki)}"
    atrybuty, wnetrze = stopki[0]
    assert re.search(r'class="[^"]*\bstopka-zrodel\b', atrybuty) and 'id="zrodla"' in atrybuty
    assert "Źródła" in wnetrze and LINK in wnetrze and "Sprawdzone 25.10.2026" in wnetrze
    assert '<a href="https://code.claude.com/docs/en/desktop">Desktop application</a>' in wnetrze
    poz = strona.index("<footer")
    for znacznik in ('id="sekcja-quiz"', 'id="sekcja-fiszki"', 'id="fiszki-lista"'):
        assert strona.index(znacznik) < poz, f"stopka stoi przed {znacznik}"
    assert poz < strona.index('<script type="application/json" id="scenariusz">')


def test_s1_zrodel_nie_ma_w_tresci_lekcji(tmp_path):
    tresc = _tresc(_strona(tmp_path, WSTEP + "\n" + ZRODLA))
    assert "Wstęp lekcji." in tresc and "Tekst części." in tresc
    assert "Źródła" not in tresc and "permission-modes" not in tresc and "Sprawdzone 25.10.2026" not in tresc


def test_s1_reszta_tresci_bez_zmian(tmp_path):
    bez = _tresc(_strona(tmp_path, WSTEP))
    z = _tresc(_strona(tmp_path, WSTEP + "\n" + ZRODLA))
    assert z.strip() == bez.strip()


def test_s1_czesc_po_zrodlach_zostaje_w_tresci(tmp_path):
    dalej = "## Co dalej\n\nDalszy tekst po źródłach.\n"
    strona = _strona(tmp_path, WSTEP + "\n" + ZRODLA + "\n" + dalej)
    tresc = _tresc(strona)
    assert "Co dalej" in tresc and "Dalszy tekst po źródłach." in tresc
    assert "permission-modes" not in tresc
    (_, wnetrze), = _stopki(strona)
    assert LINK in wnetrze and "Co dalej" not in wnetrze and "Dalszy tekst" not in wnetrze


def test_s1_lekcja_bez_zrodel_bez_stopki(tmp_path):
    strona = _strona(tmp_path, WSTEP)
    assert "<footer" not in strona
    assert not re.search(r"\{\{[A-Z]+\}\}", strona)
    assert "Tekst części." in _tresc(strona)


def test_s1_naglowek_trzeciego_stopnia_zostaje_w_tresci(tmp_path):
    lekcja = WSTEP + "\n### Źródła\n\nTo zwykły nagłówek w treści.\n"
    strona = _strona(tmp_path, lekcja)
    assert "<footer" not in strona
    assert "To zwykły nagłówek w treści." in _tresc(strona)


def test_s1_prawdziwa_lekcja_straznik_zamiast_pytan():
    strona = zloz_strone(LEKCJA_STRAZNIK)
    stopki = _stopki(strona)
    assert len(stopki) == 1, f"oczekiwana jedna stopka <footer>, jest {len(stopki)}"
    _, wnetrze = stopki[0]
    for adres in ("permission-modes", "desktop", "desktop-quickstart"):
        assert f'href="https://code.claude.com/docs/en/{adres}"' in wnetrze
    assert "Sprawdzone 23–25.10.2026" in wnetrze
    tresc = _tresc(strona)
    assert "code.claude.com/docs/en/desktop-quickstart" not in tresc and "Sprawdzone 23–25.10.2026" not in tresc
    assert "Kiedy włączać tryb Auto, a kiedy nie" in tresc  # część przed źródłami zostaje
    assert strona.index('id="fiszki-lista"') < strona.index("<footer")
