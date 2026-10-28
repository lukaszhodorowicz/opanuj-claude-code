"""Sprawdza widok strony artefaktu w ćwiczeniu aplikacji z drogami: pole `link` kroku `claude`, krok `artefakt` (strona albo slajdy, podmiana w miejscu), `aplikacja.artefakt_otwarty` i `widok_klienta` (przełącznik „Tak widzisz Ty / Tak zobaczy klient”)."""

import re

from narzedzia.scenariusz_strona import sprawdz_strone

ADRES_ARTEFAKTU = re.compile(r"https://claude\.ai/code/artifact/[A-Za-z0-9_-]+")
SKROCONY = "https://claude.ai/…"  # skrócony adres prezentacji (jeden znak U+2026); wolno go tylko w drodze kończącej się slajdami
POLA_WIDOKU = ("ty", "klient", "podpis")
POLA_OPCJONALNE = ("objasnienie",)  # polskie objaśnienie napisu gościa w widoku klienta; te same reguły co podpis, ale może zabraknąć
POLA_SLAJDU = ("tytul", "punkty", "nadtytul")  # nadtytul: nieobowiązkowy napis nad tytułem slajdu (wersaliki tylko z CSS)
POLA_KROKU = ("typ", "tytul", "strona", "slajdy", "fakt")
PUNKTY_SLAJDU = (2, 4)
# napisy interfejsu: teksty przełącznika to element kursu, więc nie mogą udawać interfejsu
GDZIE_INTERFEJSU = ("aplikacja", "claude.ai")


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


def link_odpowiedzi(k: dict, sk: str, blad) -> str | None:
    """Pole `link` kroku `claude`: adres artefaktu, który stoi w polu `tekst`; zwraca go (albo None)."""
    if "link" not in k:
        return None
    link = k["link"]
    if not _niepusty(link) or not (ADRES_ARTEFAKTU.fullmatch(link) or link == SKROCONY):
        blad(sk, f"pole link musi być adresem https://claude.ai/code/artifact/<id> (albo skróconym {SKROCONY})")
        return None
    if link not in str(k.get("tekst", "")):
        blad(sk, f"tekst odpowiedzi nie zawiera linku „{link}”")
    return link


def droga_ze_skroconym(stan: dict, sd: str, blad) -> None:
    """Po krokach drogi: skrócony adres wolno tylko tam, gdzie ostatni podgląd (plik albo artefakt) to artefakt ze slajdy."""
    if stan.get("skrocony") and not stan.get("konczy_slajdami"):
        blad(sd, f"adres {SKROCONY} tylko w drodze, której ostatni podgląd to artefakt ze slajdy")


def _slajdy(slajdy, s: str, blad) -> None:
    """Lista slajdów (tytul + 2-4 punkty); na razie tylko miejsce w formacie, symulator ich nie rysuje."""
    if not isinstance(slajdy, list) or not slajdy:
        blad(s, "slajdy muszą być niepustą listą obiektów (tytul, punkty)")
        return
    for i, sl in enumerate(slajdy):
        ss = f"{s}/slajdy[{i}]"
        if not isinstance(sl, dict):
            blad(ss, "slajd musi być obiektem (tytul, punkty)")
            continue
        for pole in sl:
            if pole not in POLA_SLAJDU:
                blad(ss, f"slajd: nieznane pole {pole} (dozwolone: {', '.join(POLA_SLAJDU)})")
        if not _niepusty(sl.get("tytul")):
            blad(ss, "slajd wymaga niepustego pola tytul")
        if "nadtytul" in sl and not _niepusty(sl["nadtytul"]):
            blad(ss, "slajd: pole nadtytul musi być niepustym napisem")
        punkty = sl.get("punkty")
        if not isinstance(punkty, list) or not PUNKTY_SLAJDU[0] <= len(punkty) <= PUNKTY_SLAJDU[1] or not all(_niepusty(p) for p in punkty):
            blad(ss, f"slajd wymaga pola punkty: {PUNKTY_SLAJDU[0]}-{PUNKTY_SLAJDU[1]} niepustych napisów")


def tresc_artefaktu(dane: dict, s: str, blad) -> None:
    """`tytul` i dokładnie jedno z `strona` (sześć pól jak w kroku plik .html) albo `slajdy`."""
    if not _niepusty(dane.get("tytul")):
        blad(s, "artefakt wymaga niepustego pola tytul")
    if "strona" in dane and "slajdy" in dane:
        blad(s, "artefakt ma albo strona, albo slajdy")
    elif "strona" in dane:
        sprawdz_strone({"nazwa": "artefakt.html", "strona": dane["strona"]}, s, blad)
    elif "slajdy" in dane:
        _slajdy(dane["slajdy"], s, blad)
    else:
        blad(s, "artefakt wymaga pola strona albo slajdy")


def krok(k: dict, sk: str, stan: dict, po_linku, blad) -> None:
    """Krok `artefakt` drogi: otwiera widok zaraz po kroku klik w link albo podmienia stronę w otwartym widoku (ten sam tytuł)."""
    for pole in k:
        if pole not in POLA_KROKU:
            blad(sk, f"artefakt: nieznane pole {pole} (dozwolone: {', '.join(POLA_KROKU[1:])})")
    tresc_artefaktu(k, sk, blad)
    otwarty = stan["artefakt"]
    if not po_linku and otwarty is None:
        blad(sk, "artefakt otwiera się tylko zaraz po kroku klik w link (albo od startu: aplikacja.artefakt_otwarty)")
    elif otwarty is not None and k.get("tytul") != otwarty:
        blad(sk, f"podmiana w miejscu wymaga tego samego tytulu: otwarty „{otwarty}”, krok ma „{k.get('tytul')}”")
    if _niepusty(k.get("tytul")) and otwarty is None:
        stan["artefakt"] = k["tytul"]
    stan["widoki"] += 1
    stan["konczy_slajdami"] = "slajdy" in k


def _widok_klienta(cw: dict, s: str, napisy, blad) -> None:
    dane = cw["widok_klienta"]
    sw = f"{s}/widok_klienta"
    if not isinstance(dane, dict):
        blad(sw, "widok_klienta musi być obiektem (ty, klient, podpis, objasnienie)")
        return
    for pole in dane:
        if pole not in POLA_WIDOKU + POLA_OPCJONALNE:
            blad(sw, f"widok_klienta: nieznane pole {pole} (dozwolone: {', '.join(POLA_WIDOKU + POLA_OPCJONALNE)})")
    for pole in POLA_WIDOKU + tuple(p for p in POLA_OPCJONALNE if p in dane):
        if not _niepusty(dane.get(pole)):
            blad(sw, f"widok_klienta wymaga niepustego pola {pole}")
        elif any(napisy.jest(dane[pole], g) for g in GDZIE_INTERFEJSU):
            blad(sw, f"widok_klienta: pole {pole} „{dane[pole]}” to napis interfejsu; przełącznik jest elementem kursu")
    if not any(isinstance(k, dict) and k.get("typ") == "artefakt" for d in cw.get("drogi") or [] if isinstance(d, dict) for k in d.get("kroki") or []) and "artefakt_otwarty" not in (cw.get("aplikacja") or {}):
        blad(sw, "widok_klienta bez widoku artefaktu: ćwiczenie nie ma kroku artefakt ani aplikacja.artefakt_otwarty")


def kto_otworzy(cw: dict, s: str, blad) -> None:
    """Pole `aplikacja.kto_otworzy` zostało usunięte; błąd w każdym ćwiczeniu aplikacji, także z `etapy`."""
    apl = cw.get("aplikacja")
    if isinstance(apl, dict) and "kto_otworzy" in apl:
        blad(f"{s}/aplikacja/kto_otworzy", "pole usunięte, użyj widok_klienta")


def sprawdz_cwiczenie(cw: dict, apl: dict, sa: str, s: str, napisy, blad) -> str | None:
    """Pola ćwiczenia: `aplikacja.artefakt_otwarty` i `widok_klienta`; zwraca tytuł artefaktu otwartego od startu (albo None)."""
    otwarty = None
    if "artefakt_otwarty" in apl:
        so = f"{sa}/artefakt_otwarty"
        dane = apl["artefakt_otwarty"]
        if "drogi" not in cw:
            blad(so, "artefakt_otwarty tylko w ćwiczeniu z drogami")
        if not isinstance(dane, dict):
            blad(so, "artefakt_otwarty musi być obiektem (tytul, strona)")
        else:
            for pole in dane:
                if pole not in ("tytul", "strona", "slajdy"):
                    blad(so, f"artefakt_otwarty: nieznane pole {pole} (dozwolone: tytul, strona, slajdy)")
            tresc_artefaktu(dane, so, blad)
            otwarty = dane["tytul"] if _niepusty(dane.get("tytul")) else None
    if "widok_klienta" in cw:
        _widok_klienta(cw, s, napisy, blad)
    return otwarty
