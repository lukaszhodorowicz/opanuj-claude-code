"""Pilnuje, żeby strona lekcji nie miała słowa „symulat…” w tym, co kursant widzi albo słyszy z czytnika ekranu (D-2026-10-27-54): w HTML strony poza komentarzami i skryptami, w literałach tekstowych silnika JS i w stylach CSS poza komentarzami."""

import json
import re
from pathlib import Path

import pytest

from narzedzia import strona

KORZEN = Path(__file__).resolve().parent.parent
KATALOG_STRONY = KORZEN / "strona"
DANE = Path(__file__).parent / "dane"
SLOWO = re.compile(r"symulat", re.IGNORECASE)
PO_SLOWIE_KLUCZOWYM = {"return", "typeof", "case", "in", "of", "else", "do", "void", "delete", "throw", "new"}
PO_ZNAK_REGEX = set("(,=:[!&|?{};+-*%<>~^")


def literaly_js(zrodlo: str) -> list[tuple[int, str]]:
    """Zwraca (numer linii, treść) każdego napisu w cudzysłowach, apostrofach i backtickach; komentarze `//` i `/* */` pomija, a `${...}` w szablonie czyta jako kod. Źle zamknięty napis, komentarz albo wyrażenie regularne to ValueError."""
    wynik: list[tuple[int, str]] = []
    n, i, linia, poprzedni = len(zrodlo), 0, 1, ""
    stos: list[list] = [["k", [0]]]  # ["k", [głębokość {}]] to kod, ["s", kawałki, linia startu] to szablon
    while i < n:
        c, gora = zrodlo[i], stos[-1]
        if gora[0] == "s":
            if c == "\\":
                gora[1].append(zrodlo[i : i + 2])
                linia += zrodlo.count("\n", i, i + 2)
                i += 2
            elif c == "`":
                wynik.append((gora[2], "".join(gora[1])))
                stos.pop()
                poprzedni, i = "`", i + 1
            elif zrodlo.startswith("${", i):
                stos.append(["k", [0]])
                poprzedni, i = "", i + 2
            else:
                linia += c == "\n"
                gora[1].append(c)
                i += 1
            continue
        if c == "\n":
            linia += 1
            i += 1
        elif c.isspace():
            i += 1
        elif zrodlo.startswith("//", i):
            koniec = zrodlo.find("\n", i)
            i = n if koniec < 0 else koniec
        elif zrodlo.startswith("/*", i):
            koniec = zrodlo.find("*/", i + 2)
            if koniec < 0:
                raise ValueError(f"linia {linia}: komentarz bez końca")
            linia += zrodlo.count("\n", i, koniec)
            i = koniec + 2
        elif c in "\"'":
            j, kawalki = i + 1, []
            while j < n and zrodlo[j] != c:
                if zrodlo[j] == "\n":
                    raise ValueError(f"linia {linia}: napis bez końca")
                kawalki.append(zrodlo[j : j + 2] if zrodlo[j] == "\\" else zrodlo[j])
                j += 2 if zrodlo[j] == "\\" else 1
            if j >= n:
                raise ValueError(f"linia {linia}: napis bez końca")
            wynik.append((linia, "".join(kawalki)))
            poprzedni, i = c, j + 1
        elif c == "`":
            stos.append(["s", [], linia])
            i += 1
        elif c == "}" and gora[1][0] == 0 and len(stos) > 1:
            stos.pop()  # koniec `${...}`, wracamy do tekstu szablonu
            i += 1
        elif c == "/" and _zaczyna_regex(zrodlo, i, poprzedni):
            j, w_klasie = i + 1, False
            while j < n and (zrodlo[j] != "/" or w_klasie):
                if zrodlo[j] == "\n":
                    raise ValueError(f"linia {linia}: wyrażenie regularne bez końca")
                w_klasie = (zrodlo[j] == "[") or (w_klasie and zrodlo[j] != "]")
                j += 2 if zrodlo[j] == "\\" else 1
            while j + 1 < n and zrodlo[j + 1].isalpha():
                j += 1
            poprzedni, i = '"', j + 1
        else:
            if c in "{}":
                gora[1][0] += 1 if c == "{" else -1
            poprzedni, i = c, i + 1
    if len(stos) != 1:
        raise ValueError("szablon albo wyrażenie `${}` bez końca")
    return wynik


def _zaczyna_regex(zrodlo: str, i: int, poprzedni: str) -> bool:
    """`/` zaczyna wyrażenie regularne po operatorze, nawiasie otwierającym, średniku albo słowie typu `return`; po wartości to dzielenie."""
    if poprzedni == "" or poprzedni in PO_ZNAK_REGEX or poprzedni == "}":
        return True
    slowo = re.search(r"[A-Za-z_$][\w$]*$", zrodlo[max(0, i - 12) : i].rstrip())
    return bool(slowo and slowo.group(0) in PO_SLOWIE_KLUCZOWYM)


def pliki_js() -> list[str]:
    """Pliki silnika ze spisu PLIKI_JS oraz każdy inny strona/*.js, żeby plik poza spisem nie ukrył słowa."""
    return sorted(set(strona.PLIKI_JS) | {p.name for p in KATALOG_STRONY.glob("*.js")})


def trafienia_literalow(nazwa: str) -> list[str]:
    zrodlo = (KATALOG_STRONY / nazwa).read_text(encoding="utf-8")
    return [f"{nazwa}:{linia}: {tekst[:90]}" for linia, tekst in literaly_js(zrodlo) if SLOWO.search(tekst)]


def test_czytnik_literalow_pomija_komentarze_i_widzi_napisy():
    zrodlo = (
        "/* Symulator w komentarzu */\n// symulator w drugim\n"
        "const a = \"w symulatorze\"; const b = 'Symulator';\n"
        "const c = `<p>${x ? `<i>${y}</i>` : \"ok\"}Symulator</p>`;\n"
        "const d = /[\"'`]/.test(a) ? 1 / 2 : 3; const e = 'bez';\n"
        "const f = [1, 2].map((z) => z / 2); const g = \"https://adres\"; /* jeszcze symulator */\n"
    )
    napisy = literaly_js(zrodlo)
    assert [(l, t) for l, t in napisy if SLOWO.search(t)] == [(3, "w symulatorze"), (3, "Symulator"), (4, "<p>Symulator</p>")]
    assert (5, "bez") in napisy and (6, "https://adres") in napisy


@pytest.mark.parametrize("zepsute", ["const a = 'bez końca;\n", "/* bez końca", "const a = `bez końca", "const a = `${x"])
def test_czytnik_literalow_zglasza_zle_zamkniete_zrodlo(zepsute):
    with pytest.raises(ValueError):
        literaly_js(zepsute)


@pytest.mark.parametrize("nazwa", pliki_js())
def test_silnik_js_czytnik_dochodzi_do_konca_pliku_i_znajduje_napisy(nazwa):
    zrodlo = (KATALOG_STRONY / nazwa).read_text(encoding="utf-8")
    assert literaly_js(zrodlo), f"{nazwa}: czytnik nie znalazł żadnego napisu, więc pewnie się zgubił"


def test_silnik_js_bez_slowa_symulat_w_napisach():
    """Każdy napis z „symulat” w strona/*.js to błąd; komentarze, nazwy klas i identyfikatorów bez słowa nie istnieją, więc wyjątków nie ma."""
    trafienia = [t for nazwa in pliki_js() for t in trafienia_literalow(nazwa)]
    assert trafienia == [], "napisy z „symulat” w silniku:\n" + "\n".join(trafienia)


def test_podpis_nad_oknem_aplikacji_nazywa_aplikacje():
    napisy = [t for _, t in literaly_js((KATALOG_STRONY / "aplikacja-okno.js").read_text(encoding="utf-8"))]
    assert any('<p class="apl-podpis">Aplikacja Claude na komputer, zakładka Code</p>' in t for t in napisy)


def test_style_css_bez_slowa_symulat_poza_komentarzami():
    trafienia = []
    for plik in sorted(KATALOG_STRONY.glob("*.css")):
        bez_komentarzy = re.sub(r"/\*.*?\*/", "", plik.read_text(encoding="utf-8"), flags=re.DOTALL)
        trafienia += [f"{plik.name}: {m.group(0)}" for m in re.finditer(r".{0,40}symulat.{0,40}", bez_komentarzy, re.IGNORECASE)]
    assert trafienia == []


def widoczny_html(katalog: Path, dane: dict) -> str:
    """Strona lekcji z ćwiczeniami z danych próbnych bez komentarzy HTML, stylów i skryptów (te dwa ostatnie pilnują testy wyżej)."""
    (katalog / "lekcja.md").write_text("# Próba\n\n" + "".join(f"<!-- cwiczenie: {c['id']} -->\n\n" for c in dane["cwiczenia"]), encoding="utf-8")
    (katalog / "scenariusz.json").write_text(json.dumps(dane, ensure_ascii=False), encoding="utf-8")
    pelny = strona.zloz_strone(katalog)
    return re.sub(r"<!--.*?-->|<style\b.*?</style>|<script\b.*?</script>", "", pelny, flags=re.DOTALL | re.IGNORECASE)


@pytest.mark.parametrize("plik", sorted(DANE.glob("*.json")), ids=lambda p: p.name)
def test_html_strony_lekcji_bez_slowa_symulat(plik, tmp_path):
    """Złożona strona z danych próbnych (aplikacja z drogami, menu +, katalog, wtyczki, harmonogram, telefon, sesje, terminal) nie ma „symulat” poza komentarzami."""
    dane = json.loads(plik.read_text(encoding="utf-8"))
    if "cwiczenia" not in dane:
        pytest.skip("plik próbny bez ćwiczeń")
    widoczne = widoczny_html(tmp_path, dane)
    assert "miejsce-cwiczenia" in widoczne and "Sprawdź się" in widoczne, "strona nie złożyła się w całość"
    trafienia = [m.group(0) for m in re.finditer(r".{0,50}symulat.{0,50}", widoczne, re.IGNORECASE)]
    assert trafienia == []
