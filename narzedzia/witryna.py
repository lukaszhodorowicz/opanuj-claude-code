"""Składa witrynę kursu do wystawienia przez GitHub Pages (strona startowa, strony lekcji z nawigacją i zapisem, CNAME) i odświeża spis lekcji w README."""

import argparse
import html
import re
import shutil
import sys
from pathlib import Path

from narzedzia import witryna_ramki as ramki
from narzedzia.witryna_agenci import html_kto_za_tym_stoi
from narzedzia.strona import KATALOG_STRONY, zloz_strone
from narzedzia.witryna_spis import (
    Lekcja,
    Modul,
    grupuj,
    wczytaj_plan,
    zapowiedzi,
    zbierz_lekcje,
)

KORZEN = Path(__file__).resolve().parent.parent
PLAN = Path("moduly") / "PLAN-MODULOW.md"
STYLE_STARTU = ("styl-strona.css", "styl-start.css")
OPIS = "Darmowy kurs Claude Code po polsku dla przedsiębiorców, marketerów i freelancerów. Krótkie lekcje i ćwiczenia w przeglądarce, bez programowania."


def domena(korzen: Path = KORZEN) -> str:
    """Adres strony kursu z pliku CNAME (jedno źródło dla GitHub Pages, README i strony)."""
    return (korzen / "CNAME").read_text(encoding="utf-8").strip()


def _plik_strony(nazwa: str) -> str:
    return (KATALOG_STRONY / nazwa).read_text(encoding="utf-8")


def html_spisu(moduly: list[Modul]) -> str:
    """Spis na stronie startowej: moduły z lekcjami i miejscem na znacznik postępu (bez zapowiedzi, Łukasz 28.10.2026)."""
    czesci = []
    for m in moduly:
        punkty = "".join(
            f'<li data-postep-lekcja="{html.escape(l.adres)}"><a href="{html.escape(l.adres)}">{html.escape(l.tytul)}</a></li>'
            for l in m.lekcje
        )
        czesci.append(
            f'<div class="spis-modul"><h3><span class="spis-modul-nr">Moduł {m.numer}</span>{html.escape(m.nazwa)}</h3>'
            f'<ol class="spis-lekcje">{punkty}</ol></div>'
        )
    return "\n".join(czesci)


def strona_startowa(moduly: list[Modul], adres: str) -> str:
    """HTML strony startowej z szablonu strona/start.html."""
    wartosci = {
        "NAZWA_TEKST": html.escape(ramki.NAZWA_KURSU),
        "TYTUL_H1": html.escape(ramki.NAZWA_KURSU).replace(
            "Claude Code", '<span class="tytul-cc">Claude Code</span>', 1
        ),
        "PODTYTUL": html.escape(ramki.PODTYTUL),
        "HASLO": html.escape(ramki.HASLO),
        "OPIS_KURSU": ramki.OPIS_KURSU,
        "OPIS": html.escape(OPIS),
        "ADRES": html.escape(adres),
        "STYL": "\n".join(_plik_strony(p) for p in STYLE_STARTU),
        "ZNAK": _plik_strony("znak.svg").strip(),
        "NAZWA": f'<span class="logo-pl"><span>{html.escape(ramki.NAZWA_KURSU)}</span></span>',
        "ZAPIS": ramki.html_zapisu("start-gora"),
        "SPIS": html_spisu(moduly),
        "KLOCKI": '<span class="postep-klocek"></span>' * 20,  # jeden klocek = 5% kursu
        "DISCORD": ramki.html_discord(),
        "KTO": html_kto_za_tym_stoi(),
        # cały znacznik <script> w kodzie, nie w szablonie: formatowanie szablonu przerabia {{…}} wewnątrz <script> na kod JS
        "SKRYPT": f"<script>\n{_plik_strony('postep.js')}\n</script>",
        "SKRYPT_ZAPISU": ramki.skrypt_zapisu(),
    }
    return re.sub(
        r"\{\{([A-Z0-9_]+)\}\}", lambda m: wartosci[m.group(1)], _plik_strony("start.html")
    )


LINK_DO_LEKCJI = re.compile(r'href="([\w-]+)\.html(#[^"]*)?"')


def przepisz_linki(strona: str, adresy: dict[str, str], do_startu: str) -> str:
    """Odsyłacze lekcji do innych lekcji („pierwsze-zadanie.html”) prowadzą na witrynie pod /<moduł>/<lekcja>/; nieznany slug zostaje bez zmian."""
    def zamien(m: re.Match) -> str:
        adres = adresy.get(m.group(1))
        return f'href="{do_startu}{adres}{m.group(2) or ""}"' if adres else m.group(0)

    return LINK_DO_LEKCJI.sub(zamien, strona)


def strona_lekcji(
    lekcja: Lekcja,
    poprzednia: Lekcja | None,
    nastepna: Lekcja | None,
    z_zapisem: bool,
    adresy: dict[str, str] | None = None,
) -> str:
    """Strona lekcji ze składacza lekcji plus dodatki witryny przed </body>; silnika lekcji nie zmienia, tylko przepisuje odsyłacze między lekcjami."""
    strona = zloz_strone(lekcja.katalog, nazwa_kursu=ramki.NAZWA_KURSU)
    do_startu = "../../"
    strona = strona.replace(
        '<a class="logo" href="#">', f'<a class="logo" href="{do_startu}">', 1
    )
    strona = przepisz_linki(strona, adresy or {}, do_startu)
    naglowek_zapisu = (
        "Koniec modułu. Chcesz wiedzieć o kolejnych?"
        if lekcja.numer == lekcja.liczba
        else "Dalsze lekcje tego modułu są w przygotowaniu"
    )
    zapis = (
        ramki.html_zapisu(f"koniec-modulu-{lekcja.modul}", naglowek_zapisu)
        if z_zapisem
        else ""
    )
    dodatki = (
        f"<style>\n{_plik_strony('styl-start.css')}\n</style>\n"
        f'<div class="dodatki-lekcji">{ramki.html_nawigacji(lekcja.adres, poprzednia, nastepna, do_startu)}'
        f"{zapis}{ramki.html_discord()}</div>\n"
        f"<script>\n{_plik_strony('postep.js')}\n</script>\n"
        f"{ramki.skrypt_zapisu() if z_zapisem else ''}\n"
    )
    if "</body>" not in strona:
        raise ValueError(
            f"{lekcja.katalog}: strona lekcji bez </body>, nie ma gdzie dołożyć nawigacji"
        )
    poz = strona.rindex("</body>")
    return strona[:poz] + dodatki + strona[poz:]


def zbuduj(korzen: Path, wyjscie: Path) -> list[Lekcja]:
    """Zapisuje witrynę do katalogu `wyjscie` (czyszcząc go) i zwraca opublikowane lekcje."""
    lekcje = zbierz_lekcje(korzen)
    moduly = grupuj(lekcje)
    plan = wczytaj_plan(korzen / PLAN)
    adres = f"https://{domena(korzen)}/"
    if wyjscie.exists():
        shutil.rmtree(wyjscie)
    wyjscie.mkdir(parents=True)
    ostatnie_w_module = {m.lekcje[-1] for m in moduly}
    adresy = {l.katalog.name: l.adres for l in lekcje}  # slug lekcji -> adres na witrynie
    for i, lekcja in enumerate(lekcje):
        poprzednia = lekcje[i - 1] if i > 0 else None
        nastepna = lekcje[i + 1] if i + 1 < len(lekcje) else None
        try:
            tresc = strona_lekcji(
                lekcja, poprzednia, nastepna, lekcja in ostatnie_w_module, adresy
            )
        except (OSError, ValueError) as blad:
            raise ValueError(
                f"lekcja {lekcja.katalog_modulu}/{lekcja.katalog.name}: {blad}"
            ) from blad
        cel = wyjscie / lekcja.adres / "index.html"
        cel.parent.mkdir(parents=True, exist_ok=True)
        cel.write_text(tresc, encoding="utf-8")
    (wyjscie / "index.html").write_text(
        strona_startowa(moduly, adres), encoding="utf-8"
    )
    shutil.copytree(KATALOG_STRONY / "zasoby", wyjscie / "zasoby")  # obrazki strony startowej
    (wyjscie / "CNAME").write_text(domena(korzen) + "\n", encoding="utf-8")
    (wyjscie / ".nojekyll").write_text(
        "", encoding="utf-8"
    )  # GitHub Pages bez przeróbek Jekylla
    return lekcje


def _tekst_linku(tytul: str) -> str:
    """Tytuł bezpieczny w [tekst](adres): nawiasy kwadratowe poprzedzone ukośnikiem."""
    return re.sub(r"([\[\]])", r"\\\1", tytul)


def markdown_spisu(moduly: list[Modul], adres: str) -> str:
    """Spis lekcji do README: moduły i numerowane linki do stron lekcji na domenie kursu."""
    if not moduly:
        return "Pierwsze lekcje są w przygotowaniu."
    czesci = []
    for m in moduly:
        linki = "\n".join(
            f"{n}. [{_tekst_linku(l.tytul)}]({adres}{l.adres})"
            for n, l in enumerate(m.lekcje, 1)
        )
        czesci.append(f"### Moduł {m.numer}. {m.nazwa}\n\n{linki}")
    return "\n\n".join(czesci)


def markdown_zapowiedzi(plan: list[Modul], moduly: list[Modul]) -> str:
    """Sekcja README z planem kolejnych modułów (D-2026-10-24-06): moduły z planu, z których nic jeszcze nie wyszło; pusta, gdy wyszło wszystko."""
    w_przygotowaniu = zapowiedzi(plan, moduly)
    if not w_przygotowaniu:
        return ""
    czesci = []
    for m in w_przygotowaniu:
        lekcje = "\n".join(f"- {t}" for t in m.lekcje)
        czesci.append(f"### Moduł {m.numer}. {m.nazwa}\n\n{lekcje}".rstrip())
    zapis = ramki.adres_newslettera("github", "zapowiedzi-readme")
    return (
        "## W przygotowaniu\n\n" + "\n\n".join(czesci)
        + f"\n\nChcesz wiedzieć, kiedy wyjdą? [Zapisz się na newsletter]({zapis}).\n"
    )


def _wstaw(tekst: str, znacznik: str, tresc: str) -> str:
    """Treść między znacznikami <!-- znacznik:start --> i <!-- znacznik:end -->, każdy w osobnej linii."""
    wzor = re.compile(
        rf"(<!-- {znacznik}:start -->)\n.*?(<!-- {znacznik}:end -->)", re.S
    )
    tresc = tresc.strip("\n")
    if not wzor.search(tekst):
        raise ValueError(
            f"README bez znaczników <!-- {znacznik}:start --> i <!-- {znacznik}:end -->"
        )
    return wzor.sub(lambda m: f"{m.group(1)}\n{tresc}\n{m.group(2)}", tekst, count=1)


def odswiez_readme(korzen: Path) -> tuple[str, str]:
    """Zwraca (stary, nowy) tekst README z odświeżonym spisem lekcji i zapowiedziami."""
    plik = korzen / "README.md"
    stary = plik.read_text(encoding="utf-8")
    moduly = grupuj(zbierz_lekcje(korzen))
    adres = f"https://{domena(korzen)}/"
    nowy = _wstaw(stary, "spis-lekcji", markdown_spisu(moduly, adres))
    nowy = _wstaw(
        nowy, "zapowiedzi", markdown_zapowiedzi(wczytaj_plan(korzen / PLAN), moduly)
    )
    return stary, nowy


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Witryna kursu: skład strony do GitHub Pages i spis lekcji w README."
    )
    pod = parser.add_subparsers(dest="polecenie", required=True)
    p_zbuduj = pod.add_parser(
        "zbuduj", help="składa witrynę do katalogu (domyślnie build/witryna)"
    )
    p_zbuduj.add_argument("--wyjscie", type=Path, default=Path("build") / "witryna")
    p_readme = pod.add_parser(
        "readme", help="odświeża spis lekcji i zapowiedzi w README.md"
    )
    p_readme.add_argument(
        "--sprawdz",
        action="store_true",
        help="tylko sprawdza, czy README jest aktualne (kod 1, gdy nie)",
    )
    args = parser.parse_args(argv)
    try:
        if args.polecenie == "zbuduj":
            lekcje = zbuduj(KORZEN, args.wyjscie)
            print(
                f"Zapisano {args.wyjscie}: strona startowa, stron lekcji: {len(lekcje)}"
            )
            return 0
        stary, nowy = odswiez_readme(KORZEN)
        if args.sprawdz:
            print(
                "README aktualne"
                if stary == nowy
                else "README nieaktualne: uruchom `uv run python -m narzedzia.witryna readme`"
            )
            return 0 if stary == nowy else 1
        (KORZEN / "README.md").write_text(nowy, encoding="utf-8")
        print("README: spis lekcji odświeżony" if stary != nowy else "README bez zmian")
        return 0
    except (OSError, ValueError) as blad:
        print(f"Błąd: {blad}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
