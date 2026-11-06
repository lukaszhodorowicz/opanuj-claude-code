"""Testy walidatora menu + z podmenu Plugins i Connectors (pozycje `Connectors`, `Plugins`, `Browse connectors`, `Browse plugins`, `Manage …`) i listy „/” z nazwanymi wierszami (krok `wiersz` z polem `na` albo `bez_napisu`), według zrzutów Łukasza z 27.10.2026 (wzór: tests/dane/napisy-menu-plus.json)."""

import copy
import json
from pathlib import Path

import pytest

from narzedzia import scenariusz as sc
from narzedzia import scenariusz_plus as plus

KORZEN = Path(__file__).resolve().parent.parent
WZOR = json.loads((Path(__file__).parent / "dane" / "napisy-menu-plus.json").read_text(encoding="utf-8"))
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")
# indeksy kroków trzech dróg wzoru
K_PLUS, K_NAUCZ1, K_RODZIC, K_NAUCZ2, K_POZYCJA = range(5)  # konektory i wtyczki: plus, nauczyciel, Connectors/Plugins, nauczyciel, Browse …
P_PLUS, P_NAUCZ1, P_SLASH, P_NAUCZ2, P_WIERSZ = range(5)  # polecenia: plus, nauczyciel, Slash commands, nauczyciel, wiersz


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


def bledy(d, napisy=NAPISY):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, napisy)


def jest(wynik, fragment):
    return any(fragment in b for b in wynik)


def kroki(d, droga):
    return next(x for x in d["cwiczenia"][0]["drogi"] if x["id"] == droga)["kroki"]


def test_wzor_przechodzi(dane):
    assert bledy(dane) == []


def test_stale_walidatora_to_sesc_pozycji_menu_i_dwa_podmenu():
    assert plus.MENU_PLUS == ("Add files or photos", "Add folder", "Import GitHub issue", "Slash commands", "Connectors", "Plugins")
    assert plus.PODMENU == {"Plugins": ("Manage plugins", "Browse plugins"), "Connectors": ("Browse connectors", "Manage connectors")}
    assert len(plus.WIERSZE_LISTY) == 13 and plus.WIERSZE_LISTY[0] == "plugin"


@pytest.mark.parametrize("stare", ["Add connectors", "Add plugins"])
def test_stare_napisy_menu_nie_sa_juz_pozycjami(dane, stare):
    kroki(dane, "polecenia")[P_SLASH]["na"] = stare
    assert jest(bledy(dane), "spoza pozycji menu +")


# podmenu: kolejność kroków

@pytest.mark.parametrize("droga, rodzic, dziecko", [("wtyczki", "Plugins", "Browse plugins"), ("konektory", "Connectors", "Browse connectors")])
def test_pozycja_podmenu_bez_klika_w_rodzica_to_blad(dane, droga, rodzic, dziecko):
    k = kroki(dane, droga)
    del k[K_RODZIC:K_POZYCJA]
    assert jest(bledy(dane), f"pozycja „{dziecko}” należy do podmenu „{rodzic}”")


def test_pozycja_podmenu_pod_innym_rodzicem_to_blad(dane):
    kroki(dane, "wtyczki")[K_RODZIC]["na"] = "Connectors"
    assert jest(bledy(dane), "pozycja „Browse plugins” należy do podmenu „Plugins”")


def test_klik_w_rodzica_zostawia_menu_otwarte(dane):
    k = kroki(dane, "wtyczki")
    k.insert(K_NAUCZ2 + 1, {"typ": "pisz", "tekst": "Cześć"})
    assert jest(bledy(dane), "krok pisz przy otwartym elemencie (menu przycisku +)")


def test_drugi_rodzic_przy_otwartym_podmenu_to_blad(dane):
    """Na wąskim ekranie podmenu zasłania menu, więc przełączanie podmenu nie jest krokiem kursu."""
    k = kroki(dane, "wtyczki")
    k.insert(K_NAUCZ2 + 1, {"typ": "klik", "cel": "pozycja", "na": "Connectors"})
    assert jest(bledy(dane), "przy otwartym podmenu „Plugins”")


def test_pozycja_podmenu_zamyka_menu_i_podmenu(dane):
    k = kroki(dane, "wtyczki")
    k[K_POZYCJA]["na"] = "Manage plugins"
    k.insert(K_POZYCJA + 1, {"typ": "klik", "cel": "pozycja", "na": "Browse plugins"})
    assert jest(bledy(dane), "klik pozycja tylko po kroku plus")


def test_manage_plugins_i_manage_connectors_zamykaja_menu_bez_skutku(dane):
    for droga, na in (("wtyczki", "Manage plugins"), ("konektory", "Manage connectors")):
        d = copy.deepcopy(dane)
        kroki(d, droga)[K_POZYCJA]["na"] = na
        w = bledy(d)
        assert not jest(w, "należy do podmenu") and not jest(w, "spoza pozycji menu +"), (droga, w)


def test_slash_commands_zamyka_menu_i_otwiera_liste(dane):
    assert bledy(dane) == []
    k = kroki(dane, "polecenia")
    k.insert(P_NAUCZ2, {"typ": "klik", "cel": "plus"})
    assert jest(bledy(dane), "krok plus przy otwartym elemencie (lista poleceń)")


def test_import_github_issue_nie_jest_celem_kroku(dane):
    kroki(dane, "polecenia")[P_SLASH]["na"] = "Import GitHub issue"
    assert jest(bledy(dane), "zawsze wyszarzona")


def test_droga_nie_konczy_sie_otwartym_podmenu(dane):
    k = kroki(dane, "wtyczki")
    del k[K_NAUCZ2:]
    assert jest(bledy(dane), "droga kończy się otwartym elementem (menu przycisku +)")


# środowisko

def test_plugins_i_add_folder_w_cloud_sa_wyszarzone(dane):
    dane["cwiczenia"][0]["aplikacja"]["srodowisko"] = "Cloud"
    w = bledy(dane)
    assert jest(w, "pozycja „Plugins” w środowisku Cloud jest wyszarzona")
    d = copy.deepcopy(WZOR)
    d["cwiczenia"][0]["aplikacja"]["srodowisko"] = "Cloud"
    kroki(d, "polecenia")[P_SLASH]["na"] = "Add folder"
    assert jest(bledy(d), "pozycja „Add folder” w środowisku Cloud jest wyszarzona")


def test_connectors_w_cloud_otwiera_podmenu_ale_browse_connectors_zostaje_bledem(dane):
    dane["cwiczenia"][0]["aplikacja"]["srodowisko"] = "Cloud"
    w = bledy(dane)
    assert not jest(w, "pozycja „Connectors” w środowisku Cloud")
    assert jest(w, "„Browse connectors” w środowisku Cloud")
    assert jest(w, "„Browse plugins” w środowisku Cloud")


@pytest.mark.parametrize("srodowisko", ["Local", "SSH"])
def test_wzor_w_local_i_ssh_przechodzi(dane, srodowisko):
    dane["cwiczenia"][0]["aplikacja"]["srodowisko"] = srodowisko
    assert bledy(dane) == []


def test_browse_plugins_w_pustej_rozmowie_zostaje_bledem(dane):
    dane["cwiczenia"][0]["aplikacja"]["rozmowa"] = []
    assert jest(bledy(dane), "w pustej rozmowie")


# lista „/”: krok wiersz z `na` albo `bez_napisu`

@pytest.mark.parametrize("nazwa", plus.WIERSZE_LISTY)
def test_kazdy_nazwany_wiersz_listy_jest_celem_kroku(dane, nazwa):
    kroki(dane, "polecenia")[P_WIERSZ]["na"] = nazwa
    assert bledy(dane) == []


def test_wiersz_z_napisem_spoza_listy_to_blad(dane):
    kroki(dane, "polecenia")[P_WIERSZ]["na"] = "design-system"
    assert jest(bledy(dane), "spoza wierszy listy poleceń")


def test_wiersz_bez_na_i_bez_bez_napisu_to_blad(dane):
    del kroki(dane, "polecenia")[P_WIERSZ]["na"]
    assert jest(bledy(dane), "wymaga pola bez_napisu: true")


def test_wiersz_z_na_i_bez_napisu_naraz_to_blad(dane):
    kroki(dane, "polecenia")[P_WIERSZ]["bez_napisu"] = True
    assert jest(bledy(dane), "albo pole na")


def test_wiersz_bez_napisu_zostaje_dozwolony_dla_starych_scenariuszy(dane):
    krok = kroki(dane, "polecenia")[P_WIERSZ]
    del krok["na"]
    krok["bez_napisu"] = True
    assert bledy(dane) == []


def test_wiersz_bez_napisu_false_to_blad(dane):
    krok = kroki(dane, "polecenia")[P_WIERSZ]
    del krok["na"]
    krok["bez_napisu"] = False
    assert jest(bledy(dane), "wymaga pola bez_napisu: true")


def test_napis_wiersza_musi_stac_w_liscie_napisow(dane):
    bez_planu = [w for w in NAPISY if w.get("napis") != "plan"]
    assert jest(bledy(dane, bez_planu), "napis „plan” spoza listy napisów interfejsu aplikacji")


def test_wiersz_bez_otwartej_listy_to_blad(dane):
    k = kroki(dane, "polecenia")
    del k[P_PLUS:P_WIERSZ]
    assert jest(bledy(dane), "klik wiersz tylko przy otwartej liście")


def test_ukosnik_otwiera_ta_sama_liste_z_nazwanymi_wierszami(dane):
    k = kroki(dane, "polecenia")
    del k[P_PLUS:P_WIERSZ]
    k.insert(0, {"typ": "ukosnik"})
    k.insert(1, {"typ": "nauczyciel", "tekst": "To lista poleceń. Kliknij wiersz plan."})
    assert bledy(dane) == []
