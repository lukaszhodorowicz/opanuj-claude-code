"""Przeklikuje każde ćwiczenie złożonej lekcji jak kursant w Chrome bez okna i zapisuje dziennik JSON ze zrzutem po każdym kroku.

Wywołanie: `uv run python -m narzedzia.kursant <build/lekcja-*.html> <katalog wyniku> [--szerokosci 1280 390] [--bez-zrzutow]`.
Droga każdego ćwiczenia na każdej szerokości: start, klik ostatniego polecenia poza kolejnością, „Od nowa”, polecenia
po kolei (przed każdym opcja 0 otwartego okna wyboru, a gdy polecenie jest nieaktywne, znacznik „kliknij tutaj”), po
ostatnim poleceniu okna wyboru i znaczniki aż do efektu końcowego (`koniec`; ćwiczenie bez poleceń od razu po starcie),
„Od nowa”, podwójny klik w pierwsze polecenie, „Od nowa”. Stan po kroku zapisuje się po 12 s bez zmian na stronie. Po każdym kroku
dziennik zapisuje, co było klikalne, czy zmienił się symulator i nauczyciel, błędy konsoli; `usterki` to rozjazdy wykryte
maszynowo. Klika skrypt `narzedzia/kursant.js`; ocena według listy kontrolnej należy do agenta `kursant` (`.claude/agents/kursant.md`).
"""

import argparse
import html
import itertools
import json
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from narzedzia.zrzuty import CHROME, chrome, przytnij

# ms czasu wirtualnego na drogę jednego ćwiczenia (skrypt kończy wcześniej) i px między
# środkiem znacznika „kliknij tutaj” a środkiem wskazanego elementu
BUDZET, ODCHYLENIE_ZNACZNIKA = 1500000, 40

BLEDY = """<script>
window.__kursantBledy = [];
addEventListener("error", (e) => __kursantBledy.push(String(e.message)));
addEventListener("unhandledrejection", (e) => __kursantBledy.push("promise: " + String(e.reason)));
(() => { const ce = console.error; console.error = (...a) => { __kursantBledy.push(a.map(String).join(" ")); ce(...a); }; })();
</script>"""

SKRYPT = (Path(__file__).with_suffix(".js")).read_text(encoding="utf-8")

RAMKA = (
    '<!doctype html><body style="margin:0"><iframe src="{src}" width="{szer}" height="14000" style="border:0;display:block">'
    '</iframe><script>addEventListener("message", (e) => {{ if (!e.data || !e.data.kursant) return; const p = document.createElement("pre");'
    ' p.id = "kursant-dziennik"; p.textContent = JSON.stringify(e.data.kursant); document.body.append(p); }});</script></body>'
)


def strona_kursanta(tekst: str, plan: dict) -> str:
    """Strona lekcji z łapaczem błędów konsoli w `<head>` i skryptem kursanta przed `</body>`."""
    tekst = re.sub(r"(<head[^>]*>)", lambda m: m.group(1) + BLEDY, tekst, count=1)
    skrypt = SKRYPT.replace("__PLAN__", json.dumps(plan))
    return tekst.replace("</body>", f"<script>\n{skrypt}</script></body>")


def uruchom(strona: Path, plan: dict, szer: int, tmp: Path, ms: int, png=None) -> dict:
    """Jedno uruchomienie Chrome: z `png` robi zrzut okna, bez niego zwraca dziennik skryptu."""
    nazwa = f"{plan['cw']}-{szer}-{plan['stop']}"
    kopia = tmp / f"{nazwa}.html"
    kopia.write_text(strona_kursanta(strona.read_text("utf-8"), plan), "utf-8")
    cel, okno = kopia, szer
    # Chrome bez okna ma min. 500 px szerokości: węższy ekran daje ramka, jak w zrzuty.py
    if szer < 500:
        cel, okno = tmp / f"{nazwa}-ramka.html", 500
        cel.write_text(RAMKA.format(src=kopia.name, szer=szer), "utf-8")
    if png:
        chrome(okno, plan["okno_wys"], ms, f"--screenshot={png}", cel.as_uri())
        return {}
    dom = chrome(okno, 900, ms, "--dump-dom", cel.as_uri()).stdout
    trafienie = re.search(r'<pre id="kursant-dziennik">(.*?)</pre>', dom, re.DOTALL)
    if not trafienie:
        raise RuntimeError(f"{nazwa}: skrypt kursanta nie oddał dziennika.")
    return json.loads(html.unescape(trafienie.group(1)))


def usterki(cw: dict) -> list[str]:
    """Rozjazdy, które widać w dzienniku jednego ćwiczenia bez patrzenia na zrzuty."""
    kroki, wynik = cw["kroki"], []
    if not kroki:
        return [f"ćwiczenie nie dało dziennika: {cw.get('blad', 'brak kroków')}"]
    start = kroki[0]
    aktywne = [p["tekst"] for p in start["polecenia"] if p["klikalny"]]
    if len(aktywne) > 1:
        wynik.append(
            f"start: aktywne {len(aktywne)} polecenia naraz ({'; '.join(aktywne)}), "
            "aktywne ma być tylko pierwsze"
        )
    po_jednym = next((k for k in kroki if k["krok"] == "polecenie-1"), None)
    wyglad = lambda k: [(p["klikalny"], p["wyslane"]) for p in k["polecenia"]]
    for nr, (poprz, k) in enumerate(itertools.pairwise(kroki), 1):
        przed, rodzaj, co = f"krok {nr}:", k["krok"], f"„{k['klik']}”"
        if rodzaj == "poza-kolejnoscia" and k["okno"] != poprz["okno"]:
            wynik.append(f"{przed} polecenie {co} poza kolejnością zmieniło symulator")
        if rodzaj.startswith("polecenie-"):
            # po „Od nowa”, które samo zagrało ćwiczenie, ta sama usterka padła już przy „Od nowa”
            zagrane = poprz["krok"] == "od-nowa" and poprz["okno"] != start["okno"]
            bez_zmian = (k["okno"], k["nauczyciel"]) == (
                poprz["okno"],
                poprz["nauczyciel"],
            )
            if bez_zmian and not zagrane:
                wynik.append(
                    f"{przed} polecenie {co} w kolejności niczego nie zmieniło"
                )
            p = k["polecenia"][int(rodzaj.split("-")[1]) - 1]
            if p["klikalny"] and not p["wyslane"]:
                wynik.append(
                    f"{przed} wysłane polecenie {co} nadal aktywne, bez „wysłane”"
                )
        if rodzaj == "od-nowa" and [k["okno"], *wyglad(k)] != [
            start["okno"],
            *wyglad(start),
        ]:
            wynik.append(f"{przed} „Od nowa” nie wraca do stanu startowego")
        if rodzaj == "podwojny-klik" and po_jednym and k["okno"] != po_jednym["okno"]:
            wynik.append(f"{przed} podwójny klik daje inny symulator niż pojedynczy")
    for nr, k in enumerate(kroki):
        z = k["znacznik"]
        if z and (z["odchylenie"] or 0) > ODCHYLENIE_ZNACZNIKA:
            wynik.append(
                f"krok {nr}: „kliknij tutaj” {z['odchylenie']} px obok „{z['element']}”"
            )
    if any(k["w_bok"] for k in kroki):
        wynik.append(
            f"przy szerokości {cw['szer']} px ćwiczenie wychodzi poza ekran w bok"
        )
    if any(k["pola_do_wpisania"] for k in kroki):
        wynik.append("ćwiczenie ma pole do wpisywania, a kursant tylko klika")
    if not start["folder"]:
        wynik.append("ćwiczenie nie ma podglądu folderu")
    if all(k["krok"] != "od-nowa" for k in kroki):
        wynik.append("ćwiczenie nie ma przycisku „Od nowa”")
    return wynik + [f"błąd konsoli: {b}" for b in dict.fromkeys(cw.get("bledy") or [])]


def przebieg(strona: Path, cw_id: str, szer: int, tmp: Path) -> dict:
    """Dziennik jednego ćwiczenia; błąd jednego przebiegu nie zatrzymuje kontroli reszty."""
    # Chrome bez okna czasem zawisa bez powodu; kolejna próba przechodzi
    for proba in range(3):
        try:
            return uruchom(strona, {"cw": cw_id, "stop": None}, szer, tmp, BUDZET)
        except subprocess.TimeoutExpired as e:
            blad = e
            continue
        except (RuntimeError, ValueError, subprocess.SubprocessError) as e:
            blad = e
            break
    return {"kroki": [], "blad": str(blad), "proby": proba + 1}


def zrob_zrzuty(strona: Path, cw: dict, wyjscie: Path, tmp: Path) -> None:
    """Zrzut ćwiczenia po każdym kroku: osobne uruchomienie, które staje po kroku `j`."""

    def jeden(j: int, k: dict) -> None:
        png = wyjscie / f"{cw['id']}-{cw['szer']}-{j:02d}-{k['krok']}.png"
        y, wys = max(0, k["y"] - 12), min(k["wys"] + 24, 6000)
        plan = {"cw": cw["id"], "stop": j, "okno_wys": y + wys + 20}
        # Chrome bez okna czasem zawisa bez powodu; kolejna próba przechodzi
        for _ in range(3):
            try:
                uruchom(strona, plan, cw["szer"], tmp, k["t"] + 3000, png)
                break
            except subprocess.TimeoutExpired:
                continue
        k["zrzut"] = png.name if png.is_file() else None
        if k["zrzut"]:
            przytnij(png, y, wys, cw["szer"])

    with ThreadPoolExecutor(4) as pula:
        list(pula.map(jeden, *zip(*enumerate(cw["kroki"]))))


def kontrola(strona: Path, wyjscie: Path, szerokosci: list[int], zrzuty=True) -> dict:
    """Przeklikuje ćwiczenia strony na każdej szerokości; dziennik zapisuje do `dziennik.json`."""
    wyjscie.mkdir(parents=True, exist_ok=True)
    dz = {
        "strona": str(strona),
        "szerokosci": szerokosci,
        "cwiczenia": [],
        "usterki": [],
    }
    tekst = strona.read_text(encoding="utf-8")
    spis = re.findall(r'class="miejsce-cwiczenia" data-id="([^"]+)"', tekst)
    with tempfile.TemporaryDirectory() as katalog, ThreadPoolExecutor(4) as pula:
        tmp = Path(katalog)
        pary = [(szer, cw_id) for szer in szerokosci for cw_id in spis]
        dzienniki = pula.map(lambda p: przebieg(strona, p[1], p[0], tmp), pary)
        for (szer, cw_id), wynik in zip(pary, dzienniki, strict=True):
            cw = {"id": cw_id, "szer": szer, **wynik}
            if zrzuty:
                zrob_zrzuty(strona, cw, wyjscie, tmp)
            cw["usterki"] = usterki(cw) + [
                f"krok {j}: brak zrzutu, Chrome nie odpowiedział trzy razy"
                for j, k in enumerate(cw["kroki"])
                if zrzuty and not k.get("zrzut")
            ]
            dz["cwiczenia"].append(cw)
            dz["usterki"] += [
                {"cw": cw_id, "szer": szer, "opis": u} for u in cw["usterki"]
            ]
    tekst = json.dumps(dz, ensure_ascii=False, indent=1)
    (wyjscie / "dziennik.json").write_text(tekst, encoding="utf-8")
    return dz


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Przeklikuje ćwiczenia lekcji jak kursant."
    )
    parser.add_argument(
        "strona", type=Path, help="złożona lekcja: build/lekcja-<slug>.html"
    )
    parser.add_argument("wyjscie", type=Path, help="katalog na dziennik.json i zrzuty")
    parser.add_argument("--szerokosci", type=int, nargs="+", default=[1280, 390])
    parser.add_argument("--bez-zrzutow", action="store_true", help="sam dziennik")
    args = parser.parse_args(argv)
    for plik in (Path(CHROME), args.strona):
        if not plik.is_file():
            print(f"Brak pliku {plik}.")
            return 1
    wyjscie = args.wyjscie.resolve()
    try:
        dz = kontrola(
            args.strona.resolve(), wyjscie, args.szerokosci, not args.bez_zrzutow
        )
    except (RuntimeError, OSError, ValueError, subprocess.SubprocessError) as e:
        print(f"Kontrola kursanta nie wyszła: {e}")
        return 1
    print(f"Przebiegi ćwiczeń: {len(dz['cwiczenia'])}, usterki: {len(dz['usterki'])}.")
    for u in dz["usterki"]:
        print(f"- {u['cw']} {u['szer']} px: {u['opis']}")
    print(wyjscie / "dziennik.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
