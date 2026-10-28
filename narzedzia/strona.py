"""Składa samodzielną stronę lekcji (jeden plik HTML) z lekcja.md, scenariusza, quizu i fiszek według strona/szablon.html."""

import argparse
import html
import json
import re
import sys
from pathlib import Path

import yaml

from narzedzia import strona_wyjasnienie as wyjasnienie  # odwracana karta: rysunek obrazkowy z przodu, schemat z tyłu
from narzedzia import strona_analogia as analogia  # komentarz analogii pod obrazem i lekcja bez scenariusz.json
from narzedzia.strona_slowniczek import pogrub_pojecia  # pogrubienie pojęć ze słowniczka w tekście lekcji
from narzedzia.strona_pliki import PLIKI_CSS, PLIKI_JS  # spis plików silnika wklejanych do strony
from narzedzia.strona_podglad import PODGLAD, PODGLAD_UZYTY, html_podgladu, sprawdz_podglady
from narzedzia.obrazy_lekcji import STYL as STYL_OBRAZU, ma_obraz, obraz_z_linii
from narzedzia.strona_zrodla import stopka_zrodel, wydziel_zrodla
from narzedzia.znacznik_lekcji import html_znacznika, wydziel

KORZEN = Path(__file__).resolve().parent.parent
KATALOG_STRONY = KORZEN / "strona"
BEZPIECZNY_ADRES = re.compile(r"(?:https?://|#)[^\s\"<>]*|[^\s:\"<>]*")
ZNACZNIK = re.compile(r"^\s*<!--\s*cwiczenie:\s*([\w-]+)\s*-->\s*$")
SENTYNEL = re.compile(r"\x01cw:([\w-]+)\x01")
KOLUMNY = re.compile(r"^\s*<!--\s*(/?)kolumny\s*-->\s*$")


def _link(m: re.Match) -> str:
    """Link tylko dla adresów http(s), kotwic i względnych bez dwukropka; inne zostają zwykłym tekstem."""
    # adres przeszedł już html.escape(quote=False), więc cudzysłów jest dosłowny; lecz bez zmian `&amp;` itd.
    adres = m.group(2)
    if not BEZPIECZNY_ADRES.fullmatch(adres):
        return m.group(0)
    return f'<a href="{html.escape(html.unescape(adres), quote=True)}">{m.group(1)}</a>'


def _inline(tekst: str) -> str:
    """Znaczniki w linii: `kod`, **pogrubienie**, *kursywa*, [tekst](adres), <kbd>; komentarze HTML znikają."""
    kody: list[str] = []

    def zapamietaj(m: re.Match) -> str:
        kody.append(m.group(1))
        return f"\x00{len(kody) - 1}\x00"

    tekst = re.sub(r"`([^`]+)`", zapamietaj, tekst)
    tekst = re.sub(r"<!--(?!\s*cwiczenie:).*?-->", "", tekst, flags=re.S)
    tekst = html.escape(tekst, quote=False)
    tekst = re.sub(r"&lt;(/?)(kbd|em|strong)&gt;", r"<\1\2>", tekst)
    tekst = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", tekst)
    tekst = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", tekst)
    tekst = re.sub(r"\[([^\]]+)\]\(([^)\s]*)\)", _link, tekst)
    tekst = re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{html.escape(kody[int(m.group(1))], quote=False)}</code>", tekst)
    return tekst.strip()


def markdown_na_html(tresc: str, katalog: Path | None = None) -> str:
    """Prosty konwerter: nagłówki, akapity, listy, bloki kodu; znacznik ćwiczenia daje sentynel \\x01cw:<id>\\x01.

    Blok `<!-- kolumny -->` … `<!-- /kolumny -->` stawia obok siebie kolumny zaczęte nagłówkiem `####`,
    a `<!-- podglad: <ćwiczenie> <terminal> [odpowiedź] -->` wstawia podgląd folderu po przebiegu z tego okna (w pierwszym menu odpowiedzią o podanym numerze od 0, domyślnie pierwszą); linia `![opis](plik)` daje obraz z podpisem z pliku w `katalog`.
    """
    wynik: list[str] = []
    akapit: list[str] = []
    lista: list[str] = []
    rodzaj_listy = ""
    kod: list[str] | None = None
    w_kolumnach = False
    kolumna_otwarta = False
    figura_wynik: int | None = None  # miejsce figury w `wynik`, gdy poprzednia linia była obrazem: komentarz analogii zaraz pod nią trafia do figury
    figura_karty: int | None = None  # miejsce figury, pod którą stoi ciąg komentarzy (analogia, wyjasnienie) w dowolnej kolejności
    pod_analogia = analogia.PodObrazem(_inline)

    def zamknij_akapit() -> None:
        if akapit:
            wynik.append("<p>" + _inline("\n".join(akapit)) + "</p>")
            akapit.clear()

    def zamknij_liste() -> None:
        nonlocal rodzaj_listy
        if lista:
            punkty = "".join(f"<li>{_inline(p)}</li>" for p in lista)
            wynik.append(f"<{rodzaj_listy}>{punkty}</{rodzaj_listy}>")
            lista.clear()
        rodzaj_listy = ""

    for linia in tresc.splitlines():
        pod_obrazem, figura_wynik = figura_wynik, None
        pod_komentarzami, figura_karty = figura_karty, None
        if kod is not None:
            if linia.strip().startswith("```"):
                wynik.append("<pre><code>" + html.escape("\n".join(kod), quote=False) + "</code></pre>")
                kod = None
            else:
                kod.append(linia)
            continue
        if linia.strip().startswith("```"):
            zamknij_akapit()
            zamknij_liste()
            kod = []
            continue
        if pod_komentarzami is not None and (karta := wyjasnienie.z_linii(linia)) is not None:  # komentarz wyjasnienie: obraz staje się kartą
            wynik[pod_komentarzami] = wyjasnienie.dodaj(wynik[pod_komentarzami], karta, katalog)
            figura_karty = figura_wynik = pod_komentarzami  # analogia może stać także pod komentarzem wyjasnienie
            continue
        if pod_analogia.linia(linia, wynik, pod_obrazem):  # komentarz analogii pod obrazem, w jednej linii albo w kilku
            figura_karty = pod_komentarzami
            continue
        if figura := obraz_z_linii(linia, katalog):
            zamknij_akapit()
            zamknij_liste()
            na_koncu = analogia.z_linii_obrazu(linia)  # komentarz analogii na końcu linii obrazu
            wynik.append(figura if na_koncu is None else analogia.dodaj(figura, na_koncu, _inline))
            figura_wynik = figura_karty = len(wynik) - 1
            continue
        kolumny = KOLUMNY.match(linia)
        podglad = PODGLAD.match(linia)
        if kolumny or podglad:
            zamknij_akapit()
            zamknij_liste()
            if podglad:
                wynik.append(html_podgladu(podglad))
                continue
            if kolumna_otwarta:
                wynik.append("</div>")
                kolumna_otwarta = False
            if w_kolumnach:
                wynik.append("</div>")
            w_kolumnach = not kolumny.group(1)
            if w_kolumnach:
                wynik.append('<div class="kolumny">')
            continue
        znacznik = ZNACZNIK.match(linia)
        if znacznik:
            zamknij_akapit()
            zamknij_liste()
            wynik.append(f"\x01cw:{znacznik.group(1)}\x01")
            continue
        if re.fullmatch(r"\s*<!--.*-->\s*", linia):
            continue
        if not linia.strip():
            zamknij_akapit()
            zamknij_liste()
            continue
        naglowek = re.match(r"(#{1,4})\s+(.*)", linia)
        if naglowek:
            zamknij_akapit()
            zamknij_liste()
            n = len(naglowek.group(1))
            if n == 4 and w_kolumnach:
                if kolumna_otwarta:
                    wynik.append("</div>")
                wynik.append('<div class="kolumna">')
                kolumna_otwarta = True
            wynik.append(f"<h{n}>{_inline(naglowek.group(2))}</h{n}>")
            continue
        punkt = re.match(r"\s*([-*]|\d+\.)\s+(.*)", linia)
        if punkt:
            zamknij_akapit()
            rodzaj = "ol" if punkt.group(1)[0].isdigit() else "ul"
            if rodzaj_listy and rodzaj_listy != rodzaj:
                zamknij_liste()
            rodzaj_listy = rodzaj
            lista.append(punkt.group(2))
            continue
        if lista and linia.startswith((" ", "\t")):
            lista[-1] += " " + linia.strip()
            continue
        zamknij_liste()
        akapit.append(linia)
    pod_analogia.koniec()
    zamknij_akapit()
    zamknij_liste()
    if kolumna_otwarta:
        wynik.append("</div>")
    if w_kolumnach:
        wynik.append("</div>")
    return "\n".join(wynik)


def _tytul(tresc: str, rezerwa: str) -> str:
    for linia in tresc.splitlines():
        if linia.startswith("# "):
            return _inline(linia[2:])
    return rezerwa


def _json_do_strony(obiekt) -> str:
    """JSON bezpieczny w znaczniku <script>: nawiasy ostre jako \\u003c, więc nic nie zamknie skryptu."""
    return json.dumps(obiekt, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e")


def _wczytaj_yaml(sciezka: Path, klucz: str) -> list:
    if not sciezka.is_file():
        return []
    try:
        dane = yaml.safe_load(sciezka.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as blad:
        raise ValueError(f"{sciezka}: {blad}") from blad
    return dane.get(klucz, []) if isinstance(dane, dict) else []


def _tresc_ze_znacznikami(html_lekcji: str, scenariusz: dict) -> str:
    """Wstawia miejsca na ćwiczenia w miejsce znaczników; znacznik bez ćwiczenia albo ćwiczenie bez znacznika to błąd."""
    znane = {cw["id"] for cw in scenariusz.get("cwiczenia", [])}
    uzyte = set(SENTYNEL.findall(html_lekcji))
    sprawdz_podglady(html_lekcji, scenariusz)
    if uzyte - znane:
        raise ValueError(f"znacznik ćwiczenia bez wpisu w scenariuszu: {sorted(uzyte - znane)}")
    if znane - uzyte:
        raise ValueError(f"ćwiczenie bez znacznika <!-- cwiczenie: id --> w lekcji: {sorted(znane - uzyte)}")
    kawalki = SENTYNEL.split(html_lekcji)  # tekst, id, tekst, id, ...
    wynik = []
    for i, kawalek in enumerate(kawalki):
        if i % 2:
            wynik.append(f'<div class="miejsce-cwiczenia" data-id="{kawalek}"></div>')
        elif kawalek.strip():
            wynik.append(f'<div class="tekst">\n{kawalek.strip()}\n</div>')
    return "\n".join(wynik)


NAZWA_DOMYSLNA = "Claude Code po ludzku"


def _nazwa_w_znaku(nazwa: str) -> str:
    """Nazwa kursu w nagłówku: „Claude Code” na górze (czcionka stałej szerokości), reszta na zakreślaczu; inna nazwa idzie cała na zakreślacz."""
    przedrostek = "Claude Code"
    if nazwa.startswith(przedrostek + " ") and nazwa[len(przedrostek):].strip():
        gora, dol = przedrostek, nazwa[len(przedrostek):].strip()
        return f'<span class="logo-cc">{html.escape(gora)}</span><span class="logo-pl"><span>{html.escape(dol)}</span></span>'
    return f'<span class="logo-pl"><span>{html.escape(nazwa)}</span></span>'


def zloz_strone(
    katalog: Path,
    scenariusz: Path | None = None,
    lekcja_md: Path | None = None,
    nazwa_kursu: str = NAZWA_DOMYSLNA,
) -> str:
    """Zwraca gotowy HTML strony lekcji z plików w katalogu lekcji (albo wskazanych wprost)."""
    lekcja_md = lekcja_md or katalog / "lekcja.md"
    bez_scenariusza = scenariusz is None and not (katalog / "scenariusz.json").is_file()  # brak pliku obok lekcji to strona bez ćwiczeń; plik wskazany wprost musi istnieć
    scenariusz = scenariusz or katalog / "scenariusz.json"
    tresc_md = lekcja_md.read_text(encoding="utf-8")
    try:
        dane_scen = analogia.SCENARIUSZ_PUSTY if bez_scenariusza else json.loads(scenariusz.read_text(encoding="utf-8"))
    except json.JSONDecodeError as blad:
        raise ValueError(f"{scenariusz}: {blad}") from blad
    quiz = _wczytaj_yaml(katalog / "quiz.yaml", "pytania")
    fiszki = _wczytaj_yaml(katalog / "fiszki.yaml", "fiszki")
    szablon = (KATALOG_STRONY / "szablon.html").read_text(encoding="utf-8")
    polozenie, tresc_bez_okruszkow = wydziel(tresc_md)
    tresc_bez_okruszkow, zrodla_md = wydziel_zrodla(tresc_bez_okruszkow)
    html_lekcji = pogrub_pojecia(markdown_na_html(tresc_bez_okruszkow, katalog))  # pierwsze wystąpienie pojęcia ze słowniczka z podpowiedzią
    if bez_scenariusza:
        analogia.sprawdz_bez_scenariusza(html_lekcji, SENTYNEL, PODGLAD_UZYTY, lekcja_md)
    pliki_css = PLIKI_CSS + ((STYL_OBRAZU,) if ma_obraz(html_lekcji) else ())
    wartosci = {
        "TYTUL": _tytul(tresc_md, katalog.name),
        "ZNAK": (KATALOG_STRONY / "znak.svg").read_text(encoding="utf-8").strip(),
        "NAZWA": _nazwa_w_znaku(nazwa_kursu),
        "ZNACZNIK": html_znacznika(polozenie),
        "STYL": "\n".join((KATALOG_STRONY / p).read_text(encoding="utf-8") for p in pliki_css),
        "TRESC": _tresc_ze_znacznikami(html_lekcji, dane_scen),
        "SCENARIUSZ": _json_do_strony(dane_scen),
        "QUIZ": _json_do_strony(quiz),
        "FISZKI": _json_do_strony(fiszki),
        "ZRODLA": stopka_zrodel(markdown_na_html(zrodla_md, katalog) if zrodla_md else ""),
        "SILNIK": "\n".join((KATALOG_STRONY / p).read_text(encoding="utf-8") for p in PLIKI_JS),
    }
    return re.sub(r"\{\{([A-Z]+)\}\}", lambda m: wartosci[m.group(1)], szablon)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Składa stronę lekcji z symulatorem w jeden plik HTML.")
    parser.add_argument("katalog", type=Path, help="katalog lekcji (lekcja.md, scenariusz.json, quiz.yaml, fiszki.yaml)")
    parser.add_argument("--wyjscie", type=Path, help="plik wynikowy (domyślnie build/<nazwa-katalogu>.html)")
    parser.add_argument("--scenariusz", type=Path, help="plik scenariusza zamiast <katalog>/scenariusz.json")
    parser.add_argument("--lekcja-md", type=Path, help="plik tekstu lekcji zamiast <katalog>/lekcja.md")
    parser.add_argument("--nazwa-kursu", default=NAZWA_DOMYSLNA, help=f"nazwa kursu w nagłówku strony (domyślnie „{NAZWA_DOMYSLNA}”)")
    args = parser.parse_args(argv)
    try:
        strona = zloz_strone(args.katalog, args.scenariusz, args.lekcja_md, args.nazwa_kursu)
    except (OSError, ValueError, json.JSONDecodeError) as blad:
        print(f"Błąd: {blad}", file=sys.stderr)
        return 1
    wyjscie = args.wyjscie or Path("build") / f"{args.katalog.resolve().name}.html"
    wyjscie.parent.mkdir(parents=True, exist_ok=True)
    wyjscie.write_text(strona, encoding="utf-8")
    print(f"Zapisano {wyjscie}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
