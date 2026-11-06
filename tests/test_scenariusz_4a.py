"""Testy walidatora paczki 4 część A silnika aplikacji (wzór: tests/dane/aplikacja-4a.json): pola `aplikacja.model` i `aplikacja.wysilek`, pole `kontekst` wiersza `aplikacja.sesje`, kroki `klik` `tryb-menu`, `tryb` i `srodowisko-menu`, wyjątek „droga bez pliku” i rytm nauczyciela po nowych klikach."""

import copy
import json
from pathlib import Path

import pytest
import yaml

from narzedzia import czytelnosc, scenariusz as sc

KORZEN = Path(__file__).resolve().parent.parent
NAPISY = sc._Napisy(sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml"))
FAKTY_ID = {w["id"] for w in yaml.safe_load((KORZEN / "dane" / "fakty.yaml").read_text(encoding="utf-8"))["fakty"]}
WZOR = json.loads((Path(__file__).parent / "dane" / "aplikacja-4a.json").read_text(encoding="utf-8"))


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def cw(d, nr):
    return next(c for c in d["cwiczenia"] if c["id"] == f"cw{nr}")


def droga(d, nr, id_drogi):
    return next(x for x in cw(d, nr)["drogi"] if x["id"] == id_drogi)


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


def zawiera(lista, fragment):
    return any(fragment in b for b in lista)


def test_wzor_bez_bledow(dane):
    assert bledy(dane) == []


# --- aplikacja.model i aplikacja.wysilek


@pytest.mark.parametrize("model", ["Opus 5.5", "Fable 5.1", "Sonnet 5.5", "Haiku 5.5"])
def test_model_ze_zrzutu_przechodzi(dane, model):
    cw(dane, 3)["aplikacja"]["model"] = model
    assert bledy(dane) == []


@pytest.mark.parametrize("model", ["GPT 5", "Sonnet 4", "sonnet 5.5", "", 5, None])
def test_model_spoza_zrzutu_to_blad(dane, model):
    cw(dane, 3)["aplikacja"]["model"] = model
    assert zawiera(bledy(dane), "model ")


@pytest.mark.parametrize("wysilek", ["Low", "Medium", "High", "Extra", "Max"])
def test_wysilek_z_listy_przechodzi(dane, wysilek):
    cw(dane, 3)["aplikacja"]["wysilek"] = wysilek
    wybor = next(k for k in droga(dane, 3, "model")["kroki"] if k.get("cel") == "poziom")
    wybor["poziom"] = 1 if wysilek != "Low" else 5  # droga kończy się wyborem poziomu: musi on różnić się od bieżącego (wyjątek „droga bez pliku”)
    assert bledy(dane) == []


@pytest.mark.parametrize("wysilek", ["Ultracode", "Ultra", "high", "Recommended", 3])
def test_wysilek_spoza_listy_to_blad(dane, wysilek):
    cw(dane, 3)["aplikacja"]["wysilek"] = wysilek
    assert zawiera(bledy(dane), "wysilek ")


def test_wysilek_bez_modelu_przechodzi_model_domyslny(dane):
    """Bez `aplikacja.model` przycisk pokazuje model domyślny Opus 5.5 z poziomem z `wysilek` (FORMAT, „Model domyślny na przycisku modelu”)."""
    apl = cw(dane, 3)["aplikacja"]
    del apl["model"]
    assert "wysilek" in apl
    assert bledy(dane) == []


def test_model_bez_wysilku_przechodzi_domyslnie_medium(dane):
    del cw(dane, 3)["aplikacja"]["wysilek"]
    assert bledy(dane) == []


def test_model_i_wysilek_dzialaja_w_cwiczeniu_z_etapami_i_krokami_bez_bledu_walidatora():
    """Pola są w obiekcie `aplikacja` każdego rodzaju ćwiczenia; przycisk modelu rysuje każde ćwiczenie aplikacji."""
    etapy = json.loads((Path(__file__).parent / "dane" / "okno-zgody-tryby.json").read_text(encoding="utf-8"))
    etapy["cwiczenia"][0]["aplikacja"].update(model="Opus 5.5", wysilek="High")
    assert bledy(etapy) == []


# --- aplikacja.sesje[].kontekst


def test_kontekst_wiersza_sesje_przechodzi(dane):
    assert next(w for w in cw(dane, 2)["aplikacja"]["sesje"] if w["id"] == "stara")["kontekst"] == 42
    assert bledy(dane) == []


@pytest.mark.parametrize("wartosc", [101, -1, "42", 4.5, True])
def test_kontekst_wiersza_sesje_poza_zakresem_albo_nie_liczba_to_blad(dane, wartosc):
    cw(dane, 2)["aplikacja"]["sesje"][0]["kontekst"] = wartosc
    assert zawiera(bledy(dane), "kontekst musi być liczbą całkowitą od 0 do 100")


def test_kontekst_wiersza_sesje_bez_karty_context_to_blad(dane):
    apl = cw(dane, 6)["aplikacja"]
    del apl["kontekst"]
    apl["panel"] = "schowany"
    assert zawiera(bledy(dane), "pole kontekst wiersza sesje bez aplikacja.kontekst")


def test_klik_context_po_otwarciu_rozmowy_bez_procentu_to_blad(dane):
    """Rozmowa bez pola kontekst ma szary pasek zamiast liczby: karty bez procentu nie ma po co otwierać."""
    droga(dane, 2, "bez")["kroki"].append({"typ": "klik", "cel": "context"})
    assert zawiera(bledy(dane), "karta jest bez procentu")


def test_klik_context_po_otwarciu_rozmowy_z_procentem_przechodzi(dane):
    assert any(k.get("cel") == "context" for k in droga(dane, 2, "stara")["kroki"])
    assert bledy(dane) == []


def test_procent_kroku_kontekst_porownuje_sie_z_procentem_otwartej_rozmowy(dane):
    """Po otwarciu rozmowy z polem kontekst 42 krok `kontekst` z 42 niczego nie zmienia, więc jest błędem; 11 przechodzi."""
    kroki = droga(dane, 2, "start")["kroki"]
    assert kroki[2]["typ"] == "kontekst"
    kroki[2]["procent"] = 42
    assert zawiera(bledy(dane), "procent 42% jest już na karcie Context")


def test_po_powrocie_do_rozmowy_krok_kontekst_widzi_jej_ostatni_procent(dane):
    """Droga „wroc”: rozmowa stara 42 -> krok 20 -> bez procentu -> powrót (20). Kolejny krok z 20 byłby błędem."""
    droga(dane, 2, "wroc")["kroki"].append({"typ": "kontekst", "procent": 20})
    assert zawiera(bledy(dane), "procent 20% jest już na karcie Context")


# --- klik tryb-menu / tryb


def kroki_trybu(dane):
    return droga(dane, 1, "tryb")["kroki"]


def test_tryb_bez_tryb_menu_to_blad(dane):
    del kroki_trybu(dane)[0]
    assert zawiera(bledy(dane), "klik „tryb” bez otwartej listy trybów")


def test_droga_konczaca_sie_przy_otwartej_liscie_trybow_to_blad(dane):
    k = kroki_trybu(dane)
    del k[2:]
    assert zawiera(bledy(dane), "droga kończy się przy otwartej liście trybów")


def test_drugi_tryb_menu_przy_otwartej_liscie_to_blad(dane):
    kroki_trybu(dane).insert(1, {"typ": "klik", "cel": "tryb-menu"})
    assert zawiera(bledy(dane), "przy otwartej liście trybów")


@pytest.mark.parametrize("typ", ["pisz", "mysli", "claude"])
def test_krok_innego_typu_przy_otwartej_liscie_trybow_to_blad(dane, typ):
    krok = {"typ": typ, "tekst": "Napisz coś."} if typ != "mysli" else {"typ": "mysli"}
    kroki_trybu(dane).insert(1, krok)
    assert zawiera(bledy(dane), "przy otwartej liście trybów: dalej tylko nauczyciel i klik „tryb”")


def test_tryb_ktory_juz_stoi_na_przelaczniku_to_blad(dane):
    kroki_trybu(dane)[2]["na"] = "Accept edits"
    assert zawiera(bledy(dane), "już jest na przełączniku")


def test_drugi_wybor_trybu_w_tej_samej_drodze_widzi_nowy_tryb(dane):
    """Po wyborze Plan przełącznik pokazuje Plan: ponowny wybór Plan w tej drodze to błąd, wybór Auto przechodzi."""
    k = kroki_trybu(dane)
    k += [{"typ": "klik", "cel": "tryb-menu"}, {"typ": "klik", "cel": "tryb", "na": "Plan"}, {"typ": "nauczyciel", "tekst": "Plan."}]
    assert zawiera(bledy(dane), "tryb „Plan” już jest na przełączniku")
    k[-2]["na"] = "Auto"
    assert bledy(dane) == []


def test_tryb_spoza_listy_napisow_albo_listy_trybow_to_blad(dane):
    kroki_trybu(dane)[2]["na"] = "Plan mode"
    assert zawiera(bledy(dane), "na „Plan mode” spoza listy napisów interfejsu aplikacji")


def test_bypass_permissions_tylko_z_bypass_dostepny(dane):
    kroki_trybu(dane)[2]["na"] = "Bypass permissions"
    assert bledy(dane) == []  # wzór ma bypass_dostepny: true
    cw(dane, 1)["aplikacja"]["bypass_dostepny"] = False
    assert zawiera(bledy(dane), "Bypass permissions dopiero z aplikacja.bypass_dostepny: true")
    del cw(dane, 1)["aplikacja"]["bypass_dostepny"]
    assert zawiera(bledy(dane), "Bypass permissions dopiero z aplikacja.bypass_dostepny: true")


def test_bypass_dostepny_w_drogach_bez_kroku_tryb_menu_dalej_jest_bledem(dane):
    cw(dane, 3)["aplikacja"]["bypass_dostepny"] = True
    assert zawiera(bledy(dane), "pole bypass_dostepny tylko w ćwiczeniu z etapami")


def test_bypass_dostepny_w_drogach_z_tryb_menu_przechodzi(dane):
    assert cw(dane, 1)["aplikacja"]["bypass_dostepny"] is True
    assert not zawiera(bledy(dane), "bypass_dostepny")


def test_pola_obce_w_kliku_tryb_to_blad(dane):
    kroki_trybu(dane)[0]["na"] = "Plan"
    assert zawiera(bledy(dane), "pole na nie należy do kroku klik z celem tryb-menu")
    kroki_trybu(dane)[0].pop("na")
    kroki_trybu(dane)[2]["notka"] = "x"
    assert zawiera(bledy(dane), "pole notka nie należy do kroku klik z celem tryb")


def test_klik_tryb_w_cwiczeniu_z_krokami_to_blad(dane):
    """W ćwiczeniu z krokami pole `klik` zna tylko `licznik` i `changes`."""
    plus = json.loads((Path(__file__).parent / "dane" / "aplikacja.json").read_text(encoding="utf-8"))
    plus["cwiczenia"][0]["kroki"][0]["klik"] = "tryb-menu"
    assert zawiera(bledy(plus), "klik „tryb-menu” spoza licznik/changes")


# --- klik srodowisko-menu


def kroki_srodowiska(dane):
    return droga(dane, 4, "srodowisko")["kroki"]


def test_srodowisko_menu_w_sesji_chmurowej_to_blad(dane):
    cw(dane, 4)["aplikacja"]["srodowisko"] = "Cloud"
    assert zawiera(bledy(dane), "tylko w sesji aplikacja.srodowisko „Local”")


def test_drugi_klik_srodowisko_menu_to_blad(dane):
    kroki_srodowiska(dane).insert(1, {"typ": "klik", "cel": "srodowisko-menu"})
    assert zawiera(bledy(dane), "menu środowiska jest już otwarte")


@pytest.mark.parametrize("krok", [{"typ": "pisz", "tekst": "Napisz coś."}, {"typ": "klik", "cel": "pierscien"}, {"typ": "mysli"}])
def test_po_otwarciu_menu_srodowiska_dalej_tylko_nauczyciel(dane, krok):
    kroki_srodowiska(dane).insert(1, krok)
    assert zawiera(bledy(dane), "po otwarciu menu środowiska: dalej tylko nauczyciel")


def test_pola_obce_w_kliku_srodowisko_menu_to_blad(dane):
    kroki_srodowiska(dane)[0]["na"] = "Cloud"
    assert zawiera(bledy(dane), "pole na nie należy do kroku klik z celem srodowisko-menu")


# --- droga bez pliku


def test_droga_bez_pliku_i_bez_nowych_celow_dalej_jest_bledem(dane):
    d = droga(dane, 5, "praca")
    d["kroki"] = [k for k in d["kroki"] if k["typ"] not in ("klik", "plik")]
    assert zawiera(bledy(dane), "droga bez kroku plik ani artefakt")


@pytest.mark.parametrize(
    "kroki",
    [
        [{"typ": "klik", "cel": "tryb-menu"}, {"typ": "klik", "cel": "tryb", "na": "Plan"}],
        [{"typ": "klik", "cel": "wybor-modelu"}, {"typ": "klik", "cel": "effort"}, {"typ": "klik", "cel": "poziom", "poziom": 3, "notka": "wysoki"}],
        [{"typ": "klik", "cel": "srodowisko-menu"}],
    ],
    ids=["tryb", "model", "srodowisko"],
)
def test_droga_z_samym_trybem_modelem_albo_srodowiskiem_przechodzi_bez_pliku(dane, kroki):
    kroki = copy.deepcopy(kroki) + [{"typ": "nauczyciel", "tekst": "Gotowe."}]
    cw(dane, 4)["drogi"] = [{"id": "x", "etykieta": "Sama zmiana", "kroki": kroki}]
    assert bledy(dane) == []


def test_droga_z_samym_krokiem_kontekst_przechodzi_bez_pliku(dane):
    """Wyjątek U3: sama karta Context (krok `kontekst`) pokazuje zmianę w oknie, plik niepotrzebny."""
    cw(dane, 6)["drogi"] = [{"id": "x", "etykieta": "Sam procent", "kroki": [{"typ": "pisz", "tekst": "Policz."}, {"typ": "mysli"}, {"typ": "claude", "tekst": "Policzone."}, {"typ": "kontekst", "procent": 20}, {"typ": "nauczyciel", "tekst": "Procent wzrósł."}]}]
    assert bledy(dane) == []


# --- rytm nauczyciela (narzedzia/czytelnosc.py)


def czytelnosc_bledow(tmp_path, d):
    plik = tmp_path / "scenariusz.json"
    plik.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return czytelnosc.sprawdz_scenariusz(plik, "scenariusz.json")


@pytest.mark.parametrize("nr,id_drogi,indeks", [(1, "tryb", 0), (1, "tryb", 2), (4, "srodowisko", 0)])
def test_po_nowym_kliku_nauczyciel_odzywa_sie_w_dwoch_krokach(tmp_path, dane, nr, id_drogi, indeks):
    assert czytelnosc_bledow(tmp_path, dane) == []
    kroki = droga(dane, nr, id_drogi)["kroki"]
    del kroki[indeks + 1 : indeks + 3]
    kroki.insert(indeks + 1, {"typ": "mysli"})
    kroki.insert(indeks + 2, {"typ": "mysli"})
    assert any("brak nauczyciela" in b for b in czytelnosc_bledow(tmp_path, dane))
