"""Fakty haseł słowniczka kursu (`dane/slowniczek.yaml`): które id faktów hasła cytują i czy każde hasło ma kształt i fakt, który istnieje."""
from pathlib import Path

import yaml

# Fakty haseł, których jeszcze nie ma w dane/fakty.yaml tej gałęzi (leżą na innej gałęzi). Po scaleniu
# z modul-pierwsza-praca (lekcja 0.0) siedem takich faktów już tu jest, więc wyjątek jest pusty.
FAKTY_NA_GALEZI_MODULU: frozenset[str] = frozenset()


def _dane(sciezka: Path) -> dict:
    return yaml.safe_load(sciezka.read_text(encoding="utf-8")) or {}


def _wpisy(sciezka: Path) -> list:
    return _dane(sciezka).get("pojecia") or []


def fakty_w_slowniczku(sciezka: Path, ids: set[str]) -> set[str]:
    """Zwraca id z `ids` użyte w polu `fakt` haseł słowniczka (brak pliku: pusty zbiór)."""
    if not sciezka.is_file():
        return set()
    wynik: set[str] = set()
    for wpis in _wpisy(sciezka):
        fakt = wpis.get("fakt") if isinstance(wpis, dict) else None
        if isinstance(fakt, str) and fakt in ids:
            wynik.add(fakt)
    return wynik


def bledy_slowniczka(sciezka: Path, ids: set[str], na_galezi_modulu: frozenset[str] = FAKTY_NA_GALEZI_MODULU) -> list[str]:
    """Błędy haseł słowniczka po polsku: brak pola, fakt, którego nie ma w `dane/fakty.yaml`, powtórzone pojęcie albo odmiana w dwóch hasłach, wyjątek już zbędny, zły kształt klucza `bez_pogrubienia` (brak pliku: bez błędów)."""
    if not sciezka.is_file():
        return []
    bledy: list[str] = []
    if "bez_pogrubienia" in (dane := _dane(sciezka)):
        frazy = dane["bez_pogrubienia"]
        if not (isinstance(frazy, list) and all(isinstance(f, str) and f.strip() for f in frazy)):
            bledy.append("Słowniczek: `bez_pogrubienia` ma być listą niepustych napisów.")
    pojecia: set[str] = set()
    odmiany: dict[str, str] = {}
    for nr, wpis in enumerate(_wpisy(sciezka), start=1):
        wpis = wpis if isinstance(wpis, dict) else {}
        nazwa = wpis.get("pojecie") if isinstance(wpis.get("pojecie"), str) else f"nr {nr}"
        for pole in ("pojecie", "wyjasnienie", "fakt"):
            if not isinstance(wpis.get(pole), str) or not wpis[pole].strip():
                bledy.append(f"Słowniczek, hasło „{nazwa}”: brak pola `{pole}`.")
        formy = wpis.get("odmiany")
        if not isinstance(formy, list) or not formy or not all(isinstance(f, str) and f.strip() for f in formy):
            bledy.append(f"Słowniczek, hasło „{nazwa}”: `odmiany` ma być niepustą listą napisów.")
            formy = []
        if nazwa in pojecia:
            bledy.append(f"Słowniczek: pojęcie „{nazwa}” występuje dwa razy.")
        pojecia.add(nazwa)
        for forma in formy:
            if odmiany.setdefault(forma, nazwa) != nazwa:
                bledy.append(f"Słowniczek: odmiana „{forma}” stoi w dwóch hasłach: „{odmiany[forma]}” i „{nazwa}”.")
        fakt = wpis.get("fakt")
        if isinstance(fakt, str) and fakt:
            if fakt in na_galezi_modulu and fakt in ids:
                bledy.append(f"Słowniczek, hasło „{nazwa}”: fakt „{fakt}” już jest w dane/fakty.yaml; usuń go z FAKTY_NA_GALEZI_MODULU w narzedzia/slowniczek_fakty.py.")
            elif fakt not in ids and fakt not in na_galezi_modulu:
                bledy.append(f"Słowniczek, hasło „{nazwa}”: fakt „{fakt}” nie istnieje w dane/fakty.yaml.")
    return bledy
