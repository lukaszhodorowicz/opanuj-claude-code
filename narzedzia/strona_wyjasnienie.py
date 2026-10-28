"""Odwracana karta w lekcji: komentarz `<!-- wyjasnienie: obrazy/plik.png | opis rysunku -->` pod obrazem schematu zamienia obraz w kartę, której przód to rysunek obrazkowy, a tył to schemat, z przyciskiem odwracania nad kartą."""

import html
import re

from narzedzia.obrazy_lekcji import adres_obrazu

WYJASNIENIE = re.compile(r"^\s*<!--\s*wyjasnienie\s*:(.*?)-->\s*$")
OBRAZ_W_FIGURZE = re.compile(r'<img src="([^"]*)" alt="([^"]*)">')
FORMA = "<!-- wyjasnienie: obrazy/plik.png | opis rysunku jednym zdaniem -->"
NAPIS_PRZOD = "Odwróć kartę, żeby zobaczyć schemat"
NAPIS_TYL = "Wróć do wyjaśnienia"
STRZALKA = (
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 11a8 8 0 1 0-2.3 5.7M20 4v7h-7" fill="none" '
    'stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
)


def z_linii(linia: str) -> str | None:
    """Treść komentarza, gdy cała linia to `<!-- wyjasnienie: … -->`; inna linia daje None."""
    trafienie = WYJASNIENIE.match(linia)
    return trafienie.group(1).strip() if trafienie else None


def _strona(klasa: str, znak: str, adres: str, alt: str) -> str:
    return (
        f'<div class="odwrot-strona {klasa}"><span class="odwrot-znak">{znak}</span>'
        f'<img src="{adres}" alt="{html.escape(alt, quote=True)}"></div>'
    )


def dodaj(figura: str, tekst: str, katalog) -> str:
    """Zamienia obraz figury na kartę: przód to plik z komentarza z opisem jako alt, tył to dotychczasowy obraz schematu.
    Zapis bez `|`, pusty plik, pusty opis, brak pliku i druga karta pod tym samym obrazem to czytelny błąd."""
    sciezka, kreska, alt = (czesc.strip() for czesc in tekst.partition("|"))
    if not kreska or not sciezka:
        raise ValueError(f"wyjaśnienie pod obrazem bez pliku: zapis ma postać {FORMA}")
    if not alt:
        raise ValueError(f"wyjaśnienie „{sciezka}” bez opisu rysunku: opis po kresce idzie do alt, zapis ma postać {FORMA}")
    if 'class="odwrot"' in figura:
        raise ValueError(f"drugie wyjaśnienie „{sciezka}” pod tym samym obrazem: schemat ma jedną kartę")
    tyl = OBRAZ_W_FIGURZE.search(figura)
    if not tyl:
        raise ValueError(f"wyjaśnienie „{sciezka}” stoi pod czymś, co nie jest obrazem schematu")
    przod = adres_obrazu(sciezka, katalog)
    karta = (
        '<div class="odwrot"><div class="odwrot-w" role="button" tabindex="0" aria-pressed="false" '
        f'aria-label="{NAPIS_PRZOD}">'
        + _strona("odwrot-przod", "Wyjaśnienie", przod, alt)
        + f'<div class="odwrot-strona odwrot-tyl"><span class="odwrot-znak">Schemat</span>{tyl.group(0)}</div></div>'
        f'<button type="button" class="odwrot-przycisk">{STRZALKA}<span class="na-przod">{NAPIS_PRZOD}</span>'
        f'<span class="na-tyl">{NAPIS_TYL}</span></button></div>'
    )
    return figura[: tyl.start()] + karta + figura[tyl.end() :]
