"""Testy walidatora karty zgody przeglądarki w drodze symulatora aplikacji, część 1: krok `zgoda` z `witryna` (przyciski Allow once, Always allow, Deny), tryby, kliki `allow_once`, `always_allow` i `deny` oraz skutek decyzji (wzory: tests/dane/strona-zewnetrzna-zgoda.json i strona-zewnetrzna-dwie-strony.json)."""

import copy
import json

import pytest

from narzedzia import scenariusz as sc
from tests.pomoc_zgoda_strona import DANE, DWIE, ODMOW, RAZ, WZOR, ZAWSZE, bledy, gdzie, jest, karta, kroki, ustaw_tryb


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


@pytest.fixture
def dwie():
    return copy.deepcopy(DWIE)


# wzory


def test_wzory_przechodza_walidator(dane, dwie):
    assert bledy(dane) == []
    assert bledy(dwie) == []
    assert [x["id"] for x in dane["cwiczenia"][0]["drogi"]] == [RAZ, ODMOW, ZAWSZE]
    assert [k["cel"] for x in dane["cwiczenia"][0]["drogi"] for k in x["kroki"] if k["typ"] == "klik" and k["cel"] != "sciezka"] == ["allow_once", "deny", "always_allow"]


def test_komenda_scenariusza_przechodzi_dla_obu_wzorow(capsys):
    assert sc.main([str(DANE / "strona-zewnetrzna-zgoda.json")]) == 0
    assert sc.main([str(DANE / "strona-zewnetrzna-dwie-strony.json")]) == 0
    assert capsys.readouterr().out.count(": ok") == 2


def test_dwie_karty_dla_dwoch_stron_w_jednej_drodze_allow_once_potem_deny(dwie):
    lista = kroki(dwie, "dwie-strony")
    assert [k["witryna"] for k in lista if k["typ"] == "zgoda"] == ["Drukarnia Kolor", "Rabaty-Druk"]
    assert [k["cel"] for k in lista if k["typ"] == "klik"][:2] == ["allow_once", "deny"]
    assert dwie["cwiczenia"][0]["aplikacja"]["tryb"] == "Accept edits"


def test_po_deny_plik_zajmuje_panel_z_wczesniej_otwarta_strona_innej_witryny(dwie):
    lista = kroki(dwie, "dwie-strony")
    ostatnia_strona = max(i for i, k in enumerate(lista) if k["typ"] == "strona")
    deny = gdzie(lista, "klik", "deny")
    assert ostatnia_strona < deny < gdzie(lista, "claude", nr=2) < gdzie(lista, "klik", "sciezka") < gdzie(lista, "plik")
    assert lista[gdzie(lista, "claude", nr=2)]["plik"] == "ceny-druku.txt"
    assert bledy(dwie) == []


# karta: pole witryna


@pytest.mark.parametrize("pole", ["plik", "polecenie"])
def test_witryna_razem_z_plik_albo_polecenie_odrzucona(dane, pole):
    karta(dane)[pole] = ".claude/settings.json" if pole == "plik" else "zip"
    assert jest(bledy(dane), "krok zgoda ma dokładnie jedno z pól plik, polecenie albo witryna")


@pytest.mark.parametrize("witryna", ["", "  ", 5, None, ["Zet"]])
def test_witryna_musi_byc_niepustym_napisem(dane, witryna):
    karta(dane)["witryna"] = witryna
    assert jest(bledy(dane), "pole witryna to nazwa strony")


def test_odliczanie_ms_w_karcie_z_witryna_odrzucone(dane):
    karta(dane).update({"odliczanie_ms": 3000})
    assert jest(bledy(dane), "odliczanie_ms nie działa w karcie zgody z polem witryna")


def test_linijki_i_obce_pole_w_karcie_z_witryna_odrzucone(dane):
    karta(dane)["linijki"] = [{"tekst": "x", "zmiana": "dodana"}]
    karta(dane)["przycisk"] = "Allow once"
    wynik = bledy(dane)
    assert jest(wynik, "karta zgody w drodze nie ma linijek") and jest(wynik, "pole przycisk nie należy do kroku zgoda")


def test_karta_bez_pola_fakt_przechodzi(dane):
    del karta(dane)["fakt"]
    assert bledy(dane) == []


# tryby


@pytest.mark.parametrize("tryb", ["Manual", "Accept edits", "Auto"])
def test_karta_przegladarki_w_trybach_manual_accept_edits_i_auto(dane, tryb):
    ustaw_tryb(dane, tryb)
    assert bledy(dane) == []


def test_karta_przegladarki_w_trybie_plan_odrzucona(dane):
    ustaw_tryb(dane, "Plan")
    wynik = bledy(dane)
    assert jest(wynik, "karta zgody przeglądarki w drodze tylko w trybie Manual, Accept edits albo Auto (teraz „Plan”)")
    assert jest(wynik, "aplikacja-browser-klasyfikator-sprawdza-klikanie-i-pisanie")


@pytest.mark.parametrize("tryb", ["Auto", "Plan"])
def test_plik_i_polecenie_zostaja_przy_manual_i_accept_edits(tryb):
    d = json.loads((DANE / "hook-zgoda-polecenie.json").read_text(encoding="utf-8"))
    ustaw_tryb(d, tryb)
    assert jest(bledy(d), "karta zgody w drodze tylko w trybie Manual albo Accept edits")


# kliki


def test_klik_zatwierdz_przy_karcie_z_witryna_odrzucony(dane):
    lista = kroki(dane)
    lista[gdzie(lista, "klik", "allow_once")]["cel"] = "zatwierdz"
    wynik = bledy(dane)
    assert jest(wynik, "klik zatwierdz przy karcie zgody z polem witryna: karta przeglądarki nie ma ptaszka, tylko przyciski Allow once, Always allow i Deny")
    assert jest(wynik, "„allow_once”, „always_allow” albo „deny”")


@pytest.mark.parametrize("cel", ["allow_once", "always_allow", "deny"])
def test_klik_decyzji_bez_karty_odrzucony(dane, cel):
    lista = kroki(dane, ODMOW)
    lista[gdzie(lista, "klik", "deny")]["cel"] = cel
    del lista[gdzie(lista, "zgoda")]
    assert jest(bledy(dane), f"klik „{cel}” bez karty zgody przeglądarki, która czeka na decyzję")


@pytest.mark.parametrize("cel", ["allow_once", "always_allow", "deny"])
def test_klik_decyzji_przy_karcie_na_plik_albo_polecenie_odrzucony(cel):
    d = json.loads((DANE / "hook-zgoda-polecenie.json").read_text(encoding="utf-8"))
    lista = next(x for x in d["cwiczenia"][0]["drogi"] if x["id"] == "hook")["kroki"]
    lista[gdzie(lista, "klik", "zatwierdz")]["cel"] = cel
    assert jest(bledy(d), f"klik „{cel}” bez karty zgody przeglądarki")


@pytest.mark.parametrize("krok", [
    {"typ": "pisz", "tekst": "Dalej."},
    {"typ": "mysli"},
    {"typ": "claude", "tekst": "Wchodzę."},
    {"typ": "klik", "cel": "sciezka"},
    {"typ": "strona", "witryna": "Serwis Rowerowy Zet", "strona": {}},
])
def test_przy_karcie_z_witryna_tylko_nauczyciel_albo_klik_decyzji(dane, krok):
    lista = kroki(dane)
    lista.insert(gdzie(lista, "zgoda") + 1, krok)
    assert jest(bledy(dane), "przy karcie zgody przeglądarki, która czeka: Claude czeka na Twój wybór")


def test_nauczyciel_przy_karcie_z_witryna_jest_dozwolony(dane):
    lista = kroki(dane)
    lista.insert(gdzie(lista, "zgoda") + 1, {"typ": "nauczyciel", "tekst": "Jeszcze jedno zdanie."})
    assert bledy(dane) == []


def test_nieznany_klik_wymienia_nowe_cele(dane):
    lista = kroki(dane)
    lista[gdzie(lista, "klik", "allow_once")]["cel"] = "licznik"
    assert jest(bledy(dane), "przyciski karty przeglądarki (cele „allow_once”, „always_allow”, „deny”)")


# skutek decyzji


@pytest.mark.parametrize("krok", [
    {"typ": "pisz", "tekst": "Dalej."},
    {"typ": "claude", "tekst": "Spisałem."},
    {"typ": "klik", "cel": "sciezka"},
])
@pytest.mark.parametrize("cel", ["allow_once", "always_allow"])
def test_po_zezwoleniu_inny_krok_niz_strona_odrzucony(dane, krok, cel):
    lista = kroki(dane)
    lista[gdzie(lista, "klik", "allow_once")]["cel"] = cel
    lista.insert(gdzie(lista, "klik", cel) + 1, krok)
    assert jest(bledy(dane), "po zezwoleniu (" + ("Allow once" if cel == "allow_once" else "Always allow") + "): najpierw krok strona z witryna „Serwis Rowerowy Zet”")


@pytest.mark.parametrize("krok", [{"typ": "nauczyciel", "tekst": "Czekamy."}, {"typ": "mysli"}])
def test_po_zezwoleniu_nauczyciel_i_mysli_przechodza(dane, krok):
    lista = kroki(dane)
    lista.insert(gdzie(lista, "klik", "allow_once") + 1, krok)
    assert bledy(dane) == []


@pytest.mark.parametrize("krok", [
    {"typ": "pisz", "tekst": "Dalej."},
    {"typ": "klik", "cel": "sciezka"},
    {"typ": "plik", "nazwa": "ceny-konkurencji.txt", "linijki": ["x"]},
])
def test_po_deny_inny_krok_niz_claude_odrzucony(dane, krok):
    lista = kroki(dane, ODMOW)
    lista.insert(gdzie(lista, "klik", "deny") + 1, krok)
    assert jest(bledy(dane), "po odmowie (Deny): najpierw odpowiedź Claude")


@pytest.mark.parametrize("krok", [{"typ": "nauczyciel", "tekst": "Odmowa."}, {"typ": "mysli"}])
def test_po_deny_nauczyciel_i_mysli_przechodza(dane, krok):
    lista = kroki(dane, ODMOW)
    lista.insert(gdzie(lista, "klik", "deny") + 1, krok)
    assert bledy(dane) == []


def test_droga_konczy_sie_karta_z_witryna_ktora_czeka(dane):
    d = next(x for x in dane["cwiczenia"][0]["drogi"] if x["id"] == ODMOW)
    d["kroki"] = d["kroki"][: gdzie(d["kroki"], "zgoda") + 1]
    assert jest(bledy(dane), "droga kończy się kartą zgody, która czeka na decyzję: dodaj klik „allow_once”, „always_allow” albo „deny”")


def test_droga_konczy_sie_allow_once_bez_kroku_strona(dane):
    lista = kroki(dane)
    del lista[gdzie(lista, "strona") :]
    assert jest(bledy(dane), "po zezwoleniu (Allow once) droga nie ma kroku strona z witryna „Serwis Rowerowy Zet”")


def test_droga_konczy_sie_deny_bez_odpowiedzi_claude(dane):
    lista = kroki(dane, ODMOW)
    del lista[gdzie(lista, "klik", "deny") + 1 :]
    assert jest(bledy(dane), "po odmowie (Deny) droga nie ma odpowiedzi Claude")
