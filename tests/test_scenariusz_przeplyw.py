"""Testy walidatora karty zgody na przepływ (krok `przeplyw`, klik `once`; wzór: tests/dane/duze-zadanie-przeplyw.json): pola kroku, tryb, kolejność kroków wokół karty, wpis przepływu w pracy w tle, druga karta po końcu pierwszego przepływu, rytm nauczyciela i polskie pola dla filtrów języka."""

import copy
import re

import pytest

from narzedzia import czytelnosc, tekst_pl
from tests.pomoc_przeplyw import KORZEN, NAPISY, WZOR, bledy, dane, indeks, jest, kroki  # noqa: F401


FRAGMENT = {"nazwa": "przeplyw: nazwa musi być", "fazy": "przeplyw: fazy muszą być"}


def test_wzor_przechodzi(dane):
    assert bledy(dane) == []


@pytest.mark.parametrize("pole,wartosc", [("nazwa", ""), ("nazwa", "  "), ("nazwa", "x" * 81), ("nazwa", "a\nb"), ("nazwa", 5), ("fazy", []), ("fazy", ["a"] * 7), ("fazy", ["a", ""]), ("fazy", ["x" * 61]), ("fazy", "Raport"), ("fazy", ["a\tb"])])
def test_zle_pola_karty_odrzucone(dane, pole, wartosc):
    kroki(dane)[indeks(dane, "przeplyw")][pole] = wartosc
    assert jest(bledy(dane), FRAGMENT[pole])


def test_graniczne_dlugosci_przechodza(dane):
    k = kroki(dane)[indeks(dane, "przeplyw")]
    k["nazwa"], k["fazy"] = "x" * 80, ["f" * 60] * 6
    assert bledy(dane) == []
    k["fazy"] = ["f"]
    assert bledy(dane) == []


def test_nazwa_i_fazy_sa_obowiazkowe(dane):
    for pole in ("nazwa", "fazy"):
        d = copy.deepcopy(dane)
        del kroki(d)[indeks(d, "przeplyw")][pole]
        assert jest(bledy(d), FRAGMENT[pole]), pole


def test_obce_pole_kroku_odrzucone(dane):
    kroki(dane)[indeks(dane, "przeplyw")]["ostrzezenie"] = "tekst"
    assert jest(bledy(dane), "pole ostrzezenie nie należy do kroku przeplyw")


def test_pole_fakt_kroku_przyjmuje_istniejacy_fakt_i_odrzuca_nieistniejacy(dane):
    k = kroki(dane)[indeks(dane, "przeplyw")]
    k["fakt"] = "aplikacja-enter-wysyla-zadanie"
    assert bledy(dane) == []
    k["fakt"] = "nie-ma-takiego-faktu"
    assert jest(bledy(dane), "nie istnieje w pliku faktów")


@pytest.mark.parametrize("tryb,ok", [("Manual", True), ("Accept edits", True), ("Auto", False), ("Bypass", False), ("Plan", False)])
def test_karta_tylko_w_manual_i_accept_edits(dane, tryb, ok):
    dane["cwiczenia"][0]["aplikacja"]["tryb"] = tryb
    assert jest(bledy(dane), "karta zgody na przepływ tylko w trybie") is (not ok)


def test_klik_once_z_obcym_polem_odrzucony(dane):
    kroki(dane)[indeks(dane, "klik", "once")]["nr"] = 1
    assert jest(bledy(dane), "pole nr nie należy do kliku once")


def test_klik_once_bez_karty_odrzucony(dane):
    d = kroki(dane)
    del d[indeks(dane, "przeplyw")]
    assert jest(bledy(dane), "klik once bez karty przepływu")


def test_klik_once_drugi_raz_przy_jednej_karcie_odrzucony(dane):
    d = kroki(dane)
    d.insert(indeks(dane, "klik", "once") + 1, {"typ": "klik", "cel": "once"})
    assert jest(bledy(dane), "klik once bez karty przepływu")


@pytest.mark.parametrize("krok", [{"typ": "mysli"}, {"typ": "claude", "tekst": "x"}, {"typ": "klik", "cel": "sciezka"}, {"typ": "pisz", "tekst": "x"}, {"typ": "klik", "cel": "menu-paska"}])
def test_przy_karcie_ktora_czeka_dalej_tylko_nauczyciel_albo_once(dane, krok):
    kroki(dane).insert(indeks(dane, "przeplyw") + 1, krok)
    assert jest(bledy(dane), "przy karcie przepływu, która czeka")


def test_nauczyciel_przy_karcie_jest_dozwolony(dane):
    assert kroki(dane)[indeks(dane, "przeplyw") + 1]["typ"] == "nauczyciel"
    kroki(dane).insert(indeks(dane, "przeplyw") + 1, {"typ": "nauczyciel", "tekst": "Jeszcze raz."})
    assert bledy(dane) == []


def test_droga_konczaca_sie_karta_ktora_czeka_odrzucona(dane):
    d = kroki(dane)
    del d[indeks(dane, "przeplyw") + 1:]
    assert jest(bledy(dane), "droga kończy się kartą przepływu, która czeka na decyzję")


def test_karta_w_cwiczeniu_z_sesjami_odrzucona(dane):
    dane["cwiczenia"][0]["aplikacja"]["sesje"] = [{"nazwa": "Druga rozmowa"}]
    assert jest(bledy(dane), "karta zgody na przepływ w ćwiczeniu z aplikacja.sesje")


def test_wpis_przeplywu_dodaje_klik_once_wiec_menu_wymaga_kliku_once_wczesniej(dane):
    k = kroki(dane)
    i = indeks(dane, "klik", "menu-paska")
    k.insert(0, k.pop(i))  # ⋮ przed pierwszą pracą w tle
    assert jest(bledy(dane), "klik menu-paska przed pierwszą pracą w tle")


def test_reczny_wpis_przeplywu_odrzucony_w_drodze_z_karta_i_bez_niej(dane):
    ręczny = [{"rodzaj": "przeplyw", "tytul": "porownanie-ofert-szkol"}]
    kroki(dane)[indeks(dane, "claude")]["w_tle"] = ręczny
    assert jest(bledy(dane), "przeplyw tylko z karty zgody")
    d = copy.deepcopy(WZOR)  # droga bez karty: ręczny wpis przepływu też jest błędem
    kr = kroki(d)
    for i in sorted((i for i, k in enumerate(kr) if k["typ"] == "przeplyw" or k.get("cel") == "once"), reverse=True):
        del kr[i]
    kr[indeks(d, "claude")]["w_tle"] = ręczny
    assert jest(bledy(d), "przeplyw tylko z karty zgody")


def test_koniec_pracy_przeplywu_zamyka_klika_e3_jak_przy_subagentach(dane):
    k = kroki(dane)
    k.insert(indeks(dane, "plik"), {"typ": "klik", "cel": "menu-paska"})
    assert jest(bledy(dane), "klik menu-paska po kroku z w_tle_koniec")


def test_koniec_bez_once_odrzucony(dane):
    d = kroki(dane)
    del d[indeks(dane, "klik", "once")]
    wynik = bledy(dane)
    assert jest(wynik, "przy karcie przepływu, która czeka") or jest(wynik, "w_tle_koniec bez wcześniejszej pracy w tle")


def _druga_karta(d):
    """Drugą kartę (z Once) dokleja po kroku `plik` i nauczycielu (po końcu pierwszego przepływu)."""
    k = kroki(d)
    nowe = [
        {"typ": "przeplyw", "nazwa": "wycinek-oferta-fala", "fazy": ["Czytanie oferty", "Sprawdzanie ustaleń"]},
        {"typ": "nauczyciel", "tekst": "Mały wycinek. Kliknij Once."},
        {"typ": "klik", "cel": "once"},
        {"typ": "nauczyciel", "tekst": "Drugi przepływ ruszył."},
    ]
    i = indeks(d, "plik") + 2  # za nauczycielem, który zamyka pierwszą drogę
    k[i:i] = nowe
    return d


def test_druga_karta_po_koncu_pierwszego_przeplywu_przechodzi(dane):
    assert bledy(_druga_karta(dane)) == []


def test_druga_karta_przed_koncem_pierwszego_przeplywu_odrzucona(dane):
    d = dane
    k = kroki(d)
    i = indeks(d, "klik", "once") + 2  # po odpowiedzi „Przepływ ruszył w tle”, przed jego końcem
    k[i:i] = [{"typ": "przeplyw", "nazwa": "drugi", "fazy": ["Faza"]}, {"typ": "klik", "cel": "once"}]
    assert jest(bledy(d), "druga karta przepływu przed w_tle_koniec poprzedniego")


def test_po_drugim_once_kliki_e3_znow_sa_dozwolone_a_przed_nim_nie(dane):
    d = _druga_karta(dane)
    k = kroki(d)
    i = next(j for j, x in enumerate(k) if x.get("nazwa") == "wycinek-oferta-fala")
    po = i + 4  # po nauczycielu za drugim Once
    k[po:po] = [{"typ": "klik", "cel": "menu-paska"}, {"typ": "klik", "cel": "background-tasks"}, {"typ": "nauczyciel", "tekst": "To panel."}]
    assert bledy(d) == []
    d2 = _druga_karta(copy.deepcopy(WZOR))
    k2 = kroki(d2)
    j = next(n for n, x in enumerate(k2) if x.get("nazwa") == "wycinek-oferta-fala")
    k2.insert(j, {"typ": "klik", "cel": "menu-paska"})
    assert jest(bledy(d2), "klik menu-paska po kroku z w_tle_koniec")


def test_przeplyw_obok_subagenta_daje_odnosnik_dwoch_prac_zgodny_ze_wzorem(dane):
    """Subagent zleca się wcześniej niż karta: przy Once są dwie prace w tle, więc pod odpowiedzią stoi „2 running tasks” (napis z listy napisów)."""
    k = kroki(dane)
    k.insert(indeks(dane, "przeplyw") - 1, {"typ": "claude", "tekst": "Zleciłem to subagentowi.", "w_tle": [{"rodzaj": "subagent", "tytul": "Oferta Fali", "zadanie": "Przeczytaj ofertę Fali.", "wynik": ["Fala: 240 zł."]}]})
    assert bledy(dane) == []


def test_przeplyw_nie_wchodzi_do_etapow(dane):
    cw = dane["cwiczenia"][0]
    cw["etapy"] = [{"kroki": [{"typ": "przeplyw", "nazwa": "a", "fazy": ["b"]}]}]
    assert bledy(dane)


def test_rytm_nauczyciela_po_once(dane):
    d = copy.deepcopy(dane)
    kr = kroki(d)
    i = indeks(d, "klik", "once")
    assert kr[i + 2]["typ"] == "nauczyciel"
    zle = czytelnosc._sprawdz_liste_krokow(kr[:i + 1] + [{"typ": "claude", "tekst": "a"}, {"typ": "mysli"}, {"typ": "mysli"}], "", "t", czytelnosc.ZMIANY_APLIKACJI)
    assert any(f"krok {i + 1} (klik)" in b and "brak nauczyciela" in b for b in zle)
    dobre = czytelnosc._sprawdz_liste_krokow(kr, "", "t", czytelnosc.ZMIANY_APLIKACJI)
    assert dobre == []


def test_polskie_pola_zawieraja_nazwe_i_fazy_karty():
    pola = dict(tekst_pl.polskie_pola(WZOR, NAPISY))
    sciezka = next(s for s in pola if re.search(r"kroki\[3\]\.nazwa$", s))
    assert pola[sciezka] == "porownanie-ofert-szkol"
    fazy = [t for s, t in pola.items() if re.search(r"kroki\[3\]\.fazy\[\d\]$", s)]
    assert fazy == ["Czytanie ofert", "Sprawdzanie ustaleń", "Raport"]


def test_napisy_przyciskow_karty_sa_w_stalej_strony_i_na_liscie_napisow_interfejsu():
    js = (KORZEN / "strona" / "aplikacja-przeplyw.js").read_text(encoding="utf-8")
    blok = re.search(r"PK\.NAPISY_PRZEPLYWU = \{(.*?)\};", js, re.S).group(1)
    assert re.findall(r':\s*"([^"]+)"', blok) == ["Once", "Always", "Deny"], "kolejność w rzędzie to umowa symulatora"
    from narzedzia import scenariusz as sc

    lista = sc._Napisy(NAPISY)
    assert all(lista.jest(n, "aplikacja") for n in ("Once", "Always", "Deny"))
    kod = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    assert "Large workflow" not in kod and "Run a dynamic workflow" not in kod, "napisy bez źródła nie wchodzą na kartę"
