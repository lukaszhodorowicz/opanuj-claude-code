"""Podglądy w tekście lekcji: rozpoznaje znacznik `<!-- podglad: ... -->`, daje miejsce na podgląd w HTML i sprawdza znacznik przeciw scenariuszowi."""

import html
import re

from narzedzia.scenariusz_sesje import KLIKI_PODGLADU as KLIKI_SESJI

# trzeci człon: numer odpowiedzi w menu terminala albo słowo `klient` (widok klienta w drodze aplikacji)
PODGLAD = re.compile(r"^\s*<!--\s*podglad:\s*([\w-]+)\s+([\w-]+)(?:\s+(\d+|klient))?\s*-->\s*$")
PODGLAD_UZYTY = re.compile(r'<div class="podglad" data-cw="([\w-]+)" data-t="([\w-]+)"(?: data-opcja="(\d+)")?(?: data-widok="(klient)")?>')


def html_podgladu(znacznik: re.Match) -> str:
    """Miejsce na podgląd: `data-opcja` dla numeru odpowiedzi, `data-widok="klient"` dla widoku klienta."""
    cw, ter, trzeci = (x and html.escape(x, quote=True) for x in znacznik.groups())
    atrybut = ""
    if trzeci == "klient":
        atrybut = ' data-widok="klient"'
    elif trzeci:
        atrybut = f' data-opcja="{trzeci}"'
    return f'<div class="podglad" data-cw="{cw}" data-t="{ter}"{atrybut}></div>'


def liczba_opcji_menu(scenariusz: dict, cw_id: str, ter_id: str) -> int:
    """Liczba odpowiedzi w pierwszym kroku `menu` przebiegu terminala w pierwszym zadaniu ćwiczenia (0, gdy menu brak)."""
    cw = next(c for c in scenariusz.get("cwiczenia", []) if c["id"] == cw_id)
    zadania = cw.get("zadania") or [{}]
    for k in (zadania[0].get("przebiegi") or {}).get(ter_id) or []:
        if isinstance(k, dict) and k.get("typ") == "menu":
            return len(k.get("opcje") or [])
    return 0


# kroki drogi aplikacji, które coś pokazują w oknie: otwarty plik, strona artefaktu albo cudza strona w panelu Browser
KROKI_PODGLADU = ("plik", "artefakt", "strona")


def _pokazuje(krok) -> bool:
    """Krok, po którym podgląd w tekście ma co pokazać: plik, artefakt, strona albo klik w pasku bocznym z rozmowami (sesja, archive, archived: okno z listą rozmów)."""
    return isinstance(krok, dict) and (krok.get("typ") in KROKI_PODGLADU or (krok.get("typ") == "klik" and krok.get("cel") in KLIKI_SESJI))


def _bez_obrazu(scenariusz: dict, cw_id: str, ter_id: str) -> None:
    """Droga aplikacji bez kroku `plik`, `artefakt` i `strona` (np. droga z odmową Deny albo z katalogiem konektorów, która kończy się rozmową) nie ma, co pokazać w podglądzie: to błąd składania."""
    cw = next(c for c in scenariusz["cwiczenia"] if c["id"] == cw_id)
    droga = next((d for d in cw.get("drogi") or [] if isinstance(d, dict) and d.get("id") == ter_id), None)
    if droga is not None and not any(_pokazuje(k) for k in droga.get("kroki") or []):
        raise ValueError(f"znacznik podglądu „{cw_id} {ter_id}”: droga nie ma kroku plik, artefakt ani strona, więc podgląd nie ma czego pokazać (np. droga z odmową Deny albo droga z katalogiem konektorów, która nie ma kroku plik ani artefakt i kończy się rozmową)")


def drogi_etapow(cw: dict) -> list:
    """Pozycje listy `etapy` ćwiczenia aplikacji, które same mają listę `etapy` (drogi etapów); zwykłe etapy nie liczą się."""
    return [d for d in cw.get("etapy") or [] if isinstance(d, dict) and isinstance(d.get("etapy"), list)]


def _klient(scenariusz: dict, cw_id: str, ter_id: str) -> None:
    """Widok klienta: droga aplikacji, która kończy się krokiem `artefakt`, w ćwiczeniu z polem `widok_klienta`."""
    cw = next(c for c in scenariusz["cwiczenia"] if c["id"] == cw_id)
    droga = next((d for d in cw.get("drogi") or [] if isinstance(d, dict) and d.get("id") == ter_id), None)
    nazwa = f"znacznik podglądu „{cw_id} {ter_id} klient”"
    if cw.get("rodzaj") != "aplikacja" or droga is None:
        raise ValueError(f"{nazwa}: widok klienta tylko dla drogi ćwiczenia aplikacji")
    ostatni = next((k for k in reversed(droga.get("kroki") or []) if isinstance(k, dict) and k.get("typ") in KROKI_PODGLADU), {})
    if ostatni.get("typ") != "artefakt":
        raise ValueError(f"{nazwa}: droga nie kończy się krokiem artefakt")
    if not isinstance(cw.get("widok_klienta"), dict):
        raise ValueError(f"{nazwa}: ćwiczenie bez pola widok_klienta")


def sprawdz_podglady(html_lekcji: str, scenariusz: dict) -> None:
    """Każdy użyty znacznik podglądu wskazuje ćwiczenie i terminal (albo drogę) ze scenariusza; zły znacznik to ValueError."""
    terminale = {cw["id"]: {t["id"] for t in [*(cw.get("terminale") or []), *(cw.get("drogi") or []), *drogi_etapow(cw)] if isinstance(t, dict) and "id" in t} for cw in scenariusz.get("cwiczenia", [])}  # drogi: podgląd pliku z ćwiczenia aplikacji
    for cw_id, ter_id, opcja, widok in PODGLAD_UZYTY.findall(html_lekcji):
        if cw_id not in terminale or ter_id not in terminale[cw_id]:
            raise ValueError(f"znacznik podglądu „{cw_id} {ter_id}” bez ćwiczenia albo terminala w scenariuszu")
        if ter_id in {d["id"] for c in scenariusz["cwiczenia"] if c["id"] == cw_id for d in drogi_etapow(c) if "id" in d} and not scenariusz.get("folder_startowy"):
            raise ValueError(f"znacznik podglądu „{cw_id} {ter_id}”: droga etapów bez folder_startowy w scenariuszu (podgląd byłby pusty)")
        _bez_obrazu(scenariusz, cw_id, ter_id)
        if widok:
            _klient(scenariusz, cw_id, ter_id)
        if opcja and int(opcja) >= liczba_opcji_menu(scenariusz, cw_id, ter_id):
            raise ValueError(f"znacznik podglądu „{cw_id} {ter_id} {opcja}”: pierwsze menu przebiegu nie ma odpowiedzi o tym numerze")
