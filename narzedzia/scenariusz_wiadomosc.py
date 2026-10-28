"""Sprawdza w drogach symulatora aplikacji kartę wiadomości od innej rozmowy: pole `wiadomosc: {do, tekst}` kroku `claude` (Claude na prośbę kursanta wysyła wiadomość do drugiej rozmowy) i klik `wiadomosc-od` (odnośnik karty otwiera rozmowę nadawcy); opis: dane/FORMAT-SCENARIUSZA.md, część „Folder każdej rozmowy i karta wiadomości”."""

POLA = ("do", "tekst")
POLA_KLIKU = ("typ", "cel", "fakt")
MAKS_ZNAKOW = 600
FAKT_KARTY = "aplikacja-wiadomosc-karta-z-tytulem-nadawcy"
FAKT_PROSBY = "aplikacja-claude-czyta-inne-sesje-zwykla-prosba"
FAKT_ARCHIWUM = "aplikacja-wiadomosc-nie-dojdzie-do-archiwum"


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


def krok(k: dict, sk: str, st: dict, blad) -> None:
    """Pole `wiadomosc` (tylko w kroku `claude`): obiekt `{do, tekst}`, `do` to id innej rozmowy z `aplikacja.sesje` albo `aplikacja.id`, niezarchiwizowanej w tej drodze; nadawca (rozmowa otwarta) ma nazwę, a wiadomość odpowiada na prośbę kursanta w tej rozmowie. Dopisuje kartę do rozmowy odbiorcy."""
    if "wiadomosc" not in k:
        return
    s = st["sesje"]
    v = k["wiadomosc"]
    if k.get("typ") != "claude":
        blad(sk, f"pole wiadomosc tylko w kroku claude (jest w kroku „{k.get('typ')}”): wiadomość wysyła Claude (fakt {FAKT_KARTY})")
    elif not s["lista"]:
        blad(sk, f"wiadomosc tylko w ćwiczeniu z aplikacja.sesje: bez drugiej rozmowy nie ma odbiorcy (fakt {FAKT_KARTY})")
    elif not isinstance(v, dict) or set(v) != set(POLA):
        blad(sk, f"wiadomosc musi być obiektem {{{', '.join(POLA)}}}")
    elif not _niepusty(v["tekst"]) or len(v["tekst"]) > MAKS_ZNAKOW:
        blad(sk, f"wiadomosc.tekst musi być niepustym napisem do {MAKS_ZNAKOW} znaków")
    elif v["do"] not in s["ids"] and v["do"] != s["id_start"]:
        blad(sk, f"wiadomosc.do: rozmowa {v['do']!r} spoza aplikacja.sesje i aplikacja.id (fakt {FAKT_KARTY})")
    else:
        _karta(v, sk, s, blad)


def _karta(v: dict, sk: str, s: dict, blad) -> None:
    """Kontrole kolejności i dopisanie karty: odbiorca inny niż nadawca, nie w archiwum, nadawca z nazwą, wcześniejsza prośba kursanta."""
    odbiorca = None if v["do"] == s["id_start"] else v["do"]
    nadawca = s["otwarta"]
    if nadawca == "nowa":
        blad(sk, "wiadomosc z nowej rozmowy: karta ma tytuł rozmowy nadawcy, a nowa rozmowa nie ma nazwy (szary pasek zamiast tytułu udawałby napis)")
    elif odbiorca == nadawca:
        blad(sk, f"wiadomosc.do „{v['do']}” to rozmowa otwarta: wiadomość do samej siebie nie ma odbiorcy (fakt {FAKT_KARTY})")
    elif v["do"] in s["archiwum"]:
        blad(sk, f"wiadomosc do rozmowy „{v['do']}”, która została zarchiwizowana w tej drodze: Claude nie dostarczy wiadomości do archiwum (fakt {FAKT_ARCHIWUM})")
    elif not _niepusty(s["nazwy"].get(nadawca)):
        blad(sk, f"wiadomosc od rozmowy bez nazwy: karta ma w nagłówku tytuł nadawcy, więc rozmowa musi mieć nazwę (aplikacja.nazwa, sesje[].nazwa albo nazwa_sesji; fakt {FAKT_KARTY})")
    elif not s["prosba"]:
        blad(sk, f"wiadomosc bez prośby kursanta (krok pisz) w tej rozmowie: Claude wysyła wiadomość na zwykłą prośbę (fakt {FAKT_PROSBY})")
    else:
        s["karty"].setdefault(odbiorca, []).append(nadawca)


def klik(k: dict, sk: str, st: dict, blad):
    """Klik `wiadomosc-od` (bez pól): otwarta rozmowa musi mieć kartę, a jej nadawca nie może być zarchiwizowany. Zwraca `(True, klucz nadawcy)` (None = rozmowa startowa) albo `(False, None)`."""
    s = st["sesje"]
    for p in k:
        if p not in POLA_KLIKU:
            blad(sk, f"pole {p} nie należy do kliku wiadomosc-od (pola: {', '.join(POLA_KLIKU)})")
    nadawcy = s["karty"].get(s["otwarta"])
    if not nadawcy:
        blad(sk, f"klik wiadomosc-od w rozmowie bez karty wiadomości: odnośnika nie ma (fakt {FAKT_KARTY})")
    elif nadawcy[-1] in s["archiwum"]:
        blad(sk, f"klik wiadomosc-od: nadawca „{nadawcy[-1]}” został zarchiwizowany w tej drodze, jego wiersza nie ma już na liście")
    else:
        return True, nadawcy[-1]
    return False, None
