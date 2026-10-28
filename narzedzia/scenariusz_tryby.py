"""Sprawdza ćwiczenie aplikacji z listą `etapy` (albo z drogami etapów w tej liście): przełącznik i menu trybu, kartę zgody w trybie Manual, zmianę bez karty w trybie Accept edits albo Auto, licznik, krok folderu i kartę planu (opis: dane/FORMAT-SCENARIUSZA-TRYBY.md i FORMAT-SCENARIUSZA.md)."""

import re

from narzedzia.scenariusz_plan import krok_planu
from narzedzia.scenariusz_tryby_folder import krok_folderu, plik_zmiany, stan_folderu
from narzedzia.scenariusz_aplikacja import (
    GDZIE,
    MAKS_MS,
    SRODOWISKA,
    TRYBY_APLIKACJI,
    _napis,
    _niepusty,
    _rozmowa,
    _zmiany,
    licznik,
)

KLIKI_ETAPU = ("zatwierdz", "przelacznik", "tryb", "licznik")
TYPY_KROKU = ("pisz", "mysli", "claude", "zgoda", "zmiana", "folder", "nauczyciel", "plan")
MANUAL = "Manual"
AUTO = "Auto"
BEZ_PYTANIA = ("Accept edits", AUTO)  # tryby, w których Claude stosuje zmiany sam
POLA_DROGI = ("id", "etykieta", "opis", "tryb", "etapy", "fakt")
ID_DROGI = re.compile(r"[\w-]+")  # jak znacznik `<!-- podglad: cw id -->` w narzedzia/strona.py


def _aplikacja(apl, sa, napisy, fakt, blad) -> bool:
    """Obiekt `aplikacja` ćwiczenia z etapami; zwraca, czy tryb Auto jest w menu (pole `auto_dostepny`, domyślnie tak)."""
    _napis(apl.get("srodowisko"), SRODOWISKA, sa, "srodowisko", napisy, blad)
    _napis(apl.get("tryb"), TRYBY_APLIKACJI, sa, "tryb", napisy, blad)
    folder = apl.get("folder")
    if not _niepusty(folder) or "/" in folder or folder.startswith("~"):
        blad(sa, "aplikacja wymaga pola folder (sama nazwa folderu, bez / i ~)")
    if apl.get("rozmowa"):  # rozmowa może być pusta: pierwszą prośbę pisze etap
        _rozmowa(apl["rozmowa"], sa, fakt, blad)
    elif "rozmowa" in apl and apl["rozmowa"] != []:
        blad(sa, "rozmowa musi być listą wiadomości")
    if "zmiany" in apl:
        blad(
            sa,
            "ćwiczenie z etapami nie ma pola zmiany: licznik liczy się z zatwierdzonej karty zgody",
        )
    if "panel" in apl:
        blad(
            sa,
            "ćwiczenie z etapami nie ma pola panel: licznik po zatwierdzeniu stoi na karcie Changes w panelu",
        )
    auto = apl.get("auto_dostepny", True)
    if not isinstance(auto, bool):
        blad(sa, "pole auto_dostepny musi być prawdą albo fałszem")
        auto = True
    if not auto and apl.get("tryb") == AUTO:
        blad(
            sa,
            "tryb startowy Auto, a auto_dostepny: false (fakt aplikacja-dostepne-tryby)",
        )
    return auto


def _zgoda(k, sk, stan, napisy, blad) -> None:
    """Karta zgody: tylko w trybie Manual, tylko edycja pliku z folder_startowy, jedna na ćwiczenie."""
    if stan["tryb"] != MANUAL:
        blad(sk, f"karta zgody tylko w trybie Manual (teraz „{stan['tryb']}”)")
    if stan["zgody"]:
        blad(
            sk,
            "druga karta zgody: licznika po drugiej zmianie nie podaje żaden fakt"
            if not stan["bez_karty"]
            else "karta zgody po zmianie z licznikiem: licznika po drugiej zmianie nie podaje żaden fakt",
        )
    plik = k.get("plik")
    plik_zmiany(plik, sk, stan["folder"], "karta zgody pokazuje tylko edycję istniejącego pliku", blad)
    _licznik_zmiany([{"plik": plik, "linijki": k.get("linijki")}], sk, napisy, blad)
    stan["czeka"] = True
    stan["zgody"] += 1


def _licznik_zmiany(zmiana, sk, napisy, blad, pole=None) -> None:
    """Pliki zmiany z co najmniej jedną linijką zmiany i licznik „+N -M” zgodny ze wzorem z listy napisów; `pole` to nazwa pola kroku z plikami, którą mają wskazywać komunikaty."""
    if pole:
        def blad_pola(sciezka, tekst):
            blad(
                sciezka.replace(f"{sk}/zmiany[", f"{sk}/{pole}["),
                tekst.replace("plik zmiany", f"plik w polu {pole}"),
            )

        _zmiany(zmiana, sk, blad_pola)
    else:
        _zmiany(zmiana, sk, blad)
    napis = licznik(zmiana)
    if not napisy.jest(napis, GDZIE):
        blad(
            sk,
            f"licznik „{napis}” nie pasuje do wzoru z listy napisów interfejsu aplikacji",
        )


def _zmiana(k, sk, stan, napisy, blad) -> None:
    """Zmiana bez karty: tylko w trybie Accept edits albo Auto, tylko pliki z folder_startowy, jedna zmiana z licznikiem na ćwiczenie."""
    if stan["tryb"] not in BEZ_PYTANIA:
        blad(
            sk,
            f"zmiana bez karty tylko w trybie Accept edits albo Auto (teraz „{stan['tryb']}”): w trybie Manual i Plan Claude nie stosuje zmian sam",
        )
    if stan["zgody"]:
        blad(
            sk,
            "druga zmiana z licznikiem (po karcie zgody albo po innej zmianie): licznika po drugiej zmianie nie podaje żaden fakt",
        )
    pliki = k.get("pliki")
    if not isinstance(pliki, list) or not pliki:
        blad(sk, "zmiana wymaga niepustej listy pliki")
        return
    nazwy = [p["plik"] for p in pliki if isinstance(p, dict) and isinstance(p.get("plik"), str)]  # inny typ zgłasza _zmiany
    for nazwa in nazwy:
        plik_zmiany(nazwa, sk, stan["folder"], "zmiana dotyczy tylko istniejącego pliku", blad)
    if len(set(nazwy)) != len(nazwy):
        blad(sk, "ten sam plik dwa razy w jednej zmianie: połącz linijki w jednym wpisie")
    _licznik_zmiany(pliki, sk, napisy, blad, "pliki")
    stan["zgody"] += 1
    stan["bez_karty"] = True


def _krok(k, sk, stan, napisy, fakt, blad) -> None:
    typ = k.get("typ")
    if typ not in TYPY_KROKU:
        blad(sk, f"typ „{typ}” spoza {'/'.join(TYPY_KROKU)}")
        return
    fakt(k, sk)
    if stan["menu"] and typ != "nauczyciel":
        blad(sk, f"krok {typ} przy otwartym menu trybu: najpierw etap z klik „tryb”")
    if stan["czeka"] and typ != "nauczyciel":
        blad(
            sk,
            f"krok {typ}, gdy karta zgody czeka: Claude czeka na zatwierdzenie (fakt tryb-manual-aplikacja-czeka-na-zatwierdzenie)",
        )
    if typ in ("pisz", "claude", "nauczyciel") and not _niepusty(k.get("tekst")):
        blad(sk, f"krok {typ} wymaga niepustego pola tekst")
    if typ == "mysli":
        if "tekst" in k:
            blad(
                sk,
                "mysli bez tekstu: dokumentacja aplikacji nie podaje napisu przy pracy Claude",
            )
        if "ms" in k and (type(k["ms"]) is not int or not 0 < k["ms"] <= MAKS_MS):
            blad(sk, f"ms musi być liczbą całkowitą od 1 do {MAKS_MS}")
    elif typ == "zgoda":
        _zgoda(k, sk, stan, napisy, blad)
    elif typ == "zmiana":
        _zmiana(k, sk, stan, napisy, blad)
    elif typ == "folder":
        krok_folderu(k, sk, stan["folder"], blad, stan["tryb"], BEZ_PYTANIA)
    elif typ == "plan":  # kroki przycisków karty: jak kroki etapu, od trybu po kliknięciu
        krok_planu(k, sk, stan, blad, lambda kr, s, st: _kroki(kr, s, st, napisy, fakt, blad))


def _kroki(kroki, s, stan, napisy, fakt, blad) -> bool:
    """Kroki etapu albo przycisku karty planu; krok `plan` kończy listę (dalej grają kroki z przycisków). Zwraca, czy lista ma krok `plan`."""
    for j, k in enumerate(kroki):
        if not isinstance(k, dict):
            blad(f"{s}/kroki[{j}]", "krok musi być obiektem")
            continue
        _krok(k, f"{s}/kroki[{j}]", stan, napisy, fakt, blad)
        if k.get("typ") == "plan" and j < len(kroki) - 1:
            blad(f"{s}/kroki[{j}]", "krok plan kończy listę kroków: dalej grają kroki z przycisków karty")
    return any(isinstance(k, dict) and k.get("typ") == "plan" for k in kroki)


def _klik(e, se, stan, auto, napisy, blad) -> None:
    """Klik etapu: zatwierdzenie karty zgody, otwarcie menu kliknięciem przełącznika, wybór trybu w menu albo kliknięcie licznika zmian."""
    klik = e.get("klik")
    if "na" in e and klik != "tryb":
        blad(se, "pole na tylko przy klik „tryb”")
    if klik is None:
        return
    if klik not in KLIKI_ETAPU:
        blad(se, f"klik „{klik}” spoza {'/'.join(KLIKI_ETAPU)}")
    elif klik == "zatwierdz":
        if not stan["czeka"]:
            blad(se, "zatwierdzenie bez karty zgody, która czeka na decyzję")
        stan["czeka"] = False
    elif klik == "przelacznik":
        if stan["menu"]:
            blad(se, "menu trybu jest już otwarte")
        if stan["czeka"]:
            blad(se, "zmiana trybu, gdy karta zgody czeka: dokumentacja nie opisuje takiego zachowania")
        stan["menu"] = True
    elif klik == "licznik":
        if not stan["zgody"] or stan["czeka"]:
            blad(
                se,
                "licznik bez zmiany: liczby +N -M są dopiero po zatwierdzonej karcie zgody albo po kroku zmiana",
            )
        if stan["menu"]:
            blad(se, "kliknięcie licznika przy otwartym menu trybu: najpierw etap z klik „tryb”")
    else:
        na = e.get("na")
        if not stan["menu"]:
            blad(
                se, "wybór trybu bez otwartego menu: najpierw etap z klik „przelacznik”"
            )
        _napis(na, TRYBY_APLIKACJI, se, "na", napisy, blad)
        if na == AUTO and not auto:
            blad(
                se,
                "Auto nie ma w menu, gdy auto_dostepny: false (fakt aplikacja-dostepne-tryby)",
            )
        elif na == stan["tryb"]:
            blad(se, f"tryb „{na}” już jest wybrany")
        stan["tryb"], stan["menu"] = na, False


def _etapy(etapy, s, stan, auto, napisy, fakt, blad, droga=False) -> None:
    """Lista etapów od stanu `stan`; w drodze (`droga`) pierwszy etap gra się po kliknięciu drogi, więc nie potrzebuje etykiety."""
    for i, e in enumerate(etapy):
        se = f"{s}/etapy[{i}]"
        if not isinstance(e, dict):
            blad(se, "etap musi być obiektem")
            continue
        if "etapy" in e:
            blad(se, "etap nie ma pola etapy: drogi się nie zagnieżdżają")
        if not (droga and i == 0 and "etykieta" not in e) and not _niepusty(e.get("etykieta")):
            blad(se, "etap wymaga niepustego pola etykieta")
        if "opis" in e and not _niepusty(e["opis"]):
            blad(se, "pole opis musi być niepustym napisem")
        fakt(e, se)
        _klik(e, se, stan, auto, napisy, blad)
        kroki = e.get("kroki", [])
        if not isinstance(kroki, list) or ("klik" not in e and not kroki):
            blad(
                se,
                "etap bez klik wymaga niepustej listy kroki (lista kroki zawsze jest listą)",
            )
            continue
        if _kroki(kroki, se, stan, napisy, fakt, blad) and i < len(etapy) - 1:
            blad(se, "po etapie z kartą planu nie ma dalszych etapów: dalej grają kroki z przycisków karty")
    if stan["menu"]:
        blad(
            s,
            "menu trybu zostaje otwarte: po etapie z klik „przelacznik” musi przyjść etap z klik „tryb”",
        )


def _stan(tryb, pliki) -> dict:
    """Stan na początku drogi (albo ćwiczenia): tryb startowy, zamknięte menu, brak zmian i folder z `folder_startowy`."""
    return {"tryb": tryb, "menu": False, "czeka": False, "zgody": 0, "bez_karty": False, "folder": stan_folderu(pliki)}


def _drogi(drogi, s, auto, pliki, napisy, fakt, blad) -> None:
    """Drogi etapów: lista `etapy` złożona z dróg (`id`, `etykieta`, `opis`?, `tryb`, `etapy`); każda droga startuje od trybu drogi i folderu z `folder_startowy`."""
    if len(drogi) < 2:
        blad(s, "drogi etapów to co najmniej dwie drogi (jedna droga to zwykła lista etapy)")
    id_drog = set()
    for i, d in enumerate(drogi):
        sd = f"{s}/etapy[{i}]"
        if not isinstance(d, dict) or "etapy" not in d:
            blad(sd, "lista etapy miesza drogi i etapy: wszystkie pozycje mają mieć pole etapy albo żadna")
            continue
        for pole in d:
            if pole not in POLA_DROGI:
                blad(sd, f"pole {pole} nie należy do drogi (pola: {', '.join(POLA_DROGI)})")
        id_drogi = d.get("id")
        if not isinstance(id_drogi, str) or not ID_DROGI.fullmatch(id_drogi):
            blad(sd, "droga wymaga pola id: litery, cyfry, _ i - (po nim idzie znacznik podglądu w lekcji)")
        elif id_drogi in id_drog:
            blad(sd, f"id drogi „{id_drogi}” powtórzone w ćwiczeniu")
        id_drog.add(id_drogi)
        if not _niepusty(d.get("etykieta")):
            blad(sd, "droga wymaga niepustego pola etykieta")
        if "opis" in d and not _niepusty(d["opis"]):
            blad(sd, "pole opis musi być niepustym napisem")
        tryb = d.get("tryb")
        _napis(tryb, TRYBY_APLIKACJI, sd, "tryb", napisy, blad)
        if tryb == AUTO and not auto:
            blad(sd, "tryb drogi Auto, a auto_dostepny: false (fakt aplikacja-dostepne-tryby)")
        fakt(d, sd)
        if not isinstance(d["etapy"], list) or not d["etapy"]:
            blad(sd, "droga wymaga niepustej listy etapy")
            continue
        _etapy(d["etapy"], sd, _stan(tryb, pliki), auto, napisy, fakt, blad, droga=True)


def sprawdz_tryby(cw: dict, s: str, napisy, fakt, blad, pliki=()) -> None:
    """Ćwiczenie `aplikacja` z listą `etapy` (zamiast `kroki` i `drogi`): zwykłe etapy albo drogi etapów; `pliki` to nazwy z `folder_startowy`."""
    apl = cw.get("aplikacja")
    if not isinstance(apl, dict):
        blad(s, "rodzaj aplikacja wymaga obiektu aplikacja")
        apl = {}
    auto = _aplikacja(apl, f"{s}/aplikacja", napisy, fakt, blad)
    for pole in ("kroki", "drogi", "nowe_pliki"):
        if pole in cw:
            blad(s, f"ćwiczenie z etapami nie ma pola {pole}")
    etapy = cw.get("etapy")
    if not isinstance(etapy, list) or not etapy:
        blad(s, "pole etapy musi być niepustą listą")
        return
    if any(isinstance(e, dict) and "etapy" in e for e in etapy):
        return _drogi(etapy, s, auto, pliki, napisy, fakt, blad)
    _etapy(etapy, s, _stan(apl.get("tryb"), pliki), auto, napisy, fakt, blad)
