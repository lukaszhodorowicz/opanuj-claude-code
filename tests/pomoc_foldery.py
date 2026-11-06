"""Wspólne pomocniki testów walidatora folderu każdej rozmowy i karty wiadomości (wzór: tests/dane/kilka-rozmow-foldery-i-wiadomosc.json): kopia wzoru, błędy walidatora i odczyt dróg."""

import copy
import json
from pathlib import Path

from narzedzia import scenariusz as sc
from tests.pomoc_sesje import FAKTY_ID, NAPISY, gdzie, jest, klik, naucz  # noqa: F401  (ponownie eksportowane dla testów)

KORZEN = Path(__file__).resolve().parent.parent
WZOR = json.loads((Path(__file__).parent / "dane" / "kilka-rozmow-foldery-i-wiadomosc.json").read_text(encoding="utf-8"))


def kopia():
    return copy.deepcopy(WZOR)


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def cwiczenie(d, id_):
    return next(c for c in d["cwiczenia"] if c["id"] == id_)


def kroki(d, id_="druga", cw="cw1"):
    return next(x for x in cwiczenie(d, cw)["drogi"] if x["id"] == id_)["kroki"]


def apl(d, cw="cw1"):
    return cwiczenie(d, cw)["aplikacja"]


def wiadomosc(d):
    """Krok `claude` z polem `wiadomosc` w drodze `wiadomosc` ćwiczenia cw2."""
    return next(k for k in kroki(d, "wiadomosc", "cw2") if "wiadomosc" in k)
