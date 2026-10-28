"""Sprawdza w drogach symulatora aplikacji ekrany ze zrzutów Łukasza z 27.10.2026 (paczka 4): menu „…” panelu otwartego pliku (klik `plik-menu`), kartę pliku w rozmowie (pole `karta_pliku` kroku `claude`) z menu prawego kliku (kliki `plik-karta-menu` i `plik-karta-pozycja`) oraz dymek pierwszej ikony paska tytułu (klik `ikona-tytulu`); opis: dane/FORMAT-SCENARIUSZA.md, część „Panel pliku, menu pliku i dymki paska tytułu”."""

GDZIE = "aplikacja"
KLIKI = ("plik-menu", "plik-karta-menu", "plik-karta-pozycja", "ikona-tytulu")
POLA_KLIKU = {
    "plik-menu": ("typ", "cel", "fakt"),
    "plik-karta-menu": ("typ", "cel", "fakt"),
    "plik-karta-pozycja": ("typ", "cel", "pozycja", "fakt"),
    "ikona-tytulu": ("typ", "cel", "nr", "fakt"),
}
POZYCJE_KARTY = ("Attach as context", "Copy", "Open in", "Show in Finder")  # menu prawego kliku na karcie pliku, zrzut 15-27-51
DYMKI_PASKA = {1: "Show session rail"}  # dymki ikon paska tytułu: jedyny, który pokazuje zrzut 15-28-18 (pierwsza ikona)
RODZAJE_KARTY = {".txt": "TXT"}  # znaczek rodzaju pliku na karcie: tylko „TXT” ze zrzutu 15-27-18
MAKS_ROZMIAR = 999  # rozmiar na karcie w postaci „NB” (bajty); większych jednostek żaden zrzut nie pokazuje
PRZY_MENU = ("nauczyciel",)  # krok dozwolony przy otwartym menu poza kliknięciem pozycji menu karty
ZAMYKAJA_PANEL = ("artefakt", "strona")  # kroki, które zajmują miejsce otwartego pliku w panelu
KLIKI_ZAMYKAJACE_PANEL = ("background-tasks", "wpis-w-tle")  # panel zadań w tle i panel subagenta stają w miejscu pliku


def stan(apl: dict) -> dict:
    """Klucz stanu drogi `plik_ekran`: `plik` (w panelu stoi plik z linijkami, a nie strona), `menu_pliku` (menu „…” otwarte), `karta` (w rozmowie jest karta pliku), `menu_karty` (menu prawego kliku otwarte) i `sesje` (ćwiczenie ma pasek boczny z rozmowami)."""
    return {"plik_ekran": {"plik": False, "menu_pliku": False, "karta": False, "menu_karty": False, "sesje": isinstance(apl, dict) and "sesje" in apl}}


def kolejnosc(k: dict, sk: str, st: dict, blad) -> None:
    """Przed każdym krokiem drogi: przy otwartym menu „…” dalej tylko `nauczyciel`, przy menu karty `nauczyciel` i klik „plik-karta-pozycja” (menu zostaje otwarte do końca drogi); potem stan otwartego pliku (krok `plik` z linijkami otwiera go, `plik` ze stroną, `artefakt`, `strona`, `/btw` i panele pracy w tle zajmują jego miejsce)."""
    m, typ = st["plik_ekran"], k.get("typ")
    if m["menu_pliku"] and typ not in PRZY_MENU:
        blad(sk, f"krok {typ} po otwarciu menu „…” panelu pliku: dalej tylko nauczyciel (menu zostaje otwarte do końca drogi, a jego pozycje nie mają skutku)")
    elif m["menu_karty"] and typ not in PRZY_MENU and not (typ == "klik" and k.get("cel") == "plik-karta-pozycja"):
        blad(sk, f"krok {typ} przy otwartym menu prawego kliku na karcie pliku: dalej tylko nauczyciel i klik „plik-karta-pozycja” (menu zostaje otwarte do końca drogi)")
    if typ == "plik":
        m["plik"] = "strona" not in k
    elif typ in ZAMYKAJA_PANEL or (typ == "komenda" and k.get("tekst") == "/btw") or (typ == "klik" and k.get("cel") in KLIKI_ZAMYKAJACE_PANEL):
        m["plik"] = False


def _bez_sesji(sk: str, st: dict, co: str, blad) -> None:
    if st["plik_ekran"]["sesje"]:
        blad(sk, f"{co} w ćwiczeniu z aplikacja.sesje: zmiana rozmowy nie ma opisanego skutku dla panelu pliku, karty pliku ani paska tytułu (nie łączymy)")


def claude(k: dict, sk: str, st: dict, napisy, blad) -> None:
    """Pole `karta_pliku` kroku `claude`: `{"rozmiar": N}` (liczba bajtów 1-999), tylko razem z `plik` o rozszerzeniu .txt (znaczek „TXT” ze zrzutu); karta stoi nad tekstem odpowiedzi."""
    _bez_sesji(sk, st, "karta_pliku", blad)
    karta, plik = k["karta_pliku"], k.get("plik")
    if not isinstance(plik, str) or not plik.strip():
        blad(sk, "karta_pliku bez pola plik: karta pokazuje nazwę pliku z odpowiedzi")
    elif not any(plik.lower().endswith(r) for r in RODZAJE_KARTY):
        blad(sk, f"karta_pliku przy pliku „{plik}”: zrzut pokazuje tylko znaczek „TXT” przy plikach .txt, innych rodzajów nie wymyślamy")
    if not isinstance(karta, dict) or set(karta) != {"rozmiar"}:
        blad(sk, 'karta_pliku musi być obiektem z jednym polem rozmiar: {"rozmiar": 72}')
        return
    r = karta["rozmiar"]
    if type(r) is not int or not 1 <= r <= MAKS_ROZMIAR:
        blad(sk, f"karta_pliku.rozmiar musi być liczbą całkowitą od 1 do {MAKS_ROZMIAR} (bajty, napis „NB” jak na zrzucie), jest {r!r}")
    elif not napisy.jest(f"{r}B", GDZIE) or not napisy.jest("TXT", GDZIE):
        blad(sk, f"napis karty „TXT {r}B” spoza listy napisów interfejsu aplikacji")
    st["plik_ekran"]["karta"] = True


def klik(k: dict, sk: str, st: dict, napisy, blad) -> None:
    """Klik `plik-menu` (otwiera menu „…” panelu otwartego pliku), `plik-karta-menu` (otwiera menu prawego kliku na karcie pliku z odpowiedzi), `plik-karta-pozycja` (podświetla pozycję `pozycja` tego menu, bez skutku) albo `ikona-tytulu` (dymek ikony `nr` paska tytułu)."""
    cel, m = k["cel"], st["plik_ekran"]
    for p in k:
        if p not in POLA_KLIKU[cel]:
            blad(sk, f"pole {p} nie należy do kliku {cel} (pola: {', '.join(POLA_KLIKU[cel])})")
    _bez_sesji(sk, st, f"klik {cel}", blad)
    if cel == "plik-menu":
        if not m["plik"]:
            blad(sk, "klik „plik-menu” bez otwartego pliku: „…” stoi w panelu pliku, więc najpierw klik w ścieżkę i krok plik z linijkami (nie ze stroną)")
        m["menu_pliku"] = True
    elif cel == "plik-karta-menu":
        if not m["karta"]:
            blad(sk, "klik „plik-karta-menu” bez karty pliku w rozmowie: najpierw krok claude z polem karta_pliku")
        m["menu_karty"] = True
    elif cel == "plik-karta-pozycja":
        _pozycja(k, sk, m, napisy, blad)
    else:
        _ikona(k, sk, napisy, blad)


def _pozycja(k: dict, sk: str, m: dict, napisy, blad) -> None:
    """`pozycja` to jedna z czterech pozycji menu karty ze zrzutu; menu musi być otwarte."""
    p = k.get("pozycja")
    if not m["menu_karty"]:
        blad(sk, "klik „plik-karta-pozycja” bez otwartego menu karty: najpierw klik „plik-karta-menu”")
    if not napisy.jest(p, GDZIE):
        blad(sk, f"pozycja „{p}” spoza listy napisów interfejsu aplikacji")
    elif p not in POZYCJE_KARTY:
        blad(sk, f"pozycja „{p}” spoza menu karty pliku ({' / '.join(POZYCJE_KARTY)})")


def _ikona(k: dict, sk: str, napisy, blad) -> None:
    """`nr` to numer ikony paska tytułu (od lewej); dymek ma tylko ikona 1, bo tylko jej dymek stoi na zrzucie 15-28-18."""
    nr = k.get("nr")
    if type(nr) is not int or nr not in DYMKI_PASKA:
        blad(sk, f"ikona-tytulu: nr musi być numerem ikony z dymkiem na zrzucie ({', '.join(str(n) for n in DYMKI_PASKA)}), jest {nr!r}: dymków pozostałych ikon żaden zrzut nie pokazuje, więc ich nie wymyślamy")
    elif not napisy.jest(DYMKI_PASKA[nr], GDZIE):
        blad(sk, f"dymek „{DYMKI_PASKA[nr]}” spoza listy napisów interfejsu aplikacji")
