"""Test walidatora: `aplikacja.wysilek` bez `aplikacja.model` przechodzi (model domyślny Opus 5.5, dane/FORMAT-SCENARIUSZA.md, część „Model domyślny na przycisku modelu”); wartość spoza listy poziomów dalej jest błędem (wzór: tests/dane/aplikacja-model.json)."""

import copy
import json
from pathlib import Path

import pytest

from narzedzia import scenariusz as sc

KORZEN = Path(__file__).resolve().parent.parent
WZOR = json.loads((Path(__file__).parent / "dane" / "aplikacja-model.json").read_text(encoding="utf-8"))
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def z_wysilkiem(wysilek):
    """Wzór bez pola `aplikacja.model` i z polem `aplikacja.wysilek`."""
    dane = copy.deepcopy(WZOR)
    apl = dane["cwiczenia"][0]["aplikacja"]
    assert "model" not in apl
    apl["wysilek"] = wysilek
    return dane


@pytest.mark.parametrize("wysilek", ["Medium", "Extra"])
def test_wysilek_bez_modelu_przechodzi(wysilek):
    """Drogi wzoru wybierają poziomy 1, 3 i 5, więc Medium (2) i Extra (4) nie kolidują z ich ostatnim wyborem."""
    assert bledy(z_wysilkiem(wysilek)) == []


def test_wysilek_spoza_listy_bez_modelu_dalej_jest_bledem():
    wynik = bledy(z_wysilkiem("Ultracode"))
    assert any("wysilek " in b and "Ultracode" in b for b in wynik), wynik
