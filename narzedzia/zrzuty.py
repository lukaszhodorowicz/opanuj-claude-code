"""Robi zrzuty strony lekcji w Chrome bez okna, według planu ujęć liczonego ze scenariusza lekcji.

Wywołanie: `uv run python -m narzedzia.zrzuty <katalog lekcji> --strona <plik html> [--wyjscie <katalog>] [--bez-znacznika | --bez-luki] [ujęcie ...]`.
Plan ujęć (`narzedzia/zrzuty_plan.py`): `start-1280` (cała strona), `<id ćwiczenia>-po-przebiegu` dla każdego ćwiczenia
(przewinięte do ćwiczenia, kliknięte pierwsze polecenie, o ile zadanie nie ma `start_od_razu`, w każdym oknie wyboru opcja 0;
w ćwiczeniu aplikacji z drogami dalej cała droga pierwszego polecenia: skrypt klika po kolei element ze znacznikiem „kliknij tutaj”,
aż znaczników nie będzie, więc ujęcie pokazuje koniec drogi, nie początek; na kolejny znacznik skrypt czeka tyle, ile najdłuższa przerwa drogi,
liczona wzorami silnika w `narzedzia/zrzuty_czas.py`, nie krócej niż 15 s) i `<id pierwszego ćwiczenia>-390` (start na szerokości
telefonu). Jeśli w katalogu lekcji leży `zrzuty.json`, jego wpisy `nazwa -> {szer, wys, budzet, polecenie?, do?, opcje?, klik?, droga?,
bez_znacznika?, bez_luki?}` dopisują nowe ujęcia albo nadpisują pola ujęć z planu (`polecenie` i `do` to id ćwiczenia, `opcje` to lista par
`[id ćwiczenia, numer opcji]`, `klik` to lista selektorów CSS klikanych po kolei po poleceniu, np. drugie polecenie ćwiczenia
aplikacji; na element, którego jeszcze nie ma, skrypt czeka do 15 s). Jawna lista `klik` albo `"droga": false` wyłącza przechodzenie
całej drogi: gra tylko pierwsze polecenie i to, co wpis wymienia. Pole `droga` z id ćwiczenia, którego nie ma na stronie (albo `"droga": true` bez
`polecenie` i `do`), przerywa ujęcie komunikatem „na stronie nie ma ćwiczenia o id …”. W nowym ujęciu brakujące `szer`, `wys` i `budzet` mają wartości
1280, 1500 i 20000.

Zrzut bez znacznika: flaga `--bez-znacznika` (wszystkie ujęcia tego wywołania) albo `"bez_znacznika": true` we wpisie `zrzuty.json`
(jedno ujęcie) chowa przed zrzutem znacznik „kliknij tutaj” (pigułkę ze strzałką) i obwódkę z podświetleniem celu, żeby obraz w tekście
lekcji nie wyglądał jak przycisk do kliknięcia. Znaczniki znikają przez `visibility: hidden` i wyłączone `outline`, `box-shadow`
i animację, więc układ strony się nie zmienia (po znaczniku zostaje puste miejsce, np. wiersz między pozycjami menu), a stan ćwiczenia
(np. menu otwarte przez kroki drogi) zostaje taki, jaki jest. Flaga `--bez-luki` (pole `"bez_luki": true`) idzie dalej: znacznik i jego
rząd wypadają z układu, więc obraz wygląda jak aplikacja bez kursu (menu bez pustego wiersza), ale elementy pod znacznikiem stoją
wyżej niż w ujęciu ze znacznikiem.
Pozycje menu i list wyglądają na zrzucie bez znacznika równo: w ćwiczeniu pozycje inne niż cel kliknięcia są wygaszone
(`aria-disabled`, `opacity: 0.38` z `strona/styl-aplikacja-plus-menu.css`: lista trybów, menu +, jego podmenu, menu modelu z wierszem
Effort, lista poziomów wysiłku), a w aplikacji wszystkie pozycje takiej listy mają pełne krycie. Kopia strony do zrzutu (`BEZ_ZNACZNIKA`,
także przy `--bez-luki`) przywraca im pełne krycie; kursant w ćwiczeniu dalej widzi wygaszenie. Szare zostają elementy, które w aplikacji
naprawdę są szare: pozycje z klasą `apl-poz-wylaczona` (w menu +: Import GitHub issue, a w sesji w chmurze Add folder i Plugins, każda z podpisem;
klasę nadaje `strona/aplikacja-plus.js`), Ultracode, szare paski danych konta i napisy pomocnicze (to inne elementy niż `.apl-menu-poz`).
Wygaszone zostają też przyciski, które nie są pozycjami menu ani listy: krzyżyk i strzałka ‹ okien i paneli, przyciski kart zgody i planu
oraz ptaszek w czasie odliczania.
Napis „Claude czeka: N s” (odliczanie przed ptaszkiem) nie jest znacznikiem kliknięcia i zostaje. Element pokazany tylko dlatego, że
jest celem (ikona ⋮ w wierszu listy, która w aplikacji pojawia się po najechaniu), zostaje widoczny, tylko bez obwódki.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from narzedzia.png_przytnij import przytnij_png
from narzedzia.zrzuty_plan import plan_ujec

CHROME_MAC = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CHROME_NAZWY = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")
LIMIT_CHROME = 120  # sekundy; zwykły zrzut trwa kilka, dłuższe czekanie znaczy, że Chrome utknął


def znajdz_chrome() -> str:
    """Ścieżka do Chrome: zmienna `PRZEWODNIK_CHROME`, potem Mac, potem `PATH`; bez trafienia ścieżka Maca."""
    wlasna = os.environ.get("PRZEWODNIK_CHROME")
    if wlasna:
        return wlasna
    if Path(CHROME_MAC).is_file():
        return CHROME_MAC
    for nazwa in CHROME_NAZWY:
        znaleziony = shutil.which(nazwa)
        if znaleziony:
            return znaleziony
    return CHROME_MAC


CHROME = znajdz_chrome()


def flagi_chrome() -> list[str]:
    """Dodatkowe flagi Chrome dla tej maszyny: na Linuksie jako root Chrome bez `--no-sandbox` się nie uruchomi."""
    if sys.platform.startswith("linux") and os.geteuid() == 0:
        return ["--no-sandbox"]
    return []


SKRYPT = """
<script>
(() => {
  const plan = %s;
  const czekaj = (ms) => new Promise((r) => setTimeout(r, ms));
  /* Chrome bez okna nie dokańcza animacji w czasie wirtualnym: kończymy je przed zrzutem, potem przewijamy do ćwiczenia */
  const przewin = () => {
    document.getAnimations().forEach((a) => { try { a.finish(); } catch (e) {} });
    if (parent !== window) parent.postMessage({ wys: document.documentElement.scrollHeight }, "*");
    if (plan.do) { const e = document.getElementById(plan.do); if (e) { const y = Math.round(e.getBoundingClientRect().top + window.scrollY); document.body.dataset.y = y; if (parent !== window) parent.postMessage(y, "*"); } }
  };
  /* cała droga ćwiczenia aplikacji: klika element ze znacznikiem, aż znaczników nie będzie; na każdy czeka najdłużej `droga_przerwa` ms (domyślnie 15 s), bo między znacznikami grają kroki drogi (nauczyciel do 9 s, mysli do 10 s, pisanie) */
  async function droga(cw) {
    const sek = document.getElementById(cw);
    const ile = Math.ceil((plan.droga_przerwa || 15000) / 250);
    for (let i = 0; i < 60; i++) {
      let e = null;
      for (let t = 0; t < ile && !(e = sek.querySelector(".apl-cel")); t++) await czekaj(250);
      if (!e) return;
      await czekaj(900);
      e.click();
      await czekaj(300);
    }
  }
  /* błąd planu: strona nie ma ćwiczenia; skrypt zapisuje go na stronie (w ramce przesyła do ramki zewnętrznej), a narzedzia/zrzuty.py przerywa ujęcie czytelnym komunikatem */
  const blad = (kod) => { document.body.dataset.blad = kod; if (parent !== window) parent.postMessage({ blad: kod }, "*"); };
  async function wybierz(cw, nr) {
    for (let i = 0; i < 200; i++) {
      const wolne = [...document.querySelectorAll('#' + cw + ' .opcja:not([disabled])')];
      if (wolne.length) { wolne[nr].click(); return; }
      await czekaj(250);
    }
  }
  (async () => {
    await czekaj(300);
    if (plan.droga && !document.getElementById(plan.droga)) return blad("droga");
    if (plan.polecenie) document.querySelector('#' + plan.polecenie + ' .polecenie').click();
    for (const [cw, nr] of plan.opcje || []) { await wybierz(cw, nr); await czekaj(400); }
    if (plan.droga) await droga(plan.droga);
    /* selektor czeka, aż element się pojawi (np. ścieżka pliku w odpowiedzi Claude), najdłużej 15 s */
    for (const sel of plan.klik || []) { await czekaj(1200); for (let i = 0; i < 60 && !document.querySelector(sel); i++) await czekaj(250); const e = document.querySelector(sel); if (e) e.click(); }
  })();
  setInterval(przewin, 300);
})();
</script>
"""

# zrzut bez znacznika: układ zostaje (visibility, nie display), znika tylko to, co mówi „kliknij tutaj”; pozycje menu i list dostają pełne krycie (w aplikacji nic na liście nie jest wygaszone przez kurs), poza naprawdę szarymi
BEZ_ZNACZNIKA = """<style>
.apl-tag:not(.apl-odliczanie) { visibility: hidden !important; }
.apl-cel, .apl-cel-obok { outline: none !important; box-shadow: none !important; animation: none !important; }
.apl-menu-poz[aria-disabled="true"]:not(.apl-poz-wylaczona) { opacity: 1 !important; }
</style>"""
# zrzut bez znacznika i bez luki: znacznik i jego rząd wypadają z układu, więc menu i lista są takie jak w aplikacji, bez pustego wiersza
BEZ_LUKI = """<style>
.apl-tag:not(.apl-odliczanie), .apl-tag-rzad:has(> .apl-tag:not(.apl-odliczanie)) { display: none !important; }
</style>"""


def chrome(
    szer: int, wys: int, budzet: int, *reszta: str
) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            CHROME,
            "--headless=new",
            "--disable-gpu",
            *flagi_chrome(),
            "--hide-scrollbars",
            f"--window-size={szer},{wys}",
            f"--virtual-time-budget={budzet}",
            *reszta,
        ],
        capture_output=True,
        text=True,
        timeout=LIMIT_CHROME,
        check=False,
    )


def html_ujecia(strona: Path, ujecie: dict) -> str:
    """Strona lekcji w kształcie, w jakim idzie do Chrome: ze stylem zrzutu bez znacznika (jeśli ujęcie go chce) i ze skryptem planu (klikanie ćwiczenia przed zrzutem)."""
    plan = {k: ujecie[k] for k in ("polecenie", "do", "opcje", "klik", "droga", "droga_przerwa") if k in ujecie}
    bez_luki = ujecie.get("bez_luki")
    style = (BEZ_ZNACZNIKA if ujecie.get("bez_znacznika") or bez_luki else "") + (BEZ_LUKI if bez_luki else "")
    return strona.read_text(encoding="utf-8").replace("</body>", style + SKRYPT % json.dumps(plan) + "</body>")


def zrob(nazwa: str, ujecie: dict, strona: Path, wyjscie: Path) -> Path:
    """Zrzut okna szer x wys; z polem `do` zrzut zaczyna się 12 px nad tym ćwiczeniem (wysokie okno, potem przycięcie obrazu)."""
    szer, wys, budzet = ujecie["szer"], ujecie["wys"], ujecie["budzet"]
    if ujecie.get("droga") is True:  # plan zamienia `true` na id z pola `polecenie` albo `do`; bez nich nie ma od czego zacząć
        raise RuntimeError(f"{nazwa}: droga: true wymaga pola polecenie albo do z id ćwiczenia, od którego zaczyna się przejście drogi.")
    html = html_ujecia(strona, ujecie)
    kopia = wyjscie / f"{nazwa}.html"
    kopia.write_text(html, encoding="utf-8")
    png = wyjscie / f"{nazwa}.png"
    cel, okno = kopia, szer
    if szer < 500:
        # Chrome bez okna ma co najmniej 500 px szerokości, więc węższy ekran daje ramka iframe o tej szerokości
        cel = wyjscie / f"{nazwa}-ramka.html"
        # wysokość ramki rośnie do wysokości treści (stała ucinała długie lekcje); file:// blokuje contentDocument,
        # więc treść sama wysyła wysokość komunikatem
        cel.write_text(
            f'<!doctype html><body style="margin:0"><iframe src="{kopia.name}" width="{szer}" height="1000" '
            'style="border:0;display:block"></iframe><script>addEventListener("message", (e) => '
            '{ const f = document.querySelector("iframe"); if (e.data && e.data.blad) document.body.dataset.blad = e.data.blad; else if (e.data && e.data.wys) '
            "{ if (e.data.wys > f.height) f.height = e.data.wys; } else document.body.dataset.y = e.data; });</script></body>",
            encoding="utf-8",
        )
        okno = 500
    y = 0
    if ujecie.get("do") or ujecie.get("droga"):
        dom = chrome(okno, 900, 3000, "--dump-dom", cel.as_uri()).stdout
        if 'data-blad="droga"' in dom:
            raise RuntimeError(f"{nazwa}: na stronie nie ma ćwiczenia o id „{ujecie['droga']}” (pole droga).")
        if ujecie.get("do"):
            trafienie = re.search(r'data-y="(\d+)"', dom)
            if not trafienie:
                raise RuntimeError(
                    f"{nazwa}: na stronie nie ma ćwiczenia o id „{ujecie['do']}”."
                )
            y = max(0, int(trafienie.group(1)) - 12)
    chrome(okno, y + wys, budzet, f"--screenshot={png}", cel.as_uri())
    if not png.is_file():
        raise RuntimeError(f"{nazwa}: Chrome nie zapisał zrzutu.")
    przytnij(png, y, wys, szer)
    return png


def przytnij(png: Path, y: int, wys: int, szer: int) -> None:
    """Wycina z obrazu pas `wys` x `szer` od wiersza `y` i lewej krawędzi (czysty Python, patrz `png_przytnij`)."""
    przytnij_png(png, y, wys, szer)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Robi zrzuty strony lekcji według planu ze scenariusza."
    )
    parser.add_argument("lekcja", type=Path, help="katalog lekcji ze scenariusz.json")
    parser.add_argument(
        "--strona",
        type=Path,
        required=True,
        help="plik html lekcji (z narzedzia.strona)",
    )
    parser.add_argument(
        "--wyjscie",
        type=Path,
        help="katalog zrzutów (domyślnie build/zrzuty/<nazwa lekcji>)",
    )
    parser.add_argument(
        "--bez-znacznika",
        action="store_true",
        help="chowa znacznik „kliknij tutaj” i obwódkę celu we wszystkich ujęciach tego wywołania",
    )
    parser.add_argument(
        "--bez-luki",
        action="store_true",
        help="jak --bez-znacznika, a rząd znacznika też znika z układu (menu bez pustego wiersza, jak w aplikacji)",
    )
    parser.add_argument(
        "ujecia",
        nargs="*",
        help="nazwy ujęć do zrobienia (domyślnie wszystkie z planu)",
    )
    args = parser.parse_intermixed_args(argv)
    if not Path(CHROME).is_file():
        print(f"Brak Chrome pod ścieżką {CHROME}.")
        return 1
    if not (args.lekcja / "scenariusz.json").is_file():
        print(f"W katalogu {args.lekcja} nie ma scenariusz.json.")
        return 1
    if not args.strona.is_file():
        print(f"Brak pliku strony {args.strona}.")
        return 1
    plan = plan_ujec(args.lekcja)
    nieznane = [n for n in args.ujecia if n not in plan]
    if nieznane:
        print(f"Nieznane ujęcia: {', '.join(nieznane)}. W planie: {', '.join(plan)}.")
        return 1
    for ujecie in plan.values():
        ujecie.update({k: True for k in ("bez_znacznika", "bez_luki") if getattr(args, k)})
    wyjscie = (args.wyjscie or Path("build/zrzuty") / args.lekcja.resolve().name).resolve()
    wyjscie.mkdir(parents=True, exist_ok=True)
    try:
        for nazwa in args.ujecia or plan:
            print(zrob(nazwa, plan[nazwa], args.strona, wyjscie))
    except (RuntimeError, ValueError, subprocess.SubprocessError) as e:
        print(f"Zrzut nie wyszedł: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
