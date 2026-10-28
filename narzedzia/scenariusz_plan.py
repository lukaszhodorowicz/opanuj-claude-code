"""Sprawdza krok `plan` w ćwiczeniu aplikacji z etapami: kartę „Claude proposed a plan” z tytułem i sekcjami planu oraz przyciski accept, auto i revise z krokami granymi po kliknięciu (D-2026-10-26-54)."""

import copy

POLA = ("typ", "tytul", "sekcje", "przyciski", "fakt")
POLA_SEKCJI = ("naglowek", "punkty")
# tryb przełącznika po kliknięciu przycisku karty (ZRODLA.md, część „Skutki przycisków”)
TRYB_PO = {"accept": "Manual", "auto": "Auto", "revise": "Plan"}
ZGODA_W_PRZYCISKU = "krok zgoda w krokach przycisku karty planu: silnik nie zatwierdza tu karty zgody"
POLA_PRZYCISKU = {"accept": ("kroki",), "auto": ("kroki",), "revise": ("poprawka", "kroki")}


def _niepusty(w) -> bool:
    return isinstance(w, str) and bool(w.strip())


def _nieznane(obiekt: dict, dozwolone, s: str, blad) -> None:
    for pole in obiekt:
        if pole not in dozwolone:
            blad(s, f"nieznane pole {pole} (dozwolone: {', '.join(dozwolone)})")


def _sekcje(sekcje, sk: str, blad) -> None:
    if not isinstance(sekcje, list) or not sekcje:
        blad(sk, "plan wymaga niepustej listy sekcje")
        return
    for i, s in enumerate(sekcje):
        ss = f"{sk}/sekcje[{i}]"
        if not isinstance(s, dict):
            blad(ss, "sekcja musi być obiektem z polami naglowek i punkty")
            continue
        _nieznane(s, POLA_SEKCJI, ss, blad)
        punkty = s.get("punkty")
        if (
            not _niepusty(s.get("naglowek"))
            or not isinstance(punkty, list)
            or not punkty
            or not all(_niepusty(p) for p in punkty)
        ):
            blad(ss, "sekcja wymaga niepustego pola naglowek i niepustej listy punkty")


def krok_planu(k: dict, sk: str, stan: dict, blad, kroki) -> None:
    """Krok `plan` tylko w trybie Plan; `kroki(lista, ścieżka, stan)` sprawdza kroki przycisku jak kroki etapu, od stanu po kroku `plan` z trybem po kliknięciu."""
    _nieznane(k, POLA, sk, blad)
    if stan.get("tryb") != "Plan":
        blad(sk, f"krok plan tylko w trybie Plan (teraz „{stan.get('tryb')}”)")
    if not _niepusty(k.get("tytul")):
        blad(sk, "plan wymaga niepustego pola tytul")
    _sekcje(k.get("sekcje"), sk, blad)
    przyciski = k.get("przyciski", {})
    if not isinstance(przyciski, dict):
        blad(sk, "przyciski muszą być obiektem z kluczami accept, auto albo revise")
        return
    for klucz, p in przyciski.items():
        sp = f"{sk}/przyciski/{klucz}"
        if klucz not in TRYB_PO:
            blad(sk, f"nieznany przycisk {klucz} (karta ma działające: {', '.join(TRYB_PO)})")
            continue
        if not isinstance(p, dict):
            blad(sp, "przycisk musi być obiektem z polem kroki")
            continue
        _nieznane(p, POLA_PRZYCISKU[klucz], sp, blad)
        if klucz == "revise" and not _niepusty(p.get("poprawka")):
            blad(sp, "revise wymaga niepustego pola poprawka")
        lista = p.get("kroki")
        if not isinstance(lista, list):
            blad(sp, "przycisk wymaga listy kroki (może być pusta)")
            continue
        for n, kr in enumerate(lista):
            if isinstance(kr, dict) and kr.get("typ") == "zgoda":
                # w krokach przycisku nie ma etapu z `klik: zatwierdz`, więc karta zgody miałaby martwy przycisk
                blad(f"{sp}/kroki[{n}]", ZGODA_W_PRZYCISKU)
        po = copy.deepcopy(stan)  # każdy przycisk to osobna dalsza droga od stanu po karcie
        po["tryb"] = TRYB_PO[klucz]
        kroki(lista, sp, po)
