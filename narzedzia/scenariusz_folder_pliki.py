"""Sprawdza pola ćwiczenia aplikacji `folder_startowy_dodatkowe` i `nowe_pliki`: ścieżki plików (dowolnej głębokości), które w folderze leżą od startu ponad `folder_startowy` albo które tworzy Claude."""

from narzedzia.scenariusz_drzewo import sciezka_ok


def dodatkowe(apl, sa, start, blad) -> set:
    """Pole `aplikacja.folder_startowy_dodatkowe`: pliki, które w tym ćwiczeniu leżą w folderze od startu ponad `folder_startowy`; zwraca poprawne nazwy."""
    if "folder_startowy_dodatkowe" not in apl:
        return set()
    lista = apl["folder_startowy_dodatkowe"]
    if not isinstance(lista, list) or not lista:
        blad(sa, "pole folder_startowy_dodatkowe musi być niepustą listą nazw plików")
        return set()
    dod = set()
    for i, nazwa in enumerate(lista):
        sn = f"{sa}/folder_startowy_dodatkowe[{i}]"
        if not sciezka_ok(nazwa):
            blad(sn, "plik dodatkowy wymaga ścieżki bez pustych członów, bez . i bez .. (np. Podfolder/plik albo .claude/skills/x/SKILL.md)")
        elif nazwa in start:
            blad(sn, f"plik „{nazwa}” już jest w folder_startowy scenariusza")
        elif nazwa in dod:
            blad(sn, f"plik „{nazwa}” powtórzony w folder_startowy_dodatkowe")
        else:
            dod.add(nazwa)
    return dod


def nowe_pliki(cw, s, start, blad, dodatkowe=frozenset(), przedrostek="") -> set:
    """Pole `nowe_pliki`: nazwy plików, których nie ma w `folder_startowy` (ani w `folder_startowy_dodatkowe` ćwiczenia), bo tworzy je Claude; zwraca poprawne nazwy.

    Nazwy liczą się od folderu rozmowy, a `start` i `dodatkowe` od korzenia podglądu, więc przed porównaniem nazwa dostaje `przedrostek` (ścieżka folderu rozmowy z `/`, w korzeniu pusty).
    """
    if "nowe_pliki" not in cw:
        return set()
    lista = cw["nowe_pliki"]
    if not isinstance(lista, list) or not lista:
        blad(s, "pole nowe_pliki musi być niepustą listą nazw plików")
        return set()
    nowe = set()
    for i, nazwa in enumerate(lista):
        sn = f"{s}/nowe_pliki[{i}]"
        if not sciezka_ok(nazwa):
            blad(sn, "nowy plik wymaga ścieżki od folderu rozmowy: niepusty napis bez pustych członów, bez . i bez .. (np. raport.csv albo .claude/skills/x/SKILL.md)")
        elif przedrostek + nazwa in start:
            blad(sn, f"nowy plik „{nazwa}” już jest w folder_startowy")
        elif przedrostek + nazwa in dodatkowe:
            blad(sn, f"nowy plik „{nazwa}” już jest w folder_startowy_dodatkowe tego ćwiczenia")
        elif nazwa in nowe:
            blad(sn, f"nowy plik „{nazwa}” powtórzony w nowe_pliki")
        else:
            nowe.add(nazwa)
    return nowe
