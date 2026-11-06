"""Wspólne dane i pomocniki testów karty zgody przeglądarki w drodze (krok `zgoda` z `witryna`, krok `strona`): wzory scenariuszy, listy faktów i napisów, czytanie kroków po typie i błędów walidatora."""

import json
from pathlib import Path

from narzedzia import scenariusz as sc

KORZEN = Path(__file__).resolve().parent.parent
DANE = Path(__file__).parent / "dane"
WZOR = json.loads((DANE / "strona-zewnetrzna-zgoda.json").read_text(encoding="utf-8"))
DWIE = json.loads((DANE / "strona-zewnetrzna-dwie-strony.json").read_text(encoding="utf-8"))
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")
FAKT_KARTY = "aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu"
RAZ, ODMOW, ZAWSZE = "zezwol-raz", "odmow", "zawsze"  # id dróg wzoru strona-zewnetrzna-zgoda.json


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def jest(wynik, fragment):
    return any(fragment in b for b in wynik)


def kroki(d, droga=RAZ):
    return next(x for x in d["cwiczenia"][0]["drogi"] if x["id"] == droga)["kroki"]


def gdzie(lista, typ, cel=None, nr=0):
    """Indeks `nr`-tego kroku danego typu (z `cel` dla kliku)."""
    trafienia = [i for i, k in enumerate(lista) if k["typ"] == typ and (cel is None or k.get("cel") == cel)]
    return trafienia[nr]


def karta(d, droga=RAZ, nr=0):
    lista = kroki(d, droga)
    return lista[gdzie(lista, "zgoda", nr=nr)]


def ustaw_tryb(d, tryb):
    d["cwiczenia"][0]["aplikacja"]["tryb"] = tryb
