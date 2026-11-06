"""Testy walidatora karty Context, poleceń w polu wiadomości i pytania z boku w ćwiczeniu z drogami symulatora aplikacji: pole `aplikacja.kontekst`, panel widoczny tylko z tym polem, kroki `kontekst`, `komenda`, `z_boku`, kliki `context` i `zamknij-z-boku` (wzór: tests/dane/kontekst-rozmowy.json)."""

import copy
import json
import re
from pathlib import Path

import pytest

from narzedzia import scenariusz as sc
from narzedzia import scenariusz_kontekst as kontekst
from narzedzia.tekst_pl import polskie_pola

KORZEN = Path(__file__).resolve().parent.parent
WZOR = json.loads((Path(__file__).parent / "dane" / "kontekst-rozmowy.json").read_text(encoding="utf-8"))
WZOR_KROKI = json.loads((Path(__file__).parent / "dane" / "aplikacja.json").read_text(encoding="utf-8"))
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")
NAPISY_OBIEKT = sc._Napisy(NAPISY)

# Indeksy w drodze `czytaj-i-streszczaj` (cw1, droga 0)
KONTEKST_71, KLIK_CONTEXT, KOMENDA_COMPACT, KONTEKST_19 = 3, 5, 7, 8
# Indeksy w drodze z pytaniem z boku (cw1 droga 1 i cw2 droga 0)
BTW, Z_BOKU, KLIK_ZAMKNIJ, PISZ_PO_PANELU = 0, 2, 4, 6


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def jest(wynik, fragment):
    return any(fragment in b for b in wynik)


def cw(d, nr=0):
    return d["cwiczenia"][nr]


def kroki(d, cwiczenie=0, droga=0):
    return d["cwiczenia"][cwiczenie]["drogi"][droga]["kroki"]


def test_wzor_przechodzi_karta_context_polecenia_i_pytanie_z_boku(dane):
    assert bledy(dane) == []
    assert cw(dane)["aplikacja"]["kontekst"] == 6 and cw(dane)["aplikacja"]["panel"] == "widoczny"
    assert [k["typ"] for k in kroki(dane, 0, 0) if k["typ"] in kontekst.TYPY] == ["kontekst", "komenda", "kontekst"]
    assert [k["typ"] for k in kroki(dane, 1, 0) if k["typ"] in kontekst.TYPY] == ["komenda", "z_boku"]


# panel i pole `aplikacja.kontekst`

def test_panel_widoczny_z_polem_kontekst_domyslnie_tez_dozwolony(dane):
    del cw(dane)["aplikacja"]["panel"]
    assert bledy(dane) == []


def test_kontekst_z_panelem_schowanym_odrzucony(dane):
    cw(dane)["aplikacja"]["panel"] = "schowany"
    assert jest(bledy(dane), "kontekst wymaga panelu „widoczny”")


def test_panel_widoczny_bez_pola_kontekst_dalej_odrzucony(dane):
    cw(dane, 1)["aplikacja"]["panel"] = "widoczny"
    assert jest(bledy(dane), "wymaga panel „schowany”")
    del cw(dane, 1)["aplikacja"]["panel"]
    assert jest(bledy(dane), "wymaga panel „schowany”")


def test_kontekst_i_zmiany_razem_odrzucone(dane):
    cw(dane)["aplikacja"]["zmiany"] = WZOR_KROKI["cwiczenia"][0]["aplikacja"]["zmiany"]
    assert jest(bledy(dane), "nie ma pola zmiany")


def test_kontekst_poza_cwiczeniem_z_drogami_odrzucony():
    d = copy.deepcopy(WZOR_KROKI)
    d["cwiczenia"][0]["aplikacja"]["kontekst"] = 6
    assert jest(bledy(d), "kontekst tylko w ćwiczeniu z drogami")


@pytest.mark.parametrize("wartosc", [-1, 101, 6.5, "6", "6%", True, None])
def test_kontekst_musi_byc_liczba_calkowita_0_100(dane, wartosc):
    cw(dane)["aplikacja"]["kontekst"] = wartosc
    assert jest(bledy(dane), "kontekst musi być liczbą całkowitą od 0 do 100")


@pytest.mark.parametrize("wartosc", [0, 1, 100])
def test_kontekst_granice_przechodza(dane, wartosc):
    cw(dane)["aplikacja"]["kontekst"] = wartosc
    kroki(dane)[KONTEKST_71]["procent"] = 50
    assert bledy(dane) == []


def test_napis_procentu_musi_pasowac_do_wzoru_z_listy(dane):
    ten = [w for w in NAPISY if w.get("wzor") == r"^\d{1,3}%$"]
    assert len(ten) == 1
    zawezone = [w for w in NAPISY if w is not ten[0]]
    wynik = sc.sprawdz_scenariusz(dane, FAKTY_ID, zawezone)
    assert jest(wynik, "napis „6%” nie pasuje do wzoru z listy napisów interfejsu aplikacji")


# krok `kontekst`

def test_krok_kontekst_bez_pola_kontekst_w_cwiczeniu(dane):
    kroki(dane, 1)[PISZ_PO_PANELU - 1:PISZ_PO_PANELU - 1] = [{"typ": "kontekst", "procent": 30}]
    assert jest(bledy(dane), "krok kontekst bez aplikacja.kontekst")


def test_krok_kontekst_musi_zmienic_procent(dane):
    kroki(dane)[KONTEKST_71]["procent"] = 6
    assert jest(bledy(dane), "procent 6% jest już na karcie Context")
    kroki(dane)[KONTEKST_71]["procent"] = 71
    kroki(dane)[KONTEKST_19]["procent"] = 71
    assert jest(bledy(dane), "procent 71% jest już na karcie Context")


@pytest.mark.parametrize("procent", [101, -5, 7.5, "71", None])
def test_krok_kontekst_procent_spoza_zakresu(dane, procent):
    kroki(dane)[KONTEKST_71]["procent"] = procent
    assert jest(bledy(dane), "procent musi być liczbą całkowitą od 0 do 100")


def test_krok_kontekst_obce_pole_i_nieznany_fakt(dane):
    kroki(dane)[KONTEKST_71]["ms"] = 500
    kroki(dane)[KONTEKST_19]["fakt"] = "fakt-ktorego-nie-ma"
    wynik = bledy(dane)
    assert jest(wynik, "pole ms nie należy do kroku kontekst")
    assert jest(wynik, "fakt „fakt-ktorego-nie-ma” nie istnieje")


# krok `komenda`

@pytest.mark.parametrize("tekst", ["/context", "/clear", "/compact zachowaj ceny", "compact", "", None, 5])
def test_komenda_tylko_compact_albo_btw(dane, tekst):
    kroki(dane)[KOMENDA_COMPACT]["tekst"] = tekst
    wynik = bledy(dane)
    assert jest(wynik, "komenda „") and (jest(wynik, "spoza listy napisów") or jest(wynik, "symulator gra tylko"))


def test_komenda_z_listy_napisow_ale_bez_gry_w_symulatorze_odrzucona(dane):
    napisy = [*NAPISY, {"napis": "/context", "gdzie": "aplikacja", "zrodlo": "próba"}]
    kroki(dane)[KOMENDA_COMPACT]["tekst"] = "/context"
    wynik = sc.sprawdz_scenariusz(dane, FAKTY_ID, napisy)
    assert jest(wynik, "symulator gra tylko /compact i /btw")


def test_komenda_obce_pole(dane):
    kroki(dane)[KOMENDA_COMPACT]["procent"] = 10
    assert jest(bledy(dane), "pole procent nie należy do kroku komenda")


def test_compact_nie_otwiera_panelu_pytania_z_boku(dane):
    kroki(dane, 1)[BTW]["tekst"] = "/compact"
    wynik = bledy(dane)
    assert jest(wynik, "krok z_boku bez otwartego panelu")
    assert not jest(wynik, "komenda „/compact”")


# krok `z_boku` i panel

def test_z_boku_bez_btw(dane):
    del kroki(dane, 1)[BTW]
    assert jest(bledy(dane), "krok z_boku bez otwartego panelu pytania z boku: najpierw komenda /btw")


@pytest.mark.parametrize("pole", ["pytanie", "odpowiedz"])
def test_z_boku_wymaga_pytania_i_odpowiedzi(dane, pole):
    kroki(dane, 1)[Z_BOKU][pole] = "  "
    assert jest(bledy(dane), f"krok z_boku wymaga niepustego pola {pole}")
    del kroki(dane, 1)[Z_BOKU][pole]
    assert jest(bledy(dane), f"krok z_boku wymaga niepustego pola {pole}")


def test_z_boku_obce_pole(dane):
    kroki(dane, 1)[Z_BOKU]["plik"] = "uwagi-autora.txt"
    assert jest(bledy(dane), "pole plik nie należy do kroku z_boku")


@pytest.mark.parametrize(
    "krok",
    [
        {"typ": "pisz", "tekst": "Dopisz coś."},
        {"typ": "mysli"},
        {"typ": "claude", "tekst": "Zrobione."},
        {"typ": "komenda", "tekst": "/compact"},
        {"typ": "komenda", "tekst": "/btw"},
        {"typ": "klik", "cel": "sciezka"},
        {"typ": "kontekst", "procent": 40},
    ],
)
def test_przy_otwartym_panelu_tylko_nauczyciel_z_boku_i_krzyzyk(dane, krok):
    kroki(dane, 0, 1).insert(Z_BOKU + 1, krok)
    assert jest(bledy(dane), "przy otwartym panelu pytania z boku: dalej tylko nauczyciel, z_boku i klik „zamknij-z-boku”")


def test_dwa_pytania_z_boku_pod_rzad_dozwolone(dane):
    kroki(dane, 1).insert(Z_BOKU + 1, {"typ": "z_boku", "pytanie": "A rozdział 2?", "odpowiedz": "Ma 12 stron."})
    assert bledy(dane) == []


def test_bez_zamkniecia_panelu_dalsza_prosba_odrzucona(dane):
    del kroki(dane, 1)[KLIK_ZAMKNIJ]
    assert jest(bledy(dane), "krok pisz przy otwartym panelu pytania z boku")


# kliki

def test_klik_context_w_cwiczeniu_bez_karty(dane):
    kroki(dane, 1)[-1:-1] = [{"typ": "klik", "cel": "context"}]
    assert jest(bledy(dane), "klik w kartę Context bez aplikacja.kontekst")


def test_klik_context_drugi_raz_w_tej_samej_drodze(dane):
    kroki(dane, 0, 0).insert(KLIK_CONTEXT + 1, {"typ": "klik", "cel": "context"})
    assert jest(bledy(dane), "klik w kartę Context, która jest już otwarta")


def test_klik_zamknij_z_boku_bez_panelu(dane):
    del kroki(dane, 1)[BTW]
    del kroki(dane, 1)[Z_BOKU - 1]  # z_boku wypada razem z poleceniem
    wynik = bledy(dane)
    assert jest(wynik, "klik zamknij-z-boku bez otwartego panelu pytania z boku")


def test_klik_zamknij_z_boku_dwa_razy(dane):
    kroki(dane, 1).insert(KLIK_ZAMKNIJ + 1, {"typ": "klik", "cel": "zamknij-z-boku"})
    assert jest(bledy(dane), "klik zamknij-z-boku bez otwartego panelu")


def test_klik_z_obcym_celem_wymienia_nowe_cele(dane):
    kroki(dane)[KLIK_CONTEXT]["cel"] = "licznik"
    assert jest(bledy(dane), "nagłówek karty Context (cel „context”) albo krzyżyk pytania z boku (cel „zamknij-z-boku”)")


def test_klik_context_przy_otwartym_panelu_odrzucony(dane):
    kroki(dane, 0, 1).insert(Z_BOKU + 1, {"typ": "klik", "cel": "context"})
    assert jest(bledy(dane), "krok klik przy otwartym panelu pytania z boku")


# stan między krokami

def test_btw_zamyka_widok_artefaktu_jak_krok_plik():
    st = {**kontekst.stan({"kontekst": 6}), "artefakt": {"tytul": "Strona"}}
    kontekst.krok({"typ": "komenda", "tekst": "/btw"}, "s", st, NAPISY_OBIEKT, lambda *a: None)
    assert st["artefakt"] is None and st["z_boku"] is True


def test_compact_nie_otwiera_panelu_ani_nie_rusza_artefaktu():
    st = {**kontekst.stan({"kontekst": 6}), "artefakt": {"tytul": "Strona"}}
    kontekst.krok({"typ": "komenda", "tekst": "/compact"}, "s", st, NAPISY_OBIEKT, lambda *a: None)
    assert st["artefakt"] == {"tytul": "Strona"} and st["z_boku"] is False


def test_stan_bez_pola_kontekst_nie_ma_karty():
    assert kontekst.stan({})["kontekst"] is None
    assert kontekst.stan({"kontekst": "6"})["kontekst"] is None


# polskie napisy dla filtrów języka

def test_tekst_pl_wypisuje_pytanie_i_odpowiedz_z_boku_ale_nie_polecenia(dane):
    pola = dict(polskie_pola(dane, NAPISY))
    assert pola["cwiczenia[1].drogi[0].kroki[2].pytanie"] == "Jaki termin oddania podał autor w uwagach?"
    assert pola["cwiczenia[1].drogi[0].kroki[2].odpowiedz"] == "W uwagach autora: 15 grudnia 2026."
    assert not any(t in ("/compact", "/btw") for t in pola.values())
    assert not any(p.endswith(".procent") for p in pola)



def test_napis_karty_context_w_pliku_js_jest_na_liscie():
    js = (KORZEN / "strona" / "aplikacja-kontekst.js").read_text(encoding="utf-8")
    blok = re.search(r"PK\.NAPISY_KONTEKSTU = \{(.*?)\};", js, re.S).group(1)
    napisy = re.findall(r':\s*"([^"]+)"', blok)
    assert napisy == ["Context"] and all(NAPISY_OBIEKT.jest(n, "aplikacja") for n in napisy)

