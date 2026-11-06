"""Testy walidatora zadania według harmonogramu w ćwiczeniu z drogami symulatora aplikacji: pole `aplikacja.harmonogram` (nazwa, polecenie, pora, częstotliwość, folder), kliki `scheduled`, `new-task`, `advanced-settings`, `create`, `run-now` z kolejnością wymuszaną przez walidator, wyjątek „droga bez pliku”, rytm nauczyciela i polskie pola w filtrach języka (wzór: tests/dane/harmonogram.json, opis: dane/FORMAT-SCENARIUSZA.md, część „Zadanie według harmonogramu”)."""

import copy
import json
from pathlib import Path

import pytest

from narzedzia import czytelnosc
from narzedzia import scenariusz as sc
from narzedzia import scenariusz_harmonogram as harm
from narzedzia import tekst_pl

KORZEN = Path(__file__).resolve().parent.parent
WZOR = json.loads((Path(__file__).parent / "dane" / "harmonogram.json").read_text(encoding="utf-8"))
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")

# kroki drogi `ustaw-zadanie`: 1 scheduled, 3 new-task, 5 advanced-settings, 7 create, 9 run-now (nauczyciel po każdym)
SCHEDULED, NEW_TASK, ADVANCED, CREATE, RUN_NOW = 1, 3, 5, 7, 9


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def jest(wynik, fragment):
    return any(fragment in b for b in wynik)


def kroki(d):
    return d["cwiczenia"][0]["drogi"][0]["kroki"]


def apl(d):
    return d["cwiczenia"][0]["aplikacja"]


def test_wzor_przechodzi_cala_droga_od_scheduled_do_run_now(dane):
    assert bledy(dane) == []
    assert [k["cel"] for k in kroki(dane) if k["typ"] == "klik"] == list(harm.CELE)


def test_czytelnosc_wzoru_po_kazdym_kliku_stoi_nauczyciel(dane):
    plik = KORZEN / "tests" / "dane" / "harmonogram.json"
    assert czytelnosc.sprawdz_scenariusz(plik, "harmonogram.json") == []


def test_czytelnosc_klik_harmonogramu_bez_nauczyciela_po_nim_to_blad(dane, tmp_path):
    assert kroki(dane)[-1]["typ"] == "nauczyciel"
    kroki(dane).pop()  # run-now zostaje ostatnim krokiem, bez nauczyciela po nim
    plik = tmp_path / "s.json"
    plik.write_text(json.dumps(dane), encoding="utf-8")
    assert jest(czytelnosc.sprawdz_scenariusz(plik, "s.json"), "brak nauczyciela")


@pytest.mark.parametrize("cel", harm.CELE)
def test_klik_bez_pola_harmonogram_to_blad(dane, cel):
    del apl(dane)["harmonogram"]
    kroki(dane)[SCHEDULED]["cel"] = cel
    assert jest(bledy(dane), f"klik {cel} w ćwiczeniu bez aplikacja.harmonogram")


def test_new_task_przed_scheduled_to_blad(dane):
    k = kroki(dane)
    k[SCHEDULED], k[NEW_TASK] = k[NEW_TASK], k[SCHEDULED]
    assert jest(bledy(dane), "klik new-task bez otwartej strony Scheduled tasks")


def test_create_bez_okna_i_run_now_bez_strony_zadania_to_blad(dane):
    k = kroki(dane)
    k[NEW_TASK]["cel"] = "create"  # strona Scheduled tasks otwarta, okna nie ma
    assert jest(bledy(dane), "klik create bez otwartego okna New scheduled task")
    k[NEW_TASK]["cel"] = "run-now"
    assert jest(bledy(dane), "klik run-now bez strony zadania")


def test_advanced_settings_przed_oknem_i_drugi_raz_to_blad(dane):
    k = kroki(dane)
    k[NEW_TASK]["cel"] = "advanced-settings"
    assert jest(bledy(dane), "klik advanced-settings bez otwartego okna")
    k[NEW_TASK]["cel"] = "new-task"
    k.insert(ADVANCED + 2, {"typ": "klik", "cel": "advanced-settings"})
    k.insert(ADVANCED + 3, {"typ": "nauczyciel", "tekst": "Sekcja jest już rozwinięta."})
    assert jest(bledy(dane), "klik advanced-settings drugi raz")


def test_scheduled_i_run_now_drugi_raz_to_blad(dane):
    k = kroki(dane)
    k.insert(CREATE, {"typ": "klik", "cel": "scheduled"})
    k.insert(CREATE + 1, {"typ": "nauczyciel", "tekst": "Znów strona zadań."})
    assert jest(bledy(dane), "klik scheduled poza rozmową albo drugi raz")
    del k[CREATE : CREATE + 2]
    k.extend([{"typ": "klik", "cel": "run-now"}, {"typ": "nauczyciel", "tekst": "Drugi przebieg."}])
    assert jest(bledy(dane), "klik run-now drugi raz")


def test_advanced_settings_mozna_pominac_a_run_now_jest_opcjonalny(dane):
    k = kroki(dane)
    del k[RUN_NOW : RUN_NOW + 2]
    del k[ADVANCED : ADVANCED + 2]
    assert bledy(dane) == []


def test_droga_moze_sie_skonczyc_na_liscie_i_na_oknie_bez_pliku(dane):
    k = kroki(dane)
    del k[CREATE:]
    assert bledy(dane) == []  # kończy się na oknie z rozwiniętą sekcją
    del k[NEW_TASK + 1 :]
    assert bledy(dane) == []  # kończy się na oknie bez rozwiniętej sekcji


@pytest.mark.parametrize("typ", ["pisz", "claude", "mysli", "klik-pierscien"])
def test_przy_stronie_harmonogramu_rozmowa_jest_schowana(dane, typ):
    krok = {"typ": "pisz", "tekst": "Prośba."} if typ == "pisz" else {"typ": "claude", "tekst": "Odpowiedź."} if typ == "claude" else {"typ": "mysli"} if typ == "mysli" else {"typ": "klik", "cel": "pierscien"}
    kroki(dane).insert(SCHEDULED + 2, krok)
    assert jest(bledy(dane), "przy otwartej stronie harmonogramu: rozmowa jest schowana")


def test_pisz_przed_scheduled_jest_dozwolone(dane):
    kroki(dane).insert(0, {"typ": "pisz", "tekst": "Ustaw mi zadanie."})
    assert bledy(dane) == []


def test_komunikat_o_niedozwolonym_kliku_wymienia_cele_harmonogramu(dane):
    kroki(dane)[SCHEDULED]["cel"] = "licznik"
    komunikat = next(b for b in bledy(dane) if "klik „licznik”: w drogach klika się tylko" in b)
    for cel in harm.CELE:
        assert f"„{cel}”" in komunikat, cel
    assert komunikat.endswith("licznika nie ma")


def test_pole_poza_typ_cel_fakt_w_kliku_to_blad(dane):
    kroki(dane)[NEW_TASK]["nazwa"] = "x"
    assert jest(bledy(dane), "pole nazwa nie należy do kliku new-task")


@pytest.mark.parametrize(
    "zmiana, fragment",
    [
        (lambda h: h.pop("nazwa"), "harmonogram.nazwa musi być niepustym napisem"),
        (lambda h: h.update(nazwa="  "), "harmonogram.nazwa musi być niepustym napisem"),
        (lambda h: h.update(polecenie=""), "harmonogram.polecenie musi być niepustym napisem"),
        (lambda h: h.update(nazwa="x" * 81), "harmonogram.nazwa: najwyżej 80 znaków"),
        (lambda h: h.update(polecenie="a\nb"), "harmonogram.polecenie: najwyżej 400 znaków i bez znaków sterujących"),
        (lambda h: h.update(pora="9:20"), "harmonogram.pora musi mieć postać"),
        (lambda h: h.update(pora="24:00"), "harmonogram.pora musi mieć postać"),
        (lambda h: h.update(pora=920), "harmonogram.pora musi mieć postać"),
        (lambda h: h.update(czestotliwosc="Weekly"), "harmonogram.czestotliwosc „Weekly” spoza Daily"),
        (lambda h: h.pop("czestotliwosc"), "harmonogram.czestotliwosc"),
        (lambda h: h.update(folder="a/b"), "harmonogram.folder: sama nazwa folderu"),
        (lambda h: h.update(folder="~/x"), "harmonogram.folder: sama nazwa folderu"),
        (lambda h: h.pop("folder"), "harmonogram.folder: sama nazwa folderu"),
        (lambda h: h.update(model="x"), "pole model nie należy do harmonogramu"),
    ],
)
def test_pole_harmonogram_zle_wartosci_to_blad(dane, zmiana, fragment):
    zmiana(apl(dane)["harmonogram"])
    assert jest(bledy(dane), fragment)


def test_harmonogram_nie_jest_obiektem_to_blad(dane):
    apl(dane)["harmonogram"] = "co rano"
    assert jest(bledy(dane), "harmonogram musi być obiektem")


def test_harmonogram_z_aplikacja_sesje_to_blad(dane):
    apl(dane)["sesje"] = [{"id": "inna", "rozmowa": [{"kto": "ty", "tekst": "Cześć."}]}]
    assert jest(bledy(dane), "harmonogram w ćwiczeniu z aplikacja.sesje")


def test_harmonogram_w_cwiczeniu_z_krokami_to_blad(dane):
    cw = dane["cwiczenia"][0]
    del cw["drogi"]
    cw["kroki"] = []
    cw["aplikacja"]["zmiany"] = []
    assert jest(bledy(dane), "harmonogram tylko w ćwiczeniu z drogami")


@pytest.mark.parametrize("pora, oczekiwane", [("09:20", "9:20 AM"), ("00:05", "12:05 AM"), ("12:00", "12:00 PM"), ("13:45", "1:45 PM"), ("23:59", "11:59 PM")])
def test_godzina_12_zapis_ze_strony_zadania(pora, oczekiwane):
    assert harm.godzina_12(pora) == oczekiwane


def test_napisy_skladane_pasuja_do_wzorow_z_listy_napisow(dane):
    napisy = sc._Napisy(NAPISY)
    h = apl(dane)["harmonogram"]
    assert harm.napisy_skladane(h) == ("Next run: today at 9:20 AM", "Daily at 9:20 AM")
    assert all(napisy.jest(t, "aplikacja") for t in harm.napisy_skladane(h))
    assert not napisy.jest("Next run: tomorrow at 9:20 AM", "aplikacja")


def test_nazwa_i_polecenie_trafiaja_do_filtrow_jezyka_a_pora_folder_i_czestotliwosc_nie(dane):
    pola = dict(tekst_pl.polskie_pola(dane, NAPISY))
    sciezki = [s for s in pola if "harmonogram" in s]
    assert sorted(s.rsplit(".", 1)[1] for s in sciezki) == ["nazwa", "polecenie"]
    assert pola[next(s for s in sciezki if s.endswith(".nazwa"))] == "Poranne nowości o AI"
