"""Składa fiszki ze wszystkich modułów w jedną talię Anki (plik .apkg) ze stałymi identyfikatorami."""

import argparse
import hashlib
import html
import re
import sys
from pathlib import Path

import genanki
import yaml

NAZWA_TALII = "Przewodnik po Claude Code"
NAZWA_MODELU = "Przewodnik po Claude Code: Przód i Tył"


def _liczba(tekst: str) -> int:
    """Stała liczba z nazwy, w zakresie bezpiecznym dla Anki (1 << 30 .. 1 << 31)."""
    h = int(hashlib.sha1(tekst.encode("utf-8")).hexdigest(), 16)
    return (1 << 30) + h % (1 << 30)


MODEL = genanki.Model(
    _liczba("model:" + NAZWA_MODELU),
    NAZWA_MODELU,
    fields=[{"name": "Przód"}, {"name": "Tył"}],
    templates=[
        {
            "name": "Karta 1",
            "qfmt": "{{Przód}}",
            "afmt": "{{FrontSide}}<hr id=answer>{{Tył}}",
        }
    ],
)


class NotatkaStala(genanki.Note):
    """Notatka z GUID wyliczonym z (moduł, przód), żeby ponowny import aktualizował."""

    @property
    def guid(self):
        return genanki.guid_for(*self._klucz)


def na_html(tekst: str) -> str:
    """Zamienia tekst fiszki na HTML pola Anki: ucieczka, `kod` na <code>, nowe linie na <br>."""
    wynik = html.escape(tekst, quote=False)
    wynik = re.sub(r"`([^`\n]+)`", r"<code>\1</code>", wynik)
    return wynik.replace("\n", "<br>")


def wczytaj_fiszki_modulow(korzen: Path) -> dict[str, list[dict]]:
    wynik: dict[str, list[dict]] = {}
    katalog = Path(korzen) / "moduly"
    for plik in sorted(katalog.glob("*/fiszki.yaml")):
        dane = yaml.safe_load(plik.read_text(encoding="utf-8")) or {}
        wynik[plik.parent.name] = list(dane.get("fiszki") or [])
    return wynik


def zloz_talie(korzen: Path) -> list[genanki.Deck]:
    talie = []
    for modul, fiszki in wczytaj_fiszki_modulow(korzen).items():
        nazwa = f"{NAZWA_TALII}::{modul}"
        talia = genanki.Deck(_liczba("talia:" + nazwa), nazwa)
        for f in fiszki:
            n = NotatkaStala(
                model=MODEL, fields=[na_html(str(f["przod"])), na_html(str(f["tyl"]))]
            )
            n._klucz = (modul, str(f["przod"]))
            talia.add_note(n)
        talie.append(talia)
    # talia nadrzędna: pusta, żeby podtalie miały wspólny korzeń
    talie.insert(0, genanki.Deck(_liczba("talia:" + NAZWA_TALII), NAZWA_TALII))
    return talie


def zapisz(korzen: Path, wyjscie: Path) -> int:
    """Zapisuje plik .apkg; zwraca liczbę notatek."""
    talie = zloz_talie(korzen)
    wyjscie.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(talie).write_to_file(str(wyjscie))
    return sum(len(t.notes) for t in talie)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Eksport fiszek do Anki.")
    parser.add_argument("--korzen", default=".", type=Path)
    parser.add_argument("--wyjscie", required=True, type=Path)
    args = parser.parse_args(argv)
    liczba = zapisz(args.korzen, args.wyjscie)
    print(f"Zapisano {args.wyjscie}: {liczba} notatek.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
