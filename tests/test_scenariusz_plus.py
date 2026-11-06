"""Testy walidatora przycisku +, listy poleceń i skilla w polu w drodze symulatora aplikacji: kroki `klik` z celami `plus`, `pozycja`, `wiersz` i krok `ukosnik` (wzór: tests/dane/gotowe-skille-plus-ukosnik.json)."""

import copy
import json
from pathlib import Path

import pytest

from narzedzia import scenariusz as sc

KORZEN = Path(__file__).resolve().parent.parent
WZOR = json.loads((Path(__file__).parent / "dane" / "gotowe-skille-plus-ukosnik.json").read_text(encoding="utf-8"))
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")
PLUS, NAUCZ1, POZYCJA, NAUCZ2, WIERSZ, NAUCZ3, PISZ = range(7)  # indeksy kroków drogi `plus`


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def jest(wynik, fragment):
    return any(fragment in b for b in wynik)


def kroki(d, droga=0):
    return d["cwiczenia"][0]["drogi"][droga]["kroki"]


def test_wzor_przechodzi(dane):
    assert bledy(dane) == []


def test_pozycja_bez_plus_to_blad(dane):
    del kroki(dane)[PLUS]
    assert jest(bledy(dane), "klik pozycja tylko po kroku plus")


def test_pozycja_z_napisem_spoza_menu_to_blad(dane):
    kroki(dane)[POZYCJA]["na"] = "Add slides"
    assert jest(bledy(dane), "spoza pozycji menu +")


def test_pozycja_bez_pola_na_to_blad(dane):
    del kroki(dane)[POZYCJA]["na"]
    assert jest(bledy(dane), "spoza pozycji menu +")


def test_inna_pozycja_menu_zamyka_menu_i_nie_otwiera_listy(dane):
    kroki(dane)[POZYCJA]["na"] = "Add plugins"
    assert jest(bledy(dane), "klik wiersz tylko przy otwartej liście")


def test_wiersz_bez_listy_to_blad(dane):
    k = kroki(dane)
    del k[PLUS:WIERSZ]
    assert jest(bledy(dane), "klik wiersz tylko przy otwartej liście")


def test_wiersz_wymaga_bez_napisu_albo_na(dane):
    del kroki(dane)[WIERSZ]["bez_napisu"]
    assert jest(bledy(dane), "wymaga pola bez_napisu: true")


@pytest.mark.parametrize("droga, indeks", [(0, WIERSZ), (1, 2)])
def test_wiersz_z_napisem_na_z_listy_zamiast_bez_napisu_przechodzi(dane, droga, indeks):
    """Napis spoza 13 wierszy listy sprawdza tests/test_scenariusz_menu_plus_napisy.py::test_wiersz_z_napisem_spoza_listy_to_blad; tu: stary wzór z `na` zamiast `bez_napisu` przechodzi w obu drogach."""
    krok = kroki(dane, droga)[indeks]
    assert krok == {"typ": "klik", "cel": "wiersz", "bez_napisu": True}
    del krok["bez_napisu"]
    krok["na"] = "plan"
    assert bledy(dane) == []


def test_nieznane_pole_w_kroku_to_blad(dane):
    kroki(dane)[PLUS]["na"] = "x"
    assert jest(bledy(dane), "pole na nie należy do kroku plus")


def test_pisz_przy_otwartym_menu_to_blad(dane):
    k = kroki(dane)
    k.insert(NAUCZ1, k.pop(PISZ))
    assert jest(bledy(dane), "krok pisz przy otwartym elemencie (menu przycisku +)")


def test_claude_przy_otwartej_liscie_to_blad(dane):
    k = kroki(dane)
    k.insert(NAUCZ2 + 1, {"typ": "claude", "tekst": "Dobrze."})
    assert jest(bledy(dane), "krok claude przy otwartym elemencie (lista poleceń)")


def test_nauczyciel_przy_otwartym_menu_jest_dozwolony(dane):
    assert not jest(bledy(dane), "przy otwartym elemencie")


def test_plus_przy_otwartym_menu_to_blad(dane):
    k = kroki(dane)
    k.insert(NAUCZ1, {"typ": "klik", "cel": "plus"})
    assert jest(bledy(dane), "krok plus przy otwartym elemencie")


def test_droga_konczy_sie_skillem_w_polu_bez_pisz(dane):
    k = kroki(dane)
    del k[PISZ:]
    k.append({"typ": "klik", "cel": "sciezka"})  # i tak błąd drogi, ale chodzi o skill w polu
    assert jest(bledy(dane), "skill w polu wiadomości")


def test_pisz_po_wierszu_zdejmuje_skill_z_pola(dane):
    assert not jest(bledy(dane), "droga kończy się otwartym elementem")


def test_droga_konczy_sie_otwartym_menu(dane):
    k = kroki(dane)
    del k[POZYCJA:]
    assert jest(bledy(dane), "droga kończy się otwartym elementem (menu przycisku +)")


def test_ukosnik_otwiera_liste_bez_menu(dane):
    k = kroki(dane, 1)
    assert k[0]["typ"] == "ukosnik" and bledy(dane) == []
    k.insert(1, {"typ": "ukosnik"})
    assert jest(bledy(dane), "krok ukosnik przy otwartym elemencie (lista poleceń)")


def test_pozycja_po_ukosniku_to_blad(dane):
    k = kroki(dane, 1)
    k.insert(1, {"typ": "klik", "cel": "pozycja", "na": "Slash commands"})
    assert jest(bledy(dane), "klik pozycja tylko po kroku plus")


def test_nieznany_cel_klik_wymienia_nowe_cele(dane):
    kroki(dane)[PLUS]["cel"] = "menu"
    assert jest(bledy(dane), "„plus”, „pozycja”, „wiersz”")


def test_napisy_ze_zrodla_w_yaml():
    for napis in ("+", "/", "Add files or photos", "Add folder", "Import GitHub issue", "Slash commands", "Connectors", "Plugins", "Type to filter"):
        assert any(w.get("napis") == napis and w.get("gdzie") == "aplikacja" for w in NAPISY), napis
