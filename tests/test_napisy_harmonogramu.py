"""Testy napisów zadania według harmonogramu: każdy napis z `PK.NAPISY_HARMONOGRAMU` (strona/aplikacja-harmonogram-widok.js) ma wpis `gdzie: aplikacja` w `dane/napisy-interfejsu.yaml`, nowe napisy podają zrzut Łukasza 05-04-44 do 05-06-07 w `zrodlo`, napisy składane z pól harmonogramu pasują do wzorów (i tylko do nich), a częstotliwości z walidatora mają wpis."""

import re
from pathlib import Path

import pytest

from narzedzia import scenariusz as sc
from narzedzia import scenariusz_harmonogram as harm

KORZEN = Path(__file__).resolve().parent.parent
WPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")
NAPISY = sc._Napisy(WPISY)
ZRZUT = re.compile(r"zrzut Łukasza 27\.10\.2026, plik materialy/zrzuty-lukasza/zrzut_2026-10-27_05-0[4-6]-\d\d\.png w pamięci projektu")
STARE = {"Auto", "General", "Connectors", "Add connectors", "Slack"}  # napisy, które aplikacja pokazuje też gdzie indziej i które miały wpis przed tą częścią


def napisy_harmonogramu() -> list[str]:
    js = (KORZEN / "strona" / "aplikacja-harmonogram-widok.js").read_text(encoding="utf-8")
    blok = re.search(r"PK\.NAPISY_HARMONOGRAMU = \{(.*?)\n\};", js, re.S).group(1)
    return re.findall(r':\s*"([^"]+)"', blok)


def test_napisy_harmonogramu_sa_na_liscie_napisow_interfejsu_aplikacji():
    napisy = napisy_harmonogramu()
    assert len(napisy) > 40
    for n in napisy:
        assert NAPISY.jest(n, "aplikacja"), f"napis „{n}” z PK.NAPISY_HARMONOGRAMU nie ma wpisu gdzie: aplikacja"


def test_nowe_napisy_harmonogramu_maja_zrzut_lukasza_w_zrodle():
    for n in set(napisy_harmonogramu()) - STARE:
        wpisy = [w for w in WPISY if w.get("gdzie") == "aplikacja" and w.get("napis") == n]
        assert wpisy, n
        assert any(ZRZUT.search(w.get("zrodlo", "")) for w in wpisy), f"napis „{n}” nie podaje zrzutu 05-04-44 do 05-06-07 w zrodlo"


def test_napisy_skladane_maja_wzory_ze_zrzutem():
    wzory = [w for w in WPISY if w.get("gdzie") == "aplikacja" and "wzor" in w and ("Next run" in w["wzor"] or "Daily at" in w["wzor"] or "created" in w["wzor"])]
    assert len(wzory) == 3 and all(ZRZUT.search(w["zrodlo"]) for w in wzory)


@pytest.mark.parametrize("napis", ["Next run: today at 9:20 AM", "Next run: today at 12:05 PM", "Daily at 9:20 AM", "Daily at 11:59 PM", "“Poranne nowości o AI” created.", "“x” created."])
def test_napisy_skladane_pasuja_do_wzorow(napis):
    assert NAPISY.jest(napis, "aplikacja")


@pytest.mark.parametrize("napis", ["Next run: tomorrow at 9:20 AM", "Next run: today at 09:20", "Next run: today at 9:20", "Daily at 9:20", "Weekly at 9:20 AM", "Poranne nowości o AI created.", "“” created."])
def test_wzory_nie_przepuszczaja_smieci(napis):
    assert not NAPISY.jest(napis, "aplikacja")


def test_czestotliwosci_z_walidatora_maja_wpis_na_liscie_napisow():
    assert harm.CZESTOTLIWOSCI == ("Daily",)
    assert all(NAPISY.jest(c, "aplikacja") for c in harm.CZESTOTLIWOSCI)


def test_dane_kursanta_z_wzoru_nie_sa_napisami_interfejsu():
    for dana in ("Poranne nowości o AI", "09:20", "Poranne-nowosci", "Zbierz najważniejsze wiadomości o sztucznej inteligencji"):
        assert not NAPISY.jest(dana, "aplikacja")


def test_zrzuty_harmonogramu_istnieja_w_zrodlach_napisow_dokladnie_w_podanym_ksztalcie():
    zrodla = [w["zrodlo"] for w in WPISY if w.get("gdzie") == "aplikacja" and ZRZUT.search(w.get("zrodlo", ""))]
    assert len(zrodla) >= 40
    assert all(re.search(r"w pamięci projektu(; także zrzut_2026-10-27_05-0[4-6]-\d\d\.png(, zrzut_2026-10-27_05-0[4-6]-\d\d\.png)*)? \(", z) for z in zrodla)
