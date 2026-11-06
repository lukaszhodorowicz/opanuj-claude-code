"""Testy walidatora kroku `zgoda` (karta zgody na zapis w folderze chronionym) i kliku `zatwierdz` w ćwiczeniu aplikacji z drogami."""

import copy
import json
from pathlib import Path

import pytest

from narzedzia import scenariusz as sc

KORZEN = Path(__file__).resolve().parent.parent
WZOR = json.loads((Path(__file__).parent / "dane" / "pierwszy-skill-zgoda-drogi.json").read_text(encoding="utf-8"))
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")
SKILL = ".claude/skills/odpowiedz-klientowi/SKILL.md"


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def jest(wynik, fragment):
    return any(fragment in b for b in wynik)


def kroki(d, cw=0, droga=0):
    return d["cwiczenia"][cw]["drogi"][droga]["kroki"]


def indeks(d, typ, cw=0, droga=0):
    return next(i for i, k in enumerate(kroki(d, cw, droga)) if k["typ"] == typ)


def test_wzor_przechodzi_nowy_plik_istniejacy_plik_i_droga_bez_zgody(dane):
    assert bledy(dane) == []
    assert [k["typ"] for k in kroki(dane)[3:7]] == ["zgoda", "nauczyciel", "klik", "claude"]
    assert not any(k["typ"] == "zgoda" for k in kroki(dane, 0, 1))  # druga droga bez zgody
    assert kroki(dane, 1, 0)[3]["plik"] in dane["cwiczenia"][1]["aplikacja"]["folder_startowy_dodatkowe"]  # plik istniejący


def test_accept_edits_zwykly_plik_bez_zgody_odrzucony(dane):
    kroki(dane)[3]["plik"] = "notatka.txt"
    wynik = bledy(dane)
    assert jest(wynik, "karta zgody w drodze to wariant „folder chroniony”") and jest(wynik, "plik „notatka.txt” musi leżeć w .claude/")
    assert jest(wynik, "accept-edits-sciezki-chronione-pytaja")


@pytest.mark.parametrize("plik", ["claude/skills/x/SKILL.md", "Klienci/.claude/skills/x/SKILL.md", ".claudeX/plik.md"])
def test_tylko_sciezka_zaczynajaca_sie_od_dot_claude_ukosnik(dane, plik):
    dane["cwiczenia"][0]["nowe_pliki"].append(plik)
    kroki(dane)[3]["plik"] = plik
    assert jest(bledy(dane), "musi leżeć w .claude/")


def test_tryb_manual_przyjmuje_karte_dla_dot_claude(dane):
    dane["cwiczenia"][0]["aplikacja"]["tryb"] = "Manual"
    assert not jest(bledy(dane), "karta zgody")


@pytest.mark.parametrize("tryb", ["Plan", "Auto"])
def test_inne_tryby_odrzucone(dane, tryb):
    dane["cwiczenia"][0]["aplikacja"]["tryb"] = tryb
    assert jest(bledy(dane), "karta zgody w drodze tylko w trybie Manual albo Accept edits")


def test_plik_nieistniejacy_odrzucony(dane):
    kroki(dane)[3]["plik"] = ".claude/skills/inny/SKILL.md"
    assert jest(bledy(dane), "plik „.claude/skills/inny/SKILL.md” nie istnieje w folder_startowy ani w nowe_pliki")


def test_plik_istniejacy_z_dodatkowych_przechodzi_a_bez_pola_nie(dane):
    del dane["cwiczenia"][1]["aplikacja"]["folder_startowy_dodatkowe"]
    assert jest(bledy(dane), f"plik „{SKILL}” nie istnieje w folder_startowy ani w nowe_pliki")


def test_linijki_w_karcie_odrzucone(dane):
    kroki(dane)[3]["linijki"] = [{"tekst": "x", "zmiana": "dodana"}]
    assert jest(bledy(dane), "karta zgody w drodze nie ma linijek")


def test_obce_pole_karty_odrzucone(dane):
    kroki(dane)[3]["etykieta"] = "Zatwierdź"
    assert jest(bledy(dane), "pole etykieta nie należy do kroku zgoda")


@pytest.mark.parametrize("plik", [None, "", 5, ".claude/../x.md", ".claude//x.md"])
def test_zla_wartosc_pola_plik(dane, plik):
    kroki(dane)[3]["plik"] = plik
    assert jest(bledy(dane), "zgoda wymaga pola plik")


@pytest.mark.parametrize("krok", [
    {"typ": "pisz", "tekst": "Jeszcze coś."},
    {"typ": "mysli"},
    {"typ": "claude", "tekst": "Zapisałem."},
    {"typ": "klik", "cel": "sciezka"},
    {"typ": "zgoda", "plik": SKILL},
])
def test_po_karcie_tylko_nauczyciel_albo_klik_zatwierdz(dane, krok):
    kroki(dane).insert(4, krok)
    assert jest(bledy(dane), "przy karcie zgody, która czeka")


def test_nauczyciel_po_karcie_jest_dozwolony(dane):
    kroki(dane).insert(4, {"typ": "nauczyciel", "tekst": "Jeszcze jedno zdanie."})
    assert not jest(bledy(dane), "przy karcie zgody")


def test_klik_zatwierdz_bez_karty(dane):
    del kroki(dane)[3]
    wynik = bledy(dane)
    assert jest(wynik, "klik zatwierdz bez karty zgody, która czeka na decyzję")


def test_klik_zatwierdz_zamiast_sciezki_w_drodze_bez_zgody(dane):
    kroki(dane, 0, 1)[4] = {"typ": "klik", "cel": "zatwierdz"}
    assert jest(bledy(dane), "klik zatwierdz bez karty zgody")


def test_cel_klika_spoza_listy_wymienia_zatwierdz(dane):
    kroki(dane)[5]["cel"] = "krzyzyk"
    assert jest(bledy(dane), "klik „krzyzyk”") and jest(bledy(dane), "cel „zatwierdz”")


def test_po_zatwierdzeniu_claude_wskazuje_ten_plik(dane):
    del kroki(dane)[6]["plik"]
    assert jest(bledy(dane), f"po zatwierdzeniu zapisu następny krok claude musi wskazać plik „{SKILL}”")
    kroki(dane)[6]["plik"] = "notatka.txt"
    kroki(dane)[6]["tekst"] = "Zapisałem notatka.txt."
    assert jest(bledy(dane), f"następny krok claude musi wskazać plik „{SKILL}”")


@pytest.mark.parametrize("krok", [{"typ": "pisz", "tekst": "Dalej."}, {"typ": "klik", "cel": "sciezka"}, {"typ": "plik", "nazwa": SKILL, "linijki": ["x"]}])
def test_po_zatwierdzeniu_inny_krok_niz_claude_odrzucony(dane, krok):
    kroki(dane).insert(6, krok)
    assert jest(bledy(dane), "po zatwierdzeniu zapisu: najpierw odpowiedź Claude z plikiem")


@pytest.mark.parametrize("krok", [{"typ": "nauczyciel", "tekst": "Zapis trwa."}, {"typ": "mysli"}])
def test_po_zatwierdzeniu_nauczyciel_i_mysli_przechodza(dane, krok):
    kroki(dane).insert(6, krok)
    assert not jest(bledy(dane), "po zatwierdzeniu zapisu")


def test_droga_konczy_sie_karta_ktora_czeka(dane):
    d = dane["cwiczenia"][0]["drogi"][0]
    d["kroki"] = d["kroki"][:4]
    wynik = bledy(dane)
    assert jest(wynik, "droga kończy się kartą zgody, która czeka na decyzję")


def test_droga_konczy_sie_zatwierdzeniem_bez_odpowiedzi(dane):
    d = dane["cwiczenia"][0]["drogi"][0]
    d["kroki"] = d["kroki"][:6]
    assert jest(bledy(dane), "po zatwierdzeniu zapisu droga nie ma odpowiedzi Claude")


def test_nowy_plik_z_zgoda_wymaga_odpowiedzi_claude(dane):
    del kroki(dane)[6]
    assert jest(bledy(dane), f"nowy plik „{SKILL}” bez odpowiedzi Claude")
