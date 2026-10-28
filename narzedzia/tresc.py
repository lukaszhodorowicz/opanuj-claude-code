"""Wczytuje i sprawdza treść przewodnika: fakty, quizy, fiszki i odwołania w lekcjach."""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import yaml

from narzedzia.fakty_silnika import fakty_w_formacie
from narzedzia.napisy import fakty_w_napisach
from narzedzia.slowniczek_fakty import bledy_slowniczka, fakty_w_slowniczku

WZOR_ID = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
WZOR_ADRES = re.compile(r"\((https://code\.claude\.com/docs/en/[^)\s]+\.md)\)")
WZOR_KOMENTARZ = re.compile(r"<!--(.*?)-->", re.DOTALL)
WZOR_SLOWO_FAKT = re.compile(r"\bfakt\b", re.IGNORECASE)
WZOR_ODWOLANIE = re.compile(r"\s*fakt\s*:\s*(\S+)\s*")
WZOR_DATA = re.compile(r"\d{4}-\d{2}-\d{2}")
PLIKI_MODULU = ("lekcja.md", "quiz.yaml", "fiszki.yaml")


def _yaml(sciezka: Path):
    return yaml.safe_load(sciezka.read_text(encoding="utf-8"))


def wczytaj_adresy_spisu(sciezka: Path) -> set[str]:
    """Adresy stron dokumentacji ze spisu (bez adresów `_llms`)."""
    tekst = sciezka.read_text(encoding="utf-8")
    return {a for a in WZOR_ADRES.findall(tekst) if "/_llms/" not in a}


def wczytaj_fakty(sciezka: Path) -> dict:
    """Zwraca słownik z kluczami `zrodla_zewnetrzne` i `fakty` (puste, gdy brak)."""
    dane = _yaml(sciezka) or {}
    if not isinstance(dane, dict):
        return {"zrodla_zewnetrzne": [], "fakty": []}
    return {
        "zrodla_zewnetrzne": dane.get("zrodla_zewnetrzne") or [],
        "fakty": dane.get("fakty") or [],
    }


def wczytaj_mape(sciezka: Path) -> list[dict]:
    dane = _yaml(sciezka) or {}
    return [s for s in (dane.get("strony") or []) if isinstance(s, dict)]


def sprawdz_odwolania_lekcji(sciezka: Path) -> tuple[list[str], list[str]]:
    """Zwraca (id odwołań, błędy): komentarz ze słowem „fakt” musi mieć postać `<!-- fakt: id -->`."""
    tekst = sciezka.read_text(encoding="utf-8")
    ids, bledy = [], []
    for m in WZOR_KOMENTARZ.finditer(tekst):
        wnetrze = m.group(1)
        if not WZOR_SLOWO_FAKT.search(wnetrze):
            continue
        dopasowanie = WZOR_ODWOLANIE.fullmatch(wnetrze)
        if dopasowanie and WZOR_ID.fullmatch(dopasowanie.group(1)):
            ids.append(dopasowanie.group(1))
        else:
            nr = tekst.count("\n", 0, m.start()) + 1
            bledy.append(
                f"{sciezka.name}, linia {nr}: źle zapisane odwołanie „{m.group(0)}”,"
                " oczekiwano <!-- fakt: id -->."
            )
    return ids, bledy


def wczytaj_odwolania_lekcji(sciezka: Path) -> list[str]:
    return sprawdz_odwolania_lekcji(sciezka)[0]


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


def _data_poprawna(wartosc) -> bool:
    if isinstance(wartosc, date):
        return True
    if not isinstance(wartosc, str) or not WZOR_DATA.fullmatch(wartosc):
        return False
    try:
        date.fromisoformat(wartosc)
        return True
    except ValueError:
        return False


def _sprawdz_fakty(fakty: list, adresy: set[str], zewnetrzne: list) -> tuple[list[str], set[str]]:
    bledy: list[str] = []
    ids: set[str] = set()
    dozwolone = adresy | {z for z in zewnetrzne if isinstance(z, str)}
    for nr, f in enumerate(fakty, 1):
        if not isinstance(f, dict):
            bledy.append(f"Fakt nr {nr}: wpis nie jest słownikiem.")
            continue
        fid = f.get("id")
        nazwa = f"Fakt „{fid}”" if fid else f"Fakt nr {nr}"
        if not isinstance(fid, str) or not WZOR_ID.fullmatch(fid):
            bledy.append(f"Fakt nr {nr}: niepoprawny id „{fid}”.")
        elif fid in ids:
            bledy.append(f"{nazwa}: id występuje więcej niż raz.")
        else:
            ids.add(fid)
        for pole in ("tresc", "zrodlo", "wersja"):
            if pole == "wersja" and f.get(pole) is not None and not isinstance(f.get(pole), str):
                bledy.append(f"{nazwa}: pole „wersja” musi być tekstem w cudzysłowie, np. \"2.1.309\".")
            elif not _niepusty(f.get(pole)):
                bledy.append(f"{nazwa}: brak pola „{pole}” albo jest puste.")
        if not _data_poprawna(f.get("sprawdzono")):
            bledy.append(f"{nazwa}: pole „sprawdzono” nie jest datą RRRR-MM-DD.")
        zrodlo = f.get("zrodlo")
        if _niepusty(zrodlo) and zrodlo.split("#", 1)[0] not in dozwolone:
            bledy.append(f"{nazwa}: źródło „{zrodlo}” nie jest w spisie ani w zrodla_zewnetrzne.")
    return bledy, ids


def _sprawdz_quiz(sciezka: Path, modul: str) -> tuple[list[str], list[str]]:
    bledy, odwolania = [], []
    try:
        dane = _yaml(sciezka)
    except yaml.YAMLError as e:
        return [f"Moduł „{modul}”: quiz.yaml nie daje się wczytać ({e})."], []
    pytania = dane.get("pytania") if isinstance(dane, dict) else None
    if not isinstance(pytania, list) or not pytania:
        return [f"Moduł „{modul}”: quiz.yaml nie ma listy „pytania”."], []
    for nr, p in enumerate(pytania, 1):
        gdzie = f"Moduł „{modul}”, pytanie {nr}"
        if not isinstance(p, dict):
            bledy.append(f"{gdzie}: wpis nie jest słownikiem.")
            continue
        for pole in ("pytanie", "wyjasnienie"):
            if not _niepusty(p.get(pole)):
                bledy.append(f"{gdzie}: brak pola „{pole}”.")
        odp = p.get("odpowiedzi")
        if not isinstance(odp, list) or not 2 <= len(odp) <= 5:
            bledy.append(f"{gdzie}: „odpowiedzi” muszą być listą 2-5 pozycji.")
        else:
            if not all(_niepusty(o) for o in odp):
                bledy.append(f"{gdzie}: odpowiedź jest pusta.")
            elif len(set(odp)) != len(odp):
                bledy.append(f"{gdzie}: odpowiedzi się powtarzają.")
            ind = p.get("poprawna")
            if isinstance(ind, bool) or not isinstance(ind, int) or not 0 <= ind < len(odp):
                bledy.append(f"{gdzie}: „poprawna” ({ind}) poza zakresem odpowiedzi.")
        if _niepusty(p.get("fakt")):
            odwolania.append(p["fakt"])
        else:
            bledy.append(f"{gdzie}: brak odwołania „fakt”.")
    return bledy, odwolania


def wczytaj_fiszki(sciezka: Path) -> list[dict]:
    dane = _yaml(sciezka)
    lista = dane.get("fiszki") if isinstance(dane, dict) else None
    return lista if isinstance(lista, list) else []


def _sprawdz_fiszki(sciezka: Path, modul: str) -> tuple[list[str], list[str]]:
    bledy, odwolania = [], []
    try:
        dane = _yaml(sciezka)
    except yaml.YAMLError as e:
        return [f"Moduł „{modul}”: fiszki.yaml nie daje się wczytać ({e})."], []
    if not isinstance(dane, dict) or not isinstance(dane.get("fiszki"), list) or not dane["fiszki"]:
        return [f"Moduł „{modul}”: fiszki.yaml nie ma listy „fiszki”."], []
    przody: set[str] = set()
    for nr, f in enumerate(dane["fiszki"], 1):
        gdzie = f"Moduł „{modul}”, fiszka {nr}"
        if not isinstance(f, dict):
            bledy.append(f"{gdzie}: wpis nie jest słownikiem.")
            continue
        for pole in ("przod", "tyl"):
            if not _niepusty(f.get(pole)):
                bledy.append(f"{gdzie}: brak pola „{pole}”.")
        if _niepusty(f.get("przod")):
            if f["przod"] in przody:
                bledy.append(f"{gdzie}: przód „{f['przod']}” się powtarza.")
            przody.add(f["przod"])
        if _niepusty(f.get("fakt")):
            odwolania.append(f["fakt"])
        else:
            bledy.append(f"{gdzie}: brak odwołania „fakt”.")
    return bledy, odwolania


def _fakty_ze_struktury(wartosc) -> list[str]:
    """Rekurencyjnie zbiera napisy z pól `fakt` w całej strukturze JSON."""
    wynik: list[str] = []
    if isinstance(wartosc, dict):
        for klucz, w in wartosc.items():
            if klucz == "fakt" and isinstance(w, str):
                wynik.append(w)
            else:
                wynik += _fakty_ze_struktury(w)
    elif isinstance(wartosc, list):
        for w in wartosc:
            wynik += _fakty_ze_struktury(w)
    return wynik


def _sprawdz_scenariusz(sciezka: Path, modul: str) -> tuple[list[str], list[str]]:
    try:
        dane = json.loads(sciezka.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return [f"Moduł „{modul}”: {sciezka.name} nie daje się wczytać ({e})."], []
    return [], _fakty_ze_struktury(dane)


def _lekcje_modulu(dir_modulu: Path) -> list[tuple[str, Path]]:
    """Zwraca lekcje modułu jako (nazwa, katalog): sam moduł albo jego podkatalogi z lekcja.md."""
    if (dir_modulu / "lekcja.md").is_file():
        return [(dir_modulu.name, dir_modulu)]
    return [
        (f"{dir_modulu.name}/{d.name}", d)
        for d in sorted(p for p in dir_modulu.iterdir() if p.is_dir())
        if (d / "lekcja.md").is_file()
    ]


def _sprawdz_lekcje(dir_modulu: Path, modul: str, ids: set[str], uzyte: set[str], bledy: list[str]) -> None:
    for nazwa in PLIKI_MODULU:
        if not (dir_modulu / nazwa).is_file():
            bledy.append(f"Moduł „{modul}”: brak pliku {nazwa}.")
    odwolania: list[tuple[str, str]] = []
    if (dir_modulu / "lekcja.md").is_file():
        ids_lekcji, b = sprawdz_odwolania_lekcji(dir_modulu / "lekcja.md")
        bledy += [f"Moduł „{modul}”: {x}" for x in b]
        odwolania += [("lekcja", o) for o in ids_lekcji]
    for plik, funkcja, etykieta in (
        ("quiz.yaml", _sprawdz_quiz, "quiz"),
        ("fiszki.yaml", _sprawdz_fiszki, "fiszki"),
        ("scenariusz.json", _sprawdz_scenariusz, "scenariusz"),
    ):
        if (dir_modulu / plik).is_file():
            b, o = funkcja(dir_modulu / plik, modul)
            bledy += b
            odwolania += [(etykieta, x) for x in o]
    for gdzie, fid in odwolania:
        if fid in ids:
            uzyte.add(fid)
        else:
            bledy.append(f"Moduł „{modul}” ({gdzie}): odwołanie do nieistniejącego faktu „{fid}”.")


def sprawdz_tresc(korzen: Path) -> list[str]:
    """Sprawdza fakty, moduły, quizy, fiszki i odwołania; zwraca listę błędów po polsku.

    Użyciem faktu jest też zapis „fakt <id>” w polu `zrodlo` napisu w `dane/napisy-interfejsu.yaml`
    oraz cytat „fakt `<id>`” w opisie formatu silnika `dane/FORMAT-SCENARIUSZA*.md`.
    """
    korzen = Path(korzen)
    bledy: list[str] = []
    spis, mapa_plik, fakty_plik = (
        korzen / "dane/zrodla/llms.txt",
        korzen / "dane/mapa-pokrycia.yaml",
        korzen / "dane/fakty.yaml",
    )
    for p in (spis, mapa_plik, fakty_plik):
        if not p.is_file():
            bledy.append(f"Brak pliku {p.relative_to(korzen)}.")
    if bledy:
        return bledy
    try:
        dane = wczytaj_fakty(fakty_plik)
        mapa = wczytaj_mape(mapa_plik)
    except yaml.YAMLError as e:
        return [f"Plik YAML nie daje się wczytać: {e}"]
    b, ids = _sprawdz_fakty(dane["fakty"], wczytaj_adresy_spisu(spis), dane["zrodla_zewnetrzne"])
    bledy += b
    moduly_w_mapie = {
        s.get("modul") for s in mapa if s.get("status") == "modul" and s.get("modul")
    }
    uzyte: set[str] = set()
    katalog = korzen / "moduly"
    for dir_modulu in sorted(p for p in katalog.iterdir() if p.is_dir()) if katalog.is_dir() else []:
        lekcje = _lekcje_modulu(dir_modulu)
        if lekcje and dir_modulu.name not in moduly_w_mapie:
            bledy.append(
                f"Moduł „{dir_modulu.name}”: w mapie brak strony ze statusem „modul” i modul: {dir_modulu.name}."
            )
        for modul, dir_lekcji in lekcje:
            _sprawdz_lekcje(dir_lekcji, modul, ids, uzyte, bledy)
    uzyte |= fakty_w_napisach(korzen / "dane/napisy-interfejsu.yaml", ids)  # fakt cytowany w napisach nie jest sierotą
    uzyte |= fakty_w_formacie(korzen, ids)  # fakt cytowany w opisie formatu silnika też
    uzyte |= fakty_w_slowniczku(korzen / "dane/slowniczek.yaml", ids)  # fakt hasła słowniczka też
    bledy += bledy_slowniczka(korzen / "dane/slowniczek.yaml", ids)  # hasło ze złym kształtem albo faktem, którego nie ma
    for fid in sorted(ids - uzyte):
        bledy.append(f"Fakt „{fid}”: osierocony, nic się do niego nie odwołuje.")
    return bledy


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sprawdza treść przewodnika.")
    parser.add_argument("--korzen", default=".", type=Path)
    args = parser.parse_args(argv)
    bledy = sprawdz_tresc(args.korzen)
    for b in bledy:
        print(b)
    if bledy:
        print(f"Błędów: {len(bledy)}")
        return 1
    print("Treść poprawna.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
