"""Testy sprawdzania opcjonalnych pól scenariusza: cele, opis, uwaga."""
import copy
import json
from pathlib import Path

import pytest

from narzedzia.napisy import wczytaj_napisy
from narzedzia.scenariusz import KORZEN, _Napisy, sprawdz_scenariusz, wczytaj_id_faktow

PRAWDZIWY = KORZEN / "moduly" / "tryby-pracy" / "tryb-planowania" / "scenariusz.json"
# dawna, terminalowa wersja tej lekcji (git show a58e7a3): ma `zadania`, których format etapów nie ma
TERMINAL = KORZEN / "tests" / "dane" / "tryb-planowania-terminal.json"


@pytest.fixture(scope="module")
def napisy():
    return _Napisy(wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml"))


@pytest.fixture(scope="module")
def fakty():
    return wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")


@pytest.fixture
def dane():
    return json.loads(PRAWDZIWY.read_text(encoding="utf-8"))


@pytest.fixture
def dane_terminal():
    return json.loads(TERMINAL.read_text(encoding="utf-8"))


def _bledy(dane, fakty, napisy):
    return sprawdz_scenariusz(copy.deepcopy(dane), fakty, napisy)


def _pierwszy_folder_przenies(dane):
    def idz(w):
        if isinstance(w, dict):
            if w.get("typ") == "folder" and w.get("akcja") == "przenies":
                return w
            for v in w.values():
                r = idz(v)
                if r:
                    return r
        elif isinstance(w, list):
            for v in w:
                r = idz(v)
                if r:
                    return r
    return idz(dane["cwiczenia"])


def test_prawdziwy_scenariusz_przechodzi(dane, fakty, napisy):
    assert _bledy(dane, fakty, napisy) == []


def test_zly_klucz_w_cele(dane, fakty, napisy):
    dane["cwiczenia"][0]["cele"] = {"nie-ma-takiego.pdf": "ma zostać"}
    bledy = _bledy(dane, fakty, napisy)
    assert any("nie-ma-takiego.pdf" in b and "nie istnieje" in b for b in bledy)


def test_wartosc_celu_nie_napis(dane, fakty, napisy):
    plik = dane["folder_startowy"][0]
    dane["cwiczenia"][0]["cele"] = {plik: 5}
    assert any("niepustym napisem" in b for b in _bledy(dane, fakty, napisy))


def test_cele_nie_obiekt(dane, fakty, napisy):
    dane["cwiczenia"][0]["cele"] = ["a"]
    assert any("cele musi być obiektem" in b for b in _bledy(dane, fakty, napisy))


def test_opis_zadania_liczba(dane_terminal, fakty, napisy):
    dane_terminal["cwiczenia"][0]["zadania"][0]["opis"] = 5
    bledy = _bledy(dane_terminal, fakty, napisy)
    assert any("opis musi być niepustym napisem" in b for b in bledy)


def test_opis_cwiczenia_liczba(dane, fakty, napisy):
    dane["cwiczenia"][0]["opis"] = 7
    assert any("opis musi być niepustym napisem" in b for b in _bledy(dane, fakty, napisy))


def test_uwaga_pusta(dane, fakty, napisy):
    krok = _pierwszy_folder_przenies(dane)
    if krok is None:
        pytest.skip("scenariusz nie ma kroku folder/przenies")
    krok["uwaga"] = " "
    assert any("uwaga musi być niepustym napisem" in b for b in _bledy(dane, fakty, napisy))
