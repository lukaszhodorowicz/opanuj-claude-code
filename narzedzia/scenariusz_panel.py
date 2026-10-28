"""Sprawdza dwa opcjonalne pola `aplikacja` z części B silnika (panel szczegółów i lista trybów): `remote_control` (stan przełącznika Remote Control na karcie Environment) i `bypass_dostepny` (pozycja Bypass permissions na liście trybów)."""

from narzedzia import scenariusz_menu_rzedu  # lista trybów w drogach (kroki tryb-menu i tryb) też ma Bypass permissions

POLA = ("remote_control", "bypass_dostepny")


def pole(cw: dict, s: str, blad) -> None:
    """Oba pola mają być prawdą albo fałszem; bez pola przełącznik jest włączony (jak na zrzutach Łukasza 27.10.2026), a Bypass permissions schowany (fakt aplikacja-dostepne-tryby: pojawia się dopiero po włączeniu). `bypass_dostepny` ma sens tylko w ćwiczeniu z etapami (też z drogami etapów) i w ćwiczeniu z drogami, które mają krok `klik` `tryb-menu`: tylko tam powstaje lista trybów, w pozostałych przełącznik trybu jest zwykłym napisem."""
    apl = cw.get("aplikacja")
    if not isinstance(apl, dict):
        return
    sa = f"{s}/aplikacja"
    for nazwa in POLA:
        if nazwa in apl and not isinstance(apl[nazwa], bool):
            blad(sa, f"pole {nazwa} musi być prawdą albo fałszem, jest {apl[nazwa]!r}")
    if "bypass_dostepny" in apl and "etapy" not in cw and not scenariusz_menu_rzedu.jest_w_drogach(cw):
        blad(sa, "pole bypass_dostepny tylko w ćwiczeniu z etapami: tylko tam powstaje lista trybów, w ćwiczeniach z krokami i z drogami przełącznik trybu niczego nie otwiera, chyba że któraś droga ma krok klik „tryb-menu”")
