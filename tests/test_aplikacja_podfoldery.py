"""Testy walidatora podfolderów w ćwiczeniach aplikacji: nazwy `Podfolder/plik`, `folder_glowny`, ścieżki od folderu rozmowy i od korzenia, pola `czyta_na_start` i `czyta`."""

import copy
import json
from pathlib import Path

import pytest

from narzedzia import scenariusz as sc

KORZEN = Path(__file__).resolve().parent.parent
WZOR = json.loads((Path(__file__).parent / "dane" / "podfoldery.json").read_text(encoding="utf-8"))
FAKTY_ID = sc.wczytaj_id_faktow(KORZEN / "dane" / "fakty.yaml")
NAPISY = sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")


@pytest.fixture
def dane():
    return copy.deepcopy(WZOR)


def bledy(d):
    return sc.sprawdz_scenariusz(d, FAKTY_ID, NAPISY)


def jest(wynik, fragment):
    return any(fragment in b for b in wynik)


def cw(d, i):
    return d["cwiczenia"][i]


def krok_mysli(d, nr_cw, droga, nr):
    return cw(d, nr_cw)["drogi"][droga]["kroki"][nr]


def test_przyklad_przechodzi_a_dwa_mysli_pod_rzad_sa_w_nim(dane):
    assert bledy(dane) == []
    kroki = cw(dane, 1)["drogi"][1]["kroki"]
    assert [k["typ"] for k in kroki[1:3]] == ["mysli", "mysli"] and all("czyta" in k for k in kroki[1:3])


def test_wzor_ma_dwa_rozne_pliki_claude_md_i_dwie_rozmowy(dane):
    assert [p for p in dane["folder_startowy"] if p.endswith("CLAUDE.md")] == [
        "CLAUDE.md", "Pracownia-Lipa/CLAUDE.md", "Kwiaciarnia-Malwa/CLAUDE.md"
    ]
    assert [c["aplikacja"]["folder"] for c in dane["cwiczenia"]] == ["Pracownia-Lipa", "Klienci"]


@pytest.mark.parametrize("nazwa", ["a/b/c.txt", "/c.txt", "a/", "a//b.txt", "a/../b.txt"])
def test_folder_startowy_najwyzej_jeden_ukosnik(dane, nazwa):
    dane["folder_startowy"].append(nazwa)
    assert jest(bledy(dane), "najwyżej jeden /")


def test_folder_startowy_dodatkowe_przyjmuje_podfolder(dane):
    cw(dane, 1)["aplikacja"]["folder_startowy_dodatkowe"] = ["Pracownia-Lipa/notatka.txt"]
    assert bledy(dane) == []


def test_folder_startowy_dodatkowe_przyjmuje_sciezke_z_dwoma_ukosnikami(dane):
    cw(dane, 1)["aplikacja"]["folder_startowy_dodatkowe"] = ["a/b/notatka.txt"]
    assert bledy(dane) == []


@pytest.mark.parametrize("nazwa", ["a//b.txt", "/a.txt", "a/", "a/../b.txt"])
def test_folder_startowy_dodatkowe_zepsuta_sciezka_odrzucona(dane, nazwa):
    cw(dane, 1)["aplikacja"]["folder_startowy_dodatkowe"] = [nazwa]
    assert jest(bledy(dane), "cw2/aplikacja/folder_startowy_dodatkowe[0]: plik dodatkowy wymaga ścieżki")


def test_nowe_pliki_przyjmuje_podfolder(dane):
    cw(dane, 0)["nowe_pliki"] = ["Podfolder/post.txt"]
    odpowiedz_z_plikiem(dane, 0, "Podfolder/post.txt")
    assert bledy(dane) == []


def test_wyjscie_nad_folder_w_nowe_pliki_jest_bledem(dane):
    cw(dane, 0)["nowe_pliki"] = ["post-premiera.txt", "../post.txt"]
    assert jest(bledy(dane), "cw1/nowe_pliki[1]: nowy plik wymaga ścieżki od folderu rozmowy")


def test_folder_glowny_to_sama_nazwa(dane):
    dane["folder_glowny"] = "Klienci/Lipa"
    assert jest(bledy(dane), "folder_glowny to sama nazwa korzenia")


@pytest.mark.parametrize("folder", ["Kwiaciarnia", "Pracownia-Lipa/CLAUDE.md", "Inny"])
def test_folder_rozmowy_to_korzen_albo_teczka(dane, folder):
    cw(dane, 0)["aplikacja"]["folder"] = folder
    assert jest(bledy(dane), "musi być korzeniem podglądu")


def test_folder_rozmowy_moze_byc_druga_teczka(dane):
    cw(dane, 0)["aplikacja"]["folder"] = "Kwiaciarnia-Malwa"
    assert not jest(bledy(dane), "musi być korzeniem")
    # plik klientki leży w innej teczce, więc od folderu rozmowy w kwiaciarni nie ma nazwy „premiera-kolekcji.txt”
    odpowiedz_z_plikiem(dane, 0, "premiera-kolekcji.txt")
    assert jest(bledy(dane), "plik „premiera-kolekcji.txt” nie istnieje")


def test_nowy_plik_liczy_sie_od_folderu_rozmowy(dane):
    # w cw1 (teczka Pracownia-Lipa) CLAUDE.md to plik klientki, więc nowy plik o tej nazwie koliduje
    cw(dane, 0)["nowe_pliki"] = ["post-premiera.txt", "CLAUDE.md"]
    assert jest(bledy(dane), "nowy plik „CLAUDE.md” już jest w folder_startowy")
    # w cw2 (korzeń) taka sama nazwa jest już plikiem wspólnym, ale „Pracownia-Lipa/CLAUDE.md” nie jest nową nazwą z /
    cw(dane, 0)["nowe_pliki"] = ["post-premiera.txt"]
    cw(dane, 1)["nowe_pliki"] = ["CLAUDE.md", "post-lipa.txt"]
    assert jest(bledy(dane), "nowy plik „CLAUDE.md” już jest w folder_startowy")


def odpowiedz_z_plikiem(d, nr_cw, plik, **pola):
    """Ustawia w pierwszej drodze ćwiczenia plik odpowiedzi Claude (z tekstem i otwartym plikiem) i zwraca krok `claude`."""
    kroki = cw(d, nr_cw)["drogi"][0]["kroki"]
    claude = next(k for k in kroki if k["typ"] == "claude")
    claude.update(plik=plik, tekst=f"Zajrzałem do pliku {plik}.", **pola)
    next(k for k in kroki if k["typ"] == "plik")["nazwa"] = plik
    return claude


def test_plik_odpowiedzi_liczy_sie_od_folderu_rozmowy(dane):
    # cw1: rozmowa w teczce, więc CLAUDE.md to plik klientki; cw2: korzeń, więc plik z teczki wymaga ścieżki z teczką
    odpowiedz_z_plikiem(dane, 0, "CLAUDE.md")
    assert not jest(bledy(dane), "nie istnieje w folder_startowy")
    odpowiedz_z_plikiem(dane, 1, "premiera-kolekcji.txt")
    assert jest(bledy(dane), "plik „premiera-kolekcji.txt” nie istnieje")
    odpowiedz_z_plikiem(dane, 1, "Pracownia-Lipa/premiera-kolekcji.txt")
    assert not jest(bledy(dane), "nie istnieje w folder_startowy")


def test_czyta_liczy_sie_od_korzenia(dane):
    # w cw2 ścieżka od folderu rozmowy (korzenia) to samo, ale w cw1 „premiera-kolekcji.txt” (od teczki) nie jest ścieżką od korzenia
    krok = krok_mysli(dane, 0, 0, 1)
    krok["czyta"] = ["premiera-kolekcji.txt"]
    assert jest(bledy(dane), "ścieżka „premiera-kolekcji.txt” (od korzenia podglądu) nie wskazuje pliku")
    krok["czyta"] = ["Pracownia-Lipa/premiera-kolekcji.txt", "CLAUDE.md"]
    assert bledy(dane) == []


@pytest.mark.parametrize("czyta", [[], "CLAUDE.md", [""], [5], ["a/b/c.txt"], ["Nie-ma/pliku.txt"]])
def test_czyta_zle_wartosci(dane, czyta):
    krok_mysli(dane, 1, 1, 1)["czyta"] = czyta
    assert bledy(dane) != []


def test_czyta_tylko_w_kroku_mysli(dane):
    krok_mysli(dane, 1, 1, 0)["czyta"] = ["CLAUDE.md"]
    assert jest(bledy(dane), "pole czyta tylko w kroku mysli")


def test_czyta_plik_dopiero_po_utworzeniu(dane):
    # post-lipa.txt powstaje w kroku 3 drogi z-plikiem; przed nim nie leży w folderze
    kroki = cw(dane, 1)["drogi"][1]["kroki"]
    kroki[1]["czyta"] = ["post-lipa.txt"]
    assert jest(bledy(dane), "ścieżka „post-lipa.txt” (od korzenia podglądu) nie wskazuje pliku, który w tym miejscu drogi leży")
    kroki[1]["czyta"] = ["Pracownia-Lipa/premiera-kolekcji.txt"]
    kroki.insert(5, {"typ": "mysli", "czyta": ["post-lipa.txt"]})
    assert bledy(dane) == []


def test_czyta_na_start_wskazuje_plik_z_folderu(dane):
    cw(dane, 0)["aplikacja"]["czyta_na_start"] = ["Pracownia-Lipa/CLAUDE.md", "Pracownia-Lipa/brak.txt"]
    assert jest(bledy(dane), "czyta_na_start[1]: ścieżka „Pracownia-Lipa/brak.txt”")


def test_czyta_na_start_plik_ktory_dopiero_powstanie_odrzucony(dane):
    cw(dane, 1)["aplikacja"]["czyta_na_start"] = ["post-lipa.txt"]
    assert jest(bledy(dane), "nie wskazuje pliku, który leży w folderze od startu")


@pytest.mark.parametrize("wartosc", [[], "CLAUDE.md", [""]])
def test_czyta_na_start_zle_wartosci(dane, wartosc):
    cw(dane, 0)["aplikacja"]["czyta_na_start"] = wartosc
    assert bledy(dane) != []


def test_czyta_na_start_tylko_w_cwiczeniu_z_drogami():
    dane = json.loads((Path(__file__).parent / "dane" / "aplikacja.json").read_text(encoding="utf-8"))
    assert bledy(dane) == []
    dane["cwiczenia"][0]["aplikacja"]["czyta_na_start"] = [dane["folder_startowy"][0]]
    assert jest(bledy(dane), "czyta_na_start tylko w ćwiczeniu z drogami")


def test_bez_zmiany_liczy_sie_od_folderu_rozmowy(dane):
    # w cw1 pliki z teczki mają nazwy bez teczki; plik wspólny nad folderem rozmowy takiej nazwy nie ma
    odpowiedz_z_plikiem(dane, 0, "premiera-kolekcji.txt", bez_zmiany=True)
    assert not jest(bledy(dane), "tylko dla pliku z folderu")
    odpowiedz_z_plikiem(dane, 0, "post-premiera.txt", bez_zmiany=True)
    assert jest(bledy(dane), "tylko dla pliku z folderu")


def test_bez_zmiany_w_korzeniu_wymaga_sciezki_z_teczka(dane):
    odpowiedz_z_plikiem(dane, 1, "premiera-kolekcji.txt", bez_zmiany=True)
    assert jest(bledy(dane), "tylko dla pliku z folderu")
    odpowiedz_z_plikiem(dane, 1, "Pracownia-Lipa/premiera-kolekcji.txt", bez_zmiany=True)
    assert not jest(bledy(dane), "tylko dla pliku z folderu")


def test_teczki_w_folder_startowy_wymagaja_folder_glowny(dane):
    del dane["folder_glowny"]
    wynik = bledy(dane)
    assert jest(wynik, "teczki w folder_startowy") and jest(wynik, "wymagają folder_glowny")
    # błąd w każdym ćwiczeniu aplikacji, bo każde rysuje podgląd
    assert jest(wynik, "cw1/aplikacja") and jest(wynik, "cw2/aplikacja")


def test_teczka_tylko_w_dodatkowych_tez_wymaga_folder_glowny():
    dane = json.loads((Path(__file__).parent / "dane" / "aplikacja-folder-dodatkowe.json").read_text(encoding="utf-8"))
    assert bledy(dane) == []
    dane["cwiczenia"][1]["aplikacja"]["folder_startowy_dodatkowe"].append("Podfolder/notatka.txt")
    assert jest(bledy(dane), "wymagają folder_glowny")
    dane["folder_glowny"] = "Firma-szkolenia"
    assert not jest(bledy(dane), "wymagają folder_glowny")


def test_plaski_folder_bez_folder_glowny_dalej_przechodzi():
    dane = json.loads((Path(__file__).parent / "dane" / "aplikacja-drogi.json").read_text(encoding="utf-8"))
    assert bledy(dane) == []
