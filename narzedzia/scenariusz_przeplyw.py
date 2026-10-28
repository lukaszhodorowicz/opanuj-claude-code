"""Sprawdza w drogach symulatora aplikacji kartę zgody na przepływ (krok `przeplyw`: nazwa i fazy; klik `once`, który kończy kartę i dodaje wpis przepływu do pracy w tle z scenariusz_w_tle) oraz kolejność kroków wokół niej (opis: dane/FORMAT-SCENARIUSZA.md, część „Karta zgody na przepływ”)."""

from narzedzia import scenariusz_w_tle

TYPY = ("przeplyw",)
KLIKI = ("once",)
TRYBY = ("Manual", "Accept edits")  # karta tylko w tych trybach: dla Auto i Bypass dokumentacja aplikacji milczy (umowa symulatora)
POLA_KROKU = ("typ", "nazwa", "fazy", "fakt")
POLA_KLIKU = ("typ", "cel", "fakt")
MAKS_NAZWA = 80
MAKS_FAZA = 60
FAZY_OD, FAZY_DO = 1, 6
FAKT_KARTY = "przeplyw-aplikacja-karta-zgody"  # tylko w komunikatach: fakt leży na gałęzi lekcji, więc scenariusz nie musi go mieć


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


def _tekst_ok(wartosc, maks: int) -> bool:
    return _niepusty(wartosc) and len(wartosc) <= maks and not any(ord(c) < 32 for c in wartosc)


def stan(apl) -> dict:
    """Klucze stanu drogi: `przeplyw_czeka` (nazwa karty, która czeka na Once, albo None), `przeplyw_trwa` (przepływ po Once pracuje w tle), `przeplyw_tryb` (tryb ćwiczenia) i `przeplyw_sesje` (ćwiczenie ma pasek boczny z rozmowami)."""
    apl = apl if isinstance(apl, dict) else {}
    return {"przeplyw_czeka": None, "przeplyw_trwa": False, "przeplyw_tryb": apl.get("tryb"), "przeplyw_sesje": "sesje" in apl}


def kolejnosc(k: dict, sk: str, st: dict, blad) -> None:
    """Przed każdym krokiem drogi: przy karcie, która czeka, dalej tylko `nauczyciel` albo klik `once`; wpis przepływu w `w_tle` kroku `claude` to błąd w każdej drodze (wpis dodaje tylko klik `once`)."""
    typ = k.get("typ")
    if st["przeplyw_czeka"] is not None and typ != "nauczyciel" and not (typ == "klik" and k.get("cel") == "once"):
        blad(sk, f"krok {typ} przy karcie przepływu, która czeka: Claude czeka na Twój wybór, dalej tylko nauczyciel albo klik „once” (fakt {FAKT_KARTY})")
    if typ == "claude" and isinstance(k.get("w_tle"), list):
        if any(isinstance(w, dict) and w.get("rodzaj") == "przeplyw" for w in k["w_tle"]):
            blad(sk, f"w_tle z rodzajem przeplyw: przeplyw tylko z karty zgody, wpis przepływu dodaje klik „once” na karcie (krok przeplyw; fakt {FAKT_KARTY})")


def krok(k: dict, sk: str, st: dict, blad) -> None:
    """Krok `przeplyw`: `nazwa` (niepusty napis do 80 znaków) i `fazy` (1-6 niepustych napisów do 60 znaków); tryb Manual albo Accept edits; bez paska bocznego z rozmowami; druga karta dopiero po `w_tle_koniec` poprzedniego przepływu."""
    for p in k:
        if p not in POLA_KROKU:
            blad(sk, f"pole {p} nie należy do kroku przeplyw (pola: {', '.join(POLA_KROKU)})")
    if st["przeplyw_tryb"] not in TRYBY:
        blad(sk, f"karta zgody na przepływ tylko w trybie {' albo '.join(TRYBY)} (teraz „{st['przeplyw_tryb']}”): dokumentacja aplikacji nie mówi, czy karta pokazuje się w innych trybach (fakt {FAKT_KARTY})")
    if st["przeplyw_sesje"]:
        blad(sk, "karta zgody na przepływ w ćwiczeniu z aplikacja.sesje: zmiana rozmowy nie ma opisanego skutku dla karty i wpisu w tle (nie łączymy)")
    if st["przeplyw_trwa"] and not st["w_tle_koniec"]:
        blad(sk, "druga karta przepływu przed w_tle_koniec poprzedniego: dwa przepływy naraz nie mają źródła, druga karta dopiero po kroku claude z w_tle_koniec")
    nazwa = k.get("nazwa")
    if not _tekst_ok(nazwa, MAKS_NAZWA):
        blad(sk, f"przeplyw: nazwa musi być niepustym napisem do {MAKS_NAZWA} znaków, bez znaków sterujących")
    fazy = k.get("fazy")
    if not isinstance(fazy, list) or not FAZY_OD <= len(fazy) <= FAZY_DO or not all(_tekst_ok(f, MAKS_FAZA) for f in fazy):
        blad(sk, f"przeplyw: fazy muszą być listą {FAZY_OD}-{FAZY_DO} niepustych napisów do {MAKS_FAZA} znaków, bez znaków sterujących")
    st["przeplyw_czeka"] = nazwa if isinstance(nazwa, str) else "?"
    st["przeplyw_trwa"] = False


def klik(k: dict, sk: str, st: dict, napisy, blad) -> None:
    """Klik `once`: wymaga karty, która czeka. Karta traci przyciski, a do pracy w tle dochodzi wpis przepływu (po `w_tle_koniec` poprzedniej pracy lista prac zaczyna się od nowa, panel zadań się zamyka); przy co najmniej dwóch pracach pod odpowiedzią stoi odnośnik „N running tasks”, którego napis musi pasować do wzoru z listy napisów."""
    for p in k:
        if p not in POLA_KLIKU:
            blad(sk, f"pole {p} nie należy do kliku once (pola: {', '.join(POLA_KLIKU)})")
    nazwa = st["przeplyw_czeka"]
    if nazwa is None:
        blad(sk, f"klik once bez karty przepływu, która czeka na decyzję (krok przeplyw; fakt {FAKT_KARTY})")
        return
    st["przeplyw_czeka"] = None
    st["przeplyw_trwa"] = True
    if st["w_tle_koniec"]:
        st["w_tle"], st["w_tle_koniec"], st["w_tle_panel"] = [], False, None
    st["w_tle"].append({"rodzaj": "przeplyw", "tytul": nazwa})
    if len(st["w_tle"]) > scenariusz_w_tle.MAKS_WPISOW:
        blad(sk, f"klik once: najwyżej {scenariusz_w_tle.MAKS_WPISOW} prac w tle w jednej drodze")
    n = len(st["w_tle"])
    odnosnik = f"{n} running tasks"
    if n >= scenariusz_w_tle.MIN_NA_ODNOSNIK and napisy is not None and not napisy.jest(odnosnik, scenariusz_w_tle.GDZIE):
        blad(sk, f"odnośnik „{odnosnik}” pod odpowiedzią nie pasuje do wzoru z listy napisów interfejsu aplikacji (fakt {scenariusz_w_tle.FAKT_ODNOSNIKA})")


def koniec(sd: str, st: dict, blad) -> None:
    """Droga nie kończy się kartą przepływu, która czeka na Once."""
    if st["przeplyw_czeka"] is not None:
        blad(sd, "droga kończy się kartą przepływu, która czeka na decyzję: dodaj klik „once”")
