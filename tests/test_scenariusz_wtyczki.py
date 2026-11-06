"""Testy walidatora przeglądarki wtyczek w drodze symulatora aplikacji: pozycja `Browse plugins` z podmenu `Plugins` menu `+`, kolejność kroków wokół otwartej przeglądarki, środowisko Cloud, pusta rozmowa i błąd składania podglądu (wzór: tests/dane/wtyczki-przegladarka.json)."""

import copy
import json
from pathlib import Path

import pytest

from narzedzia import scenariusz as sc
from narzedzia import scenariusz_wtyczki as wt
from narzedzia.strona_podglad import sprawdz_podglady

KORZEN = Path(__file__).resolve().parent.parent
WZOR = json.loads((Path(__file__).parent / "dane" / "wtyczki-przegladarka.json").read_text(encoding="utf-8"))
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")
PLUS, NAUCZ1, RODZIC, NAUCZ_R, POZYCJA, NAUCZ2 = range(6)  # indeksy kroków drogi `przegladarka` (RODZIC: klik pozycja Plugins, POZYCJA: klik pozycja Browse plugins)


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def jest(wynik, fragment):
    return any(fragment in b for b in wynik)


def kroki(d):
    return d["cwiczenia"][0]["drogi"][0]["kroki"]


def test_wzor_przechodzi(dane):
    assert bledy(dane) == []


def test_droga_konczaca_sie_otwarta_przegladarka_nie_potrzebuje_pliku_ani_artefaktu(dane):
    assert not jest(bledy(dane), "droga bez kroku plik")


def test_droga_bez_przegladarki_i_bez_pliku_nadal_to_blad(dane):
    del kroki(dane)[PLUS:]
    kroki(dane).append({"typ": "nauczyciel", "tekst": "Nic się nie dzieje."})
    assert jest(bledy(dane), "droga bez kroku plik ani artefakt")


def test_po_otwarciu_przegladarki_musi_stac_nauczyciel(dane):
    del kroki(dane)[NAUCZ2]
    assert jest(bledy(dane), "kończy się zaraz po otwarciu przeglądarki wtyczek")


def test_po_otwarciu_przegladarki_nauczyciel_dozwolony_nawet_kilka_razy(dane):
    kroki(dane).append({"typ": "nauczyciel", "tekst": "Jeszcze jedno zdanie."})
    assert bledy(dane) == []


@pytest.mark.parametrize(
    "krok",
    [
        {"typ": "pisz", "tekst": "Cześć"},
        {"typ": "mysli"},
        {"typ": "claude", "tekst": "Dobrze."},
        {"typ": "klik", "cel": "plus"},
        {"typ": "klik", "cel": "pozycja", "na": "Plugins"},
        {"typ": "klik", "cel": "pozycja", "na": "Browse plugins"},
        {"typ": "klik", "cel": "pozycja", "na": "Connectors"},
        {"typ": "klik", "cel": "pozycja", "na": "Browse connectors"},
        {"typ": "katalog_zamknij"},
    ],
)
def test_inne_kroki_przy_otwartej_przegladarce_to_blad(dane, krok):
    kroki(dane).append(krok)
    assert jest(bledy(dane), "przy otwartej przeglądarce wtyczek")


def test_browse_plugins_w_cloud_to_blad(dane):
    dane["cwiczenia"][0]["aplikacja"]["srodowisko"] = "Cloud"
    wynik = bledy(dane)
    assert jest(wynik, f"kroki[{POZYCJA}]: „Browse plugins” w środowisku Cloud")
    assert jest(wynik, f"kroki[{RODZIC}]: pozycja „Plugins” w środowisku Cloud jest wyszarzona")  # w chmurze samo podmenu Plugins też jest wyszarzone (zrzut 04-22-37)


@pytest.mark.parametrize("srodowisko", ["Local", "SSH"])
def test_browse_plugins_w_local_i_ssh_jest_dozwolone(dane, srodowisko):
    dane["cwiczenia"][0]["aplikacja"]["srodowisko"] = srodowisko
    assert bledy(dane) == []


def test_browse_plugins_w_pustej_rozmowie_to_blad(dane):
    dane["cwiczenia"][0]["aplikacja"]["rozmowa"] = []
    assert jest(bledy(dane), f"kroki[{POZYCJA}]: „Browse plugins” w pustej rozmowie")


@pytest.mark.parametrize("tryb", ["Manual", "Accept edits", "Plan", "Auto"])
def test_tryb_dowolny(dane, tryb):
    dane["cwiczenia"][0]["aplikacja"]["tryb"] = tryb
    assert bledy(dane) == []


def test_plugins_bez_otwartego_menu_to_blad(dane):
    del kroki(dane)[PLUS:NAUCZ1 + 1]
    assert jest(bledy(dane), "klik pozycja tylko po kroku plus")


def test_napisy_plugins_i_browse_plugins_ze_zrodla_w_yaml():
    assert wt.POZYCJA_WTYCZEK == "Browse plugins"
    for napis in ("Plugins", wt.POZYCJA_WTYCZEK):
        assert any(w.get("napis") == napis and w.get("gdzie") == "aplikacja" for w in NAPISY), napis


def test_podglad_drogi_z_przegladarka_to_blad_budowania(dane):
    with pytest.raises(ValueError, match="nie ma kroku plik"):
        sprawdz_podglady('<div class="podglad" data-cw="cw1" data-t="przegladarka"></div>', dane)


def test_fakty_wzoru_i_walidatora_istnieja():
    uzyte = {k["fakt"] for k in kroki(copy.deepcopy(WZOR)) if "fakt" in k}
    assert uzyte <= FAKTY_ID
    assert {"aplikacja-add-plugins-otwiera-przegladarke-wtyczek", "aplikacja-przegladarka-wtyczek-z-twoich-katalogow", "aplikacja-wtyczki-nie-w-chmurze-i-wsl"} <= FAKTY_ID


def test_walidator_nie_zmienia_katalogu_konektorow(dane):
    """Droga z `Connectors` → `Browse connectors` przechodzi tak samo jak przed dodaniem przeglądarki (wzór katalogu konektorów)."""
    wzor = json.loads((Path(__file__).parent / "dane" / "konektor-katalog.json").read_text(encoding="utf-8"))
    assert bledy(wzor) == []
