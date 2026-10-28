"""Wynik sprawdzianu myszą: pojedynczy wynik, tabela OK albo usterka ze ścieżkami zrzutów i kod wyjścia programu."""

from dataclasses import dataclass, field


@dataclass
class Wynik:
    """Jedno sprawdzenie: lekcja, rodzaj (ćwiczenie, karta, przewijanie), nazwa (id ćwiczenia albo karty), rozmiar okna, usterki i zrzuty."""

    lekcja: str
    rodzaj: str
    nazwa: str
    szerokosc: int
    wysokosc: int
    usterki: list[str] = field(default_factory=list)
    zrzuty: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.usterki


def tabela(wyniki: list[Wynik]) -> str:
    """Tabela tekstowa: jeden wiersz na wynik (lekcja, rodzaj, nazwa, rozmiar, OK albo USTERKA), pod usterką jej opisy, na końcu liczby i zrzuty usterek."""
    if not wyniki:
        return "Brak wyników: żadna lekcja nie ma sprawdzanego elementu."
    szer = [max(len(str(getattr(w, p))) for w in wyniki) for p in ("lekcja", "rodzaj", "nazwa")]
    wiersze = []
    for w in wyniki:
        rozmiar = f"{w.szerokosc}x{w.wysokosc}"
        wiersze.append(f"{w.lekcja:<{szer[0]}}  {w.rodzaj:<{szer[1]}}  {w.nazwa:<{szer[2]}}  {rozmiar:<9}  {'OK' if w.ok else 'USTERKA'}")
        wiersze.extend(f"    - {u}" for u in w.usterki)
        if not w.ok:
            wiersze.extend(f"    zrzut: {z}" for z in w.zrzuty)
    zle = sum(1 for w in wyniki if not w.ok)
    wiersze.append(f"Razem {len(wyniki)} sprawdzeń, OK {len(wyniki) - zle}, usterek {zle}.")
    return "\n".join(wiersze)


def kod_wyjscia(wyniki: list[Wynik]) -> int:
    """0, gdy wszystko OK; 1 przy jakiejkolwiek usterce albo gdy nic nie sprawdzono."""
    return 0 if wyniki and all(w.ok for w in wyniki) else 1
