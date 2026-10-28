"""Znajduje fakty cytowane w opisie formatu silnika (`dane/FORMAT-SCENARIUSZA*.md`)."""
import re
from pathlib import Path

_ID = r"`[a-z0-9]+(?:-[a-z0-9]+)*`"
WZOR_CYTAT = re.compile(rf"\bfakty? {_ID}(?:(?:, | i ){_ID})*")
WZOR_ID_W_APOSTROFACH = re.compile(r"`([^`]+)`")


def fakty_w_formacie(korzen: Path, ids: set[str]) -> set[str]:
    """Zwraca id faktów cytowanych jako „fakt `<id>`” w plikach formatu (brak plików: pusty zbiór)."""
    wynik: set[str] = set()
    for plik in sorted((Path(korzen) / "dane").glob("FORMAT-SCENARIUSZA*.md")):
        for cytat in WZOR_CYTAT.finditer(plik.read_text(encoding="utf-8")):
            wynik |= set(WZOR_ID_W_APOSTROFACH.findall(cytat.group(0))) & ids
    return wynik
