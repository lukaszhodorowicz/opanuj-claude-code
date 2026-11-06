"""Testy pola `nowe_pliki` ćwiczenia aplikacji: ścieżka do pliku spoza folder_startowy, który tworzy Claude."""

import copy
import json
from pathlib import Path

import pytest

from narzedzia import scenariusz as sc

KORZEN = Path(__file__).resolve().parent.parent
WZOR = json.loads(
    (Path(__file__).parent / "dane" / "nowy-dokument-nowe-pliki.json").read_text(
        encoding="utf-8"
    )
)
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")
NOWY = "zestawienie-kosztow-2026-10.csv"


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


def cw(d):
    return d["cwiczenia"][0]


def krok(d, t):
    return next(k for k in cw(d)["drogi"][0]["kroki"] if k["typ"] == t)


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def jest(wynik, fragment):
    return any(fragment in b for b in wynik)


def test_wzor_bez_bledow(dane):
    assert bledy(dane) == []


def test_nowy_plik_bez_pola_nowe_pliki_jest_odrzucony(dane):
    del cw(dane)["nowe_pliki"]
    assert jest(bledy(dane), f"plik „{NOWY}” nie istnieje w folder_startowy ani w nowe_pliki")


def test_plik_spoza_obu_list(dane):
    krok(dane, "claude")["plik"] = "faktura.txt"
    krok(dane, "claude")["tekst"] = "Zapisałem faktura.txt."
    wynik = bledy(dane)
    assert jest(wynik, "plik „faktura.txt” nie istnieje w folder_startowy ani w nowe_pliki")


def test_plik_z_folder_startowy_dalej_dziala(dane):
    krok(dane, "claude")["plik"] = "faktura-2026-10-orlen.pdf"
    krok(dane, "claude")["tekst"] = "Przeczytałem faktura-2026-10-orlen.pdf."
    krok(dane, "plik")["nazwa"] = "faktura-2026-10-orlen.pdf"
    wynik = bledy(dane)
    assert not jest(wynik, "nie istnieje w folder_startowy")
    assert jest(wynik, f"nowy plik „{NOWY}” bez odpowiedzi Claude")


def test_nowy_plik_bez_odpowiedzi_claude(dane):
    cw(dane)["nowe_pliki"].append("nieuzyty.csv")
    wynik = bledy(dane)
    assert jest(wynik, "nowy plik „nieuzyty.csv” bez odpowiedzi Claude")
    assert not jest(wynik, f"nowy plik „{NOWY}”")


def test_nowy_plik_powtarza_nazwe_z_folderu(dane):
    cw(dane)["nowe_pliki"].append("faktura-2026-10-biuro.pdf")
    assert jest(bledy(dane), "nowy plik „faktura-2026-10-biuro.pdf” już jest w folder_startowy")


def test_nowy_plik_powtorzony(dane):
    cw(dane)["nowe_pliki"].append(NOWY)
    assert jest(bledy(dane), f"nowy plik „{NOWY}” powtórzony w nowe_pliki")


@pytest.mark.parametrize("zla", ["", "  ", "a//b.csv", "../x.csv", 5, None])
def test_zla_nazwa_nowego_pliku(dane, zla):
    cw(dane)["nowe_pliki"] = [NOWY, zla]
    assert jest(bledy(dane), "cw1/nowe_pliki[1]: nowy plik wymaga ścieżki od folderu rozmowy")


@pytest.mark.parametrize("zle", [[], NOWY, {"a": 1}])
def test_nowe_pliki_musi_byc_niepusta_lista(dane, zle):
    cw(dane)["nowe_pliki"] = zle
    assert jest(bledy(dane), "pole nowe_pliki musi być niepustą listą")


def test_nowy_plik_wymaga_nazwy_w_tekscie_odpowiedzi(dane):
    krok(dane, "claude")["tekst"] = "Zapisałem zestawienie."
    assert jest(bledy(dane), f"tekst odpowiedzi nie zawiera ścieżki „{NOWY}”")


def test_klik_i_plik_zgodne_z_nowym_plikiem(dane):
    krok(dane, "plik")["nazwa"] = "inny.csv"
    assert jest(bledy(dane), f"nazwa „inny.csv” inna niż kliknięta ścieżka „{NOWY}”")


def test_nowe_pliki_w_cwiczeniu_z_krokami_bez_claude():
    wzor = json.loads(
        (Path(__file__).parent / "dane" / "aplikacja.json").read_text(encoding="utf-8")
    )
    wzor["cwiczenia"][0]["nowe_pliki"] = ["raport.csv"]
    assert jest(bledy(wzor), "nowy plik „raport.csv” bez odpowiedzi Claude")
