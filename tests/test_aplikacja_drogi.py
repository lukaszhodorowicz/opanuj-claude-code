"""Testy dróg symulatora aplikacji Claude: walidator (prośba kursanta, ścieżka, otwarty plik, brak licznika), rytm nauczyciela w czytelnosc.py i podgląd pliku w tekście lekcji."""

import copy
import json
import re
from pathlib import Path

import pytest

from narzedzia import czytelnosc
from narzedzia import scenariusz as sc
from narzedzia import zrzuty
from narzedzia.strona import zloz_strone

KORZEN = Path(__file__).resolve().parent.parent
WZOR = json.loads(
    (Path(__file__).parent / "dane" / "aplikacja-drogi.json").read_text(
        encoding="utf-8"
    )
)
WZOR_KROKI = json.loads(
    (Path(__file__).parent / "dane" / "aplikacja.json").read_text(encoding="utf-8")
)
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


def cw(d):
    return d["cwiczenia"][0]


def kroki(d, nr=0):
    return cw(d)["drogi"][nr]["kroki"]


def typ(d, t, nr=0):
    return next(k for k in kroki(d, nr) if k["typ"] == t)


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def jest(wynik, fragment):
    return any(fragment in b for b in wynik)


def test_wzor_bez_bledow(dane):
    assert bledy(dane) == []


def test_probka_bez_bledow():
    probka = json.loads(
        (KORZEN / "tests" / "dane" / "probka-aplikacja.json").read_text(
            encoding="utf-8"
        )
    )
    assert bledy(probka) == []


def test_kroki_albo_drogi(dane):
    cw(dane)["kroki"] = WZOR_KROKI["cwiczenia"][0]["kroki"]
    assert jest(bledy(dane), "albo listę kroki, albo listę drogi")
    del cw(dane)["kroki"], cw(dane)["drogi"]
    assert jest(bledy(dane), "albo listę kroki, albo listę drogi")


def test_drogi_wymagaja_schowanego_panelu_i_bez_zmian(dane):
    del cw(dane)["aplikacja"]["panel"]
    cw(dane)["aplikacja"]["zmiany"] = WZOR_KROKI["cwiczenia"][0]["aplikacja"]["zmiany"]
    wynik = bledy(dane)
    assert jest(wynik, "wymaga panel „schowany”")
    assert jest(wynik, "nie ma pola zmiany")


def test_panel_schowany_tylko_w_drogach():
    d = copy.deepcopy(WZOR_KROKI)
    cw(d)["aplikacja"]["panel"] = "schowany"
    assert jest(bledy(d), "panel „schowany” tylko w ćwiczeniu z drogami")
    cw(d)["aplikacja"]["panel"] = "zwiniety"
    assert jest(bledy(d), "panel „zwiniety” spoza widoczny/schowany")


def test_licznik_w_drodze_odrzucony(dane):
    typ(dane, "klik")["cel"] = "licznik"
    assert jest(bledy(dane), "klik „licznik”: w drogach klika się tylko ścieżkę pliku")


def test_sciezka_spoza_folderu_i_spoza_tekstu(dane):
    typ(dane, "claude")["plik"] = "faktura.txt"
    wynik = bledy(dane)
    assert jest(wynik, "plik „faktura.txt” nie istnieje w folder_startowy")
    assert jest(wynik, "tekst odpowiedzi nie zawiera ścieżki „faktura.txt”")


def test_klik_bez_sciezki_w_odpowiedzi(dane):
    del typ(dane, "claude")["plik"]
    assert jest(
        bledy(dane), "klik w ścieżkę bez wcześniejszej odpowiedzi Claude z polem plik"
    )


def test_prosba_miedzy_odpowiedzia_a_klikiem_kasuje_sciezke(dane):
    k = kroki(dane)
    i = next(i for i, x in enumerate(k) if x["typ"] == "klik")
    k.insert(i, {"typ": "pisz", "tekst": "A jednak nie."})
    assert jest(bledy(dane), "klik w ścieżkę bez wcześniejszej odpowiedzi")


def test_plik_tylko_zaraz_po_kliku(dane):
    k = kroki(dane)
    i = next(i for i, x in enumerate(k) if x["typ"] == "klik")
    k.insert(i + 1, {"typ": "mysli"})
    wynik = bledy(dane)
    assert jest(wynik, "po kroku klik w ścieżkę musi być krok plik")
    assert jest(wynik, "plik otwiera się tylko zaraz po kroku klik")


def test_klik_na_koncu_drogi(dane):
    k = kroki(dane)
    while k[-1]["typ"] != "klik":
        k.pop()
    wynik = bledy(dane)
    assert jest(wynik, "po kroku klik w ścieżkę musi być krok plik")
    assert jest(wynik, "droga bez kroku plik")


def test_nazwa_otwartego_pliku_inna_niz_klikniata(dane):
    typ(dane, "plik")["nazwa"] = "cennik-2026.txt"
    assert jest(
        bledy(dane),
        "nazwa „cennik-2026.txt” inna niż kliknięta ścieżka „oferta-slub.txt”",
    )


def test_mysli_bez_slow_i_z_rozsadnym_czasem(dane):
    typ(dane, "mysli")["tekst"] = "Thinking…"
    typ(dane, "mysli", 1)["ms"] = 0
    wynik = bledy(dane)
    assert jest(wynik, "mysli bez tekstu")
    assert jest(wynik, "ms musi być liczbą całkowitą od 1 do")


def test_linijki_pliku(dane):
    typ(dane, "plik")["linijki"] = ["", "  "]
    typ(dane, "plik", 1)["linijki"] = ["Oferta", 5]
    wynik = bledy(dane)
    assert jest(wynik, "co najmniej jedną niepustą")
    assert jest(wynik, "każda linijka pliku musi być napisem")


def test_id_drog(dane):
    cw(dane)["drogi"][1]["id"] = cw(dane)["drogi"][0]["id"]
    assert jest(bledy(dane), "powtórzone w ćwiczeniu")
    cw(dane)["drogi"][1]["id"] = "Cofnij"
    assert jest(bledy(dane), "droga wymaga pola id")


def test_zle_typy_bez_wyjatku(dane):
    cw(dane)["drogi"][0]["kroki"] = "x"
    cw(dane)["drogi"][1]["kroki"] = [5, {"typ": "skacz"}]
    wynik = bledy(dane)
    assert jest(wynik, "droga wymaga niepustej listy kroki")
    assert jest(wynik, "krok musi być obiektem") and jest(wynik, "typ „skacz”")


def test_przyklad_drog_z_formatu_bez_bledow(dane):
    tekst = (KORZEN / "dane" / "FORMAT-SCENARIUSZA.md").read_text(encoding="utf-8")
    przyklad = tekst[tekst.index("### Drogi: prośba kursanta") :]
    kod = re.search(r"```json\n(.*?)```", przyklad, re.S).group(1).replace("…", "x")
    cwiczenie = json.loads(kod)
    fakt = typ(dane, "pisz")["fakt"]
    for k in cwiczenie["drogi"][0]["kroki"]:
        if "fakt" in k:
            k["fakt"] = fakt
    dane["cwiczenia"] = [cwiczenie]
    assert bledy(dane) == []


# ---------- czytelnosc.py: rytm nauczyciela w drogach ----------


def _czytelnosc(tmp_path, d):
    plik = tmp_path / "scenariusz.json"
    plik.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return czytelnosc.sprawdz_scenariusz(plik, "s")


def test_czytelnosc_wzor_bez_bledow(tmp_path, dane):
    assert _czytelnosc(tmp_path, dane) == []


def test_nauczyciel_najdalej_2_kroki_po_otwarciu_pliku(tmp_path, dane):
    k = kroki(dane)
    i = next(i for i, x in enumerate(k) if x["typ"] == "plik")
    k[i + 1 : i + 1] = [{"typ": "mysli"}, {"typ": "mysli"}]
    assert _czytelnosc(tmp_path, dane) == [
        "s: ćwiczenie cw2, droga popraw, krok 6 (plik): brak nauczyciela w 2 kolejnych krokach."
    ]


def test_dlugi_nauczyciel_w_drodze_i_w_kroku(tmp_path, dane):
    typ(dane, "nauczyciel")["tekst"] = "słowo " * 26
    wynik = _czytelnosc(tmp_path, dane)
    assert jest(wynik, "droga popraw, krok 4 (nauczyciel): 26 słów")
    d = copy.deepcopy(WZOR_KROKI)
    cw(d)["kroki"][0]["nauczyciel"] = "słowo " * 26
    assert jest(_czytelnosc(tmp_path, d), "ćwiczenie cw1, krok 1 (nauczyciel): 26 słów")


# ---------- strona i zrzuty ----------

LEKCJA = "# Próbka\n\n<!-- cwiczenie: cw2 -->\n\n<!-- kolumny -->\n#### A\n<!-- podglad: cw2 popraw -->\n#### B\n<!-- podglad: cw2 cofnij -->\n<!-- /kolumny -->\n"


def _strona(tmp_path, lekcja=LEKCJA):
    (tmp_path / "lekcja.md").write_text(lekcja, encoding="utf-8")
    (tmp_path / "scenariusz.json").write_text(
        json.dumps(WZOR, ensure_ascii=False), encoding="utf-8"
    )
    return zloz_strone(tmp_path)


def test_strona_przyjmuje_podglad_drogi(tmp_path):
    html = _strona(tmp_path)
    assert '<div class="podglad" data-cw="cw2" data-t="popraw"></div>' in html
    assert '<div class="podglad" data-cw="cw2" data-t="cofnij"></div>' in html
    assert "PK.drogiAplikacji = function" in html


@pytest.mark.parametrize(
    "znacznik", ["<!-- podglad: cw2 inna -->", "<!-- podglad: cw2 popraw 1 -->"]
)
def test_strona_odrzuca_zly_podglad_drogi(tmp_path, znacznik):
    with pytest.raises(ValueError):
        _strona(tmp_path, "# P\n\n<!-- cwiczenie: cw2 -->\n\n" + znacznik + "\n")


def test_drogi_nie_wlaczaja_przyciskow_paska():
    """Dokumentacja nie wiąże kliku w ścieżkę z żadnym przyciskiem na pasku tytułu (desktop.md:236)."""
    js = (KORZEN / "strona" / "aplikacja.js").read_text(encoding="utf-8")
    drogi = js[js.index("PK.drogiAplikacji = function") :]
    assert "data-pasek" not in drogi and "wlaczony" not in drogi


def test_pauza_claude_bez_slow():
    js = (KORZEN / "strona" / "aplikacja.js").read_text(encoding="utf-8")
    assert (
        '\'<div class="apl-mysli" aria-hidden="true"><i></i><i></i><i></i></div>\''
        in js
    )


def test_zrzuty_czekaja_na_element_do_klikniecia():
    assert "!document.querySelector(sel)" in zrzuty.SKRYPT
