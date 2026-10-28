"""Sprawdza w drogach symulatora aplikacji katalog konektorów otwierany z podmenu Connectors menu `+`: pozycję `Browse connectors` (krok `klik` z celem `pozycja`), krok `klik` z celem `konektor`, krok `katalog_zamknij` oraz kolejność kroków wokół otwartego katalogu i karty logowania (opis: dane/FORMAT-SCENARIUSZA.md, część „Menu + i katalog konektorów”)."""

GDZIE = "aplikacja"
CELE = ("konektor",)  # cel kroku `klik` dodany przez katalog
POZYCJA_KATALOGU = "Browse connectors"  # pozycja podmenu Connectors (menu +), która otwiera katalog; podmenu otwiera klik w pozycję „Connectors” (scenariusz_plus.py)
POZYCJA_W_SESJI = "Add folder"  # pozycja menu +, przez którą kurs nie prowadzi w nowej sesji (fakt aplikacja-dodaj-folder-w-sesji); menu ją rysuje zawsze
KAFELKI = ("Google Drive", "Gmail", "Google Calendar", "Microsoft 365", "Slack", "Notion", "Canva", "Atlassian MCP", "Google Sheets", "Figma", "Google Docs", "Supabase")  # kafelki katalogu w kolejności ze zrzutu 04-43-33 (strona/aplikacja-ustawienia-dane.js, PK.KONEKTORY_KATALOG)
MAKS_MS = 10000
POLA = {"konektor": ("typ", "cel", "nazwa", "fakt"), "katalog_zamknij": ("typ", "ms", "fakt")}


def stan(apl, napisy=None) -> dict:
    """Klucze stanu drogi: `kat` (None, „katalog” przy otwartym oknie z kafelkami albo „karta” po kliknięciu kafelka), `kat_czeka` (po otwarciu katalogu i po karcie najpierw nauczyciel), `kat_srodowisko`, `kat_pusta` (rozmowa ćwiczenia pusta: nowa sesja) i `kat_napisy`."""
    apl = apl if isinstance(apl, dict) else {}
    return {"kat": None, "kat_czeka": False, "kat_srodowisko": apl.get("srodowisko"), "kat_pusta": not apl.get("rozmowa"), "kat_napisy": napisy}


def zaczyna_od_plusa(cw: dict) -> bool:
    """Każda droga ćwiczenia zaczyna się krokiem `klik: plus`: dodawanie konektora przed sesją, więc rozmowa może być pusta."""
    drogi = cw.get("drogi")
    if not isinstance(drogi, list) or not drogi:
        return False
    for d in drogi:
        kroki = d.get("kroki") if isinstance(d, dict) else None
        pierwszy = kroki[0] if isinstance(kroki, list) and kroki else None
        if not (isinstance(pierwszy, dict) and pierwszy.get("typ") == "klik" and pierwszy.get("cel") == "plus"):
            return False
    return True


def ma_katalog(droga: dict) -> bool:
    """Droga ma krok `klik: konektor` albo `katalog_zamknij`: nie kończy się plikiem ani artefaktem."""
    kroki = droga.get("kroki") if isinstance(droga, dict) else None
    return any(isinstance(k, dict) and (k.get("typ") == "katalog_zamknij" or (k.get("typ") == "klik" and k.get("cel") in CELE)) for k in kroki or [])


def _pola(k: dict, sk: str, nazwa: str, blad) -> None:
    for pole in k:
        if pole not in POLA[nazwa]:
            blad(sk, f"pole {pole} nie należy do kroku {nazwa} (pola: {', '.join(POLA[nazwa])})")


def _otwarcie(k: dict, sk: str, st: dict, blad) -> None:
    """Krok `klik: pozycja` z `na: Browse connectors` otwiera katalog (podmenu Connectors musi być otwarte: pilnuje tego `scenariusz_plus`); w środowisku Cloud i przy otwartym katalogu to błąd; `Add folder` w nowej sesji (pusta rozmowa) to błąd (kurs nie prowadzi przez tę pozycję)."""
    na = k.get("na")
    if st["kat"]:
        blad(sk, "klik pozycja przy otwartym katalogu: najpierw dokończ logowanie i zamknij okno krokiem katalog_zamknij")
    if na == POZYCJA_W_SESJI and st["kat_pusta"]:
        blad(sk, f"„{POZYCJA_W_SESJI}” w nowej sesji (pusta rozmowa): kurs nie prowadzi przez tę pozycję przed pierwszą wiadomością, folder dodaje się w trakcie sesji (fakt aplikacja-dodaj-folder-w-sesji); menu pozycję rysuje, zrzut 03-58-01")
    if na != POZYCJA_KATALOGU:
        return
    if st["kat_srodowisko"] == "Cloud":
        blad(sk, f"„{POZYCJA_KATALOGU}” w środowisku Cloud: konektory dodaje się w sesji lokalnej albo SSH (fakt aplikacja-add-connectors-otwiera-katalog; zrzut 04-22-37 pokazuje podmenu Connectors w sesji w chmurze, więc fakt czeka na rewizję)")
    st["kat"], st["kat_czeka"] = "katalog", True


def _konektor(k: dict, sk: str, st: dict, blad) -> None:
    """`konektor`: tylko przy otwartym katalogu (z kafelkami); `nazwa` to jeden z kafelków katalogu i napis z listy napisów aplikacji; po nim idzie nauczyciel, potem `katalog_zamknij`."""
    _pola(k, sk, "konektor", blad)
    nazwa = k.get("nazwa")
    if st["kat"] != "katalog":
        blad(sk, "klik konektor bez otwartego katalogu: najpierw plus, pozycja „Connectors” i pozycja „Browse connectors” (przy karcie logowania kafelków już nie ma)")
    if nazwa not in KAFELKI:
        blad(sk, f"nazwa „{nazwa}” spoza kafelków katalogu: {', '.join(KAFELKI)}")
    elif st["kat_napisy"] is not None and not st["kat_napisy"].jest(nazwa, GDZIE):
        blad(sk, f"nazwa „{nazwa}” spoza listy napisów interfejsu aplikacji")
    st["kat"], st["kat_czeka"] = "karta", True


def _zamkniecie(k: dict, sk: str, st: dict, blad) -> None:
    """`katalog_zamknij`: tylko przy karcie logowania; `ms` to liczba całkowita od 1 do 10000."""
    _pola(k, sk, "katalog_zamknij", blad)
    if st["kat"] != "karta":
        blad(sk, "katalog_zamknij bez karty logowania: najpierw klik konektor")
    if "ms" in k and (type(k["ms"]) is not int or not 0 < k["ms"] <= MAKS_MS):
        blad(sk, f"ms musi być liczbą całkowitą od 1 do {MAKS_MS}")
    st["kat"] = None


def kolejnosc(k: dict, sk: str, st: dict, blad) -> None:
    """Przed każdym krokiem drogi (przed `scenariusz_plus.kolejnosc`): obsługuje kroki katalogu, a przy otwartym katalogu i przy karcie dopuszcza tylko `nauczyciel` i następny krok katalogu. Zaraz po otwarciu katalogu i zaraz po karcie musi stać `nauczyciel` (najdalej w drugim kroku, jak w narzedzia/czytelnosc.py)."""
    typ, cel = k.get("typ"), k.get("cel")
    if typ == "klik" and "nazwa" in k and cel not in CELE:
        blad(sk, f"pole nazwa tylko w kroku klik z celem konektor, jest przy celu „{cel}”")
    if st["kat"] and st["kat_czeka"] and typ != "nauczyciel":
        blad(sk, "po otwarciu katalogu i po karcie logowania najpierw nauczyciel: kursant musi wiedzieć, co kliknąć albo co się dzieje")
    elif st["kat"] and typ not in ("nauczyciel", "katalog_zamknij") and not (typ == "klik" and cel in CELE):
        blad(sk, f"krok {typ} przy otwartym katalogu ({'karta logowania' if st['kat'] == 'karta' else 'kafelki'}): dalej tylko nauczyciel i następny krok katalogu")
    if typ == "klik" and cel == "plus" and st["kat"]:
        blad(sk, "klik plus przy otwartym katalogu: najpierw zamknij okno krokiem katalog_zamknij")
    if typ == "nauczyciel":
        st["kat_czeka"] = False
    elif typ == "klik" and cel == "pozycja":
        _otwarcie(k, sk, st, blad)
    elif typ == "klik" and cel == "konektor":
        _konektor(k, sk, st, blad)
    elif typ == "katalog_zamknij":
        _zamkniecie(k, sk, st, blad)


def koniec(sd: str, st: dict, blad) -> None:
    """Koniec drogi: bez otwartego katalogu i bez karty logowania."""
    if st["kat"]:
        blad(sd, f"droga kończy się otwartym katalogiem ({'karta logowania' if st['kat'] == 'karta' else 'kafelki'}): dodaj krok katalog_zamknij")
