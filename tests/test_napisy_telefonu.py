"""Testy napisów telefonu z Remote Control i strony Settings → Claude Code (zrzuty Łukasza z 27.10.2026): napisy `PK.NAPISY_TELEFONU` i `PK.USTAWIENIA_CC` mają wpisy w `dane/napisy-interfejsu.yaml` ze zrzutem w `zrodlo` w kształcie „zrzut Łukasza 27.10.2026, plik materialy/zrzuty-lukasza/<plik> w pamięci projektu”, opisy dla czytnika ekranu nie powtarzają napisów aplikacji, dokumentacja formatu opisuje nowe pola i kroki, a nowe pliki silnika mają docstring i do 300 linii."""

import json
import re
from pathlib import Path

from narzedzia import scenariusz as sc

KORZEN = Path(__file__).resolve().parent.parent
WPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")
NAPISY = sc._Napisy(WPISY)
FORMAT = (KORZEN / "dane" / "FORMAT-SCENARIUSZA.md").read_text(encoding="utf-8")
ZRZUT_TELEFONU = re.compile(r"^zrzut Łukasza 27\.10\.2026, plik materialy/zrzuty-lukasza/IMG_105[6-9]\.PNG w pamięci projektu")
ZRZUT_SETTINGS = re.compile(r"^zrzut Łukasza 27\.10\.2026, plik materialy/zrzuty-lukasza/zrzut_2026-10-27_04-44-01\.png w pamięci projektu|^zrzut Łukasza 27\.10\.2026, plik materialy/zrzuty-lukasza/zrzut_2026-10-27_\d\d-\d\d-\d\d\.png w pamięci projektu; także zrzut_2026-10-27_04-44-01\.png; ")  # napis „Remote Control” jest wspólny z kartą Environment: jeden wpis, zrzut Settings w „także”
NOWE_PLIKI = (
    "narzedzia/scenariusz_telefon.py",
    "strona/aplikacja-telefon-dane.js",
    "strona/aplikacja-telefon-widok.js",
    "strona/aplikacja-telefon.js",
    "strona/aplikacja-ustawienia-cc.js",
    "strona/styl-aplikacja-telefon.css",
    "strona/styl-aplikacja-telefon-rozmowa.css",
    "strona/styl-aplikacja-ustawienia-cc.css",
)


def stala(plik: str, nazwa: str):
    """Obiekt JSON przypisany do `PK.<nazwa>` w pliku JS (stałe są zapisane jak JSON: cudzysłowy przy kluczach)."""
    js = (KORZEN / "strona" / plik).read_text(encoding="utf-8")
    return json.loads(re.search(rf"PK\.{nazwa} = (\{{.*?\}});\n", js, re.S).group(1))


def wpisy(napis: str, gdzie: str) -> list[dict]:
    return [w for w in WPISY if w.get("napis") == napis and w.get("gdzie") == gdzie]


def napisy_telefonu() -> list[str]:
    n = stala("aplikacja-telefon-dane.js", "NAPISY_TELEFONU")
    return [v for k, v in n.items() if k not in ("model", "wysilek")] + [f"{n['model']} {n['wysilek']}"]


def napisy_settings() -> list[str]:
    u = stala("aplikacja-ustawienia-cc.js", "USTAWIENIA_CC")
    return [u["wyglad"], u["widok"]["nazwa"], u["widok"]["opis"], *u["widok"]["pozycje"], u["zdalne"], *[t for p in u["przelaczniki"] for t in (p["nazwa"], p["opis"])]]


def test_napisy_telefonu_sa_na_liscie_z_gdzie_telefon_i_zrzutem_img():
    napisy = napisy_telefonu()
    assert len(napisy) == 7
    for n in napisy:
        assert NAPISY.jest(n, "telefon"), f"napis „{n}” nie ma wpisu gdzie: telefon"
        assert any(ZRZUT_TELEFONU.search(w["zrodlo"]) for w in wpisy(n, "telefon")), f"napis „{n}” nie podaje zrzutu telefonu IMG_1056-IMG_1059 w zrodlo"


def test_napisy_strony_settings_sa_na_liscie_z_gdzie_aplikacja_i_zrzutem_04_44_01():
    napisy = napisy_settings()
    assert len(napisy) == 13
    for n in napisy:
        assert NAPISY.jest(n, "aplikacja"), f"napis „{n}” nie ma wpisu gdzie: aplikacja"
        assert any(ZRZUT_SETTINGS.search(w["zrodlo"]) for w in wpisy(n, "aplikacja")), f"napis „{n}” nie podaje zrzutu 04-44-01 w zrodlo"


def test_napisy_telefonu_nie_trafiaja_na_liste_aplikacji_i_odwrotnie():
    """Lista `gdzie: telefon` jest osobna: napis telefonu nie udaje napisu okna na komputerze."""
    for n in ("Devices", "Sessions", "New session", "now", "Reply to Claude or hold to talk", "Opus 5.5 Extra"):
        assert not NAPISY.jest(n, "aplikacja"), n
    for n in napisy_settings():
        assert not NAPISY.jest(n, "telefon"), n


def test_wpisy_z_wiecej_niz_jednym_zrzutem_maja_ksztalt_takze():
    for w in WPISY:
        zr = w.get("zrodlo", "")
        if w.get("gdzie") == "telefon" and "; także " in zr:
            assert re.search(r"w pamięci projektu; także IMG_105[6-9]\.PNG(, IMG_105[6-9]\.PNG)*; ", zr), zr
        if w.get("napis") in napisy_settings() and "; także " in zr:
            assert re.search(r"w pamięci projektu; także zrzut_2026-10-27_04-(?:07-11|44-01)\.png; ", zr), zr


def test_remote_control_ma_jeden_wpis_z_obu_zrzutow():
    """Napis „Remote Control” (karta Environment i nagłówek części w Settings) to jeden wpis, nie dwa: zrzut 04-44-01 stoi w jego „także”."""
    w = wpisy("Remote Control", "aplikacja")
    assert len(w) == 1
    assert "plik materialy/zrzuty-lukasza/zrzut_2026-10-27_04-06-00.png w pamięci projektu; także zrzut_2026-10-27_04-44-01.png; " in w[0]["zrodlo"]


def test_dane_konta_nie_sa_napisami_interfejsu():
    """Nazwa komputera, tytuł sesji i folder to pola scenariusza; w yaml ich nie ma."""
    for dana in ("MacBook-Air-ukasz", "Remote control Claude telefonie", "CV Match AI role offers", "cv-match", "Wskazówka platformy w config.yaml"):
        assert not any(w.get("napis") == dana for w in WPISY), dana


def test_opisy_dla_czytnika_ekranu_sa_po_polsku_i_nie_powtarzaja_napisow_aplikacji():
    opisy: list[str] = []
    js = (KORZEN / "strona" / "aplikacja-telefon-dane.js").read_text(encoding="utf-8") + (KORZEN / "strona" / "aplikacja-ustawienia-cc.js").read_text(encoding="utf-8")
    for blok in re.findall(r"PK\.OPISY_(?:TELEFONU|USTAWIEN_CC) = \{(.*?)\n\};", js, re.S):
        opisy += re.findall(r':\s*"([^"]+)"', blok)
    assert len(opisy) == 10
    napisy = [*napisy_telefonu(), *napisy_settings(), "Code", "Settings", "Remote Control", "Claude Code"]
    for o in opisy:
        assert not any(n in o for n in napisy), f"opis „{o}” powtarza napis aplikacji"


def test_dokumentacja_formatu_opisuje_telefon_i_ustawienia():
    assert "### Telefon i Remote Control (ćwiczenie z drogami)" in FORMAT
    czesc = FORMAT[FORMAT.index("### Telefon i Remote Control"):]
    for fragment in ("aplikacja.telefon", "urzadzenie", "telefon-sesja", "telefon-wstecz", "na_telefonie", "ustawienia-claude-code", "rc_nowe_sesje", "umowa symulatora", "IMG_1059", "zrzut_2026-10-27_04-44-01.png", "tests/dane/telefon.json", "KLIKI_TELEFONU", "aplikacja.remote_control"):
        assert fragment in czesc, fragment


def test_nowe_pliki_maja_opis_w_pierwszej_linii_i_do_300_linii():
    for plik in NOWE_PLIKI:
        linie = (KORZEN / plik).read_text(encoding="utf-8").splitlines()
        if not plik.endswith(".css"):  # limit 300 linii dotyczy plików z logiką (CLAUDE.md); arkusze stylów są dłuższe
            assert len(linie) <= 300, f"{plik}: {len(linie)} linii"
        assert linie[0].startswith(('"""', "/*")) and len(linie[0]) > 40, f"{plik}: pierwsza linia nie opisuje, do czego służy plik"


def test_fakty_nie_zostaly_zmienione_przez_telefon():
    """Zlecenie: fakty cytujemy, nie zmieniamy; wzór scenariusza cytuje tylko istniejące."""
    fakty = {w["id"] for w in __import__("yaml").safe_load((KORZEN / "dane" / "fakty.yaml").read_text(encoding="utf-8"))["fakty"]}
    wzor = (KORZEN / "tests" / "dane" / "telefon.json").read_text(encoding="utf-8")
    assert all(f in fakty for f in re.findall(r'"fakt": "([^"]+)"', wzor))
