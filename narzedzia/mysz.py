"""Sprawdzian prawdziwą myszą stron lekcji kursu w Chrome bez okna: przeklikuje ćwiczenia z poleceniami i znacznikami „kliknij tutaj”, odwracane karty i poziome przewijanie; wypisuje tabelę OK albo usterka.

Wywołanie: `uv run python -m narzedzia.mysz (--wszystko | --probka | --lekcja <slug> [<slug> ...]) [--wyjscie <katalog>]`.
`--wszystko` bierze każdą lekcję z ćwiczeniami, `--probka` pierwszą lekcję z ćwiczeniami każdego modułu, `--lekcja` wskazane lekcje (nazwa katalogu lekcji).
Ćwiczenia i przewijanie w poziomie: okna 1440x680 i 390x760; karty: 1440x900 i 390x800. Strony składa to narzędzie (z `narzedzia.strona`) do `<wyjście>/strony`,
zrzuty trafiają do `<wyjście>/zrzuty` (domyślnie `build/mysz`). Chrome idzie zawsze pod blokadą `/tmp/przewodnik-chrome.lock` (`narzedzia/mysz_cdp.py`), na wolnym porcie,
a zatrzymuje się po PID. Kod wyjścia 1 przy jakiejkolwiek usterce albo gdy nic nie sprawdzono.
Kiedy co: zmiana działania ćwiczeń (polecenia, karty, kliknięcia, przewijanie, silnik JS) → `--wszystko`; sam wygląd albo tekst lekcji → testy i `--probka` (skill `nowa-lekcja`, „Sprawdzian przed PR”).
"""

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

from narzedzia import znacznik_lekcji
from narzedzia.mysz_cdp import przegladarka
from narzedzia.mysz_przebieg import sprawdz_cwiczenia, sprawdz_karty, sprawdz_przewijanie
from narzedzia.mysz_raport import Wynik, kod_wyjscia, tabela
from narzedzia.strona import zloz_strone

KORZEN = Path(__file__).resolve().parent.parent
OKNA_CWICZEN = ((1440, 680), (390, 760))
OKNA_KART = ((1440, 900), (390, 800))


@dataclass(frozen=True)
class Lekcja:
    """Lekcja kursu: nazwa katalogu (slug), katalog, moduł (katalog nad lekcją), numer z znacznika (0 bez znacznika) i informacja, czy ma ćwiczenia."""

    slug: str
    katalog: Path
    modul: str
    numer: int
    ma_cwiczenia: bool


def _ma_cwiczenia(katalog: Path) -> bool:
    plik = katalog / "scenariusz.json"
    if not plik.is_file():
        return False
    try:
        return bool(json.loads(plik.read_text(encoding="utf-8")).get("cwiczenia"))
    except (OSError, ValueError):
        return False


def znajdz_lekcje(korzen: Path = KORZEN) -> list[Lekcja]:
    """Wszystkie lekcje `moduly/<moduł>/<lekcja>/lekcja.md`, posortowane po module, numerze z znacznika i nazwie."""
    lekcje = []
    for md in sorted((korzen / "moduly").glob("*/*/lekcja.md")):
        polozenie, _ = znacznik_lekcji.wydziel(md.read_text(encoding="utf-8"))
        lekcje.append(Lekcja(md.parent.name, md.parent, md.parent.parent.name, polozenie.numer if polozenie else 0, _ma_cwiczenia(md.parent)))
    return sorted(lekcje, key=lambda l: (l.modul, l.numer, l.slug))


def wybierz(lekcje: list[Lekcja], wszystko: bool, probka: bool, slugi: list[str]) -> list[Lekcja]:
    """`--wszystko`: lekcje z ćwiczeniami; `--probka`: pierwsza lekcja z ćwiczeniami każdego modułu; `--lekcja`: wskazane (nieznana nazwa to błąd)."""
    z_cwiczeniami = [l for l in lekcje if l.ma_cwiczenia]
    if wszystko:
        return z_cwiczeniami
    if probka:
        pierwsze: dict[str, Lekcja] = {}
        for l in z_cwiczeniami:
            pierwsze.setdefault(l.modul, l)
        return list(pierwsze.values())
    wskazane = {l.slug: l for l in lekcje}
    brak = [s for s in slugi if s not in wskazane]
    if brak:
        raise SystemExit(f"Nie ma lekcji: {', '.join(brak)}. Dostępne: {', '.join(sorted(wskazane))}")
    return [wskazane[s] for s in slugi]


def sprawdz_lekcje(lekcja: Lekcja, katalog_stron: Path, katalog_zrzutow: Path) -> list[Wynik]:
    """Składa stronę lekcji i sprawdza ją we wszystkich oknach; zwraca wszystkie wyniki."""
    katalog_stron.mkdir(parents=True, exist_ok=True)
    html = zloz_strone(lekcja.katalog)
    plik = katalog_stron / f"lekcja-{lekcja.slug}.html"
    plik.write_text(html, encoding="utf-8")
    url = plik.resolve().as_uri()
    wyniki: list[Wynik] = []
    if lekcja.ma_cwiczenia:
        for szer, wys in OKNA_CWICZEN:
            with przegladarka(szer, wys) as strona:
                wyniki += sprawdz_cwiczenia(strona, url, lekcja.slug, katalog_zrzutow)
                wyniki.append(sprawdz_przewijanie(strona, url, lekcja.slug, katalog_zrzutow))
    if 'class="odwrot"' in html:
        for szer, wys in OKNA_KART:
            with przegladarka(szer, wys) as strona:
                wyniki += sprawdz_karty(strona, url, lekcja.slug, katalog_zrzutow)
    return wyniki


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="narzedzia.mysz", description="Sprawdzian prawdziwą myszą stron lekcji (Chrome bez okna).")
    tryb = parser.add_mutually_exclusive_group(required=True)
    tryb.add_argument("--wszystko", action="store_true", help="każda lekcja z ćwiczeniami")
    tryb.add_argument("--probka", action="store_true", help="pierwsza lekcja z ćwiczeniami każdego modułu")
    tryb.add_argument("--lekcja", nargs="+", metavar="SLUG", help="wskazane lekcje (nazwa katalogu lekcji)")
    parser.add_argument("--wyjscie", type=Path, default=KORZEN / "build" / "mysz", help="katalog na strony i zrzuty (domyślnie build/mysz)")
    args = parser.parse_args(argv)
    wybrane = wybierz(znajdz_lekcje(), args.wszystko, args.probka, args.lekcja or [])
    if not wybrane:
        print("Żadna lekcja nie ma ćwiczeń do sprawdzenia.")
        return 1
    wyniki: list[Wynik] = []
    for lekcja in wybrane:
        print(f"== {lekcja.modul}/{lekcja.slug}", file=sys.stderr, flush=True)
        wyniki += sprawdz_lekcje(lekcja, args.wyjscie / "strony", args.wyjscie / "zrzuty")
    print(tabela(wyniki))
    return kod_wyjscia(wyniki)


if __name__ == "__main__":
    sys.exit(main())
