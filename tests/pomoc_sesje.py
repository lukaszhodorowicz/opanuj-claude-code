"""Wspólne dane i pomocniki testów paska bocznego z rozmowami (wzór: tests/dane/aplikacja-sesje.json): wczytanie wzoru, błędy walidatora, odczyt dróg i kroków po typie, krótkie kroki do wstawiania."""

import copy
import json
from pathlib import Path

from narzedzia import scenariusz as sc

KORZEN = Path(__file__).resolve().parent.parent
DANE = Path(__file__).parent / "dane"
WZOR = json.loads((DANE / "aplikacja-sesje.json").read_text(encoding="utf-8"))
BEZ_LISTY = json.loads((DANE / "aplikacja-drogi.json").read_text(encoding="utf-8"))  # ćwiczenie cw2 z drogami bez aplikacja.sesje
Z_KROKAMI = json.loads((DANE / "aplikacja.json").read_text(encoding="utf-8"))  # ćwiczenie cw1 z krokami (bez dróg)
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")


def kopia():
    return copy.deepcopy(WZOR)


def bez_listy():
    return copy.deepcopy(BEZ_LISTY)


def z_krokami():
    return copy.deepcopy(Z_KROKAMI)


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def jest(wynik, fragment):
    return any(fragment in b for b in wynik)


def cwiczenie(d, id_="cw2"):
    return next(c for c in d["cwiczenia"] if c["id"] == id_)


def droga(d, id_, cw="cw2"):
    return next(x for x in cwiczenie(d, cw)["drogi"] if x["id"] == id_)


def kroki(d, id_="archiwum", cw="cw2"):
    return droga(d, id_, cw)["kroki"]


def gdzie(lista, typ, cel=None, nr=0):
    """Indeks `nr`-tego kroku danego typu (z `cel` dla kliku)."""
    return [i for i, k in enumerate(lista) if k["typ"] == typ and (cel is None or k.get("cel") == cel)][nr]


def klik(cel, **pola):
    return {"typ": "klik", "cel": cel, **pola}


def naucz(tekst="Zobacz okno."):
    return {"typ": "nauczyciel", "tekst": tekst}


def nowa_droga(d, lista, cw="cw2", id_="probna"):
    """Dokłada do ćwiczenia drogę `id_` z podanymi krokami i oddaje listę kroków."""
    cwiczenie(d, cw)["drogi"].append({"id": id_, "etykieta": "Próba", "kroki": lista})
    return lista


def tylko_droga(d, lista, cw="cw2"):
    """Zastępuje drogi ćwiczenia jedną próbną drogą z podanymi krokami (reszta wzoru bez zmian)."""
    cwiczenie(d, cw)["drogi"] = [{"id": "probna", "etykieta": "Próba", "kroki": lista}]
    return lista
