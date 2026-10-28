"""Sprawdza w symulatorze aplikacji dwa opcjonalne pola okna Settings i panelu szczegółów z paczki 4B silnika: `aplikacja.konto_ustawien` (wariant lewej kolumny Settings: "A" albo "B") i `aplikacja.konektory_do_polaczenia` (karta Connectors w panelu zwinięta z napisem „N to reconnect”); opis: dane/FORMAT-SCENARIUSZA.md, części „Okno Settings: wariant lewej kolumny” i „Karta Connectors zwinięta”."""

from narzedzia import scenariusz_telefon

KONTA = ("A", "B")
KLIKI_USTAWIEN = ("ustawienia-claude-code", "ustawienia-connectors")  # kroki klik, które otwierają okno Settings (kod: strona/aplikacja-ustawienia-cc.js)
POZYCJE_OKIEN = ("Browse connectors", "Browse plugins")  # pozycje podmenu +, które otwierają okno Settings (katalog konektorów, przeglądarka wtyczek)
MAKS_KONEKTOROW = 99  # napis „N to reconnect” ma wzór z jedną albo dwiema cyframi


def _kroki(cw: dict) -> list:
    """Wszystkie kroki wszystkich dróg ćwiczenia (puste, gdy ćwiczenie nie ma dróg)."""
    return [k for d in (cw.get("drogi") if isinstance(cw.get("drogi"), list) else []) if isinstance(d, dict) for k in (d.get("kroki") if isinstance(d.get("kroki"), list) else []) if isinstance(k, dict)]


def ma_okno_settings(cw: dict) -> bool:
    """Któraś droga ćwiczenia otwiera okno Settings: klik konta (Claude Code, Connectors), komenda `/config` albo pozycja podmenu (Browse connectors, Browse plugins)."""
    return any(
        scenariusz_telefon.otwiera_claude_code(k) or (k.get("typ") == "klik" and (k.get("cel") in KLIKI_USTAWIEN or (k.get("cel") == "pozycja" and k.get("na") in POZYCJE_OKIEN)))
        for k in _kroki(cw)
    )


def _konto(cw: dict, apl: dict, sa: str, blad) -> None:
    """`konto_ustawien`: "A" albo "B", tylko w ćwiczeniu z drogami, z którymś krokiem otwierającym okno Settings (inaczej pole nic nie rysuje)."""
    if apl["konto_ustawien"] not in KONTA:
        blad(sa, f"pole konto_ustawien „{apl['konto_ustawien']}” spoza {'/'.join(KONTA)} (wariant lewej kolumny Settings: A to konto ze zrzutu 03-59-16, B ze zrzutów 04-26-45 i 04-45-04)")
    if "drogi" not in cw:
        blad(sa, "pole konto_ustawien tylko w ćwiczeniu z drogami: okno Settings otwierają kroki dróg")
    elif not ma_okno_settings(cw):
        blad(sa, "pole konto_ustawien bez kroku, który otwiera okno Settings (klik „ustawienia-claude-code”, klik „ustawienia-connectors”, komenda /config, pozycja „Browse connectors” albo „Browse plugins”): pole nic nie rysuje")


def _konektory(cw: dict, apl: dict, sa: str, napisy, blad) -> None:
    """`konektory_do_polaczenia`: liczba całkowita 1-99, której napis „N to reconnect” pasuje do wzoru z listy napisów; karta Connectors stoi w panelu szczegółów, więc nie przy `panel: "schowany"` i nie w ćwiczeniu z drogami bez `kontekst` (panel jest tam schowany)."""
    n = apl["konektory_do_polaczenia"]
    if type(n) is not int or not 1 <= n <= MAKS_KONEKTOROW:
        blad(sa, f"pole konektory_do_polaczenia musi być liczbą całkowitą od 1 do {MAKS_KONEKTOROW} (liczba konektorów do ponownego połączenia na karcie Connectors), jest {n!r}")
    elif not napisy.jest(f"{n} to reconnect", "aplikacja"):
        blad(sa, f"pole konektory_do_polaczenia: napis „{n} to reconnect” nie pasuje do wzoru z listy napisów interfejsu aplikacji")
    if apl.get("panel") == "schowany" or ("drogi" in cw and "kontekst" not in apl):
        blad(sa, "pole konektory_do_polaczenia przy schowanym panelu szczegółów: karta Connectors stoi w panelu (w ćwiczeniu z drogami panel jest widoczny tylko z polem kontekst)")


def pole(cw: dict, s: str, napisy, blad) -> None:
    """Pola `aplikacja.konto_ustawien` i `aplikacja.konektory_do_polaczenia` (oba opcjonalne)."""
    apl = cw.get("aplikacja")
    if not isinstance(apl, dict):
        return
    sa = f"{s}/aplikacja"
    if "konto_ustawien" in apl:
        _konto(cw, apl, sa, blad)
    if "konektory_do_polaczenia" in apl:
        _konektory(cw, apl, sa, napisy, blad)
