"""Testy walidatora pierścienia zużycia abonamentu w ćwiczeniu z drogami symulatora aplikacji: krok `klik` z celem `pierscien`, wyjątek „droga bez pliku”, kolejność kroków po `nowa-rozmowa` z kartą Context i rytm nauczyciela po kliku (wzór: tests/dane/aplikacja-pierscien.json)."""

import copy
import json
import re
from pathlib import Path

import pytest

from narzedzia import czytelnosc
from narzedzia import scenariusz as sc
from narzedzia import scenariusz_pierscien as pierscien

KORZEN = Path(__file__).resolve().parent.parent
WZOR = json.loads((Path(__file__).parent / "dane" / "aplikacja-pierscien.json").read_text(encoding="utf-8"))
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")

# cw1: droga `dwa-liczniki`; cw2: droga 0 `dluga`, droga 1 `nowa`
KLIK_PIERSCIEN, KLIK_CONTEXT = 1, 3
NOWA_ROZMOWA, PISZ_PO_NOWEJ, KONTEKST_PO_NOWEJ = 0, 2, 5


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def jest(wynik, fragment):
    return any(fragment in b for b in wynik)


def kroki(d, cw=0, droga=0):
    return d["cwiczenia"][cw]["drogi"][droga]["kroki"]


def test_wzor_przechodzi_pierscien_i_nowa_rozmowa_z_karta_context(dane):
    assert bledy(dane) == []
    assert kroki(dane)[KLIK_PIERSCIEN] == {"typ": "klik", "cel": "pierscien"}


def test_droga_z_klikiem_pierscien_moze_sie_skonczyc_bez_kroku_plik(dane):
    assert not any(k["typ"] in ("plik", "artefakt") for k in kroki(dane))
    assert bledy(dane) == []


def test_droga_bez_pierscienia_i_bez_pliku_dalej_jest_bledem(dane):
    del kroki(dane)[KLIK_PIERSCIEN : KLIK_PIERSCIEN + 2]  # klik pierscien i nauczyciel po nim
    assert jest(bledy(dane), "droga bez kroku plik ani artefakt")


def test_pole_poza_typ_cel_fakt_w_kliku_pierscien_to_blad(dane):
    kroki(dane)[KLIK_PIERSCIEN]["poziom"] = 2
    assert jest(bledy(dane), "pole poziom nie należy do kroku klik z celem pierscien")


def test_pole_fakt_w_kliku_pierscien_jest_dozwolone(dane):
    kroki(dane)[KLIK_PIERSCIEN]["fakt"] = "aplikacja-karta-context-procent-w-naglowku"
    assert bledy(dane) == []


def test_klik_pierscien_w_cwiczeniu_z_krokami_to_blad():
    kroki_scen = json.loads((Path(__file__).parent / "dane" / "aplikacja.json").read_text(encoding="utf-8"))
    kroki_scen["cwiczenia"][0]["kroki"][0]["klik"] = "pierscien"
    assert jest(bledy(kroki_scen), "klik „pierscien” spoza licznik/changes")  # w krokach pierścień działa bez kroku


def test_klik_context_przed_kontekstem_po_nowej_rozmowie_to_blad_karta_bez_procentu(dane):
    k = kroki(dane, 1, 1)
    k.insert(PISZ_PO_NOWEJ + 3, {"typ": "klik", "cel": "context"})  # po `claude`, przed `kontekst`
    assert jest(bledy(dane), "karta jest bez procentu")


def test_klik_context_przed_pierwsza_proba_po_nowej_rozmowie_to_blad_bo_panelu_nie_ma(dane):
    kroki(dane, 1, 1).insert(NOWA_ROZMOWA + 1, {"typ": "klik", "cel": "context"})
    assert jest(bledy(dane), "przed pierwszą prośbą panelu w ogóle nie ma")


def test_kontekst_przed_pierwsza_proba_po_nowej_rozmowie_to_blad_panel_pojawia_sie_po_prosbie(dane):
    kroki(dane, 1, 1).insert(NOWA_ROZMOWA + 1, {"typ": "kontekst", "procent": 5})
    assert jest(bledy(dane), "panel szczegółów pojawia się dopiero po wysłaniu pierwszej prośby")


def test_klik_context_po_kroku_kontekst_w_nowej_rozmowie_jest_dozwolony(dane):
    k = kroki(dane, 1, 1)
    k.insert(KONTEKST_PO_NOWEJ + 1, {"typ": "klik", "cel": "context"})
    assert bledy(dane) == []


def test_procent_po_nowej_rozmowie_nie_jest_porownywany_z_procentem_starej_rozmowy(dane):
    kroki(dane, 1, 1)[KONTEKST_PO_NOWEJ]["procent"] = 62  # tyle, co na starcie karty starej rozmowy
    assert bledy(dane) == []


def test_ten_sam_procent_dwa_razy_po_nowej_rozmowie_dalej_jest_bledem(dane):
    k = kroki(dane, 1, 1)
    k.insert(KONTEKST_PO_NOWEJ + 1, {"typ": "kontekst", "procent": 5})
    assert jest(bledy(dane), "jest już na karcie Context")


def test_nowa_rozmowa_w_cwiczeniu_bez_karty_context_nie_wlacza_regul_panelu(dane):
    cw = dane["cwiczenia"][1]
    del cw["aplikacja"]["kontekst"]
    cw["aplikacja"]["panel"] = "schowany"
    cw["drogi"] = [cw["drogi"][1]]
    k = cw["drogi"][0]["kroki"]
    del k[KONTEKST_PO_NOWEJ]
    assert bledy(dane) == []


def test_nauczyciel_najdalej_dwa_kroki_po_kliku_pierscien(dane):
    k = kroki(dane)
    del k[KLIK_PIERSCIEN + 1]  # nauczyciel zaraz po kliku
    k.insert(KLIK_PIERSCIEN + 1, {"typ": "mysli"})
    k.insert(KLIK_PIERSCIEN + 2, {"typ": "mysli"})
    k.insert(KLIK_PIERSCIEN + 3, {"typ": "mysli"})
    uwagi = czytelnosc._sprawdz_liste_krokow(k, "", "x", czytelnosc.ZMIANY_APLIKACJI)
    assert any("brak nauczyciela" in u and "klik" in u for u in uwagi)


def test_nauczyciel_w_drugim_kroku_po_kliku_pierscien_wystarcza(dane):
    k = kroki(dane)
    k.insert(KLIK_PIERSCIEN + 1, {"typ": "mysli"})
    assert czytelnosc._sprawdz_liste_krokow(k, "", "x", czytelnosc.ZMIANY_APLIKACJI) == []


def test_przyklad_z_formatu_bez_bledow(dane):
    tekst = (KORZEN / "dane" / "FORMAT-SCENARIUSZA.md").read_text(encoding="utf-8")
    czesc = tekst[tekst.index("### Pierścień zużycia") : tekst.index("### Pasek boczny z rozmowami")]
    przyklad = re.search(r"```json\n(.*?)```", czesc, re.S).group(1)
    kroki_format = [json.loads(l) for l in przyklad.strip().splitlines()]
    assert [k["typ"] for k in kroki_format] == ["nauczyciel", "klik", "nauczyciel"]
    dane = copy.deepcopy(WZOR)
    dane["cwiczenia"][0]["drogi"][0]["kroki"] = kroki_format
    assert bledy(dane) == []
    assert pierscien.KLIKI == ("pierscien",)
