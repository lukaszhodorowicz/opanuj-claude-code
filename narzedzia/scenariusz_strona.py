"""Sprawdza pole `strona` kroku `plik` w drodze symulatora aplikacji: rysunek strony oferty w panelu Browser (tytuł, opis, program, cena, opinie, kontakt) i nic ponad to; opcjonalne `pola` (ramki z tekstem) dopuszcza tylko krok `strona` (scenariusz_zgoda_strona)."""

POLA = ("tytul", "opis", "program", "cena", "opinie", "kontakt")
NAPISY = ("tytul", "opis", "cena", "kontakt")
LICZBA_PUNKTOW_PROGRAMU = 3
# elementy, które na stronie wyglądałyby na klikalne albo dałyby coś ponad opis dokumentacji
ODRZUCONE = ("przycisk", "formularz", "obraz", "adres", "link")
ROZSZERZENIE = ".html"
MAKS_POL = 4  # `pola` kroku `strona`: 1-4 ramek z etykietą nad ramką
POLA_RAMKI = ("etykieta", "wartosc")


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


def _lista(wartosc, s, pole, blad, dokladnie=None) -> None:
    """Lista niepustych napisów (z `dokladnie` pozycji, gdy podane)."""
    if not isinstance(wartosc, list) or not wartosc:
        blad(s, f"strona: pole {pole} musi być niepustą listą napisów")
    elif dokladnie and len(wartosc) != dokladnie:
        blad(s, f"strona: pole {pole} ma mieć dokładnie {dokladnie} pozycje, jest {len(wartosc)}")
    elif not all(_niepusty(p) for p in wartosc):
        blad(s, f"strona: każda pozycja pola {pole} musi być niepustym napisem")


def sprawdz_strone(krok: dict, s: str, blad) -> None:
    """Krok `plik` z polem `strona`: tylko dla pliku .html, bez `linijki`, z dokładnie sześcioma polami strony oferty."""
    if not str(krok.get("nazwa", "")).endswith(ROZSZERZENIE):
        blad(s, f"pole strona tylko dla pliku {ROZSZERZENIE}, a plik „{krok.get('nazwa')}” ma inne rozszerzenie")
    if "linijki" in krok:
        blad(s, "krok plik ma albo strona, albo linijki")
    strona = krok["strona"]
    if not isinstance(strona, dict):
        blad(s, "pole strona musi być obiektem")
        return
    for pole in strona:
        if pole in ODRZUCONE:
            blad(s, f"strona: pole {pole} odrzucone, symulator nie rysuje niczego, co wygląda na klikalne ani nie jest w opisie")
        elif pole == "pola":
            blad(s, "strona: pole pola tylko w kroku strona (cudza strona po karcie zgody), nie w kroku plik ani w artefakcie")
        elif pole not in POLA:
            blad(s, f"strona: nieznane pole {pole} (dozwolone: {', '.join(POLA)})")
    for pole in POLA:
        if pole not in strona:
            blad(s, f"strona: brak pola {pole}")
    for pole in NAPISY:
        if pole in strona and not _niepusty(strona[pole]):
            blad(s, f"strona: pole {pole} musi być niepustym napisem")
    if "program" in strona:
        _lista(strona["program"], s, "program", blad, LICZBA_PUNKTOW_PROGRAMU)
    if "opinie" in strona:
        _lista(strona["opinie"], s, "opinie", blad)


def sprawdz_pola(pola, s: str, blad) -> None:
    """Pole `pola` strony w kroku `strona`: lista 1-4 obiektów `etykieta` (niepusty napis) i `wartosc` (napis, pusty daje pustą ramkę); ramka nie jest polem formularza, więc nic ponad te dwa pola."""
    if not isinstance(pola, list) or not 1 <= len(pola) <= MAKS_POL:
        blad(s, f"strona: pole pola musi być listą od 1 do {MAKS_POL} obiektów (etykieta, wartosc)")
        return
    for i, p in enumerate(pola):
        sp = f"{s}/strona/pola[{i}]"
        if not isinstance(p, dict):
            blad(sp, "strona: każda pozycja pola pola musi być obiektem (etykieta, wartosc)")
            continue
        for pole in p:
            if pole not in POLA_RAMKI:
                blad(sp, f"strona: pola[{i}]: nieznane pole {pole} (dozwolone: {', '.join(POLA_RAMKI)}); ramka nie jest polem formularza, bez typu, podpowiedzi i przycisku")
        if not _niepusty(p.get("etykieta")):
            blad(sp, f"strona: pola[{i}]: etykieta musi być niepustym napisem")
        if not isinstance(p.get("wartosc"), str):
            blad(sp, f"strona: pola[{i}]: wartosc musi być napisem (pusty napis daje pustą ramkę)")
