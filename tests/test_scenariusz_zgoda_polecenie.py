"""Testy walidatora kroku `zgoda` w drodze symulatora aplikacji: wariant z polem `polecenie` (karta zgody na polecenie terminala, np. `zip` w Accept edits) i pole `odliczanie_ms` (wzór: tests/dane/hook-zgoda-polecenie.json)."""

import copy
import json
from pathlib import Path

import pytest

from narzedzia import scenariusz as sc

KORZEN = Path(__file__).resolve().parent.parent
WZOR = json.loads((Path(__file__).parent / "dane" / "hook-zgoda-polecenie.json").read_text(encoding="utf-8"))
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")
FAKT = "accept-edits-aplikacja-pyta-o-inne-polecenia"
ZGODA = 7  # indeks kroku `zgoda` z poleceniem w drodze `pakuj`
ODPOWIEDZ_ZIP = 6  # odpowiedź Claude, która nazywa polecenie
ZATWIERDZ = 9  # klik `zatwierdz`


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def jest(wynik, fragment):
    return any(fragment in b for b in wynik)


def kroki(d, droga=0):
    return d["cwiczenia"][0]["drogi"][droga]["kroki"]


def zgoda(d):
    return kroki(d)[ZGODA]


def test_wzor_przechodzi_polecenie_z_odliczaniem_i_karta_folder_chroniony(dane):
    assert bledy(dane) == []
    assert zgoda(dane)["polecenie"] == "zip" and zgoda(dane)["odliczanie_ms"] == 6000
    assert "plik" not in zgoda(dane)
    assert kroki(dane, 1)[3]["plik"] == ".claude/settings.json" and "odliczanie_ms" not in kroki(dane, 1)[3]


@pytest.mark.parametrize("polecenie", ["mkdir", "touch", "rm", "rmdir", "mv", "cp", "sed"])
def test_accept_edits_polecenie_z_listy_samodzielnych_odrzucone(dane, polecenie):
    zgoda(dane)["polecenie"] = polecenie
    kroki(dane)[ODPOWIEDZ_ZIP]["tekst"] = f"Użyję polecenia {polecenie}."
    wynik = bledy(dane)
    assert jest(wynik, f"Accept edits sam zatwierdza polecenie {polecenie}, karta byłaby fałszem")
    assert jest(wynik, "accept-edits-polecenia-na-plikach")


def test_manual_przyjmuje_polecenie_z_listy_samodzielnych(dane):
    dane["cwiczenia"][0]["aplikacja"]["tryb"] = "Manual"
    zgoda(dane)["polecenie"] = "mkdir"
    kroki(dane)[ODPOWIEDZ_ZIP]["tekst"] = "Utworzę folder poleceniem mkdir."
    assert bledy(dane) == []


@pytest.mark.parametrize("tryb", ["Plan", "Auto"])
def test_inne_tryby_odrzucone_takze_dla_polecenia(dane, tryb):
    dane["cwiczenia"][0]["aplikacja"]["tryb"] = tryb
    assert jest(bledy(dane), "karta zgody w drodze tylko w trybie Manual albo Accept edits")


def test_oba_pola_plik_i_polecenie_odrzucone(dane):
    zgoda(dane)["plik"] = ".claude/settings.json"
    assert jest(bledy(dane), "krok zgoda ma pole plik albo polecenie")


def test_zadne_z_pol_plik_i_polecenie_odrzucone(dane):
    del zgoda(dane)["polecenie"]
    assert jest(bledy(dane), "krok zgoda ma pole plik albo polecenie")


@pytest.mark.parametrize("polecenie", ["", " ", "zip -r paczka.zip", "zip\t", 5, None, ["zip"]])
def test_polecenie_musi_byc_niepustym_napisem_bez_spacji(dane, polecenie):
    zgoda(dane)["polecenie"] = polecenie
    assert jest(bledy(dane), "pole polecenie to nazwa polecenia")


def test_polecenie_musi_paść_w_najblizszej_wczesniejszej_odpowiedzi_claude(dane):
    kroki(dane)[ODPOWIEDZ_ZIP]["tekst"] = "Do spakowania potrzebuję innego polecenia."
    wynik = bledy(dane)
    assert jest(wynik, "polecenie „zip” nie występuje w tekście najbliższej wcześniejszej odpowiedzi Claude")
    assert jest(wynik, "karta go nie pokazuje")


def test_wystarczy_odpowiedz_najblizsza_a_nie_wczesniejsza(dane):
    kroki(dane).insert(ODPOWIEDZ_ZIP + 1, {"typ": "claude", "tekst": "Zaraz zapytam o zgodę."})  # zip padł tylko w starszej odpowiedzi
    assert jest(bledy(dane), "nie występuje w tekście najbliższej wcześniejszej odpowiedzi Claude")


@pytest.mark.parametrize("tekst", ["Użyję polecenia unzip.", "Użyję polecenia zipcloak.", "Użyję polecenia zip_all."])
def test_nazwa_polecenia_to_cale_slowo(dane, tekst):
    kroki(dane)[ODPOWIEDZ_ZIP]["tekst"] = tekst
    assert jest(bledy(dane), "nie występuje w tekście najbliższej wcześniejszej odpowiedzi Claude")


@pytest.mark.parametrize("tekst", ["zip pakuje pliki.", "Użyję `zip`, żeby spakować.", "Polecenie: zip."])
def test_nazwa_polecenia_w_roznych_miejscach_zdania(dane, tekst):
    kroki(dane)[ODPOWIEDZ_ZIP]["tekst"] = tekst
    assert bledy(dane) == []


def test_polecenie_bez_wczesniejszej_odpowiedzi_claude(dane):
    d = dane["cwiczenia"][0]["drogi"][0]
    d["kroki"] = [d["kroki"][0], d["kroki"][ZGODA], *d["kroki"][ZGODA + 1 :]]
    assert jest(bledy(dane), "zgoda na polecenie „zip” bez wcześniejszej odpowiedzi Claude")


def test_linijki_w_karcie_polecenia_odrzucone(dane):
    zgoda(dane)["linijki"] = [{"tekst": "zip", "zmiana": "dodana"}]
    assert jest(bledy(dane), "karta zgody w drodze nie ma linijek")


def test_obce_pole_karty_polecenia_odrzucone(dane):
    zgoda(dane)["komenda"] = "zip -r"
    assert jest(bledy(dane), "pole komenda nie należy do kroku zgoda")


@pytest.mark.parametrize("krok", [
    {"typ": "pisz", "tekst": "Jeszcze coś."},
    {"typ": "mysli"},
    {"typ": "claude", "tekst": "Spakowane."},
    {"typ": "klik", "cel": "sciezka"},
])
def test_po_karcie_polecenia_tylko_nauczyciel_albo_klik_zatwierdz(dane, krok):
    kroki(dane).insert(ZGODA + 1, krok)
    assert jest(bledy(dane), "przy karcie zgody, która czeka")


def test_nauczyciel_po_karcie_polecenia_jest_dozwolony(dane):
    kroki(dane).insert(ZGODA + 1, {"typ": "nauczyciel", "tekst": "Jeszcze jedno zdanie."})
    assert bledy(dane) == []


@pytest.mark.parametrize("krok", [
    {"typ": "pisz", "tekst": "Dalej."},
    {"typ": "klik", "cel": "sciezka"},
    {"typ": "plik", "nazwa": "wnioski-pazdziernik.txt", "linijki": ["x"]},
    {"typ": "zgoda", "polecenie": "zip"},
])
def test_po_zatwierdzeniu_polecenia_inny_krok_niz_claude_odrzucony(dane, krok):
    kroki(dane).insert(ZATWIERDZ + 1, krok)
    assert jest(bledy(dane), "po zatwierdzeniu polecenia: najpierw odpowiedź Claude")


@pytest.mark.parametrize("krok", [{"typ": "nauczyciel", "tekst": "Pakowanie trwa."}, {"typ": "mysli"}])
def test_po_zatwierdzeniu_polecenia_nauczyciel_i_mysli_przechodza(dane, krok):
    kroki(dane).insert(ZATWIERDZ + 1, krok)
    assert bledy(dane) == []


def test_odpowiedz_po_poleceniu_ma_pole_plik_nieobowiazkowe(dane):
    assert "plik" not in kroki(dane)[ZATWIERDZ + 1]  # wzór: bez pola plik
    kroki(dane)[ZATWIERDZ + 1].update({"plik": "wnioski-pazdziernik.txt", "tekst": "Spakowałem wnioski-pazdziernik.txt do zip."})
    assert bledy(dane) == []


def test_droga_konczy_sie_karta_polecenia_ktora_czeka(dane):
    d = dane["cwiczenia"][0]["drogi"][0]
    d["kroki"] = d["kroki"][: ZGODA + 1]
    assert jest(bledy(dane), "droga kończy się kartą zgody, która czeka na decyzję")


def test_droga_konczy_sie_zatwierdzeniem_polecenia_bez_odpowiedzi(dane):
    d = dane["cwiczenia"][0]["drogi"][0]
    d["kroki"] = d["kroki"][: ZATWIERDZ + 1]
    assert jest(bledy(dane), "po zatwierdzeniu polecenia „zip” droga nie ma odpowiedzi Claude")


def test_klik_zatwierdz_bez_karty_nadal_odrzucony(dane):
    del kroki(dane)[ZGODA]
    assert jest(bledy(dane), "klik zatwierdz bez karty zgody, która czeka na decyzję")


def test_podglad_folderu_nie_zalezy_od_polecenia_paczka_nie_jest_plikiem_scenariusza(dane):
    assert not any(k.get("plik") == "opinie-pazdziernik.zip" for k in kroki(dane))
    kroki(dane)[ZATWIERDZ + 1].update({"plik": "opinie-pazdziernik.zip", "tekst": "Spakowałem do opinie-pazdziernik.zip."})
    assert jest(bledy(dane), "plik „opinie-pazdziernik.zip” nie istnieje w folder_startowy ani w nowe_pliki")


# odliczanie_ms


@pytest.mark.parametrize("ms", [1000, 1001, 2500, 6000, 10000])
def test_odliczanie_w_zakresie_przechodzi(dane, ms):
    zgoda(dane)["odliczanie_ms"] = ms
    assert bledy(dane) == []


@pytest.mark.parametrize("ms", [0, 500, 999, 10001, 60000, -6000, 6000.0, 6000.5, "6000", True, None, [6000]])
def test_odliczanie_poza_zakresem_albo_nie_calkowite_odrzucone(dane, ms):
    zgoda(dane)["odliczanie_ms"] = ms
    assert jest(bledy(dane), "odliczanie_ms musi być liczbą całkowitą od 1000 do 10000")


def test_odliczanie_500_komunikat(dane):
    zgoda(dane)["odliczanie_ms"] = 500
    assert any("odliczanie_ms musi być liczbą całkowitą od 1000 do 10000 (milisekundy), jest 500" in b for b in bledy(dane))


@pytest.mark.parametrize("fakt", ["", "  ", None, 5])
def test_odliczanie_wymaga_pola_fakt(dane, fakt):
    if fakt is None:
        del zgoda(dane)["fakt"]
    else:
        zgoda(dane)["fakt"] = fakt
    assert jest(bledy(dane), "odliczanie_ms wymaga pola fakt")


def test_odliczanie_z_nieistniejacym_faktem_odrzucone(dane):
    zgoda(dane)["fakt"] = "fakt-ktorego-nie-ma"
    assert jest(bledy(dane), "fakt-ktorego-nie-ma")


@pytest.mark.parametrize("indeks", [0, 1, 2, 5, 9, 11])
def test_odliczanie_poza_krokiem_zgoda_odrzucone(dane, indeks):
    kroki(dane)[indeks]["odliczanie_ms"] = 3000
    assert jest(bledy(dane), "pole odliczanie_ms należy tylko do kroku zgoda")


def test_odliczanie_przy_karcie_folder_chroniony_przechodzi(dane):
    kroki(dane, 1)[3].update({"odliczanie_ms": 3000})
    assert bledy(dane) == []  # fakt kroku (sciezki-chronione-czym-sa) już w wzorze
    del kroki(dane, 1)[3]["fakt"]
    assert jest(bledy(dane), "odliczanie_ms wymaga pola fakt")


ETAPY = json.loads((Path(__file__).parent / "dane" / "okno-zgody-tryby.json").read_text(encoding="utf-8"))
TRYBY_DROGI = json.loads((Path(__file__).parent / "dane" / "tryby-drogi.json").read_text(encoding="utf-8"))
KOMUNIKAT_ETAPY = "odliczanie_ms działa tylko w karcie zgody w drogach"


def test_wzory_etapow_przechodza_bez_odliczania():
    assert bledy(copy.deepcopy(ETAPY)) == [] and bledy(copy.deepcopy(TRYBY_DROGI)) == []


def test_odliczanie_w_karcie_zgody_etapow_odrzucone():
    d = copy.deepcopy(ETAPY)
    zgoda_etapu = next(k for e in d["cwiczenia"][0]["etapy"] for k in e["kroki"] if k["typ"] == "zgoda")
    zgoda_etapu["odliczanie_ms"] = 6000
    wynik = bledy(d)
    assert jest(wynik, KOMUNIKAT_ETAPY) and jest(wynik, "etapy[0]/kroki[3]")


def test_odliczanie_w_krokach_etapu_drogi_etapow_odrzucone():
    d = copy.deepcopy(TRYBY_DROGI)
    d["cwiczenia"][0]["etapy"][0]["etapy"][0]["kroki"][0]["odliczanie_ms"] = 3000  # pierwszy krok pierwszego etapu pierwszej drogi etapów
    assert jest(bledy(d), KOMUNIKAT_ETAPY)


def test_odliczanie_w_krokach_przycisku_karty_planu_odrzucone():
    d = json.loads((Path(__file__).parent / "dane" / "plan-przyciski.json").read_text(encoding="utf-8"))
    assert bledy(copy.deepcopy(d)) == []
    plan = next(k for e in d["cwiczenia"][0]["etapy"] for w in e["etapy"] for k in w["kroki"] if k["typ"] == "plan")
    plan["przyciski"]["accept"]["kroki"].append({"typ": "mysli", "odliczanie_ms": 3000})
    assert jest(bledy(d), KOMUNIKAT_ETAPY)


def test_karta_bez_odliczania_nie_wymaga_faktu(dane):
    del zgoda(dane)["odliczanie_ms"]
    del zgoda(dane)["fakt"]
    assert bledy(dane) == []
