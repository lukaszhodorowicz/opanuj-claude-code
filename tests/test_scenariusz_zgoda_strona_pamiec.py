"""Testy walidatora karty zgody przeglądarki w drodze symulatora aplikacji, część 2: krok `strona` wymaga zgody (Allow once na jeden krok, Always allow do końca drogi, tylko dla tej strony), druga karta, odmowa i droga bez pliku, artefaktu i strony (wzór: tests/dane/strona-zewnetrzna-zgoda.json)."""

import copy

import pytest

from tests.pomoc_zgoda_strona import FAKT_KARTY, ODMOW, RAZ, WZOR, ZAWSZE, bledy, gdzie, jest, kroki


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


# krok strona: zgoda


def test_strona_bez_karty_zgody_odrzucona_z_komunikatem(dane):
    lista = kroki(dane)
    del lista[gdzie(lista, "klik", "allow_once")]
    del lista[gdzie(lista, "zgoda")]
    wynik = bledy(dane)
    assert jest(wynik, f"działanie na cudzej stronie bez karty zgody (fakt {FAKT_KARTY})")
    assert jest(wynik, "krok strona z witryna „Serwis Rowerowy Zet”")


def test_strona_przed_pierwsza_karta_odrzucona(dane):
    lista = kroki(dane, ZAWSZE)
    lista.insert(gdzie(lista, "zgoda"), lista[gdzie(lista, "strona")])
    assert jest(bledy(dane), f"działanie na cudzej stronie bez karty zgody (fakt {FAKT_KARTY})")


def test_allow_once_zuzywa_sie_na_jednym_kroku_strona(dane):
    lista = kroki(dane)
    i = gdzie(lista, "strona")
    lista.insert(i + 1, copy.deepcopy(lista[i]))  # drugi krok strona tej samej strony bez nowej karty
    assert jest(bledy(dane), f"działanie na cudzej stronie bez karty zgody (fakt {FAKT_KARTY})")


def test_nowa_karta_po_allow_once_daje_zgode_na_kolejny_krok_strona(dane):
    lista = kroki(dane)
    i = gdzie(lista, "strona")
    powtorka = [lista[gdzie(lista, "zgoda")], lista[gdzie(lista, "klik", "allow_once")], lista[i]]
    lista[i + 1 : i + 1] = [copy.deepcopy(k) for k in powtorka]
    assert bledy(dane) == []


def test_always_allow_obejmuje_wszystkie_kroki_strona_do_konca_drogi(dane):
    lista = kroki(dane, ZAWSZE)
    assert sum(k["typ"] == "strona" for k in lista) == 3 and sum(k["typ"] == "zgoda" for k in lista) == 1
    assert bledy(dane) == []


def test_always_allow_dotyczy_tylko_tej_strony(dane):
    lista = kroki(dane, ZAWSZE)
    i = gdzie(lista, "strona", nr=2)
    lista[i]["witryna"] = "Inna Hurtownia"
    wynik = bledy(dane)
    assert jest(wynik, "krok strona z witryna „Inna Hurtownia”") and jest(wynik, f"fakt {FAKT_KARTY}")


def test_pamiec_zgody_nie_przechodzi_do_nastepnej_drogi(dane):
    zawsze = kroki(dane, ZAWSZE)
    jedna = kroki(dane, RAZ)
    jedna.insert(gdzie(jedna, "plik") + 1, {"typ": "strona", "witryna": "Hurtownia Bike-Pro", "strona": zawsze[gdzie(zawsze, "strona")]["strona"]})
    assert jest(bledy(dane), "bez karty zgody")


def test_druga_karta_dla_strony_z_always_allow_odrzucona(dane):
    lista = kroki(dane, ZAWSZE)
    i = gdzie(lista, "strona", nr=1)
    lista[i:i] = [copy.deepcopy(lista[gdzie(lista, "zgoda")]), copy.deepcopy(lista[gdzie(lista, "klik", "always_allow")])]
    wynik = bledy(dane)
    assert jest(wynik, "druga karta zgody dla strony „Hurtownia Bike-Pro”, która ma już Always allow")
    assert jest(wynik, "aplikacja-browser-always-allow-zapisuje-dla-strony")


def test_druga_karta_dla_innej_strony_po_always_allow_przechodzi(dane):
    lista = kroki(dane, ZAWSZE)
    i = gdzie(lista, "strona", nr=2)
    karta_b = {**copy.deepcopy(lista[gdzie(lista, "zgoda")]), "witryna": "Inna Hurtownia"}
    lista[i:i] = [karta_b, {"typ": "klik", "cel": "allow_once"}, {**copy.deepcopy(lista[i]), "witryna": "Inna Hurtownia"}]
    assert bledy(dane) == []


def test_po_deny_strona_tej_witryny_to_blad_dopoki_nie_ma_nowej_karty(dane):
    lista = kroki(dane, ODMOW)
    lista.append(copy.deepcopy(kroki(dane, RAZ)[gdzie(kroki(dane, RAZ), "strona")]))
    wynik = bledy(dane)
    assert jest(wynik, "po odmowie (Deny): Claude na tę stronę nie wchodzi")


def test_po_deny_nowa_karta_z_zezwoleniem_otwiera_droge_do_strony(dane):
    lista = kroki(dane, ODMOW)
    wzor = kroki(dane, RAZ)
    lista += [copy.deepcopy(wzor[gdzie(wzor, "zgoda")]), copy.deepcopy(wzor[gdzie(wzor, "klik", "allow_once")]), copy.deepcopy(wzor[gdzie(wzor, "strona")])]
    assert bledy(dane) == []


def test_strona_z_inna_witryna_niz_karta_po_allow_once_odrzucona(dane):
    lista = kroki(dane)
    lista[gdzie(lista, "strona")]["witryna"] = "Inna strona"
    wynik = bledy(dane)
    assert jest(wynik, "najpierw krok strona z witryna „Serwis Rowerowy Zet”")
    assert jest(wynik, f"działanie na cudzej stronie bez karty zgody (fakt {FAKT_KARTY})")


# droga bez pliku, artefaktu i strony


def test_droga_z_deny_moze_nie_miec_pliku_artefaktu_ani_strony(dane):
    assert not any(k["typ"] in ("plik", "artefakt", "strona") for k in kroki(dane, ODMOW))
    assert bledy(dane) == []


def test_droga_bez_deny_i_bez_kroku_pokazujacego_odrzucona(dane):
    lista = kroki(dane, ODMOW)
    del lista[gdzie(lista, "zgoda") :]
    assert jest(bledy(dane), "droga bez kroku plik ani artefakt")


def test_krok_strona_liczy_sie_jak_plik_i_artefakt(dane):
    lista = kroki(dane, ZAWSZE)
    assert not any(k["typ"] in ("plik", "artefakt") for k in lista)
    assert bledy(dane) == []
