"""Pilnuje długości wypowiedzi nauczyciela (nie liczby słów lekcji) oraz tego, czy nauczyciel odzywa się po każdej zmianie w symulatorze (w terminalu i w drogach symulatora aplikacji)."""
import argparse
import json
import re
import sys
from pathlib import Path

LIMIT_SLOW_NAUCZYCIELA = 25
ZMIANY = ("folder", "tryb")
ZMIANY_APLIKACJI = ("plik", "artefakt")  # w drodze symulatora aplikacji zmianą jest otwarty plik albo otwarta lub podmieniona strona artefaktu
KLIKI_MODELU = ("wybor-modelu", "poziom")  # klik otwierający menu wyboru modelu i klik wybierający poziom wysiłku: po każdym nauczyciel mówi, co się stało
KLIKI_PASKA_BOCZNEGO = ("nowa-rozmowa", "sesja", "archive", "view-all", "archived", "folder", "wiadomosc-od", "pierscien", "background-tasks", "wpis-w-tle", "once")  # kliki w drodze aplikacji, po których okno się zmienia (jak po kroku plik): scenariusz_sesje.py (w tym `folder`, wybór teczki nowej rozmowy, i `wiadomosc-od`, strzałka karty wiadomości); pierscien otwiera okienko zużycia (scenariusz_pierscien.py), panel zadań w tle i panel subagenta (scenariusz_w_tle.py) oraz Once na karcie zgody na przepływ (scenariusz_przeplyw.py)
KLIKI_TELEFONU = ("telefon-sesja", "telefon-wstecz", "ustawienia-claude-code", "ustawienia-connectors")  # kliki w drodze aplikacji, po których zmienia się telefon albo otwiera okno Settings (scenariusz_telefon.py): nauczyciel mówi, co kursant widzi
KLIKI_MENU_RZEDU = ("tryb-menu", "tryb", "srodowisko-menu", "przegladarka", "przegladarka-menu", "strzalka-tytulu", "transcript-view", "widok-transkrypcji", "edytor-rozwin")  # kliki w drodze aplikacji, które otwierają listę trybów albo menu środowiska albo zmieniają tryb (scenariusz_menu_rzedu.py), a od przegladarka do edytor-rozwin otwierają panel Browser z menu „…”, menu sesji z widokiem rozmowy i edytor prezentacji w oknie (scenariusz_ekrany_b.py): nauczyciel mówi, co się stało
KLIKI_PLIKU = ("plik-menu", "plik-karta-menu", "plik-karta-pozycja", "ikona-tytulu")  # kliki w drodze aplikacji, które otwierają menu pliku albo karty pliku albo pokazują dymek ikony paska tytułu (scenariusz_plik_ekran.py): nauczyciel mówi, co kursant widzi
MAKS_ODSTEP_NAUCZYCIELA = 2  # nauczyciel na pozycji i+1 albo i+2
KLIKI_HARMONOGRAMU = ("scheduled", "new-task", "advanced-settings", "create", "run-now")  # kliki zadania według harmonogramu (scenariusz_harmonogram.py): każdy zmienia ekran, więc nauczyciel mówi, co się stało

WZOR_KOMENTARZ = re.compile(r"<!--.*?-->", re.DOTALL)
WZOR_ZNACZNIK = re.compile(r"<[^>]*>")
WZOR_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
WZOR_CWICZENIE = re.compile(r"<!--\s*cwiczenie\s*:.*?-->", re.DOTALL)


def policz_slowa(tekst: str) -> int:
    """Słowa lekcji: bez komentarzy HTML, znaczników i adresów linków; słowo ma literę albo cyfrę."""
    tekst = WZOR_KOMENTARZ.sub(" ", tekst)
    tekst = WZOR_ZNACZNIK.sub(" ", tekst)
    tekst = WZOR_LINK.sub(r"\1", tekst)
    return sum(1 for s in tekst.split() if re.search(r"\w", s))


def bez_zrodel(tekst: str) -> str:
    """Odcina część `## Źródła` (od tego nagłówka do następnej linii `## ` albo do końca pliku); nie liczy się do limitu lekcji."""
    wynik: list[str] = []
    w_zrodlach = False
    for linia in tekst.splitlines(keepends=True):
        if linia.startswith("## "):
            w_zrodlach = linia.strip() == "## Źródła"
        if not w_zrodlach:
            wynik.append(linia)
    return "".join(wynik)


def slowa_wypowiedzi(tekst: str) -> int:
    return len(tekst.split())


def sprawdz_lekcje(plik: Path, nazwa: str) -> tuple[int, int | None]:
    """Zwraca (słowa lekcji bez części Źródła, słowa przed pierwszym ćwiczeniem albo None); bez limitów."""
    tekst = plik.read_text(encoding="utf-8")
    razem = policz_slowa(bez_zrodel(tekst))
    m = WZOR_CWICZENIE.search(tekst)
    wstep = policz_slowa(tekst[: m.start()]) if m else None
    return razem, wstep


def _sprawdz_liste_krokow(kroki: list, gdzie: str, nazwa: str, zmiany: tuple = ZMIANY) -> list[str]:
    bledy: list[str] = []
    for i, krok in enumerate(kroki):
        if not isinstance(krok, dict):
            continue
        typ = krok.get("typ")
        miejsce = f"{gdzie}krok {i + 1} ({typ})"
        if typ == "nauczyciel" and isinstance(krok.get("tekst"), str):
            n = slowa_wypowiedzi(krok["tekst"])
            if n > LIMIT_SLOW_NAUCZYCIELA:
                bledy.append(
                    f"{nazwa}: {gdzie}krok {i + 1} (nauczyciel): {n} słów, limit {LIMIT_SLOW_NAUCZYCIELA}."
                )
        zmienia_okno = typ in zmiany and krok.get("akcja") != "czyta"  # czytanie plików w etapie nie zmienia folderu
        if zmiany == ZMIANY_APLIKACJI and typ == "klik" and krok.get("cel") in KLIKI_PASKA_BOCZNEGO:
            zmienia_okno = True  # w drodze aplikacji: nowa rozmowa, otwarta rozmowa, archiwizacja, widok listy i zakładka Archived
        if zmiany == ZMIANY_APLIKACJI and typ == "klik" and krok.get("cel") in KLIKI_HARMONOGRAMU:
            zmienia_okno = True
        if zmiany == ZMIANY_APLIKACJI and ((typ == "klik" and krok.get("cel") in KLIKI_TELEFONU) or (typ == "komenda" and krok.get("tekst") == "/config")):
            zmienia_okno = True  # telefon pokazuje rozmowę albo listę sesji, okno Settings się otwiera (klik w konto albo komenda /config)
        if typ == "klik" and krok.get("cel") in KLIKI_MODELU:  # zmianą jest też otwarcie menu modelu i wybór poziomu
            zmienia_okno = True
        if zmiany == ZMIANY_APLIKACJI and typ == "klik" and krok.get("cel") in KLIKI_MENU_RZEDU:
            zmienia_okno = True
        if zmiany == ZMIANY_APLIKACJI and typ == "klik" and krok.get("cel") in KLIKI_PLIKU:
            zmienia_okno = True
        if zmienia_okno:
            nastepne = kroki[i + 1 : i + 1 + MAKS_ODSTEP_NAUCZYCIELA]
            if not any(isinstance(k, dict) and k.get("typ") == "nauczyciel" for k in nastepne):
                bledy.append(
                    f"{nazwa}: {miejsce}: brak nauczyciela w {MAKS_ODSTEP_NAUCZYCIELA} kolejnych krokach."
                )
        for nr, opcja in enumerate(krok.get("opcje") or [], 1):
            if isinstance(opcja, dict) and isinstance(opcja.get("dalej"), list):
                bledy += _sprawdz_liste_krokow(
                    opcja["dalej"], f"{gdzie}krok {i + 1} (menu), opcja {nr}, ", nazwa, zmiany
                )
    return bledy


def _przebiegi(wartosc) -> list[tuple[str, list]]:
    """Znajduje wszystkie słowniki `przebiegi` w strukturze i zwraca (id przebiegu, lista kroków)."""
    wynik: list[tuple[str, list]] = []
    if isinstance(wartosc, dict):
        for klucz, w in wartosc.items():
            if klucz == "przebiegi" and isinstance(w, dict):
                wynik += [(k, v) for k, v in w.items() if isinstance(v, list)]
            else:
                wynik += _przebiegi(w)
    elif isinstance(wartosc, list):
        for w in wartosc:
            wynik += _przebiegi(w)
    return wynik


def sprawdz_scenariusz(plik: Path, nazwa: str) -> list[str]:
    try:
        dane = json.loads(plik.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return [f"{nazwa}: nie daje się wczytać ({e})."]
    if not isinstance(dane, dict):
        return [f"{nazwa}: scenariusz musi być obiektem JSON."]
    bledy: list[str] = []
    for cw in dane.get("cwiczenia") or []:
        if not isinstance(cw, dict):
            continue
        cid = cw.get("id", "?")
        for pole, tekst in cw.items():
            if pole.startswith("nauczyciel") and isinstance(tekst, str):
                n = slowa_wypowiedzi(tekst)
                if n > LIMIT_SLOW_NAUCZYCIELA:
                    bledy.append(
                        f"{nazwa}: ćwiczenie {cid}, pole {pole}: {n} słów, limit {LIMIT_SLOW_NAUCZYCIELA}."
                    )
        for i, krok in enumerate(cw.get("kroki") or []):  # ćwiczenie aplikacji: wypowiedź w polu nauczyciel kroku
            if isinstance(krok, dict) and isinstance(krok.get("nauczyciel"), str):
                n = slowa_wypowiedzi(krok["nauczyciel"])
                if n > LIMIT_SLOW_NAUCZYCIELA:
                    bledy.append(
                        f"{nazwa}: ćwiczenie {cid}, krok {i + 1} (nauczyciel): {n} słów, limit {LIMIT_SLOW_NAUCZYCIELA}."
                    )
        for droga in cw.get("drogi") or []:
            if isinstance(droga, dict) and isinstance(droga.get("kroki"), list):
                gdzie = f"ćwiczenie {cid}, droga {droga.get('id', '?')}, "
                bledy += _sprawdz_liste_krokow(droga["kroki"], gdzie, nazwa, ZMIANY_APLIKACJI)
        for nr, etap in enumerate(cw.get("etapy") or [], 1):  # menu trybu i karta zgody (dane/FORMAT-SCENARIUSZA-TRYBY.md)
            if isinstance(etap, dict) and isinstance(etap.get("kroki"), list):
                bledy += _sprawdz_liste_krokow(etap["kroki"], f"ćwiczenie {cid}, etap {nr}, ", nazwa, ("zgoda", "zmiana", "folder"))
            if isinstance(etap, dict) and isinstance(etap.get("etapy"), list):  # droga etapów: etapy wewnętrzne
                for m, wewn in enumerate(etap["etapy"], 1):
                    if isinstance(wewn, dict) and isinstance(wewn.get("kroki"), list):
                        gdzie = f"ćwiczenie {cid}, droga {etap.get('id', '?')}, etap {m}, "
                        bledy += _sprawdz_liste_krokow(wewn["kroki"], gdzie, nazwa, ("zgoda", "zmiana", "folder"))
        for zadanie in cw.get("zadania") or []:
            for pid, kroki in _przebiegi(zadanie):
                bledy += _sprawdz_liste_krokow(kroki, f"ćwiczenie {cid}, przebieg {pid}, ", nazwa)
    return bledy


def sprawdz_czytelnosc(
    korzen: Path, wyjatki: frozenset[str] | None = None
) -> tuple[list[str], list[str]]:
    """Sprawdza wszystkie lekcje w moduly/; zwraca (błędy, wiersze podsumowania). Argument `wyjatki` nic nie zmienia (zostaje dla starych wywołań)."""
    korzen = Path(korzen)
    bledy: list[str] = []
    podsumowanie: list[str] = []
    for lekcja in sorted((korzen / "moduly").glob("**/lekcja.md")):
        nazwa = lekcja.relative_to(korzen).as_posix()
        razem, wstep = sprawdz_lekcje(lekcja, nazwa)
        opis = f"{nazwa}: {razem} słów"
        if wstep is not None:
            opis += f", {wstep} przed pierwszym ćwiczeniem"
        podsumowanie.append(opis)
        scenariusz = lekcja.parent / "scenariusz.json"
        if scenariusz.is_file():
            bledy += sprawdz_scenariusz(scenariusz, scenariusz.relative_to(korzen).as_posix())
    return bledy, podsumowanie


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sprawdza długość lekcji i rytm nauczyciela.")
    parser.add_argument("--korzen", default=".", type=Path)
    args = parser.parse_args(argv)
    bledy, podsumowanie = sprawdz_czytelnosc(args.korzen)
    for b in bledy:
        print(b)
    if bledy:
        print(f"Błędów: {len(bledy)}")
        return 1
    print(f"Lekcji: {len(podsumowanie)}")
    for p in podsumowanie:
        print(f"  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
