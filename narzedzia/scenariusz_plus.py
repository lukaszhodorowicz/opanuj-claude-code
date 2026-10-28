"""Sprawdza w drogach symulatora aplikacji przycisk `+` obok pola wiadomości z menu pozycji (z podmenu Plugins i Connectors) i listę poleceń nad polem: kroki `klik` z celami `plus`, `pozycja`, `wiersz`, krok `ukosnik` oraz kolejność kroków wokół menu, podmenu, listy i skilla w polu (opis: dane/FORMAT-SCENARIUSZA.md)."""

GDZIE = "aplikacja"
MENU_PLUS = ("Add files or photos", "Add folder", "Import GitHub issue", "Slash commands", "Connectors", "Plugins")  # kolejność pozycji menu w symulatorze (strona/aplikacja-plus-dane.js, PK.MENU_PLUS)
PODMENU = {"Plugins": ("Manage plugins", "Browse plugins"), "Connectors": ("Browse connectors", "Manage connectors")}  # pozycje podmenu (PK.PODMENU_PLUS); podmenu otwiera klik w pozycję menu o tej nazwie
BEZ_SKUTKU = "Import GitHub issue"  # zawsze wyszarzona w symulatorze (podpis „This folder doesn’t have a GitHub remote”), więc nie jest celem kroku
LOKALNE = ("Add folder", "Plugins")  # w sesji w chmurze wyszarzone z podpisem „Only available in local sessions” (zrzut 04-22-37)
WIERSZE_LISTY = ("plugin", "model", "effort", "fast", "plan", "permissions", "skills", "workflows", "usage", "usage-credits", "config", "storage", "sandbox")  # nazwane wiersze listy „/” od góry (PK.WIERSZE_LISTY; czternasty wiersz jest szary, bez nazwy)
CELE = ("plus", "pozycja", "wiersz")
POLA = {
    "plus": ("typ", "cel", "fakt"),
    "pozycja": ("typ", "cel", "na", "fakt"),
    "wiersz": ("typ", "cel", "na", "bez_napisu", "fakt"),
    "ukosnik": ("typ", "fakt"),
}
LISTA_POLECEN = "Slash commands"  # jedyna pozycja menu, której zachowanie jest zbudowane: otwiera listę poleceń


def stan(napisy, apl=None) -> dict:
    """Klucze stanu drogi: `plus_menu` (menu otwarte), `plus_podmenu` (None albo „Plugins”/„Connectors”: otwarte podmenu, menu zostaje otwarte), `plus_lista` (lista poleceń otwarta), `plus_pole` (None, „/” albo „skill”: co stoi w polu wiadomości), `plus_srodowisko` i `plus_napisy` (lista napisów interfejsu albo None)."""
    apl = apl if isinstance(apl, dict) else {}
    return {"plus_menu": False, "plus_podmenu": None, "plus_lista": False, "plus_pole": None, "plus_srodowisko": apl.get("srodowisko"), "plus_napisy": napisy}


def _zajete(st: dict) -> str | None:
    """Co jest otwarte i czeka na dalszy krok kursanta: menu, lista albo skill w polu."""
    if st["plus_menu"]:
        return "menu przycisku +"
    if st["plus_lista"]:
        return "lista poleceń"
    return "skill w polu wiadomości" if st["plus_pole"] == "skill" else None


def _pola(k: dict, sk: str, nazwa: str, blad) -> None:
    for pole in k:
        if pole not in POLA[nazwa]:
            blad(sk, f"pole {pole} nie należy do kroku {nazwa} (pola: {', '.join(POLA[nazwa])})")


def _napis(st: dict, napis: str, sk: str, blad) -> None:
    """Napis interfejsu (`+`, `/`, pozycja menu) musi stać w liście napisów aplikacji."""
    napisy = st["plus_napisy"]
    if napisy is not None and not napisy.jest(napis, GDZIE):
        blad(sk, f"napis „{napis}” spoza listy napisów interfejsu aplikacji")


def _pozycja(k: dict, sk: str, st: dict, blad) -> None:
    """`pozycja`: tylko przy otwartym menu (po `plus`); `na` to napis menu albo podmenu z listy napisów. Klik w „Plugins” albo „Connectors” otwiera podmenu obok menu (menu zostaje otwarte; przy otwartym podmenu drugi taki klik to błąd, bo na wąskim ekranie podmenu zasłania menu); pozycja podmenu (`Browse plugins`, `Browse connectors`, `Manage …`) tylko przy otwartym podmenu swojego rodzica i zamyka menu. „Slash commands” zamyka menu i otwiera listę; inna pozycja tylko zamyka menu (jej zachowania silnik nie ma). „Import GitHub issue” jest zawsze wyszarzona, „Add folder” i „Plugins” w sesji w chmurze też."""
    na = k.get("na")
    rodzic = next((r for r, pozycje in PODMENU.items() if na in pozycje), None)
    if not st["plus_menu"]:
        blad(sk, "klik pozycja tylko po kroku plus: menu przycisku + musi być otwarte")
    if na not in MENU_PLUS and rodzic is None:
        pozycje = ", ".join((*MENU_PLUS, *(p for ps in PODMENU.values() for p in ps)))
        blad(sk, f"na „{na}” spoza pozycji menu +: {pozycje}")
    else:
        _napis(st, na, sk, blad)
    if na == BEZ_SKUTKU:
        blad(sk, f"pozycja „{BEZ_SKUTKU}” jest w symulatorze zawsze wyszarzona (podpis „This folder doesn’t have a GitHub remote”): nie jest celem kroku")
    if na in LOKALNE and st["plus_srodowisko"] == "Cloud":
        blad(sk, f"pozycja „{na}” w środowisku Cloud jest wyszarzona (podpis „Only available in local sessions”, zrzut 04-22-37): działa tylko w sesji lokalnej")
    if rodzic and st["plus_podmenu"] != rodzic:
        blad(sk, f"pozycja „{na}” należy do podmenu „{rodzic}”: najpierw klik pozycja „{rodzic}” (podmenu otwiera się obok menu)")
    if na in PODMENU:
        if st["plus_podmenu"]:
            blad(sk, f"klik pozycja „{na}” przy otwartym podmenu „{st['plus_podmenu']}”: na wąskim ekranie podmenu zasłania menu, więc po jego otwarciu droga wybiera już tylko pozycję tego podmenu")
        st["plus_podmenu"] = na  # podmenu obok menu; menu zostaje otwarte
        return
    st["plus_menu"] = False
    st["plus_podmenu"] = None
    st["plus_lista"] = na == LISTA_POLECEN


def _wiersz(k: dict, sk: str, st: dict, blad) -> None:
    """`wiersz`: tylko przy otwartej liście; dokładnie jedno z `na` (napis wiersza listy: jeden z `WIERSZE_LISTY`, napis z listy napisów aplikacji) albo `bez_napisu: true` (stare scenariusze: szary wiersz bez nazwy na końcu listy)."""
    if not st["plus_lista"]:
        blad(sk, "klik wiersz tylko przy otwartej liście poleceń (po pozycji „Slash commands” albo po kroku ukosnik)")
    if "na" in k and "bez_napisu" in k:
        blad(sk, "klik wiersz ma albo pole na (napis wiersza listy), albo bez_napisu: true, nie oba")
    elif "na" in k:
        if k["na"] not in WIERSZE_LISTY:
            blad(sk, f"na „{k['na']}” spoza wierszy listy poleceń: {', '.join(WIERSZE_LISTY)}")
        else:
            _napis(st, k["na"], sk, blad)
    elif k.get("bez_napisu") is not True:
        blad(sk, "klik wiersz wymaga pola bez_napisu: true (stare scenariusze) albo pola na z napisem wiersza listy")
    st["plus_lista"] = False
    st["plus_pole"] = "skill"


def kolejnosc(k: dict, sk: str, st: dict, blad) -> None:
    """Przed każdym krokiem drogi: obsługuje kroki menu i listy (`klik` z celami `plus`, `pozycja`, `wiersz` oraz `ukosnik`), a przy otwartym menu, otwartej liście albo skillu w polu dopuszcza tylko `nauczyciel`; `pisz` przy skillu w polu wysyła skill razem z tekstem."""
    typ, cel = k.get("typ"), k.get("cel")
    nazwa = cel if typ == "klik" and cel in CELE else "ukosnik" if typ == "ukosnik" else None
    zajete = _zajete(st)
    if nazwa:
        _pola(k, sk, nazwa, blad)
    if nazwa in ("plus", "ukosnik"):
        _napis(st, "+" if nazwa == "plus" else "/", sk, blad)
        if zajete:
            blad(sk, f"krok {nazwa} przy otwartym elemencie ({zajete}): najpierw dokończ poprzedni wybór")
        st["plus_menu"] = nazwa == "plus"
        st["plus_podmenu"] = None
        st["plus_lista"] = nazwa == "ukosnik"
        st["plus_pole"] = "/" if nazwa == "ukosnik" else None
    elif nazwa == "pozycja":
        _pozycja(k, sk, st, blad)
    elif nazwa == "wiersz":
        _wiersz(k, sk, st, blad)
    elif typ == "pisz" and st["plus_pole"] == "skill":
        st["plus_pole"] = None  # skill i tekst idą w jednej wiadomości
    elif zajete and typ != "nauczyciel":
        blad(sk, f"krok {typ} przy otwartym elemencie ({zajete}): dalej tylko nauczyciel, kolejny krok menu albo pisz po wierszu")


def koniec(sd: str, st: dict, blad) -> None:
    """Koniec drogi: bez otwartego menu, otwartej listy i skilla w polu, który nie dostał zadania."""
    zajete = _zajete(st)
    if zajete:
        blad(sd, f"droga kończy się otwartym elementem ({zajete}): dodaj kroki do końca wyboru i krok pisz z zadaniem")
