"""Testy walidatora komendy `/config` w drodze symulatora aplikacji (wzór: tests/dane/ustawienia-konta.json, ćwiczenie cw1 z kliknięciem konta zamienionym na komendę): komenda otwiera okno Settings na stronie Claude Code jak klik `ustawienia-claude-code`, więc po niej dalej tylko nauczyciel, droga nie kończy się zaraz po niej, a pola `aplikacja.rc_nowe_sesje` i `aplikacja.konto_ustawien` przyjmuje ćwiczenie z samą komendą (dane/FORMAT-SCENARIUSZA.md, „Komenda `/config` jako wejście do Settings”)."""

import copy
import json

import pytest

from tests.pomoc_sesje import DANE, bledy, jest

WZOR = json.loads((DANE / "ustawienia-konta.json").read_text(encoding="utf-8"))
FAKT = "aplikacja-config-otwiera-settings-claude-code"
KOMENDA = {"typ": "komenda", "tekst": "/config", "fakt": FAKT}


def z_komenda():
    """Wzór z ustawieniami, w którym droga cw1 otwiera Settings komendą `/config` zamiast kliknięciem konta."""
    d = copy.deepcopy(WZOR)
    d["cwiczenia"][0]["drogi"][0]["kroki"][0] = dict(KOMENDA)
    return d


def kroki(d):
    return d["cwiczenia"][0]["drogi"][0]["kroki"]


def apl(d):
    return d["cwiczenia"][0]["aplikacja"]


def test_wzor_z_klikiem_konta_dalej_jest_poprawny():
    assert bledy(WZOR) == []


def test_komenda_config_z_nauczycielem_po_niej_przechodzi():
    assert bledy(z_komenda()) == []


def test_komenda_config_nie_wymaga_pliku_w_drodze():
    d = z_komenda()
    assert all(k["typ"] in ("komenda", "nauczyciel") for k in kroki(d)), "droga bez kroku plik, artefakt i strona kończy się otwartym oknem Settings"
    assert bledy(d) == []


def test_droga_nie_konczy_sie_zaraz_po_komendzie_config():
    d = z_komenda()
    kroki(d).pop()
    assert jest(bledy(d), "droga kończy się zaraz po otwarciu okna Settings")


@pytest.mark.parametrize("krok", [{"typ": "pisz", "tekst": "Sprawdź plik."}, {"typ": "komenda", "tekst": "/compact"}, {"typ": "mysli", "ms": 500}])
def test_po_komendzie_config_dalej_tylko_nauczyciel(krok):
    d = z_komenda()
    kroki(d).insert(1, krok)
    assert jest(bledy(d), "przy otwartym oknie Settings: dalej tylko nauczyciel")


def test_druga_komenda_config_przy_otwartym_oknie_to_blad():
    d = z_komenda()
    kroki(d).insert(1, dict(KOMENDA))
    assert jest(bledy(d), "przy otwartym oknie Settings: dalej tylko nauczyciel")


def test_komenda_config_z_nieistniejacym_faktem_to_blad():
    d = z_komenda()
    kroki(d)[0]["fakt"] = "fakt-ktorego-nie-ma"
    assert jest(bledy(d), "fakt „fakt-ktorego-nie-ma” nie istnieje")


def test_komenda_config_z_dalszym_tekstem_to_blad():
    d = z_komenda()
    kroki(d)[0]["tekst"] = "/config theme"
    assert jest(bledy(d), "komenda „/config theme”")


def test_inne_polecenie_spoza_listy_ma_komunikat_z_trzema_poleceniami():
    d = z_komenda()
    kroki(d)[0]["tekst"] = "/context"
    # /context jest na liście napisów interfejsu, ale symulator go nie gra
    wynik = bledy(d)
    assert jest(wynik, "symulator gra tylko /compact i /btw oraz /config")


@pytest.mark.parametrize("pole, wartosc", [("rc_nowe_sesje", False), ("konto_ustawien", "B")])
def test_pola_okna_settings_przyjmuje_cwiczenie_z_sama_komenda(pole, wartosc):
    d = z_komenda()
    apl(d)[pole] = wartosc
    assert bledy(d) == []


@pytest.mark.parametrize("pole, wartosc, fragment", [("rc_nowe_sesje", False, "rc_nowe_sesje bez kroku klik „ustawienia-claude-code” albo komendy /config"), ("konto_ustawien", "B", "bez kroku, który otwiera okno Settings")])
def test_pola_okna_settings_bez_kroku_otwierajacego_okno_to_blad(pole, wartosc, fragment):
    d = copy.deepcopy(WZOR)
    d["cwiczenia"][0]["drogi"][0]["kroki"] = [{"typ": "komenda", "tekst": "/compact"}, {"typ": "nauczyciel", "tekst": "Zobacz okno."}]
    apl(d)[pole] = wartosc
    assert jest(bledy(d), fragment)


def test_czytelnosc_wymaga_nauczyciela_po_komendzie_config_jak_po_kliku_w_konto():
    from narzedzia import czytelnosc

    bez = czytelnosc._sprawdz_liste_krokow([dict(KOMENDA), {"typ": "mysli", "ms": 300}, {"typ": "mysli", "ms": 300}], "", "x", czytelnosc.ZMIANY_APLIKACJI)
    assert any("brak nauczyciela" in u for u in bez)
    z = czytelnosc._sprawdz_liste_krokow([dict(KOMENDA), {"typ": "nauczyciel", "tekst": "To ustawienia."}], "", "x", czytelnosc.ZMIANY_APLIKACJI)
    assert z == []
    inna = czytelnosc._sprawdz_liste_krokow([{"typ": "komenda", "tekst": "/compact"}, {"typ": "mysli", "ms": 300}, {"typ": "mysli", "ms": 300}], "", "x", czytelnosc.ZMIANY_APLIKACJI)
    assert inna == [], "/compact niczego w oknie nie zmienia"
