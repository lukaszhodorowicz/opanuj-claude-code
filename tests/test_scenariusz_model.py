"""Testy walidatora wyboru modelu i wysiłku w ćwiczeniu z drogami symulatora aplikacji: kliki `wybor-modelu`, `effort`, `poziom` (pola `poziom` 1-5 i `notka`), kolejność, menu otwarte na końcu drogi, nauczyciel po kliku (czytelność) i napisy kursu w filtrze języka (wzór: tests/dane/aplikacja-model.json)."""

import copy
import json
from pathlib import Path

import pytest

from narzedzia import czytelnosc, scenariusz as sc, scenariusz_model as model
from narzedzia.tekst_pl import polskie_pola

KORZEN = Path(__file__).resolve().parent.parent
WZOR = json.loads((Path(__file__).parent / "dane" / "aplikacja-model.json").read_text(encoding="utf-8"))
WZOR_KROKI = json.loads((Path(__file__).parent / "dane" / "aplikacja.json").read_text(encoding="utf-8"))
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")

# Indeksy kroków w każdej drodze wzoru
WYBOR, NAUCZ_1, EFFORT, POZIOM, NAUCZ_2, PISZ = 0, 1, 2, 3, 4, 5


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def jest(wynik, fragment):
    return any(fragment in b for b in wynik)


def kroki(d, droga=0):
    return d["cwiczenia"][0]["drogi"][droga]["kroki"]


def test_wzor_przechodzi_trzy_drogi_z_poziomami_1_3_5(dane):
    assert bledy(dane) == []
    assert [k["poziom"] for d in dane["cwiczenia"][0]["drogi"] for k in d["kroki"] if k.get("cel") == "poziom"] == [1, 3, 5]


def test_cele_modelu_leza_w_dozwolonych_klikach_drogi():
    assert model.KLIKI == ("wybor-modelu", "effort", "poziom")


# kolejność klików

def test_effort_bez_wyboru_modelu(dane):
    del kroki(dane)[WYBOR]  # droga zaczyna się od kliku effort
    assert jest(bledy(dane), "klik „effort” tylko zaraz po kliku „wybor-modelu”")


def test_poziom_bez_effort(dane):
    del kroki(dane)[EFFORT]
    assert jest(bledy(dane), "klik „poziom” tylko zaraz po kliku „effort”")


def test_poziom_bez_otwarcia_menu(dane):
    k = kroki(dane)
    del k[WYBOR:POZIOM]  # zostaje sam poziom
    assert jest(bledy(dane), "klik „poziom” tylko zaraz po kliku „effort”")


def test_miedzy_klikami_dozwolony_nauczyciel(dane):
    kroki(dane).insert(EFFORT, {"typ": "nauczyciel", "tekst": "Jeszcze jedno zdanie."})
    assert bledy(dane) == []


@pytest.mark.parametrize("miedzy", [
    {"typ": "pisz", "tekst": "Wiadomość w trakcie menu."},
    {"typ": "mysli", "ms": 500},
    {"typ": "claude", "tekst": "Odpowiedź w trakcie menu."},
])
def test_miedzy_klikami_inne_kroki_to_blad(dane, miedzy):
    kroki(dane).insert(EFFORT, miedzy)
    assert jest(bledy(dane), "przy otwartym menu wyboru modelu: dalej tylko nauczyciel, klik „effort” i klik „poziom”")


def test_klik_sciezki_w_menu_to_blad(dane):
    kroki(dane).insert(EFFORT, {"typ": "klik", "cel": "sciezka"})
    assert jest(bledy(dane), "przy otwartym menu wyboru modelu")


def test_drugi_wybor_modelu_przy_otwartym_menu(dane):
    kroki(dane).insert(EFFORT, {"typ": "klik", "cel": "wybor-modelu"})
    assert jest(bledy(dane), "klik w wybór modelu przy otwartym menu")


def test_effort_dwa_razy_pod_rzad(dane):
    kroki(dane).insert(EFFORT + 1, {"typ": "klik", "cel": "effort"})
    assert jest(bledy(dane), "klik „effort” tylko zaraz po kliku „wybor-modelu”")


def test_dwa_pelne_wybory_w_jednej_drodze_sa_dozwolone(dane):
    k = kroki(dane)
    k[NAUCZ_2 + 1:NAUCZ_2 + 1] = copy.deepcopy(k[WYBOR:NAUCZ_2 + 1])
    assert bledy(dane) == []


# menu otwarte na końcu drogi

def test_droga_konczy_sie_po_wyborze_modelu_to_blad(dane):
    k = kroki(dane)
    del k[EFFORT:POZIOM + 1]  # wybor-modelu, nauczyciel, potem już bez effort i poziomu
    assert jest(bledy(dane), "droga kończy się przy otwartym menu wyboru modelu")


def test_menu_otwarte_na_koncu_drogi_gdy_ostatni_krok_to_effort(dane):
    d = dane["cwiczenia"][0]["drogi"][0]
    d["kroki"] = d["kroki"][:EFFORT + 1]  # kończy się na kliku effort
    assert jest(bledy(dane), "droga kończy się przy otwartym menu wyboru modelu")


def test_menu_otwarte_na_samym_koncu_drogi_po_wyborze_modelu(dane):
    d = dane["cwiczenia"][0]["drogi"][0]
    d["kroki"] = d["kroki"][:1]
    assert jest(bledy(dane), "droga kończy się przy otwartym menu wyboru modelu")


def test_zamkniete_menu_na_koncu_drogi_przechodzi(dane):
    assert not jest(bledy(dane), "kończy się przy otwartym menu")


# pole poziom

@pytest.mark.parametrize("zly", [0, 6, -1, 3.0, "3", True, None, 10])
def test_poziom_tylko_liczba_calkowita_1_do_5(dane, zly):
    kroki(dane)[POZIOM]["poziom"] = zly
    assert jest(bledy(dane), "poziom musi być liczbą całkowitą od 1 do 5")


def test_brak_pola_poziom(dane):
    del kroki(dane)[POZIOM]["poziom"]
    assert jest(bledy(dane), "poziom musi być liczbą całkowitą od 1 do 5")


@pytest.mark.parametrize("dobry", [1, 2, 3, 4, 5])
def test_kazdy_poziom_od_1_do_5_przechodzi(dane, dobry):
    kroki(dane)[POZIOM]["poziom"] = dobry
    assert bledy(dane) == []


# pole notka

def test_brak_notki(dane):
    del kroki(dane)[POZIOM]["notka"]
    assert jest(bledy(dane), "klik poziom wymaga niepustego pola notka")


@pytest.mark.parametrize("pusta", ["", "   ", None, 5, ["niski wysiłek"]])
def test_notka_niepusty_napis(dane, pusta):
    kroki(dane)[POZIOM]["notka"] = pusta
    assert jest(bledy(dane), "klik poziom wymaga niepustego pola notka")


def test_notka_do_30_znakow_granica(dane):
    kroki(dane)[POZIOM]["notka"] = "a" * 30
    assert bledy(dane) == []
    kroki(dane)[POZIOM]["notka"] = "a" * 31
    assert jest(bledy(dane), "notka ma 31 znaków, limit 30")


@pytest.mark.parametrize("napis", ["Effort", "+ New", "Accept edits", "Local"])
def test_notka_nie_moze_byc_napisem_interfejsu(dane, napis):
    kroki(dane)[POZIOM]["notka"] = napis
    assert jest(bledy(dane), f"notka „{napis}” to napis interfejsu")


# pola poziom i notka przy innym celu

@pytest.mark.parametrize("indeks", [WYBOR, EFFORT])
@pytest.mark.parametrize("pole,wartosc", [("poziom", 2), ("notka", "niski wysiłek")])
def test_poziom_i_notka_przy_innym_celu_modelu(dane, indeks, pole, wartosc):
    kroki(dane)[indeks][pole] = wartosc
    assert jest(bledy(dane), f"pole {pole} należy tylko do kroku klik z celem poziom")


def test_poziom_przy_kliku_w_sciezke(dane):
    k = kroki(dane)
    sciezka = next(x for x in k if x.get("cel") == "sciezka")
    sciezka["poziom"] = 1
    assert jest(bledy(dane), "pole poziom należy tylko do kroku klik z celem poziom")


@pytest.mark.parametrize("indeks", [NAUCZ_1, PISZ])
def test_notka_w_kroku_innego_typu(dane, indeks):
    kroki(dane)[indeks]["notka"] = "niski wysiłek"
    assert jest(bledy(dane), "pole notka należy tylko do kroku klik z celem poziom")


# cele tylko w ćwiczeniu z drogami

@pytest.mark.parametrize("cel", ["wybor-modelu", "effort", "poziom"])
def test_cele_modelu_nie_dzialaja_w_cwiczeniu_z_krokami(cel):
    d = copy.deepcopy(WZOR_KROKI)
    d["cwiczenia"][0]["kroki"][0]["klik"] = cel
    assert jest(sc.sprawdz_scenariusz(d, None, NAPISY), f"klik „{cel}” spoza licznik/changes")


def test_cel_modelu_w_etapach_nie_przechodzi():
    etapy = json.loads((Path(__file__).parent / "dane" / "okno-zgody-tryby.json").read_text(encoding="utf-8"))
    cw = etapy["cwiczenia"][0]
    cw["etapy"][0]["klik"] = "wybor-modelu"
    assert sc.sprawdz_scenariusz(etapy, None, NAPISY)


# czytelność: nauczyciel po kliku

def _czytelnosc(dane, tmp_path):
    plik = tmp_path / "scenariusz.json"
    plik.write_text(json.dumps(dane, ensure_ascii=False), encoding="utf-8")
    return czytelnosc.sprawdz_scenariusz(plik, "scenariusz.json")


def test_wzor_ma_nauczyciela_po_wyborze_modelu_i_po_poziomie(dane, tmp_path):
    assert _czytelnosc(dane, tmp_path) == []


def test_brak_nauczyciela_po_wyborze_modelu(dane, tmp_path):
    del kroki(dane)[NAUCZ_1]  # po wybor-modelu: effort, poziom, nauczyciel: nauczyciel dopiero na trzecim miejscu
    wynik = _czytelnosc(dane, tmp_path)
    assert any("krok 1 (klik)" in b and "brak nauczyciela w 2 kolejnych krokach" in b for b in wynik)


def test_nauczyciel_po_dwoch_krokach_od_wyboru_modelu_wystarcza(dane, tmp_path):
    k = kroki(dane)
    k.insert(EFFORT, k.pop(NAUCZ_1))  # wybor-modelu, effort, nauczyciel (pozycja i+2), poziom
    assert not any("krok 1 (klik)" in b for b in _czytelnosc(dane, tmp_path))


def test_brak_nauczyciela_po_poziomie(dane, tmp_path):
    del kroki(dane)[NAUCZ_2]  # po poziomie zaraz pisz i mysli, nauczyciela nie ma
    wynik = _czytelnosc(dane, tmp_path)
    assert any("krok 4 (klik)" in b and "brak nauczyciela w 2 kolejnych krokach" in b for b in wynik)


def test_nauczyciel_po_poziomie_na_drugim_miejscu_wystarcza(dane, tmp_path):
    k = kroki(dane)
    k.insert(POZIOM + 1, {"typ": "mysli", "ms": 300})
    assert not any("krok 4 (klik)" in b for b in _czytelnosc(dane, tmp_path))


def test_klik_effort_nie_wymaga_nauczyciela(dane, tmp_path):
    del kroki(dane)[NAUCZ_1]  # wybor-modelu, effort, poziom, nauczyciel
    wynik = _czytelnosc(dane, tmp_path)
    assert not any("krok 2 (klik)" in b for b in wynik), "klik effort nie jest zmianą"


# filtr języka: notka to polski napis kursu

def test_notka_trafia_do_filtru_jezyka(dane):
    pola = dict(polskie_pola(dane, NAPISY))
    sciezka = "cwiczenia[0].drogi[0].kroki[3].notka"
    assert pola[sciezka] == "niski wysiłek"
    assert pola["cwiczenia[0].drogi[2].kroki[3].notka"] == "najwyższy wysiłek, najdłużej"


def test_effort_z_listy_napisow_nie_trafia_do_filtru(dane):
    kroki(dane)[NAUCZ_1]["tekst"] = "Effort"
    assert "cwiczenia[0].drogi[0].kroki[1].tekst" not in dict(polskie_pola(dane, NAPISY))
