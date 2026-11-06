"""Testy napisów menu +, listy „/”, przeglądarki wtyczek i katalogu konektorów: każdy napis rysowany przez silnik (strona/aplikacja-plus-dane.js, strona/aplikacja-ustawienia-dane.js) stoi w dane/napisy-interfejsu.yaml (gdzie: aplikacja) ze źródłem w zrzucie Łukasza z 27.10.2026, a stałe silnika zgadzają się z walidatorem."""

import json
import re
from pathlib import Path

import pytest

from narzedzia import scenariusz as sc
from narzedzia import scenariusz_katalog as kat
from narzedzia import scenariusz_plus as plus

KORZEN = Path(__file__).resolve().parent.parent
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")
PLUS_DANE = KORZEN / "strona" / "aplikacja-plus-dane.js"
USTAWIENIA_DANE = KORZEN / "strona" / "aplikacja-ustawienia-dane.js"
WCZESNIEJSZE = {"Add files or photos", "Add folder", "Slash commands", "Customize", "Gmail", "Google Calendar", "Microsoft 365"}  # wpisy z dokumentacji sprzed zrzutów z 27.10.2026


def stala(plik: Path, nazwa: str):
    """Wartość stałej `PK.<nazwa> = …;` z pliku JS zapisanej jak JSON (końcowe przecinki dozwolone, komentarze pomijane)."""
    tekst = re.sub(r"/\*.*?\*/", "", plik.read_text(encoding="utf-8"), flags=re.S)
    trafienie = re.search(rf"PK\.{nazwa} = (.*?);\n", tekst, flags=re.S)
    assert trafienie, f"w {plik.name} brak stałej PK.{nazwa}"
    return json.loads(re.sub(r",(\s*[\]}])", r"\1", trafienie.group(1)))


def napisy_plus() -> list[str]:
    wynik = list(stala(PLUS_DANE, "MENU_PLUS"))
    for rodzic, dzieci in stala(PLUS_DANE, "PODMENU_PLUS").items():
        wynik += [rodzic, *dzieci]
    wynik += list(stala(PLUS_DANE, "SKROT_PLUS").values())
    wynik += [stala(PLUS_DANE, "PODPIS_GITHUB"), stala(PLUS_DANE, "PODPIS_LOKALNE"), stala(PLUS_DANE, "PODPOWIEDZ_POLA")]
    wynik += stala(PLUS_DANE, "WIERSZE_LISTY") + list(stala(PLUS_DANE, "OPISY_WIERSZY").values())
    return wynik


def napisy_ustawien() -> list[str]:
    u = stala(USTAWIENIA_DANE, "USTAWIENIA")
    wynik = [u["tytul"], u["szukaj"], *u["zakladki"], u["dodaj"], u["wszystkie"]]
    for g in stala(USTAWIENIA_DANE, "USTAWIENIA_KOLUMNA"):
        wynik += [g["grupa"], *g["pozycje"]]
    p = stala(USTAWIENIA_DANE, "WTYCZKI_POLECANA")
    wynik += [p["od"], p["nazwa"], p["opis"], p["przycisk"], stala(USTAWIENIA_DANE, "WTYCZKI_SEKCJA")]
    for t in stala(USTAWIENIA_DANE, "WTYCZKI_KAFELKI"):
        wynik += [x for x in (t["nazwa"], t["opis"], t["zrodlo"]) if x]
    s = stala(USTAWIENIA_DANE, "KONEKTORY_SEKCJA")
    wynik += [s["nazwa"], s["liczba"]]
    for t in stala(USTAWIENIA_DANE, "KONEKTORY_KATALOG"):
        wynik += [x for x in (t["nazwa"], t["opis"], t["autor"]) if x]
    return wynik


def wpisy(napis: str) -> list[dict]:
    return [w for w in NAPISY if w.get("napis") == napis and w.get("gdzie") == "aplikacja"]


@pytest.mark.parametrize("napis", sorted(set(napisy_plus() + napisy_ustawien())))
def test_napis_silnika_ma_wpis_ze_zrodlem_w_zrzucie(napis):
    znalezione = wpisy(napis)
    assert znalezione, f"„{napis}” nie stoi w napisy-interfejsu.yaml (gdzie: aplikacja)"
    if napis not in WCZESNIEJSZE:
        assert any("zrzut Łukasza 27.10.2026" in w["zrodlo"] and "materialy/zrzuty-lukasza/" in w["zrodlo"] and ".png" in w["zrodlo"] for w in znalezione), napis


def test_stare_napisy_zostaja_w_yaml_ale_silnik_ich_nie_rysuje():
    for stary in ("Add connectors", "Add plugins"):
        assert wpisy(stary), stary
        assert stary not in napisy_plus() + napisy_ustawien()
        for plik in ("aplikacja-plus-dane.js", "aplikacja-plus.js", "aplikacja-katalog.js", "aplikacja-wtyczki.js", "aplikacja-ustawienia.js", "aplikacja-ustawienia-dane.js"):
            assert stary not in (KORZEN / "strona" / plik).read_text(encoding="utf-8").replace("„" + stary + "”", ""), (stary, plik)


def test_menu_i_lista_silnika_zgadzaja_sie_z_walidatorem():
    assert tuple(stala(PLUS_DANE, "MENU_PLUS")) == plus.MENU_PLUS
    assert {k: tuple(v) for k, v in stala(PLUS_DANE, "PODMENU_PLUS").items()} == plus.PODMENU
    assert tuple(stala(PLUS_DANE, "WIERSZE_LISTY")) == plus.WIERSZE_LISTY
    assert tuple(stala(PLUS_DANE, "POZYCJE_LOKALNE")) == plus.LOKALNE
    assert list(stala(PLUS_DANE, "OPISY_WIERSZY")) == [plus.WIERSZE_LISTY[0]]


def test_kafelki_katalogu_silnika_zgadzaja_sie_z_walidatorem():
    nazwy = tuple(t["nazwa"] for t in stala(USTAWIENIA_DANE, "KONEKTORY_KATALOG"))
    assert nazwy == kat.KAFELKI
    assert {"Gmail", "Google Calendar", "Microsoft 365"} <= set(nazwy)  # lekcja 5.1 stoi na tych trzech


def test_kolejnosc_menu_ze_zrzutu_03_58_01():
    assert stala(PLUS_DANE, "MENU_PLUS") == ["Add files or photos", "Add folder", "Import GitHub issue", "Slash commands", "Connectors", "Plugins"]
    assert stala(PLUS_DANE, "SKROT_PLUS") == {"Add files or photos": "⌘ U"}
    assert stala(PLUS_DANE, "PODPIS_GITHUB") == "This folder doesn’t have a GitHub remote"


def test_wiersze_listy_w_kolejnosci_ze_zrzutu_03_58_20():
    assert stala(PLUS_DANE, "WIERSZE_LISTY") == ["plugin", "model", "effort", "fast", "plan", "permissions", "skills", "workflows", "usage", "usage-credits", "config", "storage", "sandbox"]
    assert stala(PLUS_DANE, "OPISY_WIERSZY") == {"plugin": "Manage Claude Code plugins"}


def test_opisy_ucietych_kafelkow_koncza_sie_wielokropkiem_a_brakujace_to_null():
    for t in stala(USTAWIENIA_DANE, "KONEKTORY_KATALOG"):
        assert (t["opis"] is None) == (t["autor"] is None), t
    ostatnie = [t["nazwa"] for t in stala(USTAWIENIA_DANE, "KONEKTORY_KATALOG") if t["opis"] is None]
    assert ostatnie == ["Google Docs", "Supabase"]
    assert [t["nazwa"] for t in stala(USTAWIENIA_DANE, "WTYCZKI_KAFELKI") if t["opis"] is None] == ["doc-coauthoring", "web-artifacts-builder"]
