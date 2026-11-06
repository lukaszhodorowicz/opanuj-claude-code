"""Testy walidatora scenariuszy symulatora."""
import json
from pathlib import Path

import pytest

from narzedzia import scenariusz as sc

KORZEN = Path(__file__).resolve().parent.parent
DANE = Path(__file__).resolve().parent / "dane" / "scenariusz"
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")


@pytest.fixture
def poprawny():
    return json.loads((DANE / "poprawny.json").read_text(encoding="utf-8"))


def bledy(dane):
    return sc.sprawdz_scenariusz(dane, FAKTY_ID, NAPISY)


def krok_z(dane, i):
    return dane["cwiczenia"][0]["zadania"][0]["przebiegi"]["z"][i]


def test_poprawny_bez_bledow(poprawny):
    assert bledy(poprawny) == []


def test_napis_menu_spoza_listy(poprawny):
    krok_z(poprawny, 1)["opcje"][0]["napis"] = "Yes, do it"
    wynik = bledy(poprawny)
    assert any("cw1/zadania[0]/przebiegi/z[1]/opcje[0]" in b and "spoza listy" in b for b in wynik)


def test_opcja_bez_opisu(poprawny):
    del krok_z(poprawny, 1)["opcje"][1]["opis"]
    assert any("opcje[1]" in b and "opis" in b for b in bledy(poprawny))


def test_nieznany_typ(poprawny):
    krok_z(poprawny, 0)["typ"] = "taniec"
    assert any("z[0]" in b and "taniec" in b for b in bledy(poprawny))


def test_fakt_nieistniejacy(poprawny):
    poprawny["cwiczenia"][0]["zadania"][0]["przebiegi"]["bez"][5]["fakt"] = "nie-ma-takiego"
    assert any("bez[5]" in b and "nie-ma-takiego" in b for b in bledy(poprawny))


def test_fakt_pomijany_gdy_brak_zbioru(poprawny):
    krok_z(poprawny, 1)["opcje"][0]["fakt"] = "nie-ma-takiego"
    assert sc.sprawdz_scenariusz(poprawny, None, NAPISY) == []


def test_brak_przebiegu_dla_terminala(poprawny):
    del poprawny["cwiczenia"][0]["zadania"][0]["przebiegi"]["z"]
    assert any("brak przebiegu dla terminala „z”" in b for b in bledy(poprawny))


def test_zly_tryb(poprawny):
    poprawny["cwiczenia"][0]["terminale"][0]["tryb"] = "turbo"
    assert any("turbo" in b for b in bledy(poprawny))
    poprawny["cwiczenia"][0]["terminale"][0]["tryb"] = "edycje"
    krok_z(poprawny, 0)["na"] = "turbo"
    assert any("z[0]" in b and "turbo" in b for b in bledy(poprawny))


def test_przelacznik_cel_spoza_cyklu(poprawny):
    poprawny["cwiczenia"][1]["cel"] = "auto"
    assert any("cel „auto” nie leży w cyklu" in b for b in bledy(poprawny))


def test_przelacznik_brak_komentarza(poprawny):
    del poprawny["cwiczenia"][1]["komentarze"]["edycje"]
    assert any("edycje" in b for b in bledy(poprawny))


def test_wynik_spoza_listy(poprawny):
    poprawny["cwiczenia"][0]["zadania"][0]["przebiegi"]["bez"][3]["wynik"] = ["Zmyślony wynik"]
    assert any("bez[3]/wynik[0]" in b for b in bledy(poprawny))


def test_terminal_tytul_tylko_folder(poprawny):
    poprawny["terminal_tytul"] = "~/Faktury"
    assert bledy(poprawny) == []
    poprawny["terminal_tytul"] = "claude · ~/Faktury"
    assert any("terminal_tytul" in b for b in bledy(poprawny))


def test_ls_z_obcym_wynikiem(poprawny):
    krok = poprawny["cwiczenia"][0]["zadania"][0]["przebiegi"]["bez"][2]
    krok["wynik"] = ["faktura.pdf", "cokolwiek"]
    assert any("bez[2]/wynik[1]" in b and "cokolwiek" in b for b in bledy(poprawny))


def test_menu_tytul_i_pytanie_musza_byc_napisami(poprawny):
    krok = krok_z(poprawny, 1)
    krok["tytul"] = 5
    assert any("z[1]" in b and "tytul menu musi być napisem" in b for b in bledy(poprawny))
    krok["tytul"] = ""
    krok["pytanie"] = ["Do you want to proceed?"]
    assert any("z[1]" in b and "pytanie menu musi być napisem" in b for b in bledy(poprawny))


def test_powtorzone_id_cwiczenia(poprawny):
    poprawny["cwiczenia"][1]["id"] = poprawny["cwiczenia"][0]["id"]
    assert any("powtórzone w scenariuszu" in b for b in bledy(poprawny))


def test_powtorzone_id_terminala(poprawny):
    poprawny["cwiczenia"][0]["terminale"][1]["id"] = "bez"
    assert any("id terminala „bez” powtórzone" in b for b in bledy(poprawny))


def test_id_poza_wzorcem(poprawny):
    poprawny["cwiczenia"][0]["id"] = "Cw 1"
    assert any("id ćwiczenie „Cw 1”" in b for b in bledy(poprawny))
    poprawny["cwiczenia"][0]["id"] = "cw1"
    poprawny["cwiczenia"][0]["terminale"][0]["id"] = "Bez_planu"
    assert any("id terminal „Bez_planu”" in b for b in bledy(poprawny))


def test_kroki_po_menu(poprawny):
    kroki = poprawny["cwiczenia"][0]["zadania"][0]["przebiegi"]["z"]
    kroki.insert(2, {"typ": "claude", "tekst": "Nigdy tego nie zobaczysz."})
    assert any("z[2]" in b and "kroki po menu nigdy się nie wykonają" in b for b in bledy(poprawny))


def test_cli(capsys):
    assert sc.main([str(DANE / "poprawny.json")]) == 0
    assert sc.main([str(DANE / "bledny.json")]) == 1
    assert "spoza listy" in capsys.readouterr().out


def _pliki_prawdziwe():
    pliki = sorted((KORZEN / "moduly").glob("**/scenariusz.json")) + sorted((KORZEN / "wzory").glob("*.json"))
    return pliki or [None]


@pytest.mark.parametrize("plik", _pliki_prawdziwe(), ids=lambda p: "brak" if p is None else str(p.relative_to(KORZEN)))
def test_prawdziwe_scenariusze(plik):
    if plik is None:
        pytest.skip("brak plików moduly/**/scenariusz.json i wzory/*.json")
    dane = json.loads(plik.read_text(encoding="utf-8"))
    fakty = None if plik.parent.name == "wzory" else FAKTY_ID
    assert sc.sprawdz_scenariusz(dane, fakty, NAPISY) == []
