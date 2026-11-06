"""Testy walidatora ekranów ze zrzutów Łukasza z 27.10.2026 (paczka 4, wzór: tests/dane/aplikacja-plik-ekrany.json): pole `karta_pliku` kroku `claude`, kliki `plik-menu`, `plik-karta-menu`, `plik-karta-pozycja` i `ikona-tytulu`, kolejność kroków przy otwartym menu, droga bez pliku, rytm nauczyciela i brak podglądu w tekście lekcji."""

import copy
import json
from pathlib import Path

import pytest
import yaml

from narzedzia import czytelnosc, scenariusz as sc
from narzedzia.strona_podglad import _bez_obrazu

KORZEN = Path(__file__).resolve().parent.parent
NAPISY = sc._Napisy(sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml"))
FAKTY_ID = {w["id"] for w in yaml.safe_load((KORZEN / "dane" / "fakty.yaml").read_text(encoding="utf-8"))["fakty"]}
SCIEZKA_WZORU = Path(__file__).parent / "dane" / "aplikacja-plik-ekrany.json"
WZOR = json.loads(SCIEZKA_WZORU.read_text(encoding="utf-8"))


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def cw(d, nr):
    return next(c for c in d["cwiczenia"] if c["id"] == f"cw{nr}")


def droga(d, nr, id_drogi):
    return next(x for x in cw(d, nr)["drogi"] if x["id"] == id_drogi)


def zawiera(lista, fragment):
    return any(fragment in b for b in lista)


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


def test_wzor_bez_bledow(dane):
    assert bledy(dane) == []


# --- karta_pliku


def odpowiedz(dane):
    return next(k for k in droga(dane, 2, "karta")["kroki"] if k["typ"] == "claude")


@pytest.mark.parametrize("rozmiar", [1, 72, 999])
def test_rozmiar_karty_z_zakresu_przechodzi(dane, rozmiar):
    odpowiedz(dane)["karta_pliku"] = {"rozmiar": rozmiar}
    assert bledy(dane) == []


@pytest.mark.parametrize("rozmiar", [0, -3, 1000, 7.5, "72", True, None])
def test_rozmiar_karty_poza_zakresem_albo_nie_liczba_to_blad(dane, rozmiar):
    odpowiedz(dane)["karta_pliku"] = {"rozmiar": rozmiar}
    assert zawiera(bledy(dane), "karta_pliku.rozmiar")


@pytest.mark.parametrize("karta", [{}, {"rozmiar": 72, "rodzaj": "TXT"}, {"rozmiar": 72, "nazwa": "x"}, True, 72, "72B"])
def test_karta_z_innymi_polami_niz_rozmiar_to_blad(dane, karta):
    odpowiedz(dane)["karta_pliku"] = karta
    assert zawiera(bledy(dane), "karta_pliku musi być obiektem z jednym polem rozmiar")


def test_karta_bez_pliku_to_blad(dane):
    k = odpowiedz(dane)
    del k["plik"]
    assert zawiera(bledy(dane), "karta_pliku bez pola plik")


@pytest.mark.parametrize("nazwa", ["info.csv", "info.html", "info.md", "info"])
def test_karta_przy_pliku_innym_niz_txt_to_blad(dane, nazwa):
    """Zrzut pokazuje znaczek „TXT” i tylko jego: znaczków innych rodzajów nie wymyślamy."""
    for c in dane["cwiczenia"][:2]:
        c["nowe_pliki"] = [nazwa]
        for d in c["drogi"]:
            for k in d["kroki"]:
                if k.get("plik") == "info.txt":
                    k["plik"], k["tekst"] = nazwa, k["tekst"].replace("info.txt", nazwa)
                if k.get("nazwa") == "info.txt":
                    k["nazwa"] = nazwa
    assert zawiera(bledy(dane), "zrzut pokazuje tylko znaczek „TXT” przy plikach .txt")


def test_karta_w_cwiczeniu_z_sesjami_to_blad(dane):
    cw(dane, 2)["aplikacja"]["sesje"] = [{"id": "s1", "rozmowa": [{"kto": "ty", "tekst": "Inna rozmowa."}, {"kto": "claude", "tekst": "Odpowiedź."}]}]
    assert zawiera(bledy(dane), "w ćwiczeniu z aplikacja.sesje")


# --- plik-menu


def test_plik_menu_bez_otwartego_pliku_to_blad(dane):
    kroki = droga(dane, 1, "menu")["kroki"]
    i = next(i for i, k in enumerate(kroki) if k["typ"] == "plik")
    del kroki[i - 1 : i + 1]  # bez kliku w ścieżkę i bez kroku plik
    assert zawiera(bledy(dane), "klik „plik-menu” bez otwartego pliku")


def test_plik_menu_po_stronie_albo_artefakcie_w_panelu_to_blad(dane):
    """Strona oferty i artefakt zajmują miejsce pliku w panelu, więc „…” panelu pliku nie ma."""
    kroki = droga(dane, 1, "menu")["kroki"]
    i = next(i for i, k in enumerate(kroki) if k["typ"] == "plik")
    kroki[i] = {"typ": "plik", "nazwa": "info.txt", "strona": {"tytul": "A", "opis": "B", "program": ["a", "b", "c"], "cena": "1 zł", "opinie": ["ok"], "kontakt": "x"}}
    assert zawiera(bledy(dane), "klik „plik-menu” bez otwartego pliku")


def test_po_otwarciu_menu_panelu_dalej_tylko_nauczyciel(dane):
    kroki = droga(dane, 1, "menu")["kroki"]
    kroki.append({"typ": "mysli"})
    assert zawiera(bledy(dane), "krok mysli po otwarciu menu „…” panelu pliku: dalej tylko nauczyciel")


def test_po_otwarciu_menu_panelu_nauczyciel_moze_mowic_dalej(dane):
    kroki = droga(dane, 1, "menu")["kroki"]
    kroki.append({"typ": "nauczyciel", "tekst": "Pozycje menu niczego nie zmieniają."})
    assert bledy(dane) == []


def test_klik_plik_menu_z_obcym_polem_to_blad(dane):
    k = next(k for k in droga(dane, 1, "menu")["kroki"] if k.get("cel") == "plik-menu")
    k["pozycja"] = "Auto save"
    assert zawiera(bledy(dane), "pole pozycja nie należy do kliku plik-menu")


# --- plik-karta-menu i plik-karta-pozycja


def test_menu_karty_bez_karty_w_rozmowie_to_blad(dane):
    del odpowiedz(dane)["karta_pliku"]
    assert zawiera(bledy(dane), "klik „plik-karta-menu” bez karty pliku w rozmowie")


@pytest.mark.parametrize("pozycja", ["Attach as context", "Copy", "Open in", "Show in Finder"])
def test_kazda_pozycja_menu_karty_przechodzi(dane, pozycja):
    k = next(k for k in droga(dane, 2, "karta")["kroki"] if k.get("cel") == "plik-karta-pozycja")
    k["pozycja"] = pozycja
    assert bledy(dane) == []


@pytest.mark.parametrize("pozycja", ["Reveal in Finder", "Auto save", "Show session rail", "", None, 3])
def test_pozycja_spoza_menu_karty_to_blad(dane, pozycja):
    k = next(k for k in droga(dane, 2, "karta")["kroki"] if k.get("cel") == "plik-karta-pozycja")
    k["pozycja"] = pozycja
    assert zawiera(bledy(dane), "pozycja ")


def test_pozycja_bez_otwartego_menu_karty_to_blad(dane):
    kroki = droga(dane, 2, "karta")["kroki"]
    del kroki[next(i for i, k in enumerate(kroki) if k.get("cel") == "plik-karta-menu")]
    assert zawiera(bledy(dane), "klik „plik-karta-pozycja” bez otwartego menu karty")


def test_przy_menu_karty_dalej_tylko_nauczyciel_i_pozycja(dane):
    kroki = droga(dane, 2, "karta")["kroki"]
    i = next(i for i, k in enumerate(kroki) if k.get("cel") == "plik-karta-menu")
    kroki.insert(i + 1, {"typ": "claude", "tekst": "Jeszcze jedno."})
    assert zawiera(bledy(dane), "krok claude przy otwartym menu prawego kliku na karcie pliku")


def test_menu_karty_otwarte_na_koncu_drogi_przechodzi(dane):
    """Droga „samo-menu” kończy się otwartym menu karty, bez kroku plik, artefakt ani strona."""
    assert droga(dane, 2, "samo-menu")["kroki"][-2]["cel"] == "plik-karta-menu"
    assert bledy(dane) == []


def test_klik_menu_karty_z_polem_pozycja_to_blad(dane):
    k = next(k for k in droga(dane, 2, "karta")["kroki"] if k.get("cel") == "plik-karta-menu")
    k["pozycja"] = "Copy"
    assert zawiera(bledy(dane), "pole pozycja nie należy do kliku plik-karta-menu")


# --- ikona-tytulu


def ikona(dane):
    return next(k for k in droga(dane, 3, "dymek")["kroki"] if k.get("cel") == "ikona-tytulu")


@pytest.mark.parametrize("nr", [2, 3, 6, 0, -1, 1.0, "1", True, None])
def test_dymek_innej_ikony_niz_pierwsza_to_blad(dane, nr):
    """Zrzut 15-28-18 pokazuje dymek tylko pod pierwszą ikoną: dymków pozostałych nie wymyślamy."""
    ikona(dane)["nr"] = nr
    assert zawiera(bledy(dane), "ikona-tytulu: nr musi być numerem ikony z dymkiem na zrzucie")


def test_dymek_bez_numeru_ikony_to_blad(dane):
    del ikona(dane)["nr"]
    assert zawiera(bledy(dane), "ikona-tytulu: nr musi być")


def test_dymek_z_obcym_polem_to_blad(dane):
    ikona(dane)["napis"] = "Terminal"
    assert zawiera(bledy(dane), "pole napis nie należy do kliku ikona-tytulu")


def test_ikona_w_cwiczeniu_z_sesjami_to_blad(dane):
    cw(dane, 3)["aplikacja"]["sesje"] = [{"id": "s1", "rozmowa": [{"kto": "ty", "tekst": "Inna rozmowa."}, {"kto": "claude", "tekst": "Odpowiedź."}]}]
    assert zawiera(bledy(dane), "klik ikona-tytulu w ćwiczeniu z aplikacja.sesje")


def test_droga_z_samym_dymkiem_przechodzi_bez_pliku(dane):
    assert [k["typ"] for k in droga(dane, 3, "dymek")["kroki"]] == ["nauczyciel", "klik", "nauczyciel"]
    assert bledy(dane) == []


def test_droga_bez_pliku_i_bez_celu_z_paczki_dalej_jest_bledem(dane):
    kroki = droga(dane, 3, "dymek")["kroki"]
    del kroki[1:]
    assert zawiera(bledy(dane), "droga bez kroku plik ani artefakt (ani strona)")


# --- rytm nauczyciela i podgląd w lekcji


@pytest.mark.parametrize("cel", ["plik-menu", "plik-karta-menu", "plik-karta-pozycja", "ikona-tytulu"])
def test_po_kliku_nauczyciel_odzywa_sie_najdalej_dwa_kroki_dalej(dane, tmp_path, cel):
    plik = tmp_path / "scenariusz.json"
    plik.write_text(json.dumps(dane, ensure_ascii=False), encoding="utf-8")
    assert czytelnosc.sprawdz_scenariusz(plik, "x") == []
    for c in dane["cwiczenia"]:
        for d in c["drogi"]:
            kroki = d["kroki"]
            for i, k in enumerate(kroki):
                if k.get("cel") == cel:
                    kroki[i + 1 :] = [x for x in kroki[i + 1 :] if x["typ"] != "nauczyciel"]
    plik.write_text(json.dumps(dane, ensure_ascii=False), encoding="utf-8")
    assert any("brak nauczyciela" in b for b in czytelnosc.sprawdz_scenariusz(plik, "x")), cel


@pytest.mark.parametrize("cw_id, id_drogi", [("cw2", "karta"), ("cw2", "samo-menu"), ("cw3", "dymek")])
def test_podglad_drogi_bez_pliku_to_blad_skladania(dane, cw_id, id_drogi):
    """Droga kończąca się menu karty albo dymkiem nie ma kroku plik, artefakt ani strona: podgląd w tekście lekcji nie ma czego pokazać."""
    with pytest.raises(ValueError, match="podgląd nie ma czego pokazać"):
        _bez_obrazu(dane, cw_id, id_drogi)


def test_podglad_drogi_z_plik_menu_pokazuje_plik(dane):
    _bez_obrazu(dane, "cw1", "menu")  # nie rzuca: droga ma krok plik
