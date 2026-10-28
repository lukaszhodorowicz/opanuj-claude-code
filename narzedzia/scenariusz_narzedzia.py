"""Sprawdza kroki `narzedzie` i `wynik` w przebiegu: napisy wywołań i wyników oraz to, czy nad każdym `wynik` stoi wywołanie narzędzia."""


def _linie_wyniku(wynik: list, s: str, napisy, pliki: set[str], blad) -> None:
    """Każda linia wyniku z listy napisów interfejsu (miejsce `wynik`) albo nazwa pliku z folderu scenariusza."""
    for j, linia in enumerate(wynik):
        if not isinstance(linia, str) or (
            not napisy.jest(linia, "wynik") and linia not in pliki
        ):
            blad(f"{s}/wynik[{j}]", f"wynik „{linia}” spoza listy napisów interfejsu")


def krok_narzedzia(krok: dict, s: str, napisy, pliki: set[str], blad) -> None:
    """Krok `narzedzie`: nazwa z listy napisów, arg jako napis, wynik (lista, może być pusta albo pominięta)."""
    if not napisy.jest(krok.get("nazwa"), "narzedzie"):
        blad(s, f"narzędzie „{krok.get('nazwa')}” spoza listy napisów interfejsu")
    if not isinstance(krok.get("arg"), str):
        blad(s, "narzędzie wymaga pola arg")
    if "wynik" not in krok:
        return
    if not isinstance(krok["wynik"], list):
        blad(s, "pole wynik narzędzia musi być listą")
        return
    _linie_wyniku(krok["wynik"], s, napisy, pliki, blad)


def krok_wyniku(krok: dict, s: str, napisy, pliki: set[str], blad) -> None:
    """Krok `wynik`: niepusta lista linii, każda sprawdzana jak wynik kroku `narzedzie`."""
    wynik = krok.get("wynik")
    if not isinstance(wynik, list) or not wynik:
        blad(s, "krok „wynik” wymaga niepustej listy wynik")
        return
    _linie_wyniku(wynik, s, napisy, pliki, blad)


def sprawdz_kolejnosc_wynikow(kroki, s: str, blad) -> None:
    """Zgłasza krok `wynik` bez wcześniejszego kroku `narzedzie`; gałąź menu dziedziczy stan sprzed menu."""
    _idz(kroki, False, s, blad)


def _idz(kroki, bylo_narzedzie: bool, s: str, blad) -> None:
    if not isinstance(kroki, list):
        return
    for i, krok in enumerate(kroki):
        if not isinstance(krok, dict):
            continue
        typ = krok.get("typ")
        if typ == "narzedzie":
            bylo_narzedzie = True
        elif typ == "wynik" and not bylo_narzedzie:
            blad(
                f"{s}[{i}]",
                "krok „wynik” bez wcześniejszego kroku narzedzie w przebiegu",
            )
        elif typ == "menu" and isinstance(krok.get("opcje"), list):
            for j, op in enumerate(krok["opcje"]):
                if isinstance(op, dict):
                    _idz(
                        op.get("dalej"),
                        bylo_narzedzie,
                        f"{s}[{i}]/opcje[{j}]/dalej",
                        blad,
                    )
