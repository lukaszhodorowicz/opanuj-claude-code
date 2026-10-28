"""Sprawdza w ćwiczeniu z drogami symulatora aplikacji wybór modelu i wysiłku: kliki `wybor-modelu`, `effort` i `poziom` (pola `poziom` 1-5 i `notka`), ich kolejność i menu otwarte na końcu drogi (opis: dane/FORMAT-SCENARIUSZA.md, część „Wybór modelu i wysiłku”)."""

GDZIE_INTERFEJSU = ("aplikacja", "claude.ai")  # notka to element kursu, więc nie może udawać napisu interfejsu
KLIKI = ("wybor-modelu", "effort", "poziom")
MODELE = ("Opus 5.5", "Fable 5.1", "Sonnet 5.5", "Haiku 5.5")  # nazwy z menu modelu, zrzut Łukasza 27.10.2026 (04-24-16), w kolejności menu
WYSILKI = ("Low", "Medium", "High", "Extra", "Max")  # nazwy poziomów w kolejności listy (04-24-29): numer `poziom` kroku to ich miejsce od góry
POZIOMY = 5  # tyle wierszy poziomów ma lista (fakt wysilek-poziomy-zaleza-od-modelu: najnowsze modele mają pięć)
MAKS_ZNAKOW_NOTKI = 30
PRZY_MENU = ("nauczyciel",)  # krok dozwolony przy otwartym menu poza kolejnym klikiem


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


def pole(cw: dict, s: str, napisy, blad) -> None:
    """Pola `aplikacja.model` (nazwa modelu z menu ze zrzutu) i `aplikacja.wysilek` (poziom z listy; domyślnie Medium): przycisk w rzędzie pod polem pokazuje „<model> <poziom>”, menu modelu ma nazwy modeli i bieżący poziom przy Effort. Bez `model` przycisk i menu pokazują model domyślny Opus 5.5 (zrzut 04-24-16), więc `wysilek` działa też bez `model`. Wartości z listy napisów interfejsu aplikacji i z nazw ze zrzutów (dane konta autora zrzutu, ale tylko takie napisy symulator zna)."""
    apl = cw.get("aplikacja")
    if not isinstance(apl, dict):
        return
    sa = f"{s}/aplikacja"
    for pole_, dozwolone in (("model", MODELE), ("wysilek", WYSILKI)):
        if pole_ not in apl:
            continue
        wartosc = apl[pole_]
        if not napisy.jest(wartosc, "aplikacja"):
            blad(sa, f"{pole_} „{wartosc}” spoza listy napisów interfejsu aplikacji")
        elif wartosc not in dozwolone:
            blad(sa, f"{pole_} „{wartosc}” spoza {' / '.join(dozwolone)}")


def stan() -> dict:
    """Klucz stanu drogi: `model` to None (menu zamknięte), „menu” (po `wybor-modelu`) albo „lista” (po `effort`, lista poziomów otwarta)."""
    return {"model": None}


def kolejnosc(k: dict, sk: str, st: dict, blad) -> None:
    """Przed każdym krokiem drogi: pola `poziom` i `notka` stoją tylko w kliku `poziom`; przy otwartym menu dalej tylko `nauczyciel` i następny klik (menu otwiera się i zamyka w jednej serii kroków)."""
    typ, cel = k.get("typ"), k.get("cel")
    klik_modelu = typ == "klik" and cel in KLIKI
    if not (typ == "klik" and cel == "poziom"):
        for pole in ("poziom", "notka"):
            if pole in k:
                blad(sk, f"pole {pole} należy tylko do kroku klik z celem poziom (jest w kroku {typ}{' z celem ' + str(cel) if typ == 'klik' else ''})")
    if st["model"] and typ not in PRZY_MENU and not klik_modelu:
        blad(sk, f"krok {typ} przy otwartym menu wyboru modelu: dalej tylko nauczyciel, klik „effort” i klik „poziom” (menu zamyka dopiero wybór poziomu)")


def klik(k: dict, sk: str, st: dict, napisy, blad) -> None:
    """Klik `wybor-modelu` (otwiera menu), `effort` (zaraz po nim: otwiera listę poziomów) albo `poziom` (zaraz po `effort`: wybiera wiersz `poziom` 1-5 z notką `notka` i zamyka menu)."""
    cel = k["cel"]
    if cel == "wybor-modelu":
        if st["model"]:
            blad(sk, "klik w wybór modelu przy otwartym menu: najpierw klik „poziom”, który je zamyka")
        st["model"] = "menu"
    elif cel == "effort":
        if st["model"] != "menu":
            blad(sk, "klik „effort” tylko zaraz po kliku „wybor-modelu” (wiersz Effort jest w otwartym menu)")
        st["model"] = "lista"
    else:
        if st["model"] != "lista":
            blad(sk, "klik „poziom” tylko zaraz po kliku „effort” (lista poziomów otwiera się z wiersza Effort)")
        _poziom(k, sk, napisy, blad)
        st["model"] = None


def _poziom(k: dict, sk: str, napisy, blad) -> None:
    """Pole `poziom`: liczba całkowita 1-5 (numer wiersza od góry); `notka`: niepusty napis kursu do 30 znaków, nie z listy napisów interfejsu."""
    poziom = k.get("poziom")
    if type(poziom) is not int or not 1 <= poziom <= POZIOMY:
        blad(sk, f"poziom musi być liczbą całkowitą od 1 do {POZIOMY} (numer wiersza od góry), jest {poziom!r}")
    notka = k.get("notka")
    if not _niepusty(notka):
        blad(sk, "klik poziom wymaga niepustego pola notka (napis kursu przy klikniętym wierszu)")
    elif len(notka) > MAKS_ZNAKOW_NOTKI:
        blad(sk, f"notka ma {len(notka)} znaków, limit {MAKS_ZNAKOW_NOTKI}")
    elif any(napisy.jest(notka, g) for g in GDZIE_INTERFEJSU):
        blad(sk, f"notka „{notka}” to napis interfejsu; notka jest elementem kursu")


def koniec(sd: str, st: dict, blad) -> None:
    """Koniec drogi: menu wyboru modelu nie może zostać otwarte (po `wybor-modelu` albo `effort` musi przyjść `poziom`)."""
    if st["model"]:
        blad(sd, "droga kończy się przy otwartym menu wyboru modelu: po kliku „wybor-modelu” i „effort” musi być klik „poziom”")
