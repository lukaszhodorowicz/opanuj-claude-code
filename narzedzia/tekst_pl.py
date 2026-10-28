"""Wypisuje polskie napisy z scenariusz.json lekcji (ścieżka pola i tekst), do filtrów języka."""
import argparse
import json
import math
import re
import sys
from pathlib import Path

from narzedzia.napisy import wczytaj_napisy

KORZEN = Path(__file__).resolve().parent.parent
PLIK_NAPISOW = KORZEN / "dane" / "napisy-interfejsu.yaml"

POLSKA_LITERA = re.compile("[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]")

TEKST_ODLICZANIA = "Claude czeka: {} s"  # pigułka odliczania przed ptaszkiem karty zgody (strona/aplikacja-drogi-odliczanie.js, PK.tekstOdliczania)


def tekst_odliczania(ms: int) -> str:
    """Pierwszy napis pigułki odliczania kroku `zgoda` z `odliczanie_ms`: pełne sekundy zaokrąglone w górę („Claude czeka: 6 s”); dalsze malejące napisy mają ten sam wzór."""
    return TEKST_ODLICZANIA.format(math.ceil(ms / 1000))

KLUCZE_PL = {
    "tytul", "opis", "etykieta", "podpis", "dopisek", "nauczyciel", "nauczyciel_start",
    "pytanie", "pl", "tekst", "polecenie", "poza_zadaniem", "przycisk", "przyklad",
    "tekst_startowy", "uwaga", "poprawka", "odpowiedz", "notka",
}


def _jest_interfejsem(tekst: str, napisy: list[dict]) -> bool:
    """Czy napis jest na liście napisów interfejsu (równy `napis` albo pasuje do `wzor`)."""
    for w in napisy:
        if not isinstance(w, dict):
            continue
        if "napis" in w and w["napis"] == tekst:
            return True
        if "wzor" in w and re.search(w["wzor"], tekst):
            return True
    return False


def _chodz(wezel, sciezka: str, napisy: list[dict], wynik: list[tuple[str, str]]) -> None:
    """Rekurencyjnie zbiera polskie napisy w kolejności pliku."""
    if isinstance(wezel, list):
        for i, el in enumerate(wezel):
            _chodz(el, f"{sciezka}[{i}]", napisy, wynik)
        return
    if not isinstance(wezel, dict):
        return
    for klucz, wartosc in wezel.items():
        pod = f"{sciezka}.{klucz}" if sciezka else klucz
        if klucz == "cele" and isinstance(wartosc, dict):
            for plik, cel in wartosc.items():
                _dodaj(f"{pod}.{plik}", cel, napisy, wynik)
        elif klucz == "linijki" and isinstance(wartosc, list):
            for i, el in enumerate(wartosc):
                if isinstance(el, str):
                    _dodaj(f"{pod}[{i}]", el, napisy, wynik)
                else:
                    _chodz(el, f"{pod}[{i}]", napisy, wynik)
        elif klucz == "strona" and isinstance(wartosc, dict):  # strona oferty w panelu Browser: napisy i listy napisów
            for pole, w in wartosc.items():
                if pole == "pola" and isinstance(w, list):  # ramki cudzej strony (krok strona): etykieta nad ramką i tekst w ramce
                    for i, ramka in enumerate(w):
                        for czesc in ("etykieta", "wartosc"):
                            tekst = ramka.get(czesc) if isinstance(ramka, dict) else None
                            if isinstance(tekst, str) and tekst.strip():
                                _dodaj(f"{pod}.pola[{i}].{czesc}", tekst, napisy, wynik)
                    continue
                for i, el in enumerate(w if isinstance(w, list) else [w]):
                    _dodaj(f"{pod}.{pole}" + (f"[{i}]" if isinstance(w, list) else ""), el, napisy, wynik)
        elif klucz == "widok_klienta" and isinstance(wartosc, dict):  # przełącznik „Tak widzisz Ty / Tak zobaczy klient”: napisy kursu
            for pole, w in wartosc.items():
                _dodaj(f"{pod}.{pole}", w, napisy, wynik)
        elif klucz == "slajdy" and isinstance(wartosc, list):  # slajdy artefaktu: tytuł i punkty każdego slajdu
            for i, sl in enumerate(wartosc):
                for pole, w in (sl.items() if isinstance(sl, dict) else []):
                    for j, el in enumerate(w if isinstance(w, list) else [w]):
                        _dodaj(f"{pod}[{i}].{pole}" + (f"[{j}]" if isinstance(w, list) else ""), el, napisy, wynik)
        elif klucz == "sekcje" and wezel.get("typ") == "plan" and isinstance(wartosc, list):  # karta planu: nagłówek i punkty każdej sekcji
            for i, sekcja in enumerate(wartosc):
                if not isinstance(sekcja, dict):
                    continue
                _dodaj(f"{pod}[{i}].naglowek", sekcja.get("naglowek"), napisy, wynik)
                punkty = sekcja.get("punkty")
                for j, el in enumerate(punkty if isinstance(punkty, list) else []):
                    _dodaj(f"{pod}[{i}].punkty[{j}]", el, napisy, wynik)
        elif klucz in ("nazwa", "fazy") and wezel.get("typ") == "przeplyw":  # karta zgody na przepływ: nazwa i fazy to dane scenariusza, nie napisy interfejsu
            for i, el in enumerate(wartosc if isinstance(wartosc, list) else [wartosc]):
                _dodaj(pod + (f"[{i}]" if isinstance(wartosc, list) else ""), el, napisy, wynik)
        elif klucz == "w_tle" and isinstance(wartosc, list):  # prace w tle (krok claude): tytuł i zadanie karty oraz linijki wyniku w panelu subagenta
            for i, praca in enumerate(wartosc):
                for pole in ("tytul", "zadanie"):
                    _dodaj(f"{pod}[{i}].{pole}", praca.get(pole) if isinstance(praca, dict) else None, napisy, wynik)
                linijki = praca.get("wynik") if isinstance(praca, dict) else None
                for j, el in enumerate(linijki if isinstance(linijki, list) else []):
                    _dodaj(f"{pod}[{i}].wynik[{j}]", el, napisy, wynik)
        elif klucz == "harmonogram" and isinstance(wartosc, dict):  # zadanie według harmonogramu: nazwa i polecenie to polskie dane kursanta w oknie New scheduled task (pora, częstotliwość i folder nie są tekstem kursu)
            for pole in ("nazwa", "polecenie"):
                _dodaj(f"{pod}.{pole}", wartosc.get(pole), napisy, wynik)
        elif klucz == "odliczanie_ms" and wezel.get("typ") == "zgoda" and type(wartosc) is int and wartosc > 0 and "etapy[" not in sciezka:  # pigułka kursu przy karcie zgody w drodze (etapy jej nie grają)
            _dodaj(pod, tekst_odliczania(wartosc), napisy, wynik)
        elif klucz == "nazwa" and isinstance(wartosc, str) and re.search(r"(?:aplikacja|\.sesje\[\d+\]|nazwa_sesji)$", sciezka):  # nazwa rozmowy nadana przez kursanta (tytuł otwartej rozmowy, wiersz aplikacja.sesje, pole nazwa_sesji), nie nazwa pliku ani folderu
            _dodaj(pod, wartosc, napisy, wynik)
        elif klucz == "sesja" and isinstance(wartosc, str) and sciezka.endswith("aplikacja.telefon"):  # tytuł sesji na liście telefonu (aplikacja.telefon.sesja), nie id wiersza kliku sesja
            _dodaj(pod, wartosc, napisy, wynik)
        elif klucz == "polecenie" and wezel.get("typ") == "zgoda":  # nazwa polecenia terminala („zip”), nie tekst kursu
            continue
        elif klucz == "tresc" and isinstance(wartosc, str):
            if wezel.get("ramka") == "plan" or POLSKA_LITERA.search(wartosc):
                _dodaj(pod, wartosc, napisy, wynik)
        elif klucz in KLUCZE_PL and isinstance(wartosc, str):
            _dodaj(pod, wartosc, napisy, wynik)
        else:
            _chodz(wartosc, pod, napisy, wynik)


def _dodaj(sciezka: str, tekst, napisy: list[dict], wynik: list[tuple[str, str]]) -> None:
    if isinstance(tekst, str) and not _jest_interfejsem(tekst, napisy):
        wynik.append((sciezka, tekst))


def polskie_pola(scenariusz: dict, napisy: list[dict]) -> list[tuple[str, str]]:
    """Lista (ścieżka pola, tekst) polskich napisów scenariusza, bez napisów interfejsu."""
    wynik: list[tuple[str, str]] = []
    _chodz(scenariusz, "", napisy, wynik)
    return wynik


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Wypisz polskie napisy z scenariusz.json lekcji.")
    ap.add_argument("katalog", type=Path, help="katalog lekcji")
    args = ap.parse_args(argv)
    plik = args.katalog / "scenariusz.json"
    if not plik.is_file():
        print(f"Brak pliku {plik}", file=sys.stderr)
        return 1
    scenariusz = json.loads(plik.read_text(encoding="utf-8"))
    for sciezka, tekst in polskie_pola(scenariusz, wczytaj_napisy(PLIK_NAPISOW)):
        w_linii = tekst.replace("\t", "\\t").replace("\n", "\\n")
        print(f"{sciezka}\t{w_linii}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
