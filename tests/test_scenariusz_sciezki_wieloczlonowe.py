"""Testy walidatora ścieżek o dowolnej głębokości (`.claude/skills/x/SKILL.md`) w `nowe_pliki`, `aplikacja.folder_startowy_dodatkowe`, `claude.plik`, `plik.nazwa`, `czyta` i `czyta_na_start` oraz ścieżek, które dalej mają najwyżej jeden `/` (`folder_startowy`)."""

import copy
import json
from pathlib import Path

import pytest

from narzedzia import scenariusz as sc
from narzedzia.scenariusz_drzewo import sciezka_ok, teczka

KORZEN = Path(__file__).resolve().parent.parent
WZOR = json.loads((Path(__file__).parent / "dane" / "pierwszy-skill-zgoda-drogi.json").read_text(encoding="utf-8"))
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")
SKILL = ".claude/skills/odpowiedz-klientowi/SKILL.md"
ZLE = ["", "  ", "../x.txt", "a//b.txt", "/a/b.txt", "a/b/", "a/./b.txt", ".claude/../x.md"]


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def jest(wynik, fragment):
    return any(fragment in b for b in wynik)


def cw(d, i):
    return d["cwiczenia"][i]


def test_wzor_ma_sciezki_o_trzech_ukosnikach_bez_folder_glowny(dane):
    assert "folder_glowny" not in dane and SKILL.count("/") == 3
    assert cw(dane, 0)["nowe_pliki"][0] == SKILL
    assert cw(dane, 1)["aplikacja"]["folder_startowy_dodatkowe"] == [SKILL]
    assert bledy(dane) == []


def test_sciezka_ok_i_teczka():
    assert sciezka_ok("plik.txt") and sciezka_ok("a/plik.txt") and sciezka_ok(SKILL)
    assert not any(sciezka_ok(z) for z in ZLE + [None, 5])
    assert teczka(SKILL) == ".claude/skills/odpowiedz-klientowi"
    assert teczka("a/plik.txt") == "a" and teczka("plik.txt") == ""


@pytest.mark.parametrize("nazwa", ["raport/zestawienie.csv", "a/b/c/d/e.txt"])
def test_nowe_pliki_przyjmuja_kazda_glebokosc(dane, nazwa):
    cw(dane, 0)["nowe_pliki"].append(nazwa)
    wynik = bledy(dane)
    assert not jest(wynik, "nowy plik wymaga ścieżki")
    assert jest(wynik, f"nowy plik „{nazwa}” bez odpowiedzi Claude")  # dalej musi mieć odpowiedź Claude


@pytest.mark.parametrize("nazwa", ZLE + [5, None])
def test_nowe_pliki_zle_sciezki(dane, nazwa):
    cw(dane, 0)["nowe_pliki"].append(nazwa)
    assert jest(bledy(dane), "nowy plik wymaga ścieżki od folderu rozmowy")


def test_nowe_pliki_sciezka_powtorzona(dane):
    cw(dane, 0)["nowe_pliki"].append(SKILL)
    assert jest(bledy(dane), f"nowy plik „{SKILL}” powtórzony w nowe_pliki")


def test_nowy_plik_nie_powtarza_pliku_dodatkowego_tego_cwiczenia(dane):
    cw(dane, 1)["nowe_pliki"].append(SKILL)
    assert jest(bledy(dane), f"nowy plik „{SKILL}” już jest w folder_startowy_dodatkowe tego ćwiczenia")


@pytest.mark.parametrize("nazwa", ["a/b/c/CLAUDE.md", ".claude/skills/x/SKILL.md"])
def test_folder_startowy_dodatkowe_przyjmuje_kazda_glebokosc(dane, nazwa):
    cw(dane, 1)["aplikacja"]["folder_startowy_dodatkowe"].append(nazwa)
    assert bledy(dane) == []


@pytest.mark.parametrize("nazwa", ZLE)
def test_folder_startowy_dodatkowe_zle_sciezki(dane, nazwa):
    cw(dane, 1)["aplikacja"]["folder_startowy_dodatkowe"].append(nazwa)
    assert jest(bledy(dane), "plik dodatkowy wymaga ścieżki")


def test_folder_startowy_dodatkowe_sciezka_powtorzona(dane):
    cw(dane, 1)["aplikacja"]["folder_startowy_dodatkowe"].append(SKILL)
    assert jest(bledy(dane), f"plik „{SKILL}” powtórzony w folder_startowy_dodatkowe")


def test_teczka_jednoczlonowa_dalej_wymaga_folder_glowny_a_wieloczlonowa_nie(dane):
    cw(dane, 1)["aplikacja"]["folder_startowy_dodatkowe"].append("Podfolder/notatka.txt")
    assert jest(bledy(dane), "wymagają folder_glowny")
    dane["folder_glowny"] = "Klienci-maile"
    assert not jest(bledy(dane), "wymagają folder_glowny")


def test_folder_startowy_scenariusza_dalej_ma_najwyzej_jeden_ukosnik(dane):
    dane["folder_startowy"].append(SKILL)
    assert jest(bledy(dane), "najwyżej jeden /")


def test_czyta_przyjmuje_sciezke_wieloczlonowa_pliku_z_folderu(dane):
    krok = cw(dane, 1)["drogi"][1]["kroki"][1]
    assert krok["czyta"][0] == SKILL
    krok["czyta"] = [".claude/skills/inny/SKILL.md"]
    assert jest(bledy(dane), "nie wskazuje pliku, który w tym miejscu drogi leży w folderze")


@pytest.mark.parametrize("sciezka", ["a//b.txt", "../x", ".claude/../SKILL.md"])
def test_czyta_zle_sciezki(dane, sciezka):
    cw(dane, 1)["drogi"][1]["kroki"][1]["czyta"] = [sciezka]
    assert jest(bledy(dane), "ścieżka od korzenia podglądu: niepusty napis bez pustych członów")


def test_czyta_nowy_plik_dopiero_po_odpowiedzi_claude_z_tym_plikiem(dane):
    kroki = cw(dane, 0)["drogi"][0]["kroki"]
    kroki[1]["czyta"] = [SKILL]  # przed zapisem pliku nie ma go w folderze
    assert jest(bledy(dane), f"ścieżka „{SKILL}” (od korzenia podglądu) nie wskazuje pliku")
    kroki[1]["czyta"] = ["jak-odpisuje-klientom.txt"]
    kroki.insert(8, {"typ": "mysli", "czyta": [SKILL]})  # po odpowiedzi Claude z plikiem (krok 6) plik leży w folderze
    assert bledy(dane) == []


def test_nazwa_otwartego_pliku_to_pelna_sciezka(dane):
    plik = next(k for k in cw(dane, 0)["drogi"][0]["kroki"] if k["typ"] == "plik")
    plik["nazwa"] = "SKILL.md"
    assert jest(bledy(dane), f"nazwa „SKILL.md” inna niż kliknięta ścieżka „{SKILL}”")


def test_odpowiedz_claude_wymaga_pelnej_sciezki_w_tekscie(dane):
    claude = cw(dane, 0)["drogi"][0]["kroki"][6]
    claude["tekst"] = "Zapisałem skill w SKILL.md."
    assert jest(bledy(dane), f"tekst odpowiedzi nie zawiera ścieżki „{SKILL}”")


def test_odpowiedz_claude_z_samym_skill_md_nie_istnieje(dane):
    claude = cw(dane, 0)["drogi"][0]["kroki"][6]
    claude["plik"], claude["tekst"] = "SKILL.md", "Zapisałem SKILL.md."
    assert jest(bledy(dane), "plik „SKILL.md” nie istnieje w folder_startowy ani w nowe_pliki")


def test_czyta_na_start_przyjmuje_sciezke_wieloczlonowa(dane):
    apl = cw(dane, 1)["aplikacja"]
    apl["czyta_na_start"] = [SKILL]
    apl["rozmowa"] = []
    assert bledy(dane) == []
    apl["czyta_na_start"] = [".claude/skills/inny/SKILL.md"]
    assert jest(bledy(dane), "nie wskazuje pliku, który leży w folderze od startu")
