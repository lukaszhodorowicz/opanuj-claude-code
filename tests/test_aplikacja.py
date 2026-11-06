"""Testy symulatora aplikacji Claude: walidator rodzaju `aplikacja`, napisy w strona/aplikacja-ikony.js, składanie strony i zrzuty."""

import copy
import json
import re
from pathlib import Path

import pytest

from narzedzia import scenariusz as sc
from narzedzia import zrzuty
from narzedzia.scenariusz_aplikacja import licznik
from narzedzia.strona import zloz_strone

KORZEN = Path(__file__).resolve().parent.parent
WZOR = json.loads((Path(__file__).parent / "dane" / "aplikacja.json").read_text(encoding="utf-8"))
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


def cw(d):
    return d["cwiczenia"][0]


def bledy(d, napisy=NAPISY):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, napisy)


def test_wzor_bez_bledow(dane):
    assert bledy(dane) == []


def test_licznik_liczy_linijki(dane):
    assert licznik(cw(dane)["aplikacja"]["zmiany"]) == "+2 -3"


@pytest.mark.parametrize(
    "pole, wartosc, fragment",
    [
        ("tryb", "Accept Edits", "tryb „Accept Edits”"),
        ("tryb", "Changes", "tryb „Changes” spoza Auto/Manual/Accept edits/Plan"),
        ("srodowisko", "This computer", "srodowisko „This computer”"),
        ("folder", "~/Klientka", "folder"),
    ],
)
def test_pola_udajace_interfejs(dane, pole, wartosc, fragment):
    cw(dane)["aplikacja"][pole] = wartosc
    assert any(fragment in b for b in bledy(dane))


def test_licznik_spoza_wzoru(dane):
    bez_wzoru = [w for w in NAPISY if "wzor" not in w or w.get("gdzie") != "aplikacja"]
    assert any("licznik „+2 -3”" in b for b in bledy(dane, bez_wzoru))


def test_plik_bez_zmienionej_linijki(dane):
    for l in cw(dane)["aplikacja"]["zmiany"][0]["linijki"]:
        l.pop("zmiana", None)
    assert any("bez żadnej linijki" in b for b in bledy(dane))


def test_uwaga_przy_linijce_odrzucona(dane):
    """Próba z Łukaszem 25.10.2026: w folderze bez gita uwagi przy linijce nie da się dopisać, więc symulator jej nie pokazuje."""
    cw(dane)["kroki"].append(
        {"klik": "linijka", "linijka": 4, "uwaga": "Zostaw rabat", "etykieta": "x", "nauczyciel": "x"}
    )
    wynik = bledy(dane)
    assert any("klik „linijka”" in b for b in wynik)
    assert any("pole uwaga" in b for b in wynik) and any("pole linijka" in b for b in wynik)


def test_linijki_widoku_niczego_nie_otwieraja():
    js = (KORZEN / "strona" / "aplikacja.js").read_text(encoding="utf-8")
    assert "apl-uwaga" not in js and "linijka" not in js


def test_nieznany_klik_i_fakt(dane):
    cw(dane)["kroki"][0]["klik"] = "stop"
    cw(dane)["kroki"][0]["fakt"] = "nie-ma-takiego"
    wynik = bledy(dane)
    assert any("klik „stop”" in b for b in wynik)
    assert any("nie-ma-takiego" in b for b in wynik)


def test_zle_typy_bez_wyjatku(dane):
    cw(dane)["aplikacja"]["zmiany"][0]["linijki"] = 5
    cw(dane)["id"] = 'a"b'
    wynik = bledy(dane)
    assert any("niepustej listy linijki" in b for b in wynik)
    assert any("^[a-z0-9-]+$" in b for b in wynik)


def test_folder_z_tylda(dane):
    cw(dane)["aplikacja"]["folder"] = "~Klientka"
    assert any("bez / i ~" in b for b in bledy(dane))


def test_przyklad_z_formatu_bez_bledow(dane):
    tekst = (KORZEN / "dane" / "FORMAT-SCENARIUSZA.md").read_text(encoding="utf-8")
    przyklad = tekst[tekst.index("## Symulator aplikacji Claude") :]
    kod = re.search(r"```json\n(.*?)```", przyklad, re.S).group(1).replace("…", "x")
    cwiczenie = json.loads(kod)
    cwiczenie["kroki"][0]["fakt"] = cw(dane)["kroki"][0]["fakt"]
    cwiczenie["aplikacja"]["rozmowa"][1]["fakt"] = cw(dane)["kroki"][0]["fakt"]
    dane["cwiczenia"] = [cwiczenie]
    assert bledy(dane) == []


def test_brak_krokow(dane):
    cw(dane)["kroki"] = []
    assert any("niepustej listy kroki" in b for b in bledy(dane))


def test_napisy_w_pliku_js_sa_na_liscie():
    js = (KORZEN / "strona" / "aplikacja-ikony.js").read_text(encoding="utf-8")
    blok = re.search(r"PK\.NAPISY_APLIKACJI = \{(.*?)\};", js, re.S).group(1)
    napisy = re.findall(r':\s*"([^"]+)"', blok)
    lista = sc._Napisy(NAPISY)
    assert napisy and all(lista.jest(n, "aplikacja") for n in napisy)


def test_strona_sklada_cwiczenie_aplikacji(tmp_path):
    (tmp_path / "lekcja.md").write_text("# Próbka\n\n<!-- cwiczenie: cw1 -->\n", encoding="utf-8")
    (tmp_path / "scenariusz.json").write_text(json.dumps(WZOR, ensure_ascii=False), encoding="utf-8")
    html = zloz_strone(tmp_path)
    assert 'data-id="cw1"' in html
    assert "PK.aplikacja = function" in html and "PK.htmlAplikacji" in html
    assert ".apl-okno" in html and ".apl-widok-zmian" in html
    assert html.index("PK.aplikacja = function") < html.index('cw.rodzaj === "aplikacja"')


def test_zrzuty_json_przekazuje_klik(tmp_path):
    (tmp_path / "scenariusz.json").write_text(json.dumps(WZOR), encoding="utf-8")
    (tmp_path / "zrzuty.json").write_text(json.dumps({"uwaga": {"polecenie": "cw1", "klik": ["#cw1 .x"]}}), encoding="utf-8")
    assert zrzuty.plan_ujec(tmp_path)["uwaga"]["klik"] == ["#cw1 .x"]
    assert "plan.klik" in zrzuty.SKRYPT


def test_przyciecie_od_gory_nie_bierze_srodka(tmp_path):
    from narzedzia.png_przytnij import wczytaj, zapisz

    # Piksel w wierszu r i kolumnie k ma kolor (r, k, 200): po wyniku widać, skąd pochodzi każdy piksel.
    szer_obrazu, wys_obrazu = 9, 12
    png = tmp_path / "a.png"
    zapisz(png, szer_obrazu, wys_obrazu, 2, [bytearray(b for k in range(szer_obrazu) for b in (r, k, 200)) for r in range(wys_obrazu)])
    zrzuty.przytnij(png, 0, 5, 4)
    szer, wys, typ_koloru, wiersze = wczytaj(png)
    assert (szer, wys, typ_koloru) == (4, 5, 2)
    piksele = [[tuple(w[3 * k : 3 * k + 3]) for k in range(szer)] for w in wiersze]
    assert piksele == [[(r, k, 200) for k in range(4)] for r in range(5)]
