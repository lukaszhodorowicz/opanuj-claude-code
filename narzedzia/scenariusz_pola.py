"""Sprawdza opcjonalne pola scenariusza (cele, opis, przycisk, uwaga i pokrewne) opisane w dane/FORMAT-SCENARIUSZA.md."""

POLA_NAPISY_CWICZENIA = ("opis", "przycisk", "przyklad", "tekst_startowy")


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


def pola_cwiczenia(cw: dict, s: str, pliki: set[str], blad) -> None:
    """Pola ćwiczenia: opis, przycisk, przyklad, tekst_startowy (niepuste napisy) i cele (plik → napis)."""
    for pole in POLA_NAPISY_CWICZENIA:
        if pole in cw and not _niepusty(cw[pole]):
            blad(s, f"pole {pole} musi być niepustym napisem")
    if "cele" not in cw:
        return
    cele = cw["cele"]
    if not isinstance(cele, dict):
        blad(s, "pole cele musi być obiektem (plik → napis celu)")
        return
    for plik, cel in cele.items():
        if plik not in pliki:
            blad(f"{s}/cele", f"plik „{plik}” nie istnieje w folder_startowy ani nie powstaje w przebiegu")
        if not _niepusty(cel):
            blad(f"{s}/cele", f"cel pliku „{plik}” musi być niepustym napisem")


def pola_zadania(z: dict, s: str, blad) -> None:
    """Pola zadania: opis (niepusty napis) i start_od_razu (prawda/fałsz)."""
    if "opis" in z and not _niepusty(z["opis"]):
        blad(s, "pole opis musi być niepustym napisem")
    if "start_od_razu" in z and not isinstance(z["start_od_razu"], bool):
        blad(s, "pole start_od_razu musi być prawdą albo fałszem")


def pola_folderu(krok: dict, s: str, blad) -> None:
    """Pola kroku folder: uwaga i plik (niepuste napisy, jeśli są), a w akcji edytuj liczby dodane i usuniete."""
    for pole in ("uwaga", "plik"):
        if pole in krok and not _niepusty(krok[pole]):
            blad(s, f"folder: pole {pole} musi być niepustym napisem")
    if krok.get("akcja") == "edytuj":
        _liczby_edycji(krok, s, blad)


def _liczba_linijek(wartosc) -> bool:
    return isinstance(wartosc, int) and not isinstance(wartosc, bool) and wartosc >= 0


def _liczby_edycji(krok: dict, s: str, blad) -> None:
    """Akcja edytuj: dodane i usuniete to liczby całkowite ≥ 0, nie obie równe 0."""
    dobre = True
    for pole in ("dodane", "usuniete"):
        if not _liczba_linijek(krok.get(pole)):
            blad(s, f"folder edytuj wymaga pola {pole} (liczba całkowita ≥ 0)")
            dobre = False
    if dobre and krok["dodane"] == 0 and krok["usuniete"] == 0:
        blad(s, "folder edytuj: dodane i usuniete równe 0 to brak zmiany; plik wrócił do stanu sprzed zadania, więc użyj przywroc")
