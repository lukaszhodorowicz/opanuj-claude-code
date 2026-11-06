"""Testy walidatora katalogu konektorów w drodze symulatora aplikacji: pozycja `Browse connectors` z podmenu `Connectors` menu `+`, krok `klik` z celem `konektor`, krok `katalog_zamknij` i kolejność wokół otwartego katalogu (wzór: tests/dane/konektor-katalog.json)."""

import copy
import json
from pathlib import Path

import pytest

from narzedzia import scenariusz as sc
from narzedzia import scenariusz_katalog as kat
from narzedzia.strona_podglad import sprawdz_podglady

KORZEN = Path(__file__).resolve().parent.parent
WZOR = json.loads((Path(__file__).parent / "dane" / "konektor-katalog.json").read_text(encoding="utf-8"))
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")
PLUS, NAUCZ1, RODZIC, NAUCZ_R, POZYCJA, NAUCZ2, KONEKTOR, NAUCZ3, ZAMKNIJ, NAUCZ4, PISZ, MYSLI, CLAUDE, NAUCZ5 = range(14)  # indeksy kroków drogi `podlacz` (RODZIC: klik pozycja Connectors, POZYCJA: klik pozycja Browse connectors)


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


def test_konektor_bez_otwartego_katalogu_to_blad(dane):
    k = kroki(dane)
    del k[POZYCJA]
    assert jest(bledy(dane), "klik konektor bez otwartego katalogu")


def test_konektor_przy_karcie_logowania_to_blad(dane):
    k = kroki(dane)
    k.insert(NAUCZ3 + 1, {"typ": "klik", "cel": "konektor", "nazwa": "Google Calendar"})
    assert jest(bledy(dane), "klik konektor bez otwartego katalogu")


@pytest.mark.parametrize("nazwa", ["Zapier", "Add connectors", None])  # Zapier nie jest kafelkiem katalogu (Slack już jest)
def test_nazwa_spoza_kafelkow_to_blad(dane, nazwa):
    k = kroki(dane)[KONEKTOR]
    if nazwa is None:
        del k["nazwa"]
    else:
        k["nazwa"] = nazwa
    assert jest(bledy(dane), "spoza kafelków katalogu")


def test_nazwa_przy_innym_celu_to_blad(dane):
    kroki(dane)[PLUS]["nazwa"] = "Google Calendar"
    assert jest(bledy(dane), "pole nazwa tylko w kroku klik z celem konektor")


def test_nieznane_pole_w_kroku_konektor_to_blad(dane):
    kroki(dane)[KONEKTOR]["na"] = "Gmail"
    assert jest(bledy(dane), "pole na nie należy do kroku konektor")


def test_po_konektorze_musi_stac_nauczyciel(dane):
    k = kroki(dane)
    del k[NAUCZ3]
    assert jest(bledy(dane), "najpierw nauczyciel")


def test_po_otwarciu_katalogu_musi_stac_nauczyciel(dane):
    k = kroki(dane)
    del k[NAUCZ2]
    assert jest(bledy(dane), "najpierw nauczyciel")


def test_katalog_zamknij_bez_karty_logowania_to_blad(dane):
    k = kroki(dane)
    del k[KONEKTOR:ZAMKNIJ]
    assert jest(bledy(dane), "katalog_zamknij bez karty logowania")


def test_katalog_zamknij_bez_katalogu_to_blad(dane):
    k = kroki(dane)
    k.insert(PLUS, {"typ": "katalog_zamknij"})
    assert jest(bledy(dane), "katalog_zamknij bez karty logowania")


@pytest.mark.parametrize("ms", [0, 10001, 1.5, "1600", True])
def test_ms_katalog_zamknij_poza_zakresem_to_blad(dane, ms):
    kroki(dane)[ZAMKNIJ]["ms"] = ms
    assert jest(bledy(dane), "ms musi być liczbą całkowitą od 1 do 10000")


def test_katalog_zamknij_bez_ms_jest_dozwolony(dane):
    del kroki(dane)[ZAMKNIJ]["ms"]
    assert bledy(dane) == []


def test_pisz_przy_otwartym_katalogu_to_blad(dane):
    k = kroki(dane)
    k.insert(NAUCZ2 + 1, k.pop(PISZ))
    assert jest(bledy(dane), "krok pisz przy otwartym katalogu (kafelki)")


@pytest.mark.parametrize("krok", [{"typ": "mysli"}, {"typ": "claude", "tekst": "Dobrze."}, {"typ": "plik", "nazwa": "x.txt", "linijki": ["a"]}])
def test_inne_kroki_przy_karcie_logowania_to_blad(dane, krok):
    k = kroki(dane)
    k.insert(NAUCZ3 + 1, krok)
    assert jest(bledy(dane), "przy otwartym katalogu (karta logowania)")


def test_nauczyciel_przy_otwartym_katalogu_jest_dozwolony(dane):
    k = kroki(dane)
    k.insert(NAUCZ2 + 1, {"typ": "nauczyciel", "tekst": "Jeszcze jedno zdanie."})
    assert bledy(dane) == []


def test_plus_przy_otwartym_katalogu_to_blad(dane):
    k = kroki(dane)
    k.insert(NAUCZ2 + 1, {"typ": "klik", "cel": "plus"})
    assert jest(bledy(dane), "klik plus przy otwartym katalogu")


def test_pozycja_przy_otwartym_katalogu_to_blad(dane):
    k = kroki(dane)
    k.insert(NAUCZ2 + 1, {"typ": "klik", "cel": "pozycja", "na": "Plugins"})
    assert jest(bledy(dane), "klik pozycja przy otwartym katalogu")


def test_droga_konczy_sie_otwartym_katalogiem(dane):
    k = kroki(dane)
    del k[KONEKTOR:]
    assert jest(bledy(dane), "droga kończy się otwartym katalogiem (kafelki)")


def test_droga_konczy_sie_karta_logowania(dane):
    k = kroki(dane)
    del k[ZAMKNIJ:]
    assert jest(bledy(dane), "droga kończy się otwartym katalogiem (karta logowania)")


def test_browse_connectors_w_cloud_to_blad(dane):
    dane["cwiczenia"][0]["aplikacja"]["srodowisko"] = "Cloud"
    wynik = bledy(dane)
    assert jest(wynik, f"kroki[{POZYCJA}]: „Browse connectors” w środowisku Cloud")
    assert not any(b.startswith(f"cw1/drogi[0]/kroki[{RODZIC}]:") for b in wynik)  # samo podmenu Connectors w chmurze jest dozwolone (zrzut 04-22-37)


@pytest.mark.parametrize("srodowisko", ["Local", "SSH"])
def test_browse_connectors_w_local_i_ssh_jest_dozwolone(dane, srodowisko):
    dane["cwiczenia"][0]["aplikacja"]["srodowisko"] = srodowisko
    assert bledy(dane) == []


@pytest.mark.parametrize("tryb", ["Manual", "Accept edits", "Plan", "Auto"])
def test_tryb_dowolny(dane, tryb):
    dane["cwiczenia"][0]["aplikacja"]["tryb"] = tryb
    assert bledy(dane) == []


def test_pusta_rozmowa_wymaga_klik_plus_na_poczatku_kazdej_drogi(dane):
    k = kroki(dane)
    k.insert(0, {"typ": "nauczyciel", "tekst": "Zaczynamy."})
    assert jest(bledy(dane), "niepustej listy rozmowa")


def test_pusta_rozmowa_z_druga_droga_bez_plusa_na_poczatku_to_blad(dane):
    druga = copy.deepcopy(dane["cwiczenia"][0]["drogi"][0])
    druga["id"] = "druga"
    del druga["kroki"][0]
    dane["cwiczenia"][0]["drogi"].append(druga)
    assert jest(bledy(dane), "niepustej listy rozmowa")


def test_niepusta_rozmowa_tez_dziala(dane):
    dane["cwiczenia"][0]["aplikacja"]["rozmowa"] = [{"kto": "ty", "tekst": "Cześć."}, {"kto": "claude", "tekst": "Dzień dobry."}]
    assert bledy(dane) == []


def test_add_folder_w_nowej_sesji_to_blad(dane):
    kroki(dane)[POZYCJA]["na"] = "Add folder"
    assert jest(bledy(dane), "kurs nie prowadzi przez tę pozycję przed pierwszą wiadomością")


def test_add_folder_w_trakcie_sesji_nie_jest_bledem_menu(dane):
    dane["cwiczenia"][0]["aplikacja"]["rozmowa"] = [{"kto": "ty", "tekst": "Cześć."}]
    kroki(dane)[POZYCJA]["na"] = "Add folder"
    assert not jest(bledy(dane), "kurs nie prowadzi przez tę pozycję przed pierwszą wiadomością")


def test_droga_z_katalogiem_nie_potrzebuje_kroku_plik(dane):
    assert not jest(bledy(dane), "droga bez kroku plik ani artefakt")


def test_droga_bez_katalogu_i_bez_pliku_nadal_to_blad(dane):
    k = kroki(dane)
    del k[PLUS:ZAMKNIJ + 1]
    assert jest(bledy(dane), "droga bez kroku plik ani artefakt")


def test_podglad_drogi_z_katalogiem_to_blad_budowania(dane):
    with pytest.raises(ValueError, match="nie ma kroku plik ani artefakt"):
        sprawdz_podglady('<div class="podglad" data-cw="cw1" data-t="podlacz"></div>', dane)


def test_napisy_kafelkow_i_pozycji_ze_zrodla_w_yaml():
    for napis in (*kat.KAFELKI, kat.POZYCJA_KATALOGU, kat.POZYCJA_W_SESJI):
        assert any(w.get("napis") == napis and w.get("gdzie") == "aplikacja" for w in NAPISY), napis


def test_fakty_wzoru_istnieja():
    uzyte = {k["fakt"] for k in kroki(copy.deepcopy(WZOR)) if "fakt" in k}
    assert uzyte <= FAKTY_ID
    assert {"aplikacja-add-connectors-otwiera-katalog", "konektory-google-calendar-gmail-microsoft-365", "konektor-logowanie-w-claude-ai"} <= uzyte
