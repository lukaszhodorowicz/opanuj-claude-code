"""Testy wyjątku „droga bez pliku” w walidatorze (narzedzia/scenariusz_koniec_drogi.py), wzór tests/dane/aplikacja-4a.json: sam klik w kartę Context nie jest wyjątkiem (krok `kontekst` tak), a droga kończąca się klikiem `poziom` przechodzi bez pliku tylko wtedy, gdy wybrany poziom różni się od bieżącego (`aplikacja.wysilek` albo domyślny Medium, po wcześniejszych wyborach drogi ten z poprzedniego)."""

import copy
import json
from pathlib import Path

import pytest
import yaml

from narzedzia import scenariusz as sc

KORZEN = Path(__file__).resolve().parent.parent
NAPISY = sc._Napisy(sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml"))
FAKTY_ID = {w["id"] for w in yaml.safe_load((KORZEN / "dane" / "fakty.yaml").read_text(encoding="utf-8"))["fakty"]}
WZOR = json.loads((Path(__file__).parent / "dane" / "aplikacja-4a.json").read_text(encoding="utf-8"))


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def cw(d, nr):
    return next(c for c in d["cwiczenia"] if c["id"] == f"cw{nr}")


def droga(d, nr, id_drogi):
    return next(x for x in cw(d, nr)["drogi"] if x["id"] == id_drogi)


def zawiera(lista, fragment):
    return any(fragment in b for b in lista)


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


# --- wyjątek „droga bez pliku”: klik context nie wystarcza (KW1), klik poziom musi coś zmienić (KD1)


def wybor_poziomu(nr, notka="poziom"):
    return [{"typ": "klik", "cel": "wybor-modelu"}, {"typ": "klik", "cel": "effort"}, {"typ": "klik", "cel": "poziom", "poziom": nr, "notka": notka}]


def droga_x(dane, nr, kroki):
    cw(dane, nr)["drogi"] = [{"id": "x", "etykieta": "Sama zmiana", "kroki": kroki + [{"typ": "nauczyciel", "tekst": "Gotowe."}]}]


def test_droga_konczaca_sie_samym_klikiem_w_karte_context_dalej_wymaga_pliku(dane):
    droga_x(dane, 2, [{"typ": "klik", "cel": "context"}])
    assert zawiera(bledy(dane), "droga bez kroku plik ani artefakt")


def test_klik_w_karte_context_nie_jest_wyjatkiem_ale_krok_kontekst_tak(dane):
    droga_x(dane, 6, [{"typ": "pisz", "tekst": "Policz."}, {"typ": "mysli"}, {"typ": "claude", "tekst": "Policzone."}, {"typ": "kontekst", "procent": 20}, {"typ": "klik", "cel": "context"}])
    assert zawiera(bledy(dane), "droga bez kroku plik ani artefakt")
    droga_x(dane, 6, [{"typ": "pisz", "tekst": "Policz."}, {"typ": "mysli"}, {"typ": "claude", "tekst": "Policzone."}, {"typ": "klik", "cel": "context"}, {"typ": "kontekst", "procent": 20}])
    assert bledy(dane) == []


def test_poziom_rowny_domyslnemu_medium_na_koncu_drogi_to_blad(dane):
    droga_x(dane, 4, wybor_poziomu(2))
    b = bledy(dane)
    assert zawiera(b, "droga kończy się wyborem poziomu „Medium”, który już stoi")
    assert not zawiera(b, "podgląd nie ma czego pokazać")


def test_poziom_inny_niz_domyslny_bez_modelu_przechodzi(dane):
    """Bez `aplikacja.model` wyjątek dalej działa (przycisk dostanie poziom w części C), bieżący poziom to domyślny Medium."""
    assert "model" not in cw(dane, 4)["aplikacja"]
    for nr in (1, 3, 4, 5):
        droga_x(dane, 4, wybor_poziomu(nr))
        assert bledy(dane) == [], nr


@pytest.mark.parametrize("wysilek,nr,blad", [("High", 3, True), ("High", 2, False), ("Low", 1, True), ("Max", 4, False)])
def test_poziom_rowny_wysilkowi_ze_sceny_na_koncu_drogi_to_blad(dane, wysilek, nr, blad):
    cw(dane, 3)["aplikacja"]["wysilek"] = wysilek
    droga_x(dane, 3, wybor_poziomu(nr))
    assert zawiera(bledy(dane), f"droga kończy się wyborem poziomu „{wysilek}”, który już stoi") is blad
    if not blad:
        assert bledy(dane) == []


def test_poziom_liczy_sie_od_poprzedniego_wyboru_w_tej_samej_drodze(dane):
    """Domyślnie Medium: najpierw High (3), na końcu Medium (2) różni się od High, więc przechodzi; na końcu High (3) po High byłoby błędem."""
    droga_x(dane, 4, wybor_poziomu(3) + wybor_poziomu(2))
    assert bledy(dane) == []
    droga_x(dane, 4, wybor_poziomu(3) + wybor_poziomu(3))
    assert zawiera(bledy(dane), "droga kończy się wyborem poziomu „High”, który już stoi")


def test_poziom_rowny_biezacemu_ale_droga_konczy_sie_plikiem_przechodzi(dane):
    """Błąd dotyczy tylko wyjątku od reguły pliku: droga z plikiem na końcu nie potrzebuje wyjątku (wzór `aplikacja-model.json` wybiera poziom bez ograniczeń)."""
    d = droga(dane, 5, "praca")
    d["kroki"] = wybor_poziomu(2) + d["kroki"]
    cw(dane, 5)["aplikacja"].update(model="Opus 5.5", wysilek="Medium")
    assert bledy(dane) == []
