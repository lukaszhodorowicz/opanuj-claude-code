"""Robi obraz lekcji obrazy/komputer-i-telefon.png: zrzut ćwiczenia 1 przed wiadomością z sali (okno na komputerze i telefon obok) bez znacznika „kliknij tutaj”.

Wywołanie z korzenia repozytorium, po złożeniu strony lekcji (`uv run python -m narzedzia.strona moduly/praca-bez-ciebie/rozmowa-na-telefonie --wyjscie build/lekcja-rozmowa-na-telefonie.html`):
`flock /tmp/przewodnik-chrome.lock env PYTHONPATH=. uv run --with pillow python moduly/praca-bez-ciebie/rozmowa-na-telefonie/obrazy/zrodla/kadr-komputer-i-telefon.py`.
Obraz w tekście lekcji nie może mieć znacznika ani obwódki celu, bo tam nic się nie klika (uwaga Łukasza 27.10.2026).
Znacznik ukrywa narzędzie zrzutów silnika (pole `bez_znacznika` ujęcia); skrypt tylko przycina zrzut `cw1-przed` do pasa od okna aplikacji do podpisu pod telefonem.
"""

from pathlib import Path

from PIL import Image

from narzedzia.zrzuty import plan_ujec, zrob

LEKCJA = Path("moduly/praca-bez-ciebie/rozmowa-na-telefonie")
STRONA = Path("build/lekcja-rozmowa-na-telefonie.html").resolve()
WYJSCIE = Path("build/zrzuty/rozmowa-na-telefonie-kadr").resolve()
UJECIE = "cw1-przed"
OBRAZ = LEKCJA / "obrazy/komputer-i-telefon.png"
WYSOKOSC = 650  # od pasa nad oknem aplikacji do podpisu „Aplikacja Claude na telefonie”
NAD_OKNEM = 7  # pas tła strony nad górną krawędzią okna aplikacji
PROBKI = range(100, 850, 10)  # kolumny pikseli w poprzek okna aplikacji na komputerze (telefon obok zostaje poza próbkami)
WIERSZE = 10  # tyle kolejnych ciemnych wierszy to początek paska tytułu okna (przed tekstem tytułu); obwódki przycisku i dymku nad oknem mają po 3 px


def gora_okna(obraz: Image.Image) -> int:
    """Pierwszy wiersz, od którego WIERSZE kolejnych wierszy jest ciemnych w większości próbek: górna krawędź okna aplikacji (układ strony nad oknem się zmienia)."""
    szary = obraz.convert("L")

    def ciemny(y: int) -> bool:
        return sum(szary.getpixel((x, y)) < 60 for x in PROBKI) >= 0.85 * len(PROBKI)

    for y in range(szary.height - WIERSZE):
        if all(ciemny(y + i) for i in range(WIERSZE)):
            return y
    raise RuntimeError("Na zrzucie nie ma okna aplikacji.")


def main() -> None:
    WYJSCIE.mkdir(parents=True, exist_ok=True)
    ujecie = dict(plan_ujec(LEKCJA)[UJECIE])
    ujecie["wys"] = 1200  # zapas: tekst i polecenie nad oknem mają różną wysokość
    ujecie["bez_znacznika"] = True
    png = zrob(UJECIE, ujecie, STRONA, WYJSCIE)
    obraz = Image.open(png)
    y = gora_okna(obraz) - NAD_OKNEM
    obraz.crop((0, y, obraz.width, y + WYSOKOSC)).save(OBRAZ)
    print(OBRAZ)


if __name__ == "__main__":
    main()
