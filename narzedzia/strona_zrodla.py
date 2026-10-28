"""Wydziela z lekcja.md część `## Źródła`, żeby generator strony postawił ją jako stopkę po quizie i fiszkach (D-2026-10-26-54)."""

import re

NAGLOWEK_ZRODEL = re.compile(r"^##\s+Źródła\s*$")
NAGLOWEK_CZESCI = re.compile(r"^#{1,2}\s")


def wydziel_zrodla(tresc: str) -> tuple[str, str]:
    """Odcina część `## Źródła` (od nagłówka do następnego nagłówka `#` albo `##` albo do końca, poza blokami kodu); zwraca (tekst bez niej, markdown części), bez niej drugi element jest pusty."""
    linie = tresc.splitlines()
    w_kodzie = False
    start = koniec = None
    for i, linia in enumerate(linie):
        if linia.strip().startswith("```"):
            w_kodzie = not w_kodzie
            continue
        if w_kodzie:
            continue
        if start is None and NAGLOWEK_ZRODEL.match(linia):
            start = i
        elif start is not None and NAGLOWEK_CZESCI.match(linia):
            koniec = i
            break
    if start is None:
        return tresc, ""
    koniec = len(linie) if koniec is None else koniec
    return "\n".join(linie[:start] + linie[koniec:]) + "\n", "\n".join(linie[start:koniec]).strip()


def stopka_zrodel(html_zrodel: str) -> str:
    """Stopka strony ze źródłami w HTML; bez źródeł pusty napis (szablon nie zostawia wtedy żadnego `<footer>`)."""
    if not html_zrodel:
        return ""
    return f'<footer class="tekst stopka-zrodel" id="zrodla">\n{html_zrodel}\n</footer>'
