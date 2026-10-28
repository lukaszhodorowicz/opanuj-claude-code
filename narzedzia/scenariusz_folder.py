"""Śledzi pliki w folderze wzdłuż przebiegu i sprawdza, czy akcje `zmien`, `usun`, `edytuj` i `przywroc` dotyczą pliku, który w tym miejscu istnieje."""


def sprawdz_stan_folderu(kroki, start: set[str], s: str, blad) -> None:
    """Przechodzi kroki przebiegu (z gałęziami menu, każda od stanu sprzed menu) i zgłasza błędy akcji na plikach."""
    _idz(kroki, set(start), set(), s, blad)


def _idz(kroki, stan: set[str], edytowane: set[str], s: str, blad) -> None:
    """stan: pliki w folderze; edytowane: pliki ze zmienioną treścią, które da się przywrócić."""
    if not isinstance(kroki, list):
        return
    for i, krok in enumerate(kroki):
        sk = f"{s}[{i}]"
        if not isinstance(krok, dict):
            continue
        if krok.get("typ") == "folder":
            _krok_folderu(krok, stan, edytowane, sk, blad)
        if krok.get("typ") == "menu" and isinstance(krok.get("opcje"), list):
            for j, op in enumerate(krok["opcje"]):
                if isinstance(op, dict):
                    _idz(op.get("dalej"), set(stan), set(edytowane), f"{sk}/opcje[{j}]/dalej", blad)


def _brak(akcja: str, nazwa: str, stan: set[str], s: str, blad) -> bool:
    """Zgłasza błąd i zwraca True, gdy pliku nie ma w folderze w tym miejscu przebiegu."""
    if nazwa in stan:
        return False
    blad(
        s, f"folder {akcja}: pliku „{nazwa}” nie ma w folderze w tym miejscu przebiegu"
    )
    return True


def _krok_folderu(krok: dict, stan: set[str], edytowane: set[str], s: str, blad) -> None:
    akcja, nazwa, plik = krok.get("akcja"), krok.get("nazwa"), krok.get("plik")
    if not isinstance(nazwa, str):
        return
    if akcja == "nowy":
        stan.add(nazwa)
    elif akcja == "zmien" and isinstance(plik, str):
        _brak("zmien", plik, stan, s, blad)
        if nazwa in stan and nazwa != plik:
            blad(s, f"folder zmien: plik „{nazwa}” już jest w folderze")
        stan.discard(plik)
        stan.add(nazwa)
        if plik in edytowane:
            edytowane.discard(plik)
            edytowane.add(nazwa)
    elif akcja == "usun":
        _brak("usun", nazwa, stan, s, blad)
        stan.discard(nazwa)
        edytowane.discard(nazwa)
    elif akcja == "edytuj":
        if not _brak("edytuj", nazwa, stan, s, blad):
            edytowane.add(nazwa)
    elif akcja == "przywroc":
        if _brak("przywroc", nazwa, stan, s, blad):
            return
        if nazwa not in edytowane:
            blad(
                s,
                f"folder przywroc: plik „{nazwa}” nie dostał wcześniej w tym przebiegu edytuj, więc nie ma czego przywracać",
            )
        edytowane.discard(nazwa)
