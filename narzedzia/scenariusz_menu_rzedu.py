"""Sprawdza w ćwiczeniu z drogami symulatora aplikacji menu w rzędzie pod polem otwierane krokiem `klik`: listę trybów (cele `tryb-menu` i `tryb` z polem `na`) i menu środowiska (cel `srodowisko-menu`), ich kolejność i menu otwarte na końcu drogi (opis: dane/FORMAT-SCENARIUSZA.md, część „Paczka 4A”, punkty „Lista trybów w drogach” i „Menu środowiska”)."""

KLIKI = ("tryb-menu", "tryb", "srodowisko-menu")
TRYBY = ("Auto", "Manual", "Accept edits", "Plan")  # kolejność listy trybów ze zrzutu 04-41-10; ta sama stała jest w scenariusz_aplikacja.TRYBY_APLIKACJI (tu osobno: tamten moduł importuje drogi, które importują ten)
BYPASS = "Bypass permissions"
POLA_KLIKU = {"tryb-menu": ("typ", "cel", "fakt"), "tryb": ("typ", "cel", "na", "fakt"), "srodowisko-menu": ("typ", "cel", "fakt")}
PRZY_MENU = ("nauczyciel",)  # krok dozwolony przy otwartej liście trybów poza kliknięciem pozycji, a po otwarciu menu środowiska jedyny


def jest_w_drogach(cw: dict) -> bool:
    """Czy któraś droga ćwiczenia ma krok `klik` z celem `tryb-menu` albo `tryb` (lista trybów w drogach: wtedy `aplikacja.bypass_dostepny` ma sens)."""
    return any(
        isinstance(k, dict) and k.get("typ") == "klik" and k.get("cel") in ("tryb-menu", "tryb")
        for d in (cw.get("drogi") if isinstance(cw.get("drogi"), list) else [])
        if isinstance(d, dict)
        for k in (d.get("kroki") if isinstance(d.get("kroki"), list) else [])
    )


def stan(apl: dict) -> dict:
    """Klucz stanu drogi `menu_rzedu`: `tryb` (tryb na przełączniku, na starcie z `aplikacja.tryb`), `lista` (lista trybów otwarta), `srodowisko` (menu środowiska otwarte), `bypass` (pole `aplikacja.bypass_dostepny` jest prawdą: lista ma Bypass permissions) i `lokalne` (sesja `Local`)."""
    apl = apl if isinstance(apl, dict) else {}
    return {"menu_rzedu": {"tryb": apl.get("tryb"), "lista": False, "srodowisko": False, "bypass": apl.get("bypass_dostepny") is True, "lokalne": apl.get("srodowisko") == "Local"}}


def kolejnosc(k: dict, sk: str, st: dict, blad) -> None:
    """Przed każdym krokiem drogi: przy otwartej liście trybów dalej tylko `nauczyciel` i klik `tryb` (lista zamyka się dopiero wyborem pozycji), a po otwarciu menu środowiska tylko `nauczyciel` (menu zostaje otwarte do końca drogi)."""
    m = st["menu_rzedu"]
    typ, cel = k.get("typ"), k.get("cel") if k.get("typ") == "klik" else None
    if m["srodowisko"] and typ not in PRZY_MENU:
        blad(sk, f"krok {typ} po otwarciu menu środowiska: dalej tylko nauczyciel (menu zostaje otwarte do końca drogi, a jego pozycje nie mają skutku)")
    elif m["lista"] and typ not in PRZY_MENU and cel != "tryb":
        blad(sk, f"krok {typ} przy otwartej liście trybów: dalej tylko nauczyciel i klik „tryb” (lista zamyka się dopiero wyborem pozycji)")


def klik(k: dict, sk: str, st: dict, napisy, blad) -> None:
    """Klik `tryb-menu` (otwiera listę trybów z przełącznika), `tryb` (zaraz po nim: wybiera pozycję `na`, przełącznik dostaje jej napis, lista się zamyka) albo `srodowisko-menu` (otwiera menu środowiska, sesja `Local`)."""
    cel, m = k["cel"], st["menu_rzedu"]
    for p in k:
        if p not in POLA_KLIKU[cel]:
            blad(sk, f"pole {p} nie należy do kroku klik z celem {cel} (pola: {', '.join(POLA_KLIKU[cel])})")
    if cel == "tryb-menu":
        if m["lista"]:
            blad(sk, "klik „tryb-menu” przy otwartej liście trybów: najpierw klik „tryb”, który ją zamyka")
        m["lista"] = True
    elif cel == "tryb":
        _tryb(k, sk, m, napisy, blad)
    else:
        if not m["lokalne"]:
            blad(sk, "klik „srodowisko-menu” tylko w sesji aplikacja.srodowisko „Local”: zrzut menu środowiska pokazuje sesję lokalną (This computer z haczykiem)")
        if m["srodowisko"]:
            blad(sk, "klik „srodowisko-menu”, gdy menu środowiska jest już otwarte")
        m["srodowisko"] = True


def _tryb(k: dict, sk: str, m: dict, napisy, blad) -> None:
    """Klik `tryb`: lista musi być otwarta, `na` to pozycja listy (Auto, Manual, Accept edits, Plan, a Bypass permissions tylko przy `aplikacja.bypass_dostepny: true`) inna niż tryb na przełączniku."""
    na = k.get("na")
    if not m["lista"]:
        blad(sk, "klik „tryb” bez otwartej listy trybów: najpierw klik „tryb-menu”")
    mozliwe = (*TRYBY, *((BYPASS,) if m["bypass"] else ()))
    if not napisy.jest(na, "aplikacja"):
        blad(sk, f"na „{na}” spoza listy napisów interfejsu aplikacji")
    elif na not in mozliwe:
        blad(sk, f"na „{na}” spoza listy trybów w oknie ({' / '.join(mozliwe)}{'' if m['bypass'] else '; Bypass permissions dopiero z aplikacja.bypass_dostepny: true'})")
    elif na == m["tryb"]:
        blad(sk, f"tryb „{na}” już jest na przełączniku")
    m["tryb"], m["lista"] = na, False


def koniec(sd: str, st: dict, blad) -> None:
    """Koniec drogi: lista trybów nie może zostać otwarta (po `tryb-menu` musi być klik `tryb`); menu środowiska może."""
    if st["menu_rzedu"]["lista"]:
        blad(sd, "droga kończy się przy otwartej liście trybów: po kliku „tryb-menu” musi być klik „tryb”")
