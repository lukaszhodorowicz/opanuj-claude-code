"""Testy walidatora kroku `strona` w drodze symulatora aplikacji, część 3: treść strony i ramki `pola` (1-4 obiekty z etykietą i wartością), odrzucenie `pola` w kroku `plik` i w artefakcie, podgląd drogi z odmową w lekcji, polskie napisy dla filtrów i napisy przycisków karty (wzór: tests/dane/strona-zewnetrzna-zgoda.json)."""

import copy
import json
import re

import pytest

from narzedzia import scenariusz as sc
from narzedzia import strona, strona_podglad, tekst_pl
from tests.pomoc_zgoda_strona import DANE, DWIE, KORZEN, NAPISY, ODMOW, RAZ, WZOR, ZAWSZE, bledy, gdzie, jest, kroki


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


@pytest.fixture
def dwie():
    return copy.deepcopy(DWIE)


# krok strona: pola i treść


@pytest.mark.parametrize("pole", ["tytul", "opis", "program", "cena", "opinie", "kontakt"])
def test_strona_wymaga_szesciu_pol(dane, pole):
    del kroki(dane)[gdzie(kroki(dane), "strona")]["strona"][pole]
    assert jest(bledy(dane), f"brak pola {pole}")


@pytest.mark.parametrize("pole", ["przycisk", "formularz", "obraz", "adres", "link"])
def test_przycisk_i_formularz_w_kroku_strona_dalej_odrzucone(dane, pole):
    kroki(dane)[gdzie(kroki(dane), "strona")]["strona"][pole] = "x"
    assert jest(bledy(dane), f"strona: pole {pole} odrzucone")


def test_krok_strona_bez_witryna_albo_strony_odrzucony(dane):
    lista = kroki(dane)
    i = gdzie(lista, "strona")
    del lista[i]["witryna"]
    assert jest(bledy(dane), "krok strona wymaga pola witryna")
    lista[i]["witryna"] = "Serwis Rowerowy Zet"
    del lista[i]["strona"]
    assert jest(bledy(dane), "krok strona wymaga obiektu strona")


def test_krok_strona_z_obcym_polem_odrzucony(dane):
    kroki(dane)[gdzie(kroki(dane), "strona")]["tekst"] = "x"
    assert jest(bledy(dane), "pole tekst nie należy do kroku strona")


def test_krok_strona_z_nieistniejacym_faktem_odrzucony(dane):
    kroki(dane)[gdzie(kroki(dane), "strona")]["fakt"] = "fakt-ktorego-nie-ma"
    assert jest(bledy(dane), "fakt-ktorego-nie-ma")


def pola_trzecie(d):
    return kroki(d, ZAWSZE)[gdzie(kroki(d, ZAWSZE), "strona", nr=2)]["strona"]


def test_pola_wzor_ma_trzy_ramki_a_pusta_wartosc_przechodzi(dane):
    pola = pola_trzecie(dane)["pola"]
    assert [p["etykieta"] for p in pola] == ["Firma", "E-mail", "Wiadomość"]
    assert kroki(dane, ZAWSZE)[gdzie(kroki(dane, ZAWSZE), "strona")]["strona"]["pola"][0]["wartosc"] == ""
    assert bledy(dane) == []


@pytest.mark.parametrize("ile", [1, 2, 3, 4])
def test_pola_od_jednej_do_czterech_ramek_przechodza(dane, ile):
    strona = pola_trzecie(dane)
    strona["pola"] = [{"etykieta": f"Pole {n}", "wartosc": "x"} for n in range(ile)]
    assert bledy(dane) == []


@pytest.mark.parametrize("pola", [[], [{"etykieta": "A", "wartosc": "b"}] * 5, "Firma", {"etykieta": "A", "wartosc": "b"}, None, 3])
def test_pola_poza_lista_od_1_do_4_odrzucone(dane, pola):
    pola_trzecie(dane)["pola"] = pola
    assert jest(bledy(dane), "pole pola musi być listą od 1 do 4 obiektów (etykieta, wartosc)")


@pytest.mark.parametrize("pozycja", ["Firma", 5, None, ["Firma", ""]])
def test_pozycja_pola_musi_byc_obiektem(dane, pozycja):
    pola_trzecie(dane)["pola"][0] = pozycja
    assert jest(bledy(dane), "każda pozycja pola pola musi być obiektem")


@pytest.mark.parametrize("etykieta", ["", "  ", 5, None, ["Firma"]])
def test_etykieta_ramki_musi_byc_niepustym_napisem(dane, etykieta):
    pola_trzecie(dane)["pola"][1]["etykieta"] = etykieta
    assert jest(bledy(dane), "pola[1]: etykieta musi być niepustym napisem")


@pytest.mark.parametrize("wartosc", [5, None, ["x"], True])
def test_wartosc_ramki_musi_byc_napisem(dane, wartosc):
    pola_trzecie(dane)["pola"][1]["wartosc"] = wartosc
    assert jest(bledy(dane), "pola[1]: wartosc musi być napisem")


def test_brak_wartosci_ramki_odrzucony_a_pusty_napis_przechodzi(dane):
    del pola_trzecie(dane)["pola"][2]["wartosc"]
    assert jest(bledy(dane), "pola[2]: wartosc musi być napisem")
    pola_trzecie(dane)["pola"][2]["wartosc"] = ""
    assert bledy(dane) == []


@pytest.mark.parametrize("obce", ["typ", "placeholder", "przycisk", "name"])
def test_ramka_z_obcym_polem_odrzucona(dane, obce):
    pola_trzecie(dane)["pola"][0][obce] = "x"
    assert jest(bledy(dane), f"pola[0]: nieznane pole {obce}")


def test_pola_w_kroku_plik_odrzucone():
    d = json.loads((DANE / "aplikacja-przegladarka.json").read_text(encoding="utf-8"))
    lista = d["cwiczenia"][0]["drogi"][0]["kroki"]
    lista[gdzie(lista, "plik")]["strona"]["pola"] = [{"etykieta": "Firma", "wartosc": ""}]
    assert jest(bledy(d), "strona: pole pola tylko w kroku strona")


def test_pola_w_artefakcie_odrzucone():
    d = json.loads((DANE / "artefakt.json").read_text(encoding="utf-8"))
    krok = next(k for x in d["cwiczenia"][0]["drogi"] for k in x["kroki"] if k["typ"] == "artefakt" and "strona" in k)
    krok["strona"]["pola"] = [{"etykieta": "Firma", "wartosc": ""}]
    assert jest(bledy(d), "strona: pole pola tylko w kroku strona")


# podgląd w lekcji i polskie napisy


def lekcja_z_podgladem(droga):
    return f'<div class="podglad" data-cw="cw1" data-t="{droga}"></div>'


def test_podglad_drogi_zakonczonej_krokiem_strona_przechodzi(dane):
    strona_podglad.sprawdz_podglady(lekcja_z_podgladem(ZAWSZE), dane)
    strona_podglad.sprawdz_podglady(lekcja_z_podgladem(RAZ), dane)


def test_podglad_drogi_z_odmowa_to_blad_skladania(dane):
    with pytest.raises(ValueError, match="droga nie ma kroku plik, artefakt ani strona"):
        strona_podglad.sprawdz_podglady(lekcja_z_podgladem(ODMOW), dane)


def test_podglad_drogi_z_odmowa_i_plikiem_po_niej_przechodzi(dwie):
    strona_podglad.sprawdz_podglady(lekcja_z_podgladem("dwie-strony"), dwie)


def test_widok_klienta_nie_uznaje_strony_za_artefakt(dane):
    dane["cwiczenia"][0]["widok_klienta"] = {"ty": "Ty", "klient": "Klient", "podpis": "Podpis"}
    with pytest.raises(ValueError, match="droga nie kończy się krokiem artefakt"):
        strona_podglad.sprawdz_podglady('<div class="podglad" data-cw="cw1" data-t="zawsze" data-widok="klient"></div>', dane)


def test_tekst_pl_wypisuje_etykiety_i_wartosci_pol(dane):
    wynik = dict(tekst_pl.polskie_pola(dane, NAPISY))
    sciezka = "cwiczenia[0].drogi[2].kroki[{}].strona.pola[{}].{}"
    i = gdzie(kroki(dane, ZAWSZE), "strona", nr=2)
    assert wynik[sciezka.format(i, 0, "etykieta")] == "Firma"
    assert wynik[sciezka.format(i, 1, "wartosc")] == "kontakt@detka.example"
    assert wynik[sciezka.format(i, 2, "wartosc")] == "Prosimy o cennik hurtowy. Zamawiamy części co miesiąc."
    assert wynik[sciezka.format(i, 1, "etykieta")] == "E-mail"


def test_tekst_pl_pomija_puste_wartosci_ramek_i_nie_wypisuje_witryny(dane):
    wynik = dict(tekst_pl.polskie_pola(dane, NAPISY))
    i = gdzie(kroki(dane, ZAWSZE), "strona")
    assert not any(s.endswith(f"kroki[{i}].strona.pola[0].wartosc") for s in wynik)
    assert not any(s.endswith(".witryna") for s in wynik)


def test_napisy_przyciskow_karty_sa_na_liscie_napisow_interfejsu():
    js = (KORZEN / "strona" / "aplikacja-drogi-strona.js").read_text(encoding="utf-8")
    blok = re.search(r"PK\.NAPISY_ZGODY_STRONY = \{(.*?)\};", js, re.S).group(1)
    napisy = re.findall(r':\s*"([^"]+)"', blok)
    lista = sc._Napisy(NAPISY)
    assert napisy == ["Allow once", "Always allow", "Deny"]
    assert all(lista.jest(n, "aplikacja") for n in napisy)


def test_karta_w_etapach_nie_przyjmuje_witryny():
    d = json.loads((DANE / "okno-zgody-tryby.json").read_text(encoding="utf-8"))
    zgoda = next(k for e in d["cwiczenia"][0]["etapy"] for k in e["kroki"] if k["typ"] == "zgoda")
    zgoda["witryna"] = "Serwis Rowerowy Zet"
    del zgoda["plik"]
    assert bledy(d) != []


def zloz(tmp_path, dane, droga):
    (tmp_path / "lekcja.md").write_text(f"# Próba\n\n<!-- cwiczenie: cw1 -->\n\n<!-- podglad: cw1 {droga} -->\n", encoding="utf-8")
    (tmp_path / "scenariusz.json").write_text(json.dumps(dane, ensure_ascii=False), encoding="utf-8")
    return strona.zloz_strone(tmp_path)


def test_skladanie_lekcji_z_podgladem_drogi_z_odmowa_konczy_sie_bledem(tmp_path, dane):
    with pytest.raises(ValueError, match="droga nie ma kroku plik, artefakt ani strona"):
        zloz(tmp_path, dane, ODMOW)


def test_skladanie_lekcji_z_podgladem_drogi_ze_strona_przechodzi_i_ma_nowy_plik_js(tmp_path, dane):
    html = zloz(tmp_path, dane, ZAWSZE)
    assert 'data-cw="cw1" data-t="zawsze"' in html and "PK.stronaZewnetrzna" in html and "PK.podgladyDrogCwiczenia" in html
