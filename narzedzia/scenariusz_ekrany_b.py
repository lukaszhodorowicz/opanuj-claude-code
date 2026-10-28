"""Sprawdza w drogach symulatora aplikacji trzy ekrany ze zrzutów Łukasza z 27.10.2026 (paczka 4 część B): panel Browser z pustą kartą i menu „…” (kliki `przegladarka` i `przegladarka-menu`), menu sesji ze strzałki przy tytule rozmowy z podmenu Transcript view (kliki `strzalka-tytulu`, `transcript-view` i `widok-transkrypcji` z polem `na`) oraz edytor prezentacji rozwinięty na całe okno (klik `edytor-rozwin`); kolejność kroków wokół otwartych menu i okna (opis: dane/FORMAT-SCENARIUSZA.md, część „Menu panelu Browser, edytor prezentacji i Transcript view (zrzuty paczki 4)”)."""

GDZIE = "aplikacja"
KLIKI = ("przegladarka", "przegladarka-menu", "strzalka-tytulu", "transcript-view", "widok-transkrypcji", "edytor-rozwin")
WIDOKI = ("Normal", "Verbose")  # pozycje podmenu Transcript view; Thinking pojawia się dopiero po myśleniu Claude (zrzut 15-32-22), więc go nie ma
POLA_KLIKU = {c: ("typ", "cel", "fakt") for c in KLIKI}
POLA_KLIKU["widok-transkrypcji"] = ("typ", "cel", "na", "fakt")
PANELE_WYPIERAJACE = ("plik", "artefakt", "strona")  # kroki, które zajmują miejsce panelu Browser (jak panel pytania z boku)
KLIKI_ZMIANY_ROZMOWY = ("nowa-rozmowa", "sesja")  # kliki w pasku bocznym, które otwierają inną rozmowę i zamykają panel obok rozmowy (strona/aplikacja-sesje-gra.js)
PRZY_MENU = ("nauczyciel",)  # krok dozwolony przy otwartym menu panelu Browser i przy otwartym edytorze, a po ich otwarciu jedyny


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


def stan(apl: dict) -> dict:
    """Klucz stanu drogi `ekrany_b`: `zajety` (miejsce obok rozmowy zajmuje plik, strona, artefakt albo panel; na starcie `aplikacja.artefakt_otwarty`), `slajdy` (w panelu stoi edytor prezentacji), `browser` (panel z pustą kartą otwarty), `browser_menu` (menu „…” otwarte), `tytul_menu` (menu sesji otwarte), `podmenu` (podmenu Transcript view otwarte), `widok` (wybrana pozycja podmenu, na starcie Normal) i `edytor` (okno edytora otwarte)."""
    otwarty = apl.get("artefakt_otwarty") if isinstance(apl, dict) else None
    otwarty = otwarty if isinstance(otwarty, dict) else {}
    return {"ekrany_b": {"zajety": bool(otwarty), "slajdy": "slajdy" in otwarty, "browser": False, "browser_menu": False, "tytul_menu": False, "podmenu": False, "widok": WIDOKI[0], "edytor": False}}


def kolejnosc(k: dict, sk: str, st: dict, blad) -> None:
    """Przed każdym krokiem drogi: po otwarciu menu „…” panelu Browser i okna edytora dalej tylko `nauczyciel` (oba zostają otwarte do końca drogi, a ich elementy nie mają skutku); przy otwartym menu sesji tylko `nauczyciel`, klik `transcript-view` (przed podmenu) i `widok-transkrypcji` (po nim). Plik, strona, artefakt, `/btw` i klik w pasku bocznym z rozmowami zajmują miejsce panelu Browser albo je zwalniają."""
    e = st["ekrany_b"]
    typ, cel = k.get("typ"), k.get("cel") if k.get("typ") == "klik" else None
    if e["browser_menu"] and typ not in PRZY_MENU:
        blad(sk, f"krok {typ} po otwarciu menu panelu Browser: dalej tylko nauczyciel (menu zostaje otwarte do końca drogi, a jego pozycje nie mają skutku)")
    elif e["edytor"] and typ not in PRZY_MENU:
        blad(sk, f"krok {typ} po otwarciu edytora prezentacji: dalej tylko nauczyciel (okno zostaje otwarte do końca drogi, a jego elementy nie mają skutku)")
    elif e["tytul_menu"] and typ not in PRZY_MENU and cel not in ("transcript-view", "widok-transkrypcji"):
        blad(sk, f"krok {typ} przy otwartym menu sesji: dalej tylko nauczyciel, klik „transcript-view” i klik „widok-transkrypcji” (menu zostaje otwarte do końca drogi, a jego pozostałe pozycje nie mają skutku)")
    if typ in PANELE_WYPIERAJACE or (typ == "komenda" and k.get("tekst") == "/btw") or (typ == "klik" and cel in ("background-tasks", "wpis-w-tle")):
        e.update(browser=False, browser_menu=False, zajety=True, slajdy="slajdy" in k if typ == "artefakt" else False)
    elif typ == "klik" and cel in KLIKI_ZMIANY_ROZMOWY:
        e.update(browser=False, browser_menu=False, zajety=False, slajdy=False)  # inna rozmowa: panel obok rozmowy się zamyka


def klik(k: dict, sk: str, st: dict, napisy, blad) -> None:
    """Klik z listy `KLIKI`: `przegladarka` (pusty panel Browser), `przegladarka-menu` (menu „…” panelu), `strzalka-tytulu` (menu sesji), `transcript-view` (podmenu widoku), `widok-transkrypcji` (wybór Normal albo Verbose w polu `na`) i `edytor-rozwin` (edytor prezentacji na całe okno)."""
    cel, e = k["cel"], st["ekrany_b"]
    for p in k:
        if p not in POLA_KLIKU[cel]:
            blad(sk, f"pole {p} nie należy do kroku klik z celem {cel} (pola: {', '.join(POLA_KLIKU[cel])})")
    if cel == "przegladarka":
        if e["browser"]:
            blad(sk, "klik „przegladarka” przy panelu Browser, który już jest otwarty")
        elif e["zajety"]:
            blad(sk, "klik „przegladarka”, gdy obok rozmowy stoi już plik, strona, artefakt albo panel: pusta karta Browser otwiera się tylko w pustym miejscu (przed krokiem plik, artefakt i strona)")
        e["browser"], e["zajety"] = True, True
    elif cel == "przegladarka-menu":
        if not e["browser"]:
            blad(sk, "klik „przegladarka-menu” bez otwartego panelu Browser z pustą kartą: najpierw klik „przegladarka”")
        e["browser_menu"] = True
    elif cel == "strzalka-tytulu":
        if e["tytul_menu"]:
            blad(sk, "klik „strzalka-tytulu” przy menu sesji, które jest już otwarte")
        e["tytul_menu"] = True
    elif cel == "transcript-view":
        if not e["tytul_menu"]:
            blad(sk, "klik „transcript-view” bez otwartego menu sesji: najpierw klik „strzalka-tytulu”")
        elif e["podmenu"]:
            blad(sk, "klik „transcript-view” przy podmenu, które jest już otwarte")
        e["podmenu"] = True
    elif cel == "widok-transkrypcji":
        _widok(k, sk, e, napisy, blad)
    else:
        _edytor(sk, e, blad)


def _widok(k: dict, sk: str, e: dict, napisy, blad) -> None:
    """Klik `widok-transkrypcji`: podmenu musi być otwarte, `na` to Normal albo Verbose inne niż wybrane (ptaszek się przesuwa, menu zostaje otwarte)."""
    na = k.get("na")
    if not e["podmenu"]:
        blad(sk, "klik „widok-transkrypcji” bez otwartego podmenu Transcript view: najpierw klik „transcript-view”")
    if not _niepusty(na) or not napisy.jest(na, GDZIE):
        blad(sk, f"na „{na}” spoza listy napisów interfejsu aplikacji")
    elif na not in WIDOKI:
        blad(sk, f"na „{na}” spoza {' / '.join(WIDOKI)} (Thinking pojawia się dopiero po myśleniu Claude, zrzut 15-32-22 go nie pokazuje)")
    elif na == e["widok"]:
        blad(sk, f"widok „{na}” już jest wybrany (ptaszek stoi przy nim)")
    else:
        e["widok"] = na


def _edytor(sk: str, e: dict, blad) -> None:
    """Klik `edytor-rozwin`: ikona rozwinięcia w nagłówku edytora prezentacji z panelu Browser; wymaga otwartej prezentacji (slajdy)."""
    if e["edytor"]:
        blad(sk, "klik „edytor-rozwin” przy edytorze, który już jest rozwinięty")
    elif not e["slajdy"]:
        blad(sk, "klik „edytor-rozwin” bez otwartej prezentacji w panelu Browser: najpierw krok artefakt ze slajdami (albo aplikacja.artefakt_otwarty ze slajdami)")
    e["edytor"] = True


def pokazuje(st: dict) -> bool:
    """Czy droga kończy się ekranem tej części: otwartym panelem Browser (z menu albo bez), otwartym menu sesji albo rozwiniętym edytorem; taka droga może nie mieć kroku `plik`, `artefakt` ani `strona`."""
    e = st["ekrany_b"]
    return e["browser"] or e["tytul_menu"] or e["edytor"]
