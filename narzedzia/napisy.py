"""Wczytuje listę napisów interfejsu i sprawdza, czy dany napis do niej należy."""
import re
from pathlib import Path

import yaml


def wczytaj_napisy(sciezka: Path) -> list[dict]:
    """Lista wpisów z `dane/napisy-interfejsu.yaml`."""
    dane = yaml.safe_load(sciezka.read_text(encoding="utf-8")) or {}
    return dane.get("napisy") or []


def fakty_w_napisach(sciezka: Path, ids: set[str]) -> set[str]:
    """Zwraca id faktów cytowanych jako „fakt <id>” w polu `zrodlo` napisów (brak pliku: pusty zbiór)."""
    if not sciezka.is_file():
        return set()
    wynik: set[str] = set()
    for wpis in wczytaj_napisy(sciezka):
        zrodlo = wpis.get("zrodlo") if isinstance(wpis, dict) else None
        if isinstance(zrodlo, str):
            wynik |= {f for f in ids if re.search(rf"\bfakt {re.escape(f)}(?![\w-])", zrodlo)}
    return wynik


class _Napisy:
    def __init__(self, wpisy):
        self.wpisy = [w for w in (wpisy or []) if isinstance(w, dict)]

    def jest(self, tekst, gdzie: str) -> bool:
        if not isinstance(tekst, str):
            return False
        for w in self.wpisy:
            if w.get("gdzie") != gdzie:
                continue
            if "napis" in w and w["napis"] == tekst:
                return True
            if "wzor" in w and re.search(w["wzor"], tekst):
                return True
        return False
