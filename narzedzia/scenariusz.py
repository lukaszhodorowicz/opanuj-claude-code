"""Sprawdza scenariusze symulatora (scenariusz.json) wobec formatu, listy napisów interfejsu i faktów."""
import argparse
import json
import re
import sys
from pathlib import Path

import yaml

from narzedzia.napisy import _Napisy, wczytaj_napisy  # noqa: F401
from narzedzia.scenariusz_aplikacja import sprawdz_aplikacje
from narzedzia.scenariusz_drzewo import sprawdz_gore
from narzedzia.scenariusz_folder import sprawdz_stan_folderu
from narzedzia.scenariusz_narzedzia import (
    krok_narzedzia,
    krok_wyniku,
    sprawdz_kolejnosc_wynikow,
)
from narzedzia.scenariusz_pola import pola_cwiczenia, pola_folderu, pola_zadania

KORZEN = Path(__file__).resolve().parent.parent
TRYBY = ("manual", "edycje", "plan", "auto")
RODZAJE = ("porownanie", "pojedynczy", "przelacznik", "aplikacja")
LICZBA_TERMINALI = {"porownanie": 2, "pojedynczy": 1, "przelacznik": 1}
TYPY = ("pisz", "kolejka", "mysli", "claude", "narzedzie", "wynik", "folder", "tryb", "nauczyciel", "czekaj", "menu")
AKCJE_FOLDERU = ("utworz", "przenies", "nowy", "zmien", "usun", "edytuj", "przywroc")
RAMKI = ("plan", "zgoda")


def wczytaj_id_faktow(sciezka: Path) -> set[str]:
    """Zbiór `id` faktów z pliku faktów."""
    dane = yaml.safe_load(sciezka.read_text(encoding="utf-8")) or {}
    return {f["id"] for f in (dane.get("fakty") or []) if isinstance(f, dict) and "id" in f}


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


class _Kontrola:
    def __init__(self, napisy, fakty_id, nazwy_plikow, start=(), glowny=None):
        self.start = {p for p in start if isinstance(p, str)}
        self.glowny = glowny  # `folder_glowny` z góry scenariusza: korzeń podglądu folderu aplikacji
        self.napisy = napisy
        self.fakty = fakty_id
        self.pliki = nazwy_plikow
        self.bledy: list[str] = []

    def blad(self, sciezka: str, tresc: str):
        self.bledy.append(f"{sciezka}: {tresc}")

    def fakt(self, krok, sciezka):
        if "fakt" not in krok or self.fakty is None:
            return
        if krok["fakt"] not in self.fakty:
            self.blad(sciezka, f"fakt „{krok['fakt']}” nie istnieje w pliku faktów")

    def tryb(self, wartosc, sciezka, pole):
        if wartosc not in TRYBY:
            self.blad(sciezka, f"{pole} „{wartosc}” spoza trybów {'/'.join(TRYBY)}")

    def kroki(self, kroki, sciezka: str):
        if not isinstance(kroki, list):
            self.blad(sciezka, "kroki muszą być listą")
            return
        for i, krok in enumerate(kroki):
            self.krok(krok, f"{sciezka}[{i}]")
            if isinstance(krok, dict) and krok.get("typ") == "menu" and i < len(kroki) - 1:
                self.blad(f"{sciezka}[{i + 1}]", "kroki po menu nigdy się nie wykonają; przenieś je do dalej")
                break

    def krok(self, krok, s: str):
        if not isinstance(krok, dict):
            self.blad(s, "krok musi być obiektem")
            return
        typ = krok.get("typ")
        if typ not in TYPY:
            self.blad(s, f"nieznany typ kroku „{typ}”")
            return
        if typ in ("pisz", "kolejka", "claude", "nauczyciel") and not _niepusty(krok.get("tekst")):
            self.blad(s, f"krok „{typ}” wymaga niepustego pola tekst")
        if typ in ("mysli", "czekaj") and not isinstance(krok.get("ms"), int):
            self.blad(s, f"krok „{typ}” wymaga liczby całkowitej w polu ms")
        if typ == "tryb":
            self.tryb(krok.get("na"), s, "na")
        if typ == "folder":
            if krok.get("akcja") not in AKCJE_FOLDERU:
                self.blad(s, f"folder: akcja „{krok.get('akcja')}” spoza {'/'.join(AKCJE_FOLDERU)}")
            if not _niepusty(krok.get("nazwa")):
                self.blad(s, "folder wymaga pola nazwa")
            if krok.get("akcja") == "zmien" and not _niepusty(krok.get("plik")):
                self.blad(s, "folder zmien wymaga pola plik (stara nazwa)")
            pola_folderu(krok, s, self.blad)
        if typ == "narzedzie":
            krok_narzedzia(krok, s, self.napisy, self.pliki, self.blad)
        if typ == "wynik":
            krok_wyniku(krok, s, self.napisy, self.pliki, self.blad)
        if typ == "menu":
            self.menu(krok, s)
        self.fakt(krok, s)

    def menu(self, krok, s):
        if "ramka" in krok and krok["ramka"] not in RAMKI:
            self.blad(s, f"ramka „{krok['ramka']}” spoza {'/'.join(RAMKI)}")
        tytul = krok.get("tytul")
        if "tytul" in krok and not isinstance(tytul, str):
            self.blad(s, "tytul menu musi być napisem")
        elif _niepusty(tytul) and not self.napisy.jest(tytul, "menu"):
            self.blad(s, f"tytuł menu „{tytul}” spoza listy napisów interfejsu")
        if not isinstance(krok.get("pytanie"), str):
            self.blad(s, "pytanie menu musi być napisem")
        elif not self.napisy.jest(krok.get("pytanie"), "menu"):
            self.blad(s, f"pytanie menu „{krok.get('pytanie')}” spoza listy napisów interfejsu")
        opcje = krok.get("opcje")
        if not isinstance(opcje, list) or not opcje:
            self.blad(s, "menu wymaga niepustej listy opcje")
            return
        for i, op in enumerate(opcje):
            so = f"{s}/opcje[{i}]"
            if not isinstance(op, dict):
                self.blad(so, "opcja musi być obiektem")
                continue
            if not self.napisy.jest(op.get("napis"), "menu"):
                self.blad(so, f"napis opcji „{op.get('napis')}” spoza listy napisów interfejsu")
            for pole in ("pl", "opis"):
                if not _niepusty(op.get(pole)):
                    self.blad(so, f"opcja bez pola {pole}")
            self.fakt(op, so)
            if not isinstance(op.get("dalej"), list):
                self.blad(so, "opcja bez listy dalej")
            else:
                self.kroki(op["dalej"], f"{so}/dalej")

    def cwiczenie(self, cw, s: str):
        rodzaj = cw.get("rodzaj")
        if rodzaj not in RODZAJE:
            self.blad(s, f"nieznany rodzaj ćwiczenia „{rodzaj}”")
            return
        pola_cwiczenia(cw, s, self.pliki, self.blad)
        for pole in ("tytul", "nauczyciel_start"):
            if not _niepusty(cw.get(pole)):
                self.blad(s, f"brak pola {pole}")
        if rodzaj == "aplikacja":
            self.id_ok(cw.get("id"), s, "ćwiczenie")
            return sprawdz_aplikacje(cw, s, self.napisy, self.fakt, self.blad, self.start, self.glowny)
        term = cw.get("terminale")
        if not isinstance(term, list) or len(term) != LICZBA_TERMINALI[rodzaj]:
            self.blad(s, f"rodzaj {rodzaj} wymaga {LICZBA_TERMINALI[rodzaj]} terminali")
            term = term if isinstance(term, list) else []
        ids = []
        self.id_ok(cw.get("id"), s, "ćwiczenie")
        for i, t in enumerate(term):
            st = f"{s}/terminale[{i}]"
            if not isinstance(t, dict) or not _niepusty(t.get("id")):
                self.blad(st, "terminal wymaga pola id")
                continue
            self.id_ok(t["id"], st, "terminal")
            if t["id"] in ids:
                self.blad(st, f"id terminala „{t['id']}” powtórzone w ćwiczeniu")
            ids.append(t["id"])
            for pole in ("podpis", "dopisek"):
                if not _niepusty(t.get(pole)):
                    self.blad(st, f"terminal bez pola {pole}")
            self.tryb(t.get("tryb"), st, "tryb")
        if rodzaj == "przelacznik":
            self.przelacznik(cw, s)
        else:
            self.zadania(cw, s, ids)

    def id_ok(self, wartosc, sciezka, co):
        if isinstance(wartosc, str) and not re.fullmatch(r"[a-z0-9-]+", wartosc):
            self.blad(sciezka, f"id {co} „{wartosc}” musi pasować do ^[a-z0-9-]+$")

    def zadania(self, cw, s, ids):
        zadania = cw.get("zadania")
        if not isinstance(zadania, list) or not zadania:
            self.blad(s, "ćwiczenie wymaga niepustej listy zadania")
            return
        for i, z in enumerate(zadania):
            sz = f"{s}/zadania[{i}]"
            if not isinstance(z, dict):
                self.blad(sz, "zadanie musi być obiektem")
                continue
            pola_zadania(z, sz, self.blad)
            for pole in ("etykieta", "polecenie"):
                if not _niepusty(z.get(pole)):
                    self.blad(sz, f"zadanie bez pola {pole}")
            if not isinstance(z.get("slowa_kluczowe"), list):
                self.blad(sz, "zadanie bez listy slowa_kluczowe")
            przebiegi = z.get("przebiegi")
            if not isinstance(przebiegi, dict):
                self.blad(sz, "zadanie bez obiektu przebiegi")
                continue
            for tid in ids:
                if tid not in przebiegi:
                    self.blad(f"{sz}/przebiegi", f"brak przebiegu dla terminala „{tid}”")
            for tid, kroki in przebiegi.items():
                if tid not in ids:
                    self.blad(f"{sz}/przebiegi", f"przebieg dla nieznanego terminala „{tid}”")
                self.kroki(kroki, f"{sz}/przebiegi/{tid}")
                sprawdz_stan_folderu(kroki, self.start, f"{sz}/przebiegi/{tid}", self.blad)
                sprawdz_kolejnosc_wynikow(kroki, f"{sz}/przebiegi/{tid}", self.blad)

    def przelacznik(self, cw, s):
        cykl, cel, kom = cw.get("cykl"), cw.get("cel"), cw.get("komentarze")
        if not isinstance(cykl, list) or not cykl:
            self.blad(s, "przełącznik wymaga niepustej listy cykl")
            cykl = []
        for i, t in enumerate(cykl):
            self.tryb(t, f"{s}/cykl[{i}]", "tryb")
        self.tryb(cel, s, "cel")
        if cel in TRYBY and cel not in cykl:
            self.blad(s, f"cel „{cel}” nie leży w cyklu")
        if not isinstance(kom, dict):
            self.blad(s, "przełącznik wymaga obiektu komentarze")
            return
        for t in cykl:
            if not _niepusty(kom.get(t)):
                self.blad(f"{s}/komentarze", f"brak komentarza dla trybu „{t}”")


def _nazwy_plikow(dane: dict) -> set[str]:
    nazwy = {p for p in dane.get("folder_startowy", []) if isinstance(p, str)}

    def idz(w):
        if isinstance(w, dict):
            if w.get("typ") == "folder":
                nazwy.update(x for x in (w.get("nazwa"), w.get("plik")) if isinstance(x, str))
            for v in w.values():
                idz(v)
        elif isinstance(w, list):
            for v in w:
                idz(v)

    idz(dane.get("cwiczenia"))
    return nazwy


def sprawdz_scenariusz(dane: dict, fakty_id: set | None, napisy) -> list[str]:
    """Zwraca błędy scenariusza po polsku; `fakty_id=None` pomija sprawdzanie faktów."""
    if not isinstance(dane, dict):
        return ["scenariusz musi być obiektem JSON"]
    start = dane.get("folder_startowy") if isinstance(dane.get("folder_startowy"), list) else []
    k = _Kontrola(napisy if isinstance(napisy, _Napisy) else _Napisy(napisy), fakty_id, _nazwy_plikow(dane), start, dane.get("folder_glowny"))
    sprawdz_gore(dane, k.blad)
    if not _niepusty(dane.get("lekcja")):
        k.blad("scenariusz", "brak pola lekcja")
    if not isinstance(dane.get("folder_startowy"), list):
        k.blad("scenariusz", "brak listy folder_startowy")
    if "terminal_tytul" in dane and not k.napisy.jest(dane["terminal_tytul"], "okno"):
        k.blad("terminal_tytul", "pasek okna terminala pokazuje tylko folder roboczy (~/folder)")
    cwiczenia = dane.get("cwiczenia")
    if not isinstance(cwiczenia, list) or not cwiczenia:
        k.blad("scenariusz", "brak niepustej listy cwiczenia")
        return k.bledy
    widziane = set()
    for i, cw in enumerate(cwiczenia):
        if isinstance(cw, dict) and cw.get("id") in widziane:
            k.blad(f"cwiczenia[{i}]", f"id ćwiczenia „{cw['id']}” powtórzone w scenariuszu")
        if isinstance(cw, dict) and isinstance(cw.get("id"), str):
            widziane.add(cw["id"])
        if not isinstance(cw, dict):
            k.blad(f"cwiczenia[{i}]", "ćwiczenie musi być obiektem")
            continue
        if not _niepusty(cw.get("id")):
            k.blad(f"cwiczenia[{i}]", "ćwiczenie bez pola id")
        k.cwiczenie(cw, str(cw.get("id", f"cwiczenia[{i}]")))
    return k.bledy


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Sprawdza scenariusze symulatora.")
    ap.add_argument("pliki", nargs="+", type=Path)
    ap.add_argument("--fakty", type=Path, action="append", default=[], help="dodatkowy plik faktów")
    ap.add_argument("--napisy", type=Path, default=KORZEN / "dane" / "napisy-interfejsu.yaml")
    arg = ap.parse_args(argv)
    napisy = _Napisy(wczytaj_napisy(arg.napisy))
    fakty = wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
    for p in arg.fakty:
        fakty |= wczytaj_id_faktow(p)
    kod = 0
    for plik in arg.pliki:
        try:
            dane = json.loads(plik.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"{plik}: nie da się wczytać: {e}")
            kod = 1
            continue
        w_wzorach = "wzory" in plik.resolve().parts
        bledy = sprawdz_scenariusz(dane, None if w_wzorach else fakty, napisy)
        for b in bledy:
            print(f"{plik}: {b}")
        kod = 1 if bledy else kod
        if not bledy:
            print(f"{plik}: ok")
    return kod


if __name__ == "__main__":
    sys.exit(main())
