"""Napisy paczki 4 część A silnika (strona/aplikacja-napisy-pola.js): każdy napis z `PK.NAPISY_POLA`, `PK.NAPISY_MODELI` i `PK.NAPISY_SRODOWISK` ma wpis `gdzie: aplikacja` w dane/napisy-interfejsu.yaml ze zrzutem w `zrodlo` (zrzut Łukasza z katalogu zrzuty-lukasza albo kadr zrzutu z lekcji 0.1, którego oryginału w katalogu nie ma), a nazwy w walidatorze zgadzają się z nazwami w kodzie strony."""

import re
from pathlib import Path

from narzedzia import scenariusz as sc
from narzedzia.scenariusz_model import MODELE, WYSILKI

KORZEN = Path(__file__).resolve().parent.parent
WPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")
NAPISY = sc._Napisy(WPISY)
JS = (KORZEN / "strona" / "aplikacja-napisy-pola.js").read_text(encoding="utf-8")
ZRZUT = re.compile(r"zrzut Łukasza 27\.10\.2026, plik materialy/zrzuty-lukasza/(zrzut_2026-10-2[67]_\d\d-\d\d-\d\d|IMG_\d+)\.(png|PNG)")
KADR = re.compile(r"kadr zrzutu Łukasza .*plik moduly/pierwsza-praca/pierwsze-zadanie/obrazy/[\w-]+\.png w drzewie modułu 0")


def napisy_js() -> list[str]:
    napisy = []
    for nazwa in ("NAPISY_POLA", "NAPISY_SRODOWISK"):
        blok = re.search(rf"PK\.{nazwa} = \{{(.*?)\n\}};", JS, re.S).group(1)
        napisy += re.findall(r':\s*"([^"]+)"', blok)
    napisy += re.findall(r'"([^"]+)"', re.search(r"PK\.NAPISY_MODELI = \[(.*?)\];", JS, re.S).group(1))
    return napisy


def test_napisy_pola_modeli_i_srodowisk_sa_na_liscie_z_zrzutem_w_zrodle():
    napisy = napisy_js()
    assert len(napisy) == 5 + 4 + 4  # pole (nowa, rozmowa i trzy części podpowiedzi pracy), środowisko, modele
    for n in napisy:
        assert NAPISY.jest(n, "aplikacja"), f"napis „{n}” nie ma wpisu gdzie: aplikacja"
        wpisy = [w for w in WPISY if w.get("gdzie") == "aplikacja" and w.get("napis") == n]
        assert wpisy, n
        assert any(ZRZUT.search(w.get("zrodlo", "")) or KADR.search(w.get("zrodlo", "")) for w in wpisy), f"napis „{n}” nie podaje zrzutu w zrodlo"


def test_napisy_ze_zrzutow_w_katalogu_maja_zrzut_w_ksztalcie_ze_zlecenia():
    """Napisy z plików w katalogu zrzuty-lukasza: dokładny kształt „zrzut Łukasza 27.10.2026, plik materialy/zrzuty-lukasza/<plik>.png w pamięci projektu”."""
    for n in ("Describe a task or ask a question", "Type / for commands", "Opus 5.5", "Fable 5.1", "Sonnet 5.5", "Haiku 5.5"):
        wpisy = [w for w in WPISY if w.get("gdzie") == "aplikacja" and w.get("napis") == n]
        assert len(wpisy) == 1, f"„{n}”: jeden wpis, nie {len(wpisy)}"
        assert re.search(r"^zrzut Łukasza 27\.10\.2026, plik materialy/zrzuty-lukasza/zrzut_2026-10-27_\d\d-\d\d-\d\d\.png w pamięci projektu", wpisy[0]["zrodlo"]), n


def test_nazwy_modeli_i_poziomow_w_walidatorze_zgadzaja_sie_z_kodem_strony():
    modele = re.findall(r'"([^"]+)"', re.search(r"PK\.NAPISY_MODELI = \[(.*?)\];", JS, re.S).group(1))
    assert tuple(modele) == MODELE
    ekran = (KORZEN / "strona" / "aplikacja-ekran.js").read_text(encoding="utf-8")
    blok = re.search(r"wysilek: \{(.*?)\n  \},", ekran, re.S).group(1)
    poziomy = [re.search(rf'{k}: "([^"]+)"', blok).group(1) for k in ("low", "medium", "high", "extra", "max")]
    assert tuple(poziomy) == WYSILKI


def test_poziom_i_model_nie_maja_drugiego_wpisu_w_yaml():
    """Napis już obecny dostaje zrzut dopisany do `zrodlo`, nie drugi wpis (zlecenie 4A)."""
    for n in ("Medium", "High", "Local", "Cloud", "This computer"):
        assert len([w for w in WPISY if w.get("gdzie") == "aplikacja" and w.get("napis") == n]) == 1, n
    medium = next(w for w in WPISY if w.get("gdzie") == "aplikacja" and w.get("napis") == "Medium")
    assert "zrzut_2026-10-27_03-58-01.png" in medium["zrodlo"] and "zrzut_2026-10-27_04-24-16.png" in medium["zrodlo"]
