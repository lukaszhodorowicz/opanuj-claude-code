"""Robi obraz lekcji obrazy/formularz-w-cwiczeniu.png: zrzut ćwiczenia z oknem New scheduled task bez znacznika „kliknij tutaj”.

Wywołanie z korzenia repozytorium, po złożeniu strony lekcji:
`flock /tmp/przewodnik-chrome.lock env PYTHONPATH=. uv run --with pillow python moduly/praca-bez-ciebie/zadanie-co-rano/obrazy/zrodla/kadr-formularza.py`.
Obraz w tekście lekcji nie może mieć znacznika ani obwódki celu, bo tam nic się nie klika (uwaga Łukasza 27.10.2026).
Znacznik ukrywa narzędzie zrzutów silnika (pole `bez_luki` ujęcia); skrypt tylko przycina zrzut do okna aplikacji.
"""

from pathlib import Path

from PIL import Image

from narzedzia.zrzuty import plan_ujec, zrob

LEKCJA = Path("moduly/praca-bez-ciebie/zadanie-co-rano")
STRONA = Path("build/lekcja-zadanie-co-rano.html").resolve()
WYJSCIE = Path("build/zrzuty/zadanie-co-rano-kadr").resolve()
UJECIE = "cw1-formularz-okno"
OBRAZ = LEKCJA / "obrazy/formularz-w-cwiczeniu.png"
WYSOKOSC = 654  # od paska okna aplikacji do dolnej krawędzi okna New scheduled task
NAD_OKNEM = 7  # pas tła strony nad górną krawędzią okna aplikacji
PROBKI = range(120, 1160, 40)  # kolumny pikseli w poprzek okna aplikacji


def gora_okna(obraz: Image.Image) -> int:
    """Pierwszy wiersz ciemny w całej szerokości okna: górna krawędź okna aplikacji (układ strony nad oknem się zmienia)."""
    szary = obraz.convert("L")
    for y in range(szary.height):
        if all(szary.getpixel((x, y)) < 60 for x in PROBKI):
            return y
    raise RuntimeError("Na zrzucie nie ma okna aplikacji.")


def main() -> None:
    WYJSCIE.mkdir(parents=True, exist_ok=True)
    ujecie = dict(plan_ujec(LEKCJA)[UJECIE])
    # bez ostatniego kliku (Advanced settings): obraz pokazuje wypełnione okno, nie rozwiniętą sekcję
    ujecie["klik"] = [k for k in ujecie["klik"] if "apl-harm-zaaw-glowa" not in k]
    ujecie["wys"] = 1400  # zapas: dymek i polecenia nad oknem mają różną wysokość
    ujecie["bez_luki"] = True
    png = zrob(UJECIE, ujecie, STRONA, WYJSCIE)
    obraz = Image.open(png)
    y = gora_okna(obraz) - NAD_OKNEM
    obraz.crop((0, y, obraz.width, y + WYSOKOSC)).save(OBRAZ)
    print(OBRAZ)


if __name__ == "__main__":
    main()
