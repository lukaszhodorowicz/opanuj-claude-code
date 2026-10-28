"""Sprawdza w drogach symulatora aplikacji kartę zgody przeglądarki (krok `zgoda` z polem `witryna`: przyciski Allow once, Always allow i Deny przy pierwszym działaniu Claude na cudzej stronie), kliki `allow_once`, `always_allow` i `deny`, krok `strona` (cudza strona w panelu Browser, z ramkami `pola` albo bez) i pamięć zgody w drodze (opis: dane/FORMAT-SCENARIUSZA.md, część „Karta zgody w drodze”, wariant „strona”)."""

from narzedzia.scenariusz_strona import sprawdz_pola, sprawdz_strone

TYPY = ("strona",)
KLIKI = ("allow_once", "always_allow", "deny")
TRYBY = ("Manual", "Accept edits", "Auto")  # tryby, w których karta przeglądarki ma sens (fakty aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu, aplikacja-browser-klasyfikator-sprawdza-klikanie-i-pisanie); Plan nie
POLA_KROKU = ("typ", "witryna", "strona", "fakt")
FAKT_KARTY = "aplikacja-browser-karta-zgody-przy-pierwszym-dzialaniu"
FAKT_ZAWSZE = "aplikacja-browser-always-allow-zapisuje-dla-strony"
NAZWY_KLIKOW = {"allow_once": "Allow once", "always_allow": "Always allow", "deny": "Deny"}
CELE_PO_KARCIE = "„allow_once”, „always_allow” albo „deny”"


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


def stan() -> dict:
    """Klucze stanu drogi: `zgody_stron` (strony z Always allow do końca drogi), `jednorazowa` (strona z Allow once, na jeden krok `strona`), `odmowy` (strony, którym odmówiono i które nie dostały nowej zgody), `po_decyzji` (para (cel kliku, strona) po decyzji, na którą ma odpowiedzieć następny krok, albo None), `odmowa` (w drodze padło Deny) i `strony` (liczba kroków `strona`)."""
    return {"zgody_stron": set(), "jednorazowa": None, "odmowy": set(), "po_decyzji": None, "odmowa": False, "strony": 0}


def blad_trybu(tryb: str) -> str:
    """Komunikat dla karty przeglądarki w trybie spoza `TRYBY`."""
    return f"karta zgody przeglądarki w drodze tylko w trybie {', '.join(TRYBY[:-1])} albo {TRYBY[-1]} (teraz „{tryb}”): żaden fakt nie mówi o karcie zgody na cudzej stronie w innych trybach (fakty {FAKT_KARTY}, aplikacja-browser-klasyfikator-sprawdza-klikanie-i-pisanie)"


def karta(k: dict, sk: str, st: dict, blad) -> None:
    """Karta z `witryna` (nazwa strony: niepusty napis; karta jej nie pokazuje, nazywa ją odpowiedź Claude nad kartą), bez `odliczanie_ms` (karta nie ma ptaszka, który odliczanie wstrzymuje) i bez drugiej karty dla strony z Always allow."""
    witryna = k["witryna"]
    if not _niepusty(witryna):
        blad(sk, "zgoda: pole witryna to nazwa strony (np. nazwa firmy): niepusty napis")
    elif witryna in st["zgody_stron"]:
        blad(sk, f"druga karta zgody dla strony „{witryna}”, która ma już Always allow w tej drodze: zgoda jest zapisana do końca drogi, więc karta by się nie pojawiła (fakt {FAKT_ZAWSZE})")
    if "odliczanie_ms" in k:
        blad(sk, "odliczanie_ms nie działa w karcie zgody z polem witryna: odliczanie wstrzymuje ptaszek, a karta przeglądarki ma przyciski z napisami (Allow once, Always allow, Deny)")
    st["zgoda"] = ("witryna", witryna if isinstance(witryna, str) else "?")


def przy_karcie(k: dict, sk: str, blad) -> None:
    """Gdy karta przeglądarki czeka: dalej tylko `nauczyciel` albo klik w jeden z trzech przycisków (klik `zatwierdz` przejdzie dalej i dostanie własny komunikat)."""
    typ = k.get("typ")
    if typ != "nauczyciel" and not (typ == "klik" and k.get("cel") in (*KLIKI, "zatwierdz")):
        blad(sk, f"krok {typ} przy karcie zgody przeglądarki, która czeka: Claude czeka na Twój wybór, dalej tylko nauczyciel albo klik {CELE_PO_KARCIE} (fakt {FAKT_KARTY})")


def klik_zatwierdz(sk: str, st: dict, blad) -> None:
    """Klik `zatwierdz` przy karcie z `witryna`: ta karta nie ma ptaszka; karta przestaje czekać, żeby jeden błąd nie dawał lawiny dalszych."""
    blad(sk, f"klik zatwierdz przy karcie zgody z polem witryna: karta przeglądarki nie ma ptaszka, tylko przyciski Allow once, Always allow i Deny (cele klik {CELE_PO_KARCIE}; fakt {FAKT_KARTY})")
    st["zgoda"] = None


def klik(k: dict, sk: str, st: dict, blad) -> None:
    """Klik `allow_once`, `always_allow` albo `deny`: wymaga karty z `witryna`, która czeka. Allow once daje zgodę na jeden krok `strona`, Always allow na wszystkie do końca drogi (tylko dla tej strony), Deny nie daje żadnej."""
    cel = k["cel"]
    czekajaca = st["zgoda"]
    if not czekajaca or czekajaca[0] != "witryna":
        blad(sk, f"klik „{cel}” bez karty zgody przeglądarki, która czeka na decyzję (krok zgoda z polem witryna)")
        return
    witryna = czekajaca[1]
    st["zgoda"] = None
    st["po_decyzji"] = (cel, witryna)
    st["jednorazowa"] = None
    if cel == "deny":
        st["odmowa"] = True
        st["odmowy"].add(witryna)
        return
    st["odmowy"].discard(witryna)  # nowa karta z zezwoleniem po odmowie jest dozwolona
    if cel == "always_allow":
        st["zgody_stron"].add(witryna)
    else:
        st["jednorazowa"] = witryna


def po_decyzji(k: dict, sk: str, st: dict, blad) -> None:
    """Pierwszy krok po decyzji poza `nauczyciel` i `mysli`: po Allow once i Always allow to `strona` z tą samą `witryna`, po Deny odpowiedź `claude` (słowa po odmowie)."""
    cel, witryna = st["po_decyzji"]
    st["po_decyzji"] = None
    typ = k.get("typ")
    if cel == "deny":
        if typ != "claude":
            blad(sk, f"krok {typ} po odmowie (Deny): najpierw odpowiedź Claude, który na stronę „{witryna}” nie wchodzi (fakt {FAKT_KARTY})")
    elif typ != "strona" or k.get("witryna") != witryna:
        st["jednorazowa"] = None
        blad(sk, f"krok {typ} po zezwoleniu ({NAZWY_KLIKOW[cel]}): najpierw krok strona z witryna „{witryna}”, bo Claude po zgodzie wchodzi na stronę (fakt {FAKT_KARTY})")


def _zgoda_na_strone(witryna: str, sk: str, st: dict, blad) -> None:
    """Krok `strona` potrzebuje zgody: Always allow dla tej strony w tej drodze albo Allow once tuż przed nim (zużywa się na jednym kroku)."""
    if witryna in st["zgody_stron"]:
        return
    if st["jednorazowa"] == witryna:
        st["jednorazowa"] = None
    elif witryna in st["odmowy"]:
        blad(sk, f"krok strona z witryna „{witryna}” po odmowie (Deny): Claude na tę stronę nie wchodzi; strona pojawi się dopiero po nowej karcie z Allow once albo Always allow (fakt {FAKT_KARTY})")
    else:
        blad(sk, f"działanie na cudzej stronie bez karty zgody (fakt {FAKT_KARTY}): krok strona z witryna „{witryna}” nie ma przed sobą klika allow_once (zgoda na jeden krok) ani wcześniejszego klika always_allow dla tej strony w tej drodze")


def krok(k: dict, sk: str, st: dict, blad) -> None:
    """Krok `strona`: cudza strona w panelu Browser (`witryna` i `strona`: sześć pól jak w kroku `plik` z .html i opcjonalne `pola`), bez klika w ścieżkę; wymaga zgody."""
    for pole in k:
        if pole not in POLA_KROKU:
            blad(sk, f"pole {pole} nie należy do kroku strona (pola: {', '.join(POLA_KROKU)})")
    witryna = k.get("witryna")
    if not _niepusty(witryna):
        blad(sk, "krok strona wymaga pola witryna: niepustego napisu, tej samej nazwy strony co w karcie zgody")
    else:
        _zgoda_na_strone(witryna, sk, st, blad)
    strona = k.get("strona")
    if not isinstance(strona, dict):
        blad(sk, "krok strona wymaga obiektu strona: sześć pól jak w kroku plik z .html (tytul, opis, program, cena, opinie, kontakt) i opcjonalne pola")
    else:
        sprawdz_strone({"nazwa": "strona.html", "strona": {p: w for p, w in strona.items() if p != "pola"}}, sk, blad)
        if "pola" in strona:
            sprawdz_pola(strona["pola"], sk, blad)
    st["strony"] += 1
    st["artefakt"] = None  # strona zajmuje panel Browser: widok artefaktu się zamyka, kolejny artefakt wymaga znów kliku w link
    st["konczy_slajdami"] = False  # ostatni podgląd to strona


def koniec(sd: str, st: dict, blad) -> None:
    """Koniec drogi: bez decyzji, na którą nie odpowiedział następny krok (strona po zezwoleniu, `claude` po Deny)."""
    if st["po_decyzji"]:
        cel, witryna = st["po_decyzji"]
        if cel == "deny":
            blad(sd, "po odmowie (Deny) droga nie ma odpowiedzi Claude")
        else:
            blad(sd, f"po zezwoleniu ({NAZWY_KLIKOW[cel]}) droga nie ma kroku strona z witryna „{witryna}”")
