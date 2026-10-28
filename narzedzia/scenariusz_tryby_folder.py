"""Śledzi stan folderu w ćwiczeniu aplikacji z etapami i sprawdza krok `folder` (czyta, nowy, zmien, usun, utworz, przenies) oraz pliki zmian względem tego stanu (opis: dane/FORMAT-SCENARIUSZA-TRYBY.md)."""

from narzedzia.scenariusz_aplikacja import _niepusty

# akcja kroku `folder` -> pola, które do niej należą (poza typ, akcja i fakt)
AKCJE_FOLDERU = {
    "czyta": ("pliki",),
    "nowy": ("plik",),
    "zmien": ("plik", "nazwa"),
    "usun": ("plik",),
    "utworz": ("nazwa",),
    "przenies": ("plik", "do", "uwaga"),
}
POLA_WSPOLNE = ("typ", "akcja", "fakt")


def stan_folderu(start) -> dict:
    """Stan startowy: `gdzie` (plik -> teczka albo None dla luźnego), `zajete` (nazwy na kartach, także usuniętych), `znane` (każda nazwa, która kiedykolwiek była), `teczki`."""
    nazwy = [p for p in start if isinstance(p, str)]
    return {
        "gdzie": dict.fromkeys(nazwy),
        "zajete": set(nazwy),
        "znane": set(nazwy),
        "teczki": set(),
    }


def plik_zmiany(nazwa, sk, folder, co, blad) -> None:
    """Plik, który zmienia karta zgody albo krok `zmiana`, musi w tej chwili leżeć w folderze (po wcześniejszych zmianach nazw i usunięciach)."""
    if not _niepusty(nazwa) or nazwa in folder["gdzie"]:
        return
    if nazwa in folder["znane"]:
        blad(
            sk,
            f"plik „{nazwa}” już nie leży w folderze (usunięty albo ze zmienioną nazwą): {co}",
        )
    else:
        blad(sk, f"plik „{nazwa}” nie istnieje w folder_startowy: {co}")


def _nazwa(wartosc, pole, sk, akcja, blad) -> bool:
    """Niepusty napis bez ukośnika."""
    if not _niepusty(wartosc):
        blad(sk, f"folder {akcja} wymaga pola {pole}")
    elif "/" in wartosc:
        blad(sk, f"pole {pole} „{wartosc}” bez /: sama nazwa, bez ścieżki")
    else:
        return True
    return False


def _powod(nazwa, folder) -> str:
    return "usunięty albo ze zmienioną nazwą" if nazwa in folder["znane"] else "nie ma go w folder_startowy ani w krokach folderu"


def _istniejacy(k, pole, sk, folder, akcja, blad):
    """Nazwa z pola, jeśli plik leży teraz w folderze; inaczej None i błąd."""
    nazwa = k.get(pole)
    if not _nazwa(nazwa, pole, sk, akcja, blad):
        return None
    if nazwa in folder["gdzie"]:
        return nazwa
    blad(sk, f"folder {akcja}: plik „{nazwa}” nie leży w folderze ({_powod(nazwa, folder)})")
    return None


def _wolna_nazwa(k, pole, sk, folder, akcja, blad):
    """Nazwa z pola, jeśli żaden plik na kartach jej jeszcze nie nosi; inaczej None i błąd."""
    nazwa = k.get(pole)
    if not _nazwa(nazwa, pole, sk, akcja, blad):
        return None
    if nazwa in folder["zajete"]:
        blad(
            sk,
            f"folder {akcja}: nazwa „{nazwa}” jest już zajęta w folderze (karta usuniętego pliku też ją zajmuje)",
        )
        return None
    return nazwa


def _czyta(k, sk, folder, blad) -> None:
    pliki = k.get("pliki")
    if not isinstance(pliki, list) or not pliki or not all(_niepusty(p) for p in pliki):
        blad(sk, "folder czyta wymaga niepustej listy pliki (nazwy plików)")
        return
    if len(set(pliki)) != len(pliki):
        blad(sk, "ten sam plik dwa razy w liście pliki")
    for p in pliki:
        if p not in folder["gdzie"]:
            blad(sk, f"folder czyta: plik „{p}” nie leży w folderze ({_powod(p, folder)})")


def _przenies(k, sk, folder, blad) -> None:
    plik = _istniejacy(k, "plik", sk, folder, "przenies", blad)
    teczka = k.get("do")
    if not _nazwa(teczka, "do", sk, "przenies", blad):
        teczka = None
    elif teczka not in folder["teczki"]:
        blad(
            sk,
            f"folder przenies: teczka „{teczka}” nie powstała wcześniej krokiem utworz",
        )
        teczka = None
    if "uwaga" in k and not _niepusty(k["uwaga"]):
        blad(sk, "pole uwaga musi być niepustym napisem")
    if plik and teczka:
        stara = folder["gdzie"][plik]
        if stara:
            blad(
                sk,
                f"plik „{plik}” już leży w teczce „{stara}”: przenieść można tylko plik luźny, nie z teczki do teczki",
            )
        else:
            folder["gdzie"][plik] = teczka


def krok_folderu(k, sk, folder, blad, tryb=None, bez_pytania=()) -> None:
    """Krok `folder`: wymaga folder_startowy, sprawdza pola akcji i przesuwa stan folderu; akcja inna niż `czyta` tylko w trybie z listy `bez_pytania`."""
    if not folder["znane"]:
        blad(sk, "krok folder wymaga niepustej listy folder_startowy w scenariuszu")
        return
    akcja = k.get("akcja")
    if akcja not in AKCJE_FOLDERU:
        blad(sk, f"folder: akcja „{akcja}” spoza {'/'.join(AKCJE_FOLDERU)}")
        return
    if akcja != "czyta" and tryb not in bez_pytania:
        blad(
            sk,
            f"folder {akcja} tylko w trybie {' albo '.join(bez_pytania)} (teraz „{tryb}”): w trybie Manual i Plan Claude nie zmienia plików sam",
        )
    for pole in k:
        if pole not in POLA_WSPOLNE + AKCJE_FOLDERU[akcja]:
            blad(
                sk,
                f"pole {pole} nie należy do akcji folder {akcja} (pola: {', '.join(AKCJE_FOLDERU[akcja])})",
            )
    if akcja == "czyta":
        _czyta(k, sk, folder, blad)
    elif akcja == "nowy":
        nazwa = _wolna_nazwa(k, "plik", sk, folder, akcja, blad)
        if nazwa:
            folder["gdzie"][nazwa] = None
            folder["zajete"].add(nazwa)
            folder["znane"].add(nazwa)
    elif akcja == "zmien":
        plik = _istniejacy(k, "plik", sk, folder, akcja, blad)
        nazwa = _wolna_nazwa(k, "nazwa", sk, folder, akcja, blad)
        if plik and nazwa:
            folder["gdzie"][nazwa] = folder["gdzie"].pop(plik)
            folder["zajete"].discard(plik)
            folder["zajete"].add(nazwa)
            folder["znane"].add(nazwa)
    elif akcja == "usun":
        plik = _istniejacy(k, "plik", sk, folder, akcja, blad)
        if plik:
            del folder["gdzie"][
                plik
            ]  # karta zostaje przekreślona, więc nazwa zostaje w `zajete`
    elif akcja == "utworz":
        if _nazwa(k.get("nazwa"), "nazwa", sk, akcja, blad):
            if k["nazwa"] in folder["teczki"]:
                blad(sk, f"teczka „{k['nazwa']}” już istnieje: utworz zakłada nową")
            folder["teczki"].add(k["nazwa"])
    else:
        _przenies(k, sk, folder, blad)
