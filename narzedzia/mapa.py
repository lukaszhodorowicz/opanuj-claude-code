"""Mapa pokrycia dokumentacji Claude Code: które strony wchodzą do modułów przewodnika, a które pomijamy."""

import argparse
import sys
import urllib.request
from collections import Counter
from pathlib import Path

import yaml

from narzedzia.spis_stron import wczytaj_strony

KORZEN = Path(__file__).resolve().parent.parent
SPIS = KORZEN / "dane" / "zrodla" / "llms.txt"
MAPA = KORZEN / "dane" / "mapa-pokrycia.yaml"
MODULY = KORZEN / "moduly"
ADRES_SPISU = "https://code.claude.com/docs/llms.txt"
STATUSY = ("modul", "pomijamy", "do-ustalenia")


class BladMapy(ValueError):
    """Plik mapy ma zły kształt (np. `strony` nie jest listą)."""


def wczytaj_mape(sciezka) -> dict:
    sciezka = Path(sciezka)
    if not sciezka.exists():
        return {"strony": []}
    dane = yaml.safe_load(sciezka.read_text(encoding="utf-8"))
    if dane is None:
        dane = {}
    if not isinstance(dane, dict):
        raise BladMapy(f"Plik mapy {sciezka} musi być mapą z kluczem „strony”.")
    if dane.get("strony") is None:
        dane["strony"] = []
    if not isinstance(dane["strony"], list):
        raise BladMapy(f"Pole „strony” w {sciezka} musi być listą wpisów.")
    return dane


def zapisz_mape(sciezka, mapa: dict) -> None:
    tekst = yaml.safe_dump(mapa, allow_unicode=True, sort_keys=False, width=1000)
    Path(sciezka).write_text(tekst, encoding="utf-8")


def sprawdz_mape(strony, mapa, katalog_moduly) -> list[str]:
    """Zwraca błędy mapy względem spisu stron (pusta lista = mapa poprawna)."""
    bledy: list[str] = []
    wpisy = (mapa or {}).get("strony") or []
    adresy_spisu = {s["url"] for s in strony}
    licznik = Counter(w.get("url") for w in wpisy if isinstance(w, dict))
    for s in strony:
        n = licznik.get(s["url"], 0)
        if n == 0:
            bledy.append(f"Brak w mapie strony ze spisu: {s['url']}")
        elif n > 1:
            bledy.append(f"Strona występuje w mapie {n} razy: {s['url']}")
    for nr, w in enumerate(wpisy, start=1):
        if not isinstance(w, dict):
            bledy.append(f"Wpis nr {nr} nie jest mapą: {w!r}")
            continue
        url = w.get("url")
        if url not in adresy_spisu:
            bledy.append(f"Wpis spoza spisu: {url}")
        status = w.get("status")
        if status not in STATUSY:
            bledy.append(
                f"Zły status „{status}” przy {url} (dozwolone: {', '.join(STATUSY)})"
            )
            continue
        modul, powod = w.get("modul"), w.get("powod")
        if status == "modul":
            if not modul:
                bledy.append(f"Status modul bez pola modul: {url}")
            elif not (Path(katalog_moduly) / str(modul)).is_dir():
                bledy.append(
                    f"Moduł „{modul}” nie ma katalogu w {katalog_moduly}: {url}"
                )
            if powod:
                bledy.append(f"Status modul z polem powod: {url}")
        elif status == "pomijamy":
            if not (isinstance(powod, str) and powod.strip()):
                bledy.append(f"Status pomijamy bez powodu: {url}")
            if modul:
                bledy.append(f"Status pomijamy z polem modul: {url}")
        else:
            if modul or powod:
                bledy.append(
                    f"Status do-ustalenia nie może mieć pól modul ani powod: {url}"
                )
    return bledy


def uzupelnij(strony, mapa: dict) -> list[dict]:
    """Dopisuje do mapy brakujące strony ze statusem do-ustalenia; zwraca dopisane wpisy."""
    znane = {w.get("url") for w in mapa["strony"]}
    nowe = [
        {
            "url": s["url"],
            "tytul": s["tytul"],
            "sekcja": s["sekcja"],
            "status": "do-ustalenia",
        }
        for s in strony
        if s["url"] not in znane
    ]
    mapa["strony"].extend(nowe)
    return nowe


def policz_roznice(strony, mapa: dict) -> tuple[list[str], list[str]]:
    adresy_spisu = [s["url"] for s in strony]
    adresy_mapy = [w.get("url") for w in mapa["strony"]]
    nowe = [u for u in adresy_spisu if u not in set(adresy_mapy)]
    usuniete = [u for u in adresy_mapy if u not in set(adresy_spisu)]
    return nowe, usuniete


def pobierz_spis(adres: str = ADRES_SPISU) -> str:
    # code.claude.com odrzuca domyślny User-Agent urllib błędem 403.
    zapytanie = urllib.request.Request(
        adres, headers={"User-Agent": "Mozilla/5.0 (przewodnik-claude-code; narzedzia.mapa)"}
    )
    with urllib.request.urlopen(zapytanie, timeout=30) as odp:
        return odp.read().decode("utf-8")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="narzedzia.mapa", description=__doc__)
    p.add_argument("polecenie", choices=["uzupelnij", "roznice", "stan", "pobierz"])
    p.add_argument("--spis", default=str(SPIS), help="plik migawki llms.txt")
    p.add_argument("--mapa", default=str(MAPA), help="plik mapy pokrycia (YAML)")
    p.add_argument("--moduly", default=str(MODULY), help="katalog modułów")
    a = p.parse_args(argv)

    if a.polecenie == "pobierz":
        Path(a.spis).write_text(pobierz_spis(), encoding="utf-8")
        print(f"Zapisano migawkę: {a.spis}")
        return 0

    strony = wczytaj_strony(a.spis)
    try:
        mapa = wczytaj_mape(a.mapa)
    except BladMapy as blad:
        print(f"Błąd: {blad}", file=sys.stderr)
        return 2

    if a.polecenie == "uzupelnij":
        nowe = uzupelnij(strony, mapa)
        if nowe:
            zapisz_mape(a.mapa, mapa)
        print(f"Dopisano stron: {len(nowe)}")
        return 0
    if a.polecenie == "roznice":
        nowe, usuniete = policz_roznice(strony, mapa)
        for u in nowe:
            print(f"NOWA (w spisie, brak w mapie): {u}")
        for u in usuniete:
            print(f"USUNIETA (w mapie, brak w spisie): {u}")
        if not (nowe or usuniete):
            print("Bez różnic.")
        return 1 if (nowe or usuniete) else 0
    liczby = Counter(w.get("status") for w in mapa["strony"])
    for status in STATUSY:
        print(f"{status}: {liczby.get(status, 0)}")
    for status, n in liczby.items():
        if status not in STATUSY:
            print(f"{status}: {n}")
    print(f"razem: {len(mapa['strony'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
