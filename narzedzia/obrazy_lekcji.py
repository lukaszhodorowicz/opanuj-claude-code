"""Zamienia linię `![opis](obrazy/plik.png)` z lekcja.md na obraz z podpisem wpisany do strony jako data URI."""

import base64
import html
import re
from pathlib import Path

LINIA_OBRAZU = re.compile(r"^\s*!\[([^\]]*)\]\(([^)]*)\)\s*(?:<!--.*?-->\s*)*$")
OBRAZ_W_TEKSCIE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
FORMATY = {  # rozszerzenie -> (typ MIME, początek pliku)
    ".png": ("image/png", (b"\x89PNG\r\n\x1a\n",)),
    ".jpg": ("image/jpeg", (b"\xff\xd8\xff",)),
    ".jpeg": ("image/jpeg", (b"\xff\xd8\xff",)),
    ".webp": ("image/webp", (b"RIFF",)),
}
KLASA = "obraz"
STYL = "styl-obraz.css"


def _plik_obrazu(sciezka: str, katalog: Path | None) -> Path:
    """Plik obrazu w katalogu lekcji; adres, ścieżka bezwzględna, `..` albo brak pliku to błąd z nazwą pliku."""
    if katalog is None:
        raise ValueError(
            f"obraz „{sciezka}”: nie wiadomo, w którym katalogu lekcji go szukać"
        )
    if not sciezka:
        raise ValueError("obraz bez ścieżki: zapis ma postać ![opis](obrazy/plik.png)")
    if re.match(r"[A-Za-z][\w+.-]*:", sciezka) or sciezka.startswith(("/", "~", "\\")):
        raise ValueError(
            f"obraz „{sciezka}”: ścieżka ma być względna do katalogu lekcji (bez adresu i bez / na początku)"
        )
    if "\\" in sciezka or ".." in sciezka.split("/"):
        raise ValueError(
            f"obraz „{sciezka}”: ścieżka wychodzi poza katalog lekcji (..) albo ma ukośnik \\"
        )
    baza = katalog.resolve()
    plik = (baza / sciezka).resolve()
    if not plik.is_relative_to(baza):
        raise ValueError(
            f"obraz „{sciezka}”: ścieżka wychodzi poza katalog lekcji {katalog}"
        )
    if not plik.is_file():
        raise ValueError(
            f"obraz „{sciezka}”: nie ma takiego pliku w katalogu lekcji {katalog}"
        )
    return plik


def _data_uri(plik: Path, sciezka: str) -> str:
    """Treść pliku jako data URI; rozszerzenie spoza FORMATY albo treść niezgodna z rozszerzeniem to błąd."""
    format_ = FORMATY.get(plik.suffix.lower())
    if not format_:
        raise ValueError(
            f"obraz „{sciezka}”: nieobsługiwany format, dozwolone {', '.join(FORMATY)}"
        )
    mime, poczatki = format_
    dane = plik.read_bytes()
    if not dane.startswith(poczatki) or (
        mime == "image/webp" and dane[8:12] != b"WEBP"
    ):
        raise ValueError(f"obraz „{sciezka}”: treść pliku nie jest obrazem {mime}")
    return f"data:{mime};base64,{base64.b64encode(dane).decode('ascii')}"


def adres_obrazu(sciezka: str, katalog: Path | None) -> str:
    """Data URI obrazu z katalogu lekcji; brak pliku, zła ścieżka albo zły format to czytelny błąd."""
    return _data_uri(_plik_obrazu(sciezka, katalog), sciezka)


def obraz_z_linii(linia: str, katalog: Path | None) -> str | None:
    """HTML obrazu z podpisem, gdy linia to sam zapis obrazu; None, gdy obrazu w linii nie ma; obraz w środku tekstu to błąd."""
    trafienie = LINIA_OBRAZU.match(linia)
    if not trafienie:
        bez_kodu = re.sub(r"<!--.*?-->|`[^`]*`", "", linia)
        if OBRAZ_W_TEKSCIE.search(bez_kodu):
            raise ValueError(
                f"obraz w środku tekstu: „{linia.strip()}”; zapis ![opis](plik) stoi w osobnej linii"
            )
        return None
    opis, sciezka = trafienie.group(1).strip(), trafienie.group(2).strip()
    if not opis:
        raise ValueError(
            f"obraz „{sciezka}” bez opisu: opis w nawiasach kwadratowych idzie do alt i do podpisu"
        )
    adres = _data_uri(_plik_obrazu(sciezka, katalog), sciezka)
    return (
        f'<figure class="{KLASA}"><img src="{adres}" alt="{html.escape(opis, quote=True)}">'
        f"<figcaption>{html.escape(opis, quote=False)}</figcaption></figure>"
    )


def ma_obraz(html_lekcji: str) -> bool:
    """Czy w HTML lekcji stoi choć jeden obraz (wtedy strona dostaje styl obrazów)."""
    return f'<figure class="{KLASA}">' in html_lekcji
