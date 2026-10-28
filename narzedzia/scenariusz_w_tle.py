"""Sprawdza w drogach symulatora aplikacji pracę w tle: pole `w_tle` (lista prac) i `w_tle_koniec` kroku `claude`, kliki `menu-paska`, `background-tasks` i `wpis-w-tle` (odnośnik „N running tasks” w rozmowie jest tylko narysowany, nieaktywny: nie ma celu `running-tasks`) oraz kolejność kroków wokół menu ⋮, panelu zadań w tle i panelu subagenta (opis: dane/FORMAT-SCENARIUSZA.md, część „Praca w tle: menu ⋮, panel zadań i panel subagenta”)."""

GDZIE = "aplikacja"
KLIKI = ("menu-paska", "background-tasks", "wpis-w-tle")
RODZAJE = ("subagent", "przeplyw")  # rodzaj pracy w tle; zadanie i wynik w panelu subagenta ma tylko subagent
MAKS_WPISOW = 6  # prac w tle w jednej drodze (panel ma wtedy sześć kart)
MAKS_LINIJEK_WYNIKU = 6
POLA_W_TLE = ("rodzaj", "tytul", "zadanie", "wynik")
MIN_NA_ODNOSNIK = 2  # odnośnik „N running tasks” stoi przy co najmniej dwóch pracach w tle (wzór napisu: liczba od 2, formy dla jednej żaden zrzut nie pokazuje)
MAKS_TYTUL = 80
MAKS_ZADANIE = 400
POLA_KLIKU = {
    "menu-paska": ("typ", "cel", "fakt"),
    "background-tasks": ("typ", "cel", "fakt"),
    "wpis-w-tle": ("typ", "cel", "nr", "fakt"),
}
PANELE_WYPIERAJACE = ("plik", "artefakt", "strona")  # kroki, które zajmują miejsce panelu zadań w tle (jak panel pytania z boku)
FAKT_PRACY = "aplikacja-panel-zadan-w-tle-co-pokazuje"
FAKT_MENU = "aplikacja-menu-paska-panele-bez-przycisku"
FAKT_WPISU = "aplikacja-wpis-w-tle-wynik-w-panelu-subagenta"
FAKT_ODNOSNIKA = "aplikacja-link-running-tasks-w-rozmowie"


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


def stan(apl: dict) -> dict:
    """Klucze stanu drogi: `w_tle` (prace w tle w kolejności kroków: rodzaje), `w_tle_menu` (menu ⋮ otwarte), `w_tle_panel` (None, „zadania” albo „subagent”: co stoi w miejscu otwartego pliku), `w_tle_koniec` (Claude podał już wynik pracy w tle), `w_tle_plik` (po tym kroku stanął krok `plik`: panel nie zostaje otwarty po końcu pracy) i `w_tle_sesje` (ćwiczenie ma pasek boczny z rozmowami)."""
    return {"w_tle": [], "w_tle_menu": False, "w_tle_panel": None, "w_tle_koniec": False, "w_tle_plik": False, "w_tle_sesje": isinstance(apl, dict) and "sesje" in apl}


def kolejnosc(k: dict, sk: str, st: dict, blad) -> None:
    """Przed każdym krokiem drogi: przy otwartym menu ⋮ dalej tylko `nauczyciel` i klik „background-tasks” (menu stoi, dopóki kursant nie wybierze pozycji); `plik`, `artefakt`, `strona` i `/btw` zajmują miejsce panelu (Z16: panel nie otwiera się sam ponownie)."""
    typ = k.get("typ")
    if st["w_tle_menu"] and typ != "nauczyciel" and not (typ == "klik" and k.get("cel") == "background-tasks"):
        blad(sk, f"krok {typ} przy otwartym menu ⋮: dalej tylko nauczyciel i klik „background-tasks” (menu stoi, dopóki kursant nie wybierze pozycji; fakt {FAKT_MENU})")
    if typ in PANELE_WYPIERAJACE or (typ == "komenda" and k.get("tekst") == "/btw"):
        st["w_tle_panel"] = None
    if typ == "plik" and st["w_tle_koniec"]:
        st["w_tle_plik"] = True


def claude(k: dict, sk: str, st: dict, napisy, blad) -> None:
    """Pola `w_tle` (lista nowych prac w tle) i `w_tle_koniec: true` (Claude podaje wynik pracy w tle) kroku `claude`; jeden krok nie ma obu naraz."""
    if st["w_tle_sesje"]:
        blad(sk, "w_tle w ćwiczeniu z aplikacja.sesje: zmiana rozmowy nie ma opisanego skutku dla panelu zadań w tle (nie łączymy)")
    if "w_tle" in k and "w_tle_koniec" in k:
        blad(sk, "w_tle i w_tle_koniec w jednym kroku: Claude albo zleca pracę w tle, albo podaje jej wynik")
    if "w_tle" in k:
        _w_tle(k["w_tle"], sk, st, napisy, blad)
    if "w_tle_koniec" in k:
        if k["w_tle_koniec"] is not True:
            blad(sk, "w_tle_koniec musi być prawdą (true) albo nie występować")
        elif not st["w_tle"]:
            blad(sk, f"w_tle_koniec bez wcześniejszej pracy w tle (krok claude z polem w_tle): Claude nie ma czego podać (fakt {FAKT_PRACY})")
        st["w_tle_koniec"] = True


def _w_tle(lista, sk: str, st: dict, napisy, blad) -> None:
    """`w_tle`: niepusta lista prac; po zleceniu przy co najmniej dwóch pracach pod odpowiedzią stoi odnośnik „N running tasks”, którego napis musi pasować do wzoru z listy napisów."""
    if st["w_tle_koniec"]:
        blad(sk, "w_tle po kroku z w_tle_koniec: po wyniku pracy w tle nie dokładamy nowej (stan po zakończeniu nie ma źródła)")
    if not isinstance(lista, list) or not lista:
        blad(sk, "w_tle musi być niepustą listą prac {rodzaj, tytul, zadanie, wynik}")
        return
    for i, w in enumerate(lista):
        _wpis_w_tle(w, f"{sk}/w_tle[{i}]", blad)
        if isinstance(w, dict):
            st["w_tle"].append(w)
    if len(st["w_tle"]) > MAKS_WPISOW:
        blad(sk, f"w_tle: najwyżej {MAKS_WPISOW} prac w tle w jednej drodze")
    n = len(st["w_tle"])
    odnosnik = f"{n} running tasks"
    if n >= MIN_NA_ODNOSNIK and napisy is not None and not napisy.jest(odnosnik, GDZIE):
        blad(sk, f"odnośnik „{odnosnik}” pod odpowiedzią nie pasuje do wzoru z listy napisów interfejsu aplikacji (fakt {FAKT_ODNOSNIKA})")


def _tekst(w: dict, pole: str, maks: int, sw: str, blad) -> None:
    wartosc = w.get(pole)
    if not _niepusty(wartosc):
        blad(sw, f"{pole} musi być niepustym napisem")
    elif len(wartosc) > maks or any(ord(c) < 32 for c in wartosc):
        blad(sw, f"{pole}: najwyżej {maks} znaków i bez znaków sterujących")


def _wpis_w_tle(w, sw: str, blad) -> None:
    """Jedna praca: `rodzaj`, `tytul` (tytuł zadania na karcie i w nagłówku panelu subagenta); subagent ma też `zadanie` (treść, którą napisał Claude) i `wynik` (lista niepustych linijek), przepływ ich nie ma (dokumentacja nie mówi, co pokazuje klik w taki wpis)."""
    if not isinstance(w, dict):
        blad(sw, "praca w tle musi być obiektem {rodzaj, tytul, zadanie, wynik}")
        return
    for p in w:
        if p not in POLA_W_TLE:
            blad(sw, f"pole {p} nie należy do w_tle (pola: {', '.join(POLA_W_TLE)})")
    rodzaj = w.get("rodzaj")
    if rodzaj not in RODZAJE:
        blad(sw, f"rodzaj „{rodzaj}” spoza {'/'.join(RODZAJE)}")
        return
    _tekst(w, "tytul", MAKS_TYTUL, sw, blad)
    if rodzaj == "przeplyw":
        for p in ("zadanie", "wynik"):
            if p in w:
                blad(sw, f"{p} tylko przy rodzaju subagent: dla przepływu dokumentacja nie opisuje, co pokazuje klik we wpis")
        return
    _tekst(w, "zadanie", MAKS_ZADANIE, sw, blad)
    wynik = w.get("wynik")
    if not isinstance(wynik, list) or not 1 <= len(wynik) <= MAKS_LINIJEK_WYNIKU or not all(_niepusty(l) for l in wynik):
        blad(sw, f"wynik subagenta musi być listą 1-{MAKS_LINIJEK_WYNIKU} niepustych linijek (fakt {FAKT_WPISU})")


def klik(k: dict, sk: str, st: dict, blad) -> None:
    """Klik `menu-paska` (otwiera menu ⋮), `background-tasks` (otwiera panel zadań w tle) i `wpis-w-tle` (otwiera panel subagenta z wynikiem)."""
    cel = k["cel"]
    for p in k:
        if p not in POLA_KLIKU[cel]:
            blad(sk, f"pole {p} nie należy do kliku {cel} (pola: {', '.join(POLA_KLIKU[cel])})")
    if st["w_tle_koniec"]:
        blad(sk, f"klik {cel} po kroku z w_tle_koniec: po wyniku pracy w tle panel nie otwiera się ponownie, jego miejsce zajmuje plik (stan po zakończeniu nie ma źródła)")
    if cel == "menu-paska":
        _menu_paska(sk, st, blad)
    elif cel == "background-tasks":
        if not st["w_tle_menu"]:
            blad(sk, f"klik background-tasks bez otwartego menu ⋮: najpierw klik menu-paska (fakt {FAKT_MENU})")
        st["w_tle_menu"] = False
        st["w_tle_panel"] = "zadania"
    else:
        _wpis(k, sk, st, blad)


def _menu_paska(sk: str, st: dict, blad) -> None:
    if not st["w_tle"]:
        blad(sk, f"klik menu-paska przed pierwszą pracą w tle: pozycja Background tasks pojawia się w menu dopiero, gdy rozmowa ma pracę w tle, a ⋮ zostaje do tej pory nieaktywny (fakty {FAKT_MENU}, {FAKT_PRACY})")
    if st["w_tle_menu"]:
        blad(sk, "klik menu-paska przy menu, które jest już otwarte")
    if st["w_tle_panel"] == "zadania":
        blad(sk, "klik menu-paska przy otwartym panelu zadań w tle: panel już stoi obok rozmowy")
    st["w_tle_menu"] = True


def _wpis(k: dict, sk: str, st: dict, blad) -> None:
    """`wpis-w-tle`: tylko przy otwartym panelu zadań; `nr` (od 1) wskazuje istniejący wpis rodzaju subagent."""
    nr, wpisy = k.get("nr"), st["w_tle"]
    if st["w_tle_panel"] != "zadania":
        blad(sk, f"klik wpis-w-tle bez otwartego panelu zadań w tle: najpierw klik background-tasks (fakt {FAKT_PRACY})")
    if type(nr) is not int or not 1 <= nr <= len(wpisy):
        blad(sk, f"wpis-w-tle: nr musi być liczbą całkowitą od 1 do {len(wpisy)} (liczba prac w tle w tej chwili), jest {nr!r}")
    elif wpisy[nr - 1].get("rodzaj") != "subagent":
        blad(sk, f"wpis-w-tle: wpis {nr} to {wpisy[nr - 1].get('rodzaj')}, a panel subagenta ma tylko subagent (fakt {FAKT_WPISU})")
    st["w_tle_panel"] = "subagent"


def koniec(sd: str, st: dict, blad) -> None:
    """Droga nie kończy się otwartym menu ⋮ (kursant nie wybrał pozycji), a po kroku z `w_tle_koniec` stoi krok `plik` (panel zadań, który stał, zajmuje plik; bez niego zostałby otwarty po końcu pracy)."""
    if st["w_tle_menu"]:
        blad(sd, "droga kończy się otwartym menu ⋮: dodaj klik background-tasks")
    if st["w_tle_koniec"] and not st["w_tle_plik"]:
        blad(sd, f"droga ma krok z w_tle_koniec, ale po nim nie ma kroku plik: panel zadań w tle zostałby otwarty po końcu pracy (fakt {FAKT_PRACY})")
