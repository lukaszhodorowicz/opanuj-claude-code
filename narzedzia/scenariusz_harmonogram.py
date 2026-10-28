"""Sprawdza w drogach symulatora aplikacji zadanie według harmonogramu: pole `aplikacja.harmonogram` (nazwa, polecenie, pora, częstotliwość, folder) i kliki `scheduled`, `new-task`, `advanced-settings`, `create` i `run-now` z ich kolejnością (opis: dane/FORMAT-SCENARIUSZA.md, część „Zadanie według harmonogramu”)."""

import re

GDZIE = "aplikacja"
CELE = ("scheduled", "new-task", "advanced-settings", "create", "run-now")
POLA = ("nazwa", "polecenie", "pora", "czestotliwosc", "folder")
POLA_KLIKU = ("typ", "cel", "fakt")
CZESTOTLIWOSCI = ("Daily",)  # napisy z listy „Daily” w oknie New scheduled task (zrzuty 05-04-51, 05-05-25); żaden zrzut nie pokazuje innej wartości listy
MAKS_NAZWA = 80
MAKS_POLECENIE = 400
MAKS_FOLDER = 60
WZOR_PORY = re.compile(r"([01]\d|2[0-3]):([0-5]\d)")


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


def godzina_12(pora: str) -> str:
    """Pora „09:20” w zapisie ze strony zadania („9:20 AM”): bez zera z przodu, 00:xx to 12:xx AM, 12:xx to 12:xx PM."""
    godz, minuty = int(pora[:2]), pora[3:]
    return f"{godz % 12 or 12}:{minuty} {'AM' if godz < 12 else 'PM'}"


def napisy_skladane(h: dict) -> tuple[str, str]:
    """Dwa napisy składane z pól harmonogramu, które rysuje strona zadania: „Next run: today at 9:20 AM” i „Daily at 9:20 AM”."""
    g = godzina_12(h["pora"])
    return f"Next run: today at {g}", f"{h['czestotliwosc']} at {g}"


def _tekst(h: dict, pole: str, maks: int, s: str, blad) -> None:
    wartosc = h.get(pole)
    if not _niepusty(wartosc):
        blad(s, f"harmonogram.{pole} musi być niepustym napisem")
    elif len(wartosc) > maks or any(ord(c) < 32 for c in wartosc):
        blad(s, f"harmonogram.{pole}: najwyżej {maks} znaków i bez znaków sterujących")


def pole(cw: dict, s: str, napisy, blad) -> None:
    """`aplikacja.harmonogram`: obiekt z polami nazwa, polecenie, pora („GG:MM”), czestotliwosc (napis z listy napisów, dziś tylko „Daily”) i folder (sama nazwa folderu); tylko w ćwiczeniu z drogami i bez `aplikacja.sesje` (zmiana rozmowy nie ma opisanego skutku dla strony zadań)."""
    apl = cw.get("aplikacja")
    if not isinstance(apl, dict) or "harmonogram" not in apl:
        return
    sh = f"{s}/aplikacja/harmonogram"
    h = apl["harmonogram"]
    if "drogi" not in cw:
        blad(sh, "harmonogram tylko w ćwiczeniu z drogami: pasek boczny ze Scheduled, strona Scheduled tasks i okno New scheduled task zmieniają kroki dróg")
    if "sesje" in apl:
        blad(sh, "harmonogram w ćwiczeniu z aplikacja.sesje: zmiana rozmowy nie ma opisanego skutku dla strony zadań (nie łączymy)")
    if not isinstance(h, dict):
        blad(sh, f"harmonogram musi być obiektem {{{', '.join(POLA)}}}")
        return
    for p in h:
        if p not in POLA:
            blad(sh, f"pole {p} nie należy do harmonogramu (pola: {', '.join(POLA)})")
    _tekst(h, "nazwa", MAKS_NAZWA, sh, blad)
    _tekst(h, "polecenie", MAKS_POLECENIE, sh, blad)
    folder = h.get("folder")
    if not _niepusty(folder) or "/" in folder or folder.startswith("~") or len(folder) > MAKS_FOLDER:
        blad(sh, f"harmonogram.folder: sama nazwa folderu, bez / i ~, najwyżej {MAKS_FOLDER} znaków")
    pora_ok = isinstance(h.get("pora"), str) and WZOR_PORY.fullmatch(h["pora"])
    if not pora_ok:
        blad(sh, "harmonogram.pora musi mieć postać „GG:MM” (24 godziny, np. „09:20”)")
    czest = h.get("czestotliwosc")
    if czest not in CZESTOTLIWOSCI:
        blad(sh, f"harmonogram.czestotliwosc „{czest}” spoza {'/'.join(CZESTOTLIWOSCI)}: tylko napis z listy w oknie New scheduled task widoczny na zrzucie")
    elif napisy is not None and not napisy.jest(czest, GDZIE):
        blad(sh, f"harmonogram.czestotliwosc „{czest}” spoza listy napisów interfejsu aplikacji")
    if pora_ok and czest in CZESTOTLIWOSCI and napisy is not None:
        for tekst in napisy_skladane(h):
            if not napisy.jest(tekst, GDZIE):
                blad(sh, f"napis „{tekst}” ze strony zadania nie pasuje do wzoru z listy napisów interfejsu aplikacji")


def stan(apl) -> dict:
    """Klucze stanu drogi: `harm_pole` (ćwiczenie ma `aplikacja.harmonogram`), `harm_widok` (None = rozmowa, „lista” = strona Scheduled tasks, „okno” = okno New scheduled task nad nią, „zadanie” = strona zadania), `harm_byla` (był klik `scheduled`), `harm_adv` (Advanced settings rozwinięte) i `harm_bieg` (był klik `run-now`)."""
    return {"harm_pole": isinstance(apl, dict) and "harmonogram" in apl, "harm_widok": None, "harm_byla": False, "harm_adv": False, "harm_bieg": False}


def pokazuje(st: dict) -> bool:
    """Droga z klikiem `scheduled` może się skończyć bez kroku `plik` i `artefakt`: pokazuje stronę harmonogramu zamiast rozmowy."""
    return st["harm_byla"]


def kolejnosc(k: dict, sk: str, st: dict, blad) -> None:
    """Przed każdym krokiem drogi: gdy stoi strona harmonogramu (lista, okno albo strona zadania), rozmowa jest schowana, więc dalej tylko `nauczyciel` i kliki harmonogramu (prośba, odpowiedź Claude, plik, karta i pozostałe kliki nie mają tam miejsca)."""
    typ = k.get("typ")
    if st["harm_widok"] and typ != "nauczyciel" and not (typ == "klik" and k.get("cel") in CELE):
        blad(sk, f"krok {typ} przy otwartej stronie harmonogramu: rozmowa jest schowana, dalej tylko nauczyciel i kliki {', '.join(CELE)}")


def klik(k: dict, sk: str, st: dict, blad) -> None:
    """Kliki harmonogramu w kolejności: `scheduled` (pasek boczny → strona Scheduled tasks, raz w drodze), `new-task` (okno New scheduled task z polami z `aplikacja.harmonogram`), `advanced-settings` (rozwija sekcję, raz), `create` (zamyka okno → strona zadania), `run-now` (na stronie zadania, raz: w History pojawia się jeden wpis przebiegu)."""
    cel = k["cel"]
    for p in k:
        if p not in POLA_KLIKU:
            blad(sk, f"pole {p} nie należy do kliku {cel} (pola: {', '.join(POLA_KLIKU)})")
    if not st["harm_pole"]:
        blad(sk, f"klik {cel} w ćwiczeniu bez aplikacja.harmonogram: pozycja Scheduled w pasku bocznym istnieje tylko z tym polem")
        return
    w = st["harm_widok"]
    if cel == "scheduled":
        if w is not None or st["harm_byla"]:
            blad(sk, "klik scheduled poza rozmową albo drugi raz w drodze: z strony harmonogramu symulator nie wraca do rozmowy")
        else:
            st["harm_widok"], st["harm_byla"] = "lista", True
    elif cel == "new-task":
        if w != "lista":
            blad(sk, "klik new-task bez otwartej strony Scheduled tasks: najpierw klik scheduled")
        else:
            st["harm_widok"] = "okno"
    elif cel == "advanced-settings":
        if w != "okno":
            blad(sk, "klik advanced-settings bez otwartego okna New scheduled task: najpierw klik new-task")
        elif st["harm_adv"]:
            blad(sk, "klik advanced-settings drugi raz: sekcja jest już rozwinięta")
        else:
            st["harm_adv"] = True
    elif cel == "create":
        if w != "okno":
            blad(sk, "klik create bez otwartego okna New scheduled task: najpierw klik new-task")
        else:
            st["harm_widok"] = "zadanie"
    elif w != "zadanie":
        blad(sk, "klik run-now bez strony zadania: najpierw klik create")
    elif st["harm_bieg"]:
        blad(sk, "klik run-now drugi raz: historia pokazuje jeden wpis przebiegu")
    else:
        st["harm_bieg"] = True
