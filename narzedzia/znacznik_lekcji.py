"""Czyta z pierwszej linii lekcja.md moduł i numer lekcji („Moduł 1: Tryby pracy · Lekcja 3 z 4”) i składa z nich znacznik na górę strony."""

import html
import re
from dataclasses import dataclass

WZOR = re.compile(
    r"Moduł\s+(?P<modul>\d+)\s*:\s*(?P<nazwa>[^·]+?)\s*·\s*Lekcja\s+(?P<numer>\d+)\s+z\s+(?P<liczba>\d+)\s*$"
)
OBWOLUTA = re.compile(
    r"^\s*(?:<em>(?P<em>.*)</em>|\*(?P<gw>[^*].*?)\*|(?P<goly>.*?))\s*$"
)
NAJWIECEJ_LEKCJI = 30


@dataclass(frozen=True)
class Polozenie:
    modul: int
    nazwa_modulu: str
    numer: int
    liczba: int


def odczytaj(linia: str) -> Polozenie | None:
    """Położenie lekcji z linii okruszków albo None, gdy linia nie pasuje do wzoru albo liczby się nie zgadzają."""
    m = OBWOLUTA.match(linia)
    srodek = next((g for g in m.groups() if g is not None), "") if m else ""
    w = WZOR.search(srodek)
    if not w:
        return None
    numer, liczba = int(w["numer"]), int(w["liczba"])
    if not 1 <= numer <= liczba <= NAJWIECEJ_LEKCJI:
        return None
    return Polozenie(int(w["modul"]), w["nazwa"].strip(), numer, liczba)


def wydziel(tresc_md: str) -> tuple[Polozenie | None, str]:
    """Zwraca (położenie, treść bez linii okruszków); gdy pierwsza niepusta linia nie pasuje, treść zostaje bez zmian."""
    linie = tresc_md.splitlines(keepends=True)
    for i, linia in enumerate(linie):
        if not linia.strip():
            continue
        polozenie = odczytaj(linia)
        if polozenie is None:
            return None, tresc_md
        return polozenie, "".join(linie[:i] + linie[i + 1 :])
    return None, tresc_md


def html_znacznika(p: Polozenie | None) -> str:
    """Znacznik: moduł z nazwą, a obok ciemna plakietka „Lekcja N z M” z paskiem odcinków, bieżący zaznaczony."""
    if p is None:
        return ""
    odcinki = "".join(
        f'<span class="zl-odcinek{" zl-biezacy" if n == p.numer else ""}"></span>'
        for n in range(1, p.liczba + 1)
    )
    return (
        f'<div class="znacznik-lekcji">'
        f'<p class="zl-modul"><span class="zl-modul-nr">Moduł {p.modul}</span> '
        f'<span class="zl-modul-nazwa">{html.escape(p.nazwa_modulu)}</span></p>'
        f'<p class="zl-lekcja"><span class="zl-napis">Lekcja <b>{p.numer}</b> z {p.liczba}</span>'
        f'<span class="zl-pasek" aria-hidden="true">{odcinki}</span></p>'
        f"</div>"
    )
