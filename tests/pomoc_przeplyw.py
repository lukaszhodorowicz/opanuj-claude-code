"""Wspólne dane i pomocniki testów karty zgody na przepływ (wzór: tests/dane/duze-zadanie-przeplyw.json): wczytanie wzoru, błędy walidatora, kroki drogi i indeks kroku po typie i celu."""

import copy
import json
from pathlib import Path

import pytest

from narzedzia import scenariusz as sc

KORZEN = Path(__file__).resolve().parent.parent
WZOR = json.loads((Path(__file__).parent / "dane" / "duze-zadanie-przeplyw.json").read_text(encoding="utf-8"))
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def jest(wynik, fragment):
    return any(fragment in b for b in wynik)


def kroki(d):
    return d["cwiczenia"][0]["drogi"][0]["kroki"]


def indeks(d, typ, cel=None):
    return next(i for i, k in enumerate(kroki(d)) if k["typ"] == typ and (cel is None or k.get("cel") == cel))
