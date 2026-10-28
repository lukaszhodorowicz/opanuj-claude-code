"""Sprawdza pole `bez_zmiany` kroku `claude` w drogach symulatora aplikacji: ścieżka pliku z folderu, którą Claude tylko wymienia, bez znacznika zmiany w podglądzie folderu."""

POLE = "bez_zmiany"


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


def _krok(k: dict, sk: str, folder: set, blad) -> None:
    """Krok z polem `bez_zmiany`: tylko `claude`, wartość true, razem z `plik` leżącym w folderze od startu."""
    if k.get("typ") != "claude":
        blad(sk, f"pole {POLE} tylko w kroku claude (jest w kroku „{k.get('typ')}”)")
        return
    if k[POLE] is not True:
        blad(
            sk,
            f"pole {POLE} musi mieć wartość true; gdy Claude zmienia plik, pole pomijasz",
        )
    plik = k.get("plik")
    if not _niepusty(plik):
        blad(
            sk,
            f"pole {POLE} wymaga pola plik: bez ścieżki nie ma karty, której znacznik pomijamy",
        )
    elif plik not in folder:
        blad(
            sk,
            f"pole {POLE} tylko dla pliku z folderu (folder_startowy albo aplikacja.folder_startowy_dodatkowe), "
            f"a „{plik}” w nim nie leży",
        )


def sprawdz(cw: dict, s: str, folder: set, blad) -> None:
    """Ćwiczenie aplikacji: `bez_zmiany` w krokach dróg; `folder` to nazwy z `folder_startowy` i `aplikacja.folder_startowy_dodatkowe` (bez `nowe_pliki`)."""
    for i, k in enumerate(cw.get("kroki") if isinstance(cw.get("kroki"), list) else []):
        if isinstance(k, dict) and POLE in k:
            blad(
                f"{s}/kroki[{i}]",
                f"pole {POLE} tylko w drogach, w kroku claude z polem plik",
            )
    drogi = cw.get("drogi")
    for i, d in enumerate(drogi if isinstance(drogi, list) else []):
        kroki = d.get("kroki") if isinstance(d, dict) else None
        for j, k in enumerate(kroki if isinstance(kroki, list) else []):
            if isinstance(k, dict) and POLE in k:
                _krok(k, f"{s}/drogi[{i}]/kroki[{j}]", folder, blad)
