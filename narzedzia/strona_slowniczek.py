"""Słowniczek kursu w generatorze strony: pogrubia w tekście lekcji pierwsze wystąpienie pojęcia (z podpowiedzią z wyjaśnienia) i składa stronę słowniczka z `dane/slowniczek.yaml`.

Strona słowniczka: `uv run python -m narzedzia.strona_slowniczek --wyjscie build/slowniczek.html`.
Pogrubienie wołane jest z `narzedzia/strona.py`; podpowiedzią steruje `strona/slowniczek.js`, wyglądem `strona/styl-slowniczek.css`.
Pięć zasad dopasowania (lekcja 0.0): bez okruszków, tylko zwykły tekst akapitów i list (bez nagłówków, opisów obrazów, rozwijanej analogii pod obrazem, linków i kodu),
dłuższa forma przed krótszą, wielkość liter ma znaczenie, forma ze znakami pasuje całą frazą, a zwykła całym wyrazem.
Frazy z klucza `bez_pogrubienia` (napisy interfejsu i nazwy programów) stoją w tym samym wzorze co odmiany, ale trafienie w nie zostawia tekst bez zmian i nie zużywa żadnego hasła.
"""

import argparse
import html
import re
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import yaml

KORZEN = Path(__file__).resolve().parent.parent
PLIK_SLOWNICZKA = KORZEN / "dane" / "slowniczek.yaml"
PLIK_FAKTOW = KORZEN / "dane" / "fakty.yaml"
NAZWA_STRONY = "Słowniczek"

OKRUSZKI = re.compile(r"\A\s*<p>(?:<em>)?\s*Przewodnik po Claude Code\b.*?</p>", re.S)  # linia okruszków, gdy nie została wydzielona wcześniej
ZNACZNIK = re.compile(r"(<[^>]*>)")
NAZWA_ZNACZNIKA = re.compile(r"<(/?)([A-Za-z][A-Za-z0-9]*)")
PUSTE = {"img", "br", "hr", "input", "meta", "link", "wbr"}
AKAPITY = {"p", "li"}  # tylko ich zwykły tekst się liczy
WYKLUCZONE = {"a", "code", "pre", "kbd", "script", "style", "button", "figure"}  # tekst linków i kodu się nie liczy; figure to opis obrazu i rozwijana analogia pod nim, więc pojęcie liczy się dopiero w tekście głównym
OD = r"(?<!\w)(?<!\w-)"  # granica słowa z polskimi znakami; łącznik między literami łączy wyrazy („pre-hook” to nie „hook”)
DO = r"(?!\w)(?!-\w)"


@dataclass(frozen=True)
class Haslo:
    pojecie: str
    odmiany: tuple[str, ...]
    wyjasnienie: str
    fakt: str


def _dane(sciezka: Path) -> dict:
    """Zawartość pliku słowniczka (brak pliku: pusty słownik); błąd składni YAML to ValueError ze ścieżką."""
    if not sciezka.is_file():
        return {}
    try:
        return yaml.safe_load(sciezka.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as blad:
        raise ValueError(f"{sciezka}: {blad}") from blad


def wczytaj_bez_pogrubienia(sciezka: Path) -> tuple[str, ...]:
    """Frazy z klucza `bez_pogrubienia` (brak klucza albo pliku: pusta lista); inny kształt niż lista niepustych napisów to ValueError z nazwą klucza."""
    frazy = _dane(sciezka).get("bez_pogrubienia", [])
    if not (isinstance(frazy, list) and all(isinstance(f, str) and f.strip() for f in frazy)):
        raise ValueError(f"{sciezka}: `bez_pogrubienia` ma być listą niepustych napisów")
    return tuple(frazy)


def wczytaj(sciezka: Path) -> tuple[Haslo, ...]:
    """Hasła z pliku słowniczka w kolejności pliku; brak pliku to puste hasła, zły kształt wpisu to ValueError ze ścieżką."""
    dane = _dane(sciezka)
    hasla = []
    for nr, wpis in enumerate(dane.get("pojecia") or [], start=1):
        wpis = wpis if isinstance(wpis, dict) else {}
        odmiany = wpis.get("odmiany")
        if not (isinstance(wpis.get("pojecie"), str) and isinstance(wpis.get("wyjasnienie"), str) and isinstance(odmiany, list) and odmiany and all(isinstance(o, str) and o.strip() for o in odmiany)):
            raise ValueError(f"{sciezka}: hasło nr {nr} musi mieć pojecie, wyjasnienie i niepustą listę odmiany")
        hasla.append(Haslo(wpis["pojecie"], tuple(odmiany), wpis["wyjasnienie"], str(wpis.get("fakt") or "")))
    return tuple(hasla)


def _norma(forma: str) -> str:
    """Forma z pojedynczymi spacjami: twarda spacja i złamanie linii w tekście lekcji to zwykła spacja."""
    return re.sub(r"\s+", " ", forma).strip()


class Slownik:
    """Hasła i jeden wzór na wszystkie ich odmiany i frazy bez pogrubienia: dłuższe formy stoją w nim przed krótszymi, wielkość liter się liczy."""

    def __init__(self, hasla: tuple[Haslo, ...], bez_pogrubienia: tuple[str, ...] = ()):
        self.hasla = hasla
        self.forma_na_haslo: dict[str, int] = {}
        for nr, haslo in enumerate(hasla):
            for forma in haslo.odmiany:
                self.forma_na_haslo.setdefault(_norma(html.escape(forma, quote=False)), nr)  # tekst lekcji jest już po html.escape
        self.bez: set[str] = {_norma(html.escape(fraza, quote=False)) for fraza in bez_pogrubienia}
        formy = sorted([*self.forma_na_haslo, *self.bez], key=len, reverse=True)
        wzory = (r"\s+".join(re.escape(czesc) for czesc in forma.split(" ")) for forma in formy)
        self.wzor = re.compile(OD + "(?:" + "|".join(wzory) + ")" + DO) if formy else None

    def _element(self, nr: int, tekst: str) -> str:
        """Pogrubione słowo (do ruchu klawiaturą i dotyku) i ukryta podpowiedź, którą czyta aria-describedby; steruje nią strona/slowniczek.js."""
        haslo, pid = self.hasla[nr], f"pojecie-{nr}"
        pojecie, opis = html.escape(haslo.pojecie, quote=True), html.escape(haslo.wyjasnienie, quote=False)
        return (
            f'<span class="pojecie"><strong class="pojecie-slowo" role="button" tabindex="0" aria-expanded="false" aria-describedby="{pid}" data-pojecie="{pojecie}">{tekst}</strong>'
            f'<span class="pojecie-podp" role="tooltip"><span class="pojecie-nazwa" aria-hidden="true">{html.escape(haslo.pojecie, quote=False)}</span><span class="pojecie-opis" id="{pid}">{opis}</span></span></span>'
        )

    def _w_tekscie(self, tekst: str, uzyte: set[int]) -> str:
        wynik, poz = [], 0
        for m in self.wzor.finditer(tekst):  # po kolei od lewej; trafienie w pojęcie już pogrubione też zjada tekst, więc krótsza forma w środku nic nie łapie
            forma = _norma(m.group(0))
            if forma in self.bez:  # napis interfejsu albo nazwa programu: tekst zostaje, hasło nie jest zużyte (tekst trafienia i tak jest wycięty z dalszego szukania)
                continue
            nr = self.forma_na_haslo[forma]
            if nr in uzyte:
                continue
            uzyte.add(nr)
            wynik += [tekst[poz : m.start()], self._element(nr, m.group(0))]
            poz = m.end()
        return "".join(wynik) + tekst[poz:]

    def pogrub(self, html_lekcji: str) -> str:
        """Pierwsze wystąpienie każdego pojęcia w tekście akapitów i list (poza linkami i kodem) dostaje pogrubienie z podpowiedzią."""
        if self.wzor is None:
            return html_lekcji
        okruszki = OKRUSZKI.match(html_lekcji)
        poczatek = okruszki.end() if okruszki else 0
        wynik, stos, uzyte = [html_lekcji[:poczatek]], [], set()
        for kawalek in ZNACZNIK.split(html_lekcji[poczatek:]):
            if kawalek.startswith("<"):
                if (m := NAZWA_ZNACZNIKA.match(kawalek)) and m.group(2).lower() not in PUSTE and not kawalek.endswith("/>"):
                    nazwa = m.group(2).lower()
                    if m.group(1):
                        while stos and stos.pop() != nazwa:
                            pass
                    else:
                        stos.append(nazwa)
                wynik.append(kawalek)
            elif kawalek.strip() and AKAPITY.intersection(stos) and not WYKLUCZONE.intersection(stos):
                wynik.append(self._w_tekscie(kawalek, uzyte))
            else:
                wynik.append(kawalek)
        return "".join(wynik)


@lru_cache(maxsize=8)
def _slownik(sciezka: str, czas: int) -> Slownik:
    return Slownik(wczytaj(Path(sciezka)), wczytaj_bez_pogrubienia(Path(sciezka)))


def slownik(sciezka: Path = PLIK_SLOWNICZKA) -> Slownik:
    """Słownik z pliku (zapamiętany do zmiany pliku); brak pliku daje słownik bez haseł, który nic nie pogrubia."""
    return _slownik(str(sciezka), sciezka.stat().st_mtime_ns if sciezka.is_file() else 0)


def pogrub_pojecia(html_lekcji: str, sciezka: Path = PLIK_SLOWNICZKA) -> str:
    """Skrót dla generatora strony lekcji: pogrubia pojęcia ze słowniczka w HTML tekstu lekcji."""
    return slownik(sciezka).pogrub(html_lekcji)


def pogrubione(html_lekcji: str) -> list[str]:
    """Pojęcia pogrubione w HTML strony, w kolejności występowania (do sprawdzeń i zestawień)."""
    return [html.unescape(p) for p in re.findall(r'<strong class="pojecie-slowo"[^>]* data-pojecie="([^"]*)"', html_lekcji)]


_ALFABET = "aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż"
_ASCII = str.maketrans("ąćęłńóśźż", "acelnoszz")


def klucz_alfabetyczny(tekst: str) -> list[tuple[int, int]]:
    """Klucz sortowania po polsku: ą po a, ć po c itd., wielkość liter bez znaczenia, spacja i znaki przed literami."""
    return [(1, _ALFABET.index(c)) if c in _ALFABET else (0, ord(c)) for c in tekst.lower()]


def _kotwica(pojecie: str, zajete: set[str]) -> str:
    baza = re.sub(r"[^a-z0-9]+", "-", pojecie.lower().translate(_ASCII)).strip("-") or "haslo"
    kotwica, n = f"pojecie-{baza}", 1
    while kotwica in zajete:
        n += 1
        kotwica = f"pojecie-{baza}-{n}"
    zajete.add(kotwica)
    return kotwica


def adres_zrodla(adres: str) -> str:
    """Adres strony dokumentacji bez końcówki `.md` (fakty podają surowy Markdown, czytelnik ma stronę)."""
    return re.sub(r"\.md(?=#|$)", "", adres)


def zrodla_faktow(sciezka: Path) -> dict[str, str]:
    """Id faktu -> adres źródła z `dane/fakty.yaml`; brak pliku daje pusty słownik."""
    if not sciezka.is_file():
        return {}
    dane = yaml.safe_load(sciezka.read_text(encoding="utf-8")) or {}
    return {f["id"]: f["zrodlo"] for f in dane.get("fakty") or [] if isinstance(f, dict) and f.get("id") and f.get("zrodlo")}


def html_hasel(hasla: tuple[Haslo, ...], zrodla: dict[str, str]) -> str:
    """Lista haseł alfabetycznie: pojęcie, wyjaśnienie i odnośnik do źródła z faktu (gdy fakt ma źródło)."""
    zajete: set[str] = set()
    wiersze = []
    for h in sorted(hasla, key=lambda x: klucz_alfabetyczny(x.pojecie)):
        zrodlo = zrodla.get(h.fakt)
        odnosnik = ""
        if zrodlo:
            odnosnik = f'<p class="slowniczek-zrodlo"><a href="{html.escape(adres_zrodla(zrodlo), quote=True)}" aria-label="Źródło: {html.escape(h.pojecie, quote=True)}, dokumentacja Claude Code">Źródło w dokumentacji</a></p>'
        wiersze.append(
            f'<div class="slowniczek-haslo" id="{_kotwica(h.pojecie, zajete)}"><dt>{html.escape(h.pojecie, quote=False)}</dt>'
            f"<dd><p>{html.escape(h.wyjasnienie, quote=False)}</p>{odnosnik}</dd></div>"
        )
    return '<dl class="slowniczek-lista">\n' + "\n".join(wiersze) + "\n</dl>"


def zloz_strone_slowniczka(plik: Path = PLIK_SLOWNICZKA, fakty: Path = PLIK_FAKTOW, nazwa_kursu: str | None = None) -> str:
    """Samodzielna strona słowniczka (jeden plik HTML) w stylu strony lekcji: wszystkie hasła alfabetycznie z szablonu `strona/szablon-slowniczek.html`."""
    from narzedzia import strona  # tu, bo strona.py sama importuje ten moduł

    katalog = strona.KATALOG_STRONY
    hasla = wczytaj(plik)
    if not hasla:
        raise ValueError(f"{plik}: brak haseł słowniczka")
    wartosci = {
        "TYTUL": NAZWA_STRONY,
        "ZNAK": (katalog / "znak.svg").read_text(encoding="utf-8").strip(),
        "NAZWA": strona._nazwa_w_znaku(nazwa_kursu or strona.NAZWA_DOMYSLNA),
        "STYL": "\n".join((katalog / p).read_text(encoding="utf-8") for p in ("styl-strona.css", "styl-slowniczek.css")),
        "TRESC": html_hasel(hasla, zrodla_faktow(fakty)),
    }
    szablon = (katalog / "szablon-slowniczek.html").read_text(encoding="utf-8")
    return re.sub(r"\{\{([A-Z]+)\}\}", lambda m: wartosci[m.group(1)], szablon)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Składa stronę słowniczka kursu z dane/slowniczek.yaml w jeden plik HTML.")
    parser.add_argument("--wyjscie", type=Path, default=Path("build") / "slowniczek.html", help="plik wynikowy (domyślnie build/slowniczek.html)")
    parser.add_argument("--slowniczek", type=Path, default=PLIK_SLOWNICZKA, help="plik z hasłami (domyślnie dane/slowniczek.yaml)")
    parser.add_argument("--fakty", type=Path, default=PLIK_FAKTOW, help="plik faktów ze źródłami (domyślnie dane/fakty.yaml)")
    args = parser.parse_args(argv)
    try:
        strona_html = zloz_strone_slowniczka(args.slowniczek, args.fakty)
    except (OSError, ValueError, yaml.YAMLError) as blad:
        print(f"Błąd: {blad}", file=sys.stderr)
        return 1
    args.wyjscie.parent.mkdir(parents=True, exist_ok=True)
    args.wyjscie.write_text(strona_html, encoding="utf-8")
    print(f"Zapisano {args.wyjscie}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
