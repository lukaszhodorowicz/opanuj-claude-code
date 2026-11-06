"""Wspólne dane i pomocniki testów widoku strony artefaktu w symulatorze aplikacji: wzór scenariusza, listy faktów i napisów, krótkie funkcje do czytania kroków i błędów walidatora."""

import json
from pathlib import Path

from narzedzia import scenariusz as sc

KORZEN = Path(__file__).resolve().parent.parent
WZOR = json.loads((Path(__file__).parent / "dane" / "artefakt.json").read_text(encoding="utf-8"))
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")
LEKCJA = (
    "# Próba\n\n<!-- cwiczenie: cw1 -->\n\n<!-- cwiczenie: cw2 -->\n\n<!-- kolumny -->\n\n#### Ty\n\n<!-- podglad: cw1 publikuj -->\n\n"
    "#### Klient\n\n<!-- podglad: cw1 publikuj klient -->\n\n<!-- /kolumny -->\n"
)


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def jest(wynik, fragment):
    return any(fragment in b for b in wynik)


def kroki(d, nr=0):
    return d["cwiczenia"][nr]["drogi"][0]["kroki"]


def krok(d, typ, nr=0):
    return next(k for k in kroki(d, nr) if k["typ"] == typ)
