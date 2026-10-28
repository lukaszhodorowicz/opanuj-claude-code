"""Wczytuje z migawki llms.txt unikalne strony dokumentacji Claude Code (url, tytuł, sekcja)."""
import re
from pathlib import Path

_NAGLOWEK = re.compile(r"^#{2,4}\s+(.+?)\s*$")
_STRONA = re.compile(r"^- \[(.+?)\]\((https://code\.claude\.com/docs/en/[^)\s]+\.md)\)")


def wczytaj_strony(sciezka) -> list[dict]:
    """Zwraca strony w kolejności z pliku, bez powtórzeń adresu (zostaje pierwsze wystąpienie)."""
    strony: list[dict] = []
    widziane: set[str] = set()
    sekcja = ""
    for linia in Path(sciezka).read_text(encoding="utf-8").splitlines():
        n = _NAGLOWEK.match(linia)
        if n:
            sekcja = n.group(1)
            continue
        s = _STRONA.match(linia)
        if s and s.group(2) not in widziane:
            widziane.add(s.group(2))
            strony.append({"url": s.group(2), "tytul": s.group(1), "sekcja": sekcja})
    return strony
