"""Testy części B silnika (prawdziwe napisy ze zrzutów Łukasza z 27.10.2026): napisy `PK.NAPISY_EKRANU` mają wpisy w `dane/napisy-interfejsu.yaml` ze zrzutem w `zrodlo`, składane napisy pasują do wzorów, pola `remote_control` i `bypass_dostepny` walidator przyjmuje tylko jako prawdę albo fałsz, kolejność trybów zgadza się ze zrzutem, a dokumentacja formatu opisuje nowe pola."""

import copy
import json
import re
from pathlib import Path

import pytest

from narzedzia import scenariusz as sc
from narzedzia.scenariusz_aplikacja import TRYBY_APLIKACJI

KORZEN = Path(__file__).resolve().parent.parent
SCIEZKA_NAPISOW = KORZEN / "dane" / "napisy-interfejsu.yaml"
WPISY = sc.wczytaj_napisy(SCIEZKA_NAPISOW)
NAPISY = sc._Napisy(WPISY)
FAKTY_ID = {w["id"] for w in __import__("yaml").safe_load((KORZEN / "dane" / "fakty.yaml").read_text(encoding="utf-8"))["fakty"]}
WZOR = json.loads((Path(__file__).parent / "dane" / "aplikacja.json").read_text(encoding="utf-8"))
ZRZUT = re.compile(r"zrzut Łukasza 27\.10\.2026, plik materialy/zrzuty-lukasza/zrzut_2026-10-27_\d\d-\d\d-\d\d\.png w pamięci projektu")


def napisy_ekranu() -> list[str]:
    js = (KORZEN / "strona" / "aplikacja-ekran.js").read_text(encoding="utf-8")
    blok = re.search(r"PK\.NAPISY_EKRANU = \{(.*?)\n\};", js, re.S).group(1)
    return re.findall(r':\s*"([^"]+)"', blok)


def test_napisy_ekranu_sa_na_liscie_napisow_interfejsu_aplikacji():
    napisy = napisy_ekranu()
    assert len(napisy) > 50
    for n in napisy:
        assert NAPISY.jest(n, "aplikacja"), f"napis „{n}” z PK.NAPISY_EKRANU nie ma wpisu gdzie: aplikacja"


def test_napisy_ekranu_maja_zrzut_lukasza_w_zrodle():
    for n in napisy_ekranu():
        wpisy = [w for w in WPISY if w.get("gdzie") == "aplikacja" and w.get("napis") == n]
        assert wpisy, n
        assert any(ZRZUT.search(w.get("zrodlo", "")) for w in wpisy), f"napis „{n}” nie podaje zrzutu Łukasza w zrodlo"


@pytest.mark.parametrize(
    "napis",
    ["9% used", "100% used", "90k / 1M", "0k / 1M", "17.8k", "3k", "937k", "1.8%", "93.7%", "0.3%", "2", "3", "4"],
)
def test_napisy_skladane_z_liczba_pasuja_do_wzorow(napis):
    assert NAPISY.jest(napis, "aplikacja")


@pytest.mark.parametrize("liczba", ["0", "1", "5", "6", "9", "10", "42", "99", "100"])
def test_zwykla_liczba_nie_jest_napisem_interfejsu(liczba):
    """Cyfry skrótu z menu modelu to trzy osobne wpisy (2, 3, 4); wzór na dowolną liczbę 1-99 uczyniłby napisem interfejsu np. `notka` z liczbą, a licznik prac przy Background tasks to dana, nie napis."""
    assert not NAPISY.jest(liczba, "aplikacja")


@pytest.mark.parametrize("napis", ["% used", "abc% used", "0", "100", "9%%", "k / 1M"])
def test_wzory_nie_przepuszczaja_smieci(napis):
    assert not NAPISY.jest(napis, "aplikacja")


def test_kolejnosc_trybow_jak_na_zrzucie_i_w_js():
    assert TRYBY_APLIKACJI == ("Auto", "Manual", "Accept edits", "Plan")
    js = (KORZEN / "strona" / "aplikacja-tryby.js").read_text(encoding="utf-8")
    assert tuple(json.loads(re.search(r"PK\.TRYBY_APLIKACJI = (\[.*?\]);", js).group(1))) == TRYBY_APLIKACJI


def test_kazdy_tryb_i_bypass_maja_podpis_ze_zrzutu():
    js = (KORZEN / "strona" / "aplikacja-ekran.js").read_text(encoding="utf-8")
    blok = re.search(r"tryby: \{(.*?)\n  \},", js, re.S).group(1)
    klucze = re.findall(r'^\s*"?([\w ]+)"?:\s*"', blok, re.M)
    assert klucze == ["naglowek", "Auto", "Manual", "Accept edits", "Plan", "Bypass permissions"]
    for t in (*TRYBY_APLIKACJI, "Bypass permissions"):
        assert NAPISY.jest(t, "aplikacja"), t


def test_nazwa_pozycji_nie_trafia_do_aplikacja_sesje_js():
    """Istniejący test zabrania „Search” i „New session” w aplikacja-sesje.js: napisy ekranu stoją w osobnym pliku."""
    sesje = re.sub(r"/\*.*?\*/", "", (KORZEN / "strona" / "aplikacja-sesje.js").read_text(encoding="utf-8"), flags=re.S)
    ekran = (KORZEN / "strona" / "aplikacja-ekran.js").read_text(encoding="utf-8")
    assert "Search" not in sesje and "Search" in ekran


# walidator pól remote_control i bypass_dostepny


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


def test_wzor_bez_bledow(dane):
    assert bledy(dane) == []


ETAPY = json.loads((Path(__file__).parent / "dane" / "okno-zgody-tryby.json").read_text(encoding="utf-8"))
DROGI = json.loads((Path(__file__).parent / "dane" / "aplikacja-drogi.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("wartosc", [True, False])
def test_remote_control_prawda_albo_falsz_przechodzi(dane, wartosc):
    dane["cwiczenia"][0]["aplikacja"]["remote_control"] = wartosc
    assert bledy(dane) == []


@pytest.mark.parametrize("wartosc", [True, False])
def test_bypass_dostepny_prawda_albo_falsz_przechodzi_w_cwiczeniu_z_etapami(wartosc):
    scen = copy.deepcopy(ETAPY)
    scen["cwiczenia"][0]["aplikacja"]["bypass_dostepny"] = wartosc
    assert bledy(scen) == []


@pytest.mark.parametrize("wartosc", ["tak", "true", 1, 0, None, [], "wlaczony"])
def test_remote_control_inny_niz_bool_to_blad(dane, wartosc):
    dane["cwiczenia"][0]["aplikacja"]["remote_control"] = wartosc
    assert any("pole remote_control musi być prawdą albo fałszem" in b for b in bledy(dane)), wartosc


@pytest.mark.parametrize("wartosc", ["tak", "true", 1, 0, None, [], "wlaczony"])
def test_bypass_dostepny_inny_niz_bool_to_blad_takze_w_etapach(wartosc):
    scen = copy.deepcopy(ETAPY)
    scen["cwiczenia"][0]["aplikacja"]["bypass_dostepny"] = wartosc
    assert any("pole bypass_dostepny musi być prawdą albo fałszem" in b for b in bledy(scen)), wartosc


@pytest.mark.parametrize("wartosc", [True, False])
def test_bypass_dostepny_w_cwiczeniu_z_krokami_to_blad_z_czytelnym_komunikatem(dane, wartosc):
    dane["cwiczenia"][0]["aplikacja"]["bypass_dostepny"] = wartosc
    assert any("pole bypass_dostepny tylko w ćwiczeniu z etapami" in b for b in bledy(dane))


def test_bypass_dostepny_w_cwiczeniu_z_drogami_to_blad():
    scen = copy.deepcopy(DROGI)
    scen["cwiczenia"][0]["aplikacja"]["bypass_dostepny"] = True
    assert any("pole bypass_dostepny tylko w ćwiczeniu z etapami" in b for b in bledy(scen))


def ma_liste_trybow(cw: dict) -> bool:
    """Ćwiczenie, w którym powstaje lista trybów: z `etapy` albo z drogami, z których któraś ma krok `{"typ": "klik", "cel": "tryb-menu"}` (paczka 4A, dane/FORMAT-SCENARIUSZA.md). Tylko tam `aplikacja.bypass_dostepny` ma sens."""
    if "etapy" in cw:
        return True
    drogi = cw.get("drogi") if isinstance(cw.get("drogi"), list) else []
    return any(
        isinstance(k, dict) and k.get("typ") == "klik" and k.get("cel") == "tryb-menu"
        for d in drogi
        if isinstance(d, dict)
        for k in (d.get("kroki") if isinstance(d.get("kroki"), list) else [])
    )


def test_regula_listy_trybow_lapie_drogi_bez_tryb_menu_i_przepuszcza_drogi_z_tryb_menu():
    """Pilnuje samej reguły z testu niżej, żeby nie przepuszczała wszystkiego: drogi bez kroku `tryb-menu` (aplikacja-drogi.json) nie mają listy trybów, cw1 z aplikacja-4a.json i ćwiczenie z etapami mają."""
    wzor_4a = json.loads((Path(__file__).parent / "dane" / "aplikacja-4a.json").read_text(encoding="utf-8"))
    cw1 = next(cw for cw in wzor_4a["cwiczenia"] if cw["id"] == "cw1")
    assert ma_liste_trybow(cw1)
    assert ma_liste_trybow(ETAPY["cwiczenia"][0])
    assert not ma_liste_trybow(DROGI["cwiczenia"][0])
    assert not ma_liste_trybow(WZOR["cwiczenia"][0])
    zly = copy.deepcopy(cw1)
    for d in zly["drogi"]:
        d["kroki"] = [k for k in d["kroki"] if not (k.get("typ") == "klik" and k.get("cel") in ("tryb-menu", "tryb"))]
    assert not ma_liste_trybow(zly)


def test_zaden_scenariusz_w_repozytorium_nie_uzywa_bypass_dostepny_poza_etapami_i_drogami_z_tryb_menu():
    """Reguła z walidatora nie zrywa żadnej lekcji: pole pojawia się tylko w ćwiczeniach z `etapy` albo z drogami, w których jest krok `klik` `tryb-menu` (albo wcale)."""
    for plik in [*(KORZEN / "moduly").glob("*/scenariusz.json"), *(KORZEN / "tests" / "dane").glob("*.json")]:
        scen = json.loads(plik.read_text(encoding="utf-8"))
        for cw in scen.get("cwiczenia", []) if isinstance(scen, dict) else []:
            apl = cw.get("aplikacja") if isinstance(cw, dict) else None
            if isinstance(apl, dict) and "bypass_dostepny" in apl:
                assert ma_liste_trybow(cw), f"{plik}: {cw.get('id')} ma bypass_dostepny bez etapów i bez kroku klik „tryb-menu”"


def test_dokumentacja_formatu_opisuje_nowe_pola():
    format_ = (KORZEN / "dane" / "FORMAT-SCENARIUSZA.md").read_text(encoding="utf-8")
    tryby = (KORZEN / "dane" / "FORMAT-SCENARIUSZA-TRYBY.md").read_text(encoding="utf-8")
    for pole in ("remote_control", "bypass_dostepny"):
        assert f"`{pole}`" in format_
    assert "`bypass_dostepny`" in tryby
    assert "### Napisy ze zrzutów Łukasza" in format_
