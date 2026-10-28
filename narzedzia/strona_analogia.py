"""Składanie strony lekcji: komentarz `<!-- analogia: … -->` pod obrazem (w jednej linii albo w kilku) staje się rozwijanym blokiem „Jak to sobie wyobrazić?” w ramce obrazu, a lekcja bez scenariusz.json składa się jako strona bez ćwiczeń (znacznik ćwiczenia albo podglądu bez scenariusza to czytelny błąd)."""

import re
from collections.abc import Callable
from pathlib import Path

ANALOGIA = re.compile(r"<!--\s*analogia\s*:(.*?)-->", re.DOTALL)
CALA_LINIA = re.compile(r"^\s*<!--\s*analogia\s*:(.*?)-->\s*$")
OTWARTA_LINIA = re.compile(r"^\s*<!--\s*analogia\s*:(.*)$")  # początek komentarza, którego `-->` stoi w którejś z następnych linii
NAGLOWEK = "Jak to sobie wyobrazić?"
SCENARIUSZ_PUSTY = {"cwiczenia": []}


def z_linii_obrazu(linia: str) -> str | None:
    """Tekst analogii z komentarza na końcu linii obrazu (`![opis](plik) <!-- analogia: … -->`) albo None."""
    trafienie = ANALOGIA.search(linia)
    return trafienie.group(1).strip() if trafienie else None


def z_linii_pod_obrazem(linia: str) -> str | None:
    """Tekst analogii, gdy cała linia pod obrazem to komentarz `<!-- analogia: … -->`; inny komentarz albo tekst daje None (analogia w innym miejscu zostaje niewidocznym komentarzem)."""
    trafienie = CALA_LINIA.match(linia)
    return trafienie.group(1).strip() if trafienie else None


def dodaj(figura: str, tekst: str, inline: Callable[[str], str]) -> str:
    """Wstawia blok `<details><summary>Jak to sobie wyobrazić?</summary><p>…</p></details>` na koniec figury, pod podpisem obrazu; tekst idzie przez `inline` (kod, pogrubienie i kursywa jak w reszcie lekcji). Pusty tekst to błąd; druga analogia pod tym samym obrazem zostaje komentarzem."""
    if not tekst:
        raise ValueError(f"analogia pod obrazem bez tekstu: zapis ma postać <!-- analogia: tekst --> ({NAGLOWEK})")
    if "<details>" in figura:
        return figura
    blok = f"<details><summary>{NAGLOWEK}</summary><p>{inline(tekst)}</p></details>"
    return figura[: -len("</figure>")] + blok + "</figure>" if figura.endswith("</figure>") else figura + blok


class PodObrazem:
    """Komentarz analogii pod obrazem w pętli po liniach lekcji (`strona.markdown_na_html`): jedna linia `<!-- analogia: … -->` albo kilka (`<!-- analogia: pierwsza`, `druga -->`); części łączą się spacją w jeden tekst bloku."""

    def __init__(self, inline: Callable[[str], str]):
        self.inline = inline
        self.czesci: list[str] | None = None  # części komentarza otwartego, ale jeszcze niezamkniętego
        self.figura = 0  # miejsce figury w liście wyniku, do której trafi blok

    def linia(self, linia: str, wynik: list[str], pod_obrazem: int | None) -> bool:
        """Czy linia należy do analogii (wtedy pętla ją pomija); `pod_obrazem` to miejsce figury, gdy poprzednia linia była obrazem."""
        if self.czesci is not None:
            przed, zamkniecie, po = linia.partition("-->")
            self.czesci.append(przed)
            if not zamkniecie:
                return True
            if po.strip():
                raise ValueError(f"tekst po zamknięciu komentarza analogii (-->): „{po.strip()}”; komentarz kończy swoją linię")
            tekst, self.czesci = " ".join(c.strip() for c in self.czesci if c.strip()), None
            wynik[self.figura] = dodaj(wynik[self.figura], tekst, self.inline)
            return True
        if pod_obrazem is None:
            return False
        if (tekst := z_linii_pod_obrazem(linia)) is not None:
            wynik[pod_obrazem] = dodaj(wynik[pod_obrazem], tekst, self.inline)
            return True
        otwarta = OTWARTA_LINIA.match(linia) if "-->" not in linia else None
        if otwarta:
            self.czesci, self.figura = [otwarta.group(1)], pod_obrazem
        return bool(otwarta)

    def koniec(self) -> None:
        """Po ostatniej linii lekcji komentarz analogii musi być zamknięty."""
        if self.czesci is not None:
            raise ValueError("komentarz analogii pod obrazem nie ma zamknięcia -->: zapis ma postać <!-- analogia: tekst --> (tekst może zajmować kilka linii)")


def sprawdz_bez_scenariusza(html_lekcji: str, sentynel: re.Pattern, podglad: re.Pattern, lekcja_md: Path) -> None:
    """Lekcja bez scenariusz.json nie ma ćwiczeń ani podglądów: znacznik `<!-- cwiczenie: … -->` albo `<!-- podglad: … -->` w jej tekście to błąd ze ścieżką pliku lekcji."""
    for wzor, co in ((sentynel, "ćwiczenia <!-- cwiczenie: id -->"), (podglad, "podglądu <!-- podglad: ćwiczenie terminal -->")):
        if wzor.search(html_lekcji):
            raise ValueError(f"{lekcja_md}: lekcja ma znacznik {co}, ale w jej katalogu nie ma scenariusz.json: dodaj scenariusz albo usuń znacznik (lekcja bez scenariusza składa się jako strona bez ćwiczeń)")
