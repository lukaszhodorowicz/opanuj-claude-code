"""Sprawdza w drogach symulatora aplikacji folder każdej rozmowy: pole `aplikacja.id` (id rozmowy startowej), `sesje[].folder`, klik `folder` (wybór teczki w nowej rozmowie przed pierwszą prośbą) i ścieżki plików liczone od folderu otwartej rozmowy (opis: dane/FORMAT-SCENARIUSZA.md, część „Folder każdej rozmowy i karta wiadomości”)."""

import re

FAKT_ROZMOWY = "aplikacja-kazda-rozmowa-to-sesja"
FAKT_WYBORU = "aplikacja-rzad-pod-polem-srodowisko-folder-tryb-model"
FAKT_POWROTU = "aplikacja-powrot-do-sesji-klik-w-pasku-bocznym"


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


def _wiersze(apl: dict) -> list:
    wiersze = apl.get("sesje") if isinstance(apl, dict) else None
    return [w for w in wiersze if isinstance(w, dict)] if isinstance(wiersze, list) else []


def jest(apl: dict) -> bool:
    """Ćwiczenie ma folder każdej rozmowy: choć jeden wiersz `aplikacja.sesje` ma pole `folder`."""
    return any("folder" in w for w in _wiersze(apl))


def przedrostek(folder, glowny) -> str:
    """Ścieżka folderu rozmowy od korzenia podglądu, z `/` na końcu; korzeń (`folder_glowny`) daje pusty napis."""
    return "" if not _niepusty(glowny) or folder == glowny else f"{folder}/"


def pole(apl: dict, sa: str, blad) -> None:
    """`aplikacja.id` (id rozmowy startowej, wzór `^[a-z0-9-]+$`, niepowtarzalne z `sesje[].id`, tylko z listą `sesje`) i `sesje[].folder` (sama nazwa folderu; wszystkie wiersze albo żaden)."""
    wiersze = _wiersze(apl)
    if "id" in apl:
        if "sesje" not in apl:
            blad(sa, f"id rozmowy startowej tylko w ćwiczeniu z aplikacja.sesje: klik sesja wraca do niej po tym id (fakt {FAKT_POWROTU})")
        elif not isinstance(apl["id"], str) or not re.fullmatch(r"[a-z0-9-]+", apl["id"]):
            blad(sa, "aplikacja.id musi pasować do ^[a-z0-9-]+$")
        elif apl["id"] in {w.get("id") for w in wiersze}:
            blad(sa, f"aplikacja.id „{apl['id']}” powtórzone w aplikacja.sesje")
    if not jest(apl):
        return
    for i, w in enumerate(wiersze):
        sw = f"{sa}/sesje[{i}]"
        if "folder" not in w:
            blad(sw, f"wiersz bez pola folder, gdy inne wiersze je mają: każda rozmowa ma własny folder (fakt {FAKT_ROZMOWY})")
        elif not _niepusty(w["folder"]) or "/" in w["folder"] or w["folder"].startswith("~"):
            blad(sw, "folder wiersza to sama nazwa folderu (korzeń albo teczka podglądu), bez / i ~")


def foldery(apl: dict, sa: str, uklad, glowny, blad) -> None:
    """Folder każdego wiersza to korzeń podglądu (`folder_glowny`) albo teczka z plikami od startu; bez `folder_glowny` folder każdej rozmowy nie ma sensu (teczek nie ma)."""
    if not jest(apl):
        return
    if not _niepusty(glowny):
        blad(sa, "folder każdej rozmowy wymaga folder_glowny: korzenia podglądu, w którym leżą teczki rozmów")
        return
    mozliwe = dozwolone(glowny, uklad)
    for i, w in enumerate(_wiersze(apl)):
        if _niepusty(w.get("folder")) and w["folder"] not in mozliwe:
            blad(f"{sa}/sesje[{i}]", f"folder „{w['folder']}” musi być korzeniem podglądu albo teczką z plikami od startu: {mozliwe}")


def dozwolone(glowny, uklad) -> list:
    """Foldery, które może mieć rozmowa: korzeń podglądu (`folder_glowny`) i teczki z plikami od startu."""
    return [glowny, *sorted(t for t in uklad.teczki if "/" not in t)] if _niepusty(glowny) and uklad is not None else []


def stan(apl: dict, glowny, uklad) -> dict:
    """Klucze stanu drogi: `e1` (folder każdej rozmowy), `foldery` (folder rozmowy startowej pod kluczem None i każdego wiersza pod jego id), `glowny`, `teczki` (foldery do wyboru w kliku `folder`) i `folder_nowej` (folder nowej rozmowy: na początku folder rozmowy startowej)."""
    mapa = {None: apl.get("folder") if isinstance(apl, dict) else None}
    mapa.update({w["id"]: w.get("folder") for w in _wiersze(apl) if isinstance(w.get("id"), str)})
    return {"e1": jest(apl), "foldery": mapa, "glowny": glowny, "teczki": dozwolone(glowny, uklad), "folder_nowej": mapa[None]}


def otwarto(st: dict) -> None:
    """Po zmianie otwartej rozmowy (`nowa-rozmowa`, `sesja`, `wiadomosc-od`, `folder`): ścieżki widoczne dla kursanta liczą się od folderu tej rozmowy."""
    s = st["sesje"]
    if not s["e1"]:
        return
    folder = s["folder_nowej"] if s["otwarta"] == "nowa" else s["foldery"].get(s["otwarta"])
    st["przedrostek"] = przedrostek(folder, s["glowny"])


def klik(k: dict, sk: str, st: dict, blad) -> None:
    """Klik `folder` z polem `folder: <teczka>`: tylko w ćwiczeniu z folderem każdej rozmowy, w nowej rozmowie przed pierwszą prośbą, na teczkę inną niż bieżąca (fakt: folder wybierasz przed pierwszą wiadomością)."""
    s = st["sesje"]
    wybrany = k.get("folder")
    if not s["e1"]:
        blad(sk, f"klik folder tylko w ćwiczeniu z folderem każdej rozmowy (aplikacja.sesje[].folder): bez niego żaden wiersz nie ma własnego folderu (fakt {FAKT_ROZMOWY})")
    elif s["otwarta"] != "nowa" or not s["pusta"]:
        blad(sk, f"klik folder poza nową rozmową przed pierwszą prośbą: folder wybierasz w rzędzie pod polem, zanim wyślesz pierwszą wiadomość (fakt {FAKT_WYBORU})")
    elif not _niepusty(wybrany):
        blad(sk, "klik folder wymaga pola folder z nazwą teczki")
    elif wybrany == s["folder_nowej"]:
        blad(sk, f"klik folder na teczkę „{wybrany}”, która jest już folderem nowej rozmowy: kliknięcie niczego by nie zmieniło")
    elif wybrany not in s["teczki"]:
        blad(sk, f"klik folder: teczka „{wybrany}” spoza korzenia i teczek podglądu {s['teczki']}")
    else:
        s["folder_nowej"] = wybrany
        otwarto(st)


def widoczne(pliki, przed: str) -> set:
    """Nazwy plików tak, jak widzi je kursant w rozmowie o folderze `przed`: od tego folderu; pliki spoza niego nie mają takiej nazwy."""
    return {p[len(przed):] for p in pliki if p.startswith(przed)}


def widoczne_wszedzie(uklad, glowny) -> set:
    """Nazwy plików tak, jak widzi je kursant w którejkolwiek rozmowie ćwiczenia (od jej folderu): suma nazw dla korzenia i każdej teczki."""
    wynik = set()
    for folder in dozwolone(glowny, uklad):
        wynik |= widoczne(uklad.pliki | uklad.nowe, przedrostek(folder, glowny))
    return wynik
