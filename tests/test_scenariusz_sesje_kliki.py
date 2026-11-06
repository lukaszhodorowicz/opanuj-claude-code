"""Testy walidatora paska bocznego z rozmowami, część 2: kroki `klik` z celami `nowa-rozmowa`, `sesja`, `menu-sesji`, `archive`, `group-and-sort`, `view-all` i `archived`, kolejność wokół menu i widoku listy, wyjątek od reguły „droga kończy się plikiem” (wzór: tests/dane/aplikacja-sesje.json)."""

import pytest

from tests.pomoc_sesje import bez_listy, bledy, droga, gdzie, jest, klik, kopia, kroki, naucz, tylko_droga


@pytest.fixture
def dane():
    return kopia()


MENU = [klik("menu-sesji", sesja="stare-zapytania")]
ARCHIWUM = [*MENU, klik("archive"), naucz()]
GRUPA = [klik("group-and-sort"), klik("view-all"), naucz()]
PISZ = {"typ": "pisz", "tekst": "Dokończ ofertę."}


def probna(d, lista):
    tylko_droga(d, lista)
    return bledy(d)


# wzory: dwie drogi ćwiczenia 2 kończą się bez kroku plik

def test_droga_archiwum_z_wzoru_przechodzi_i_konczy_sie_klikiem_archived(dane):
    lista = kroki(dane, "archiwum")
    assert [k.get("cel") for k in lista if k["typ"] == "klik"] == ["menu-sesji", "archive", "group-and-sort", "view-all", "archived"]
    assert not any(k["typ"] in ("plik", "artefakt", "strona") for k in lista)
    assert bledy(dane) == []


def test_drogi_cwiczenia_1_zaczynaja_sie_od_nowa_rozmowa_i_od_sesja_i_koncza_plikiem(dane):
    nowa, stara = droga(dane, "nowa", "cw1")["kroki"], droga(dane, "stara", "cw1")["kroki"]
    assert nowa[0] == klik("nowa-rozmowa", fakt="aplikacja-nowa-sesja-new-albo-cmd-n")
    assert stara[0]["cel"] == "sesja" and stara[0]["sesja"] == "galeria"
    assert nowa[-2]["typ"] == stara[-2]["typ"] == "plik"


# nowa-rozmowa

def test_nowa_rozmowa_dziala_tez_w_cwiczeniu_bez_listy_rozmow():
    scen = bez_listy()
    kroki_drogi = scen["cwiczenia"][0]["drogi"][0]["kroki"]
    kroki_drogi[:0] = [klik("nowa-rozmowa"), naucz()]
    assert bledy(scen) == []


def test_nowa_rozmowa_z_polem_sesja_odrzucona(dane):
    assert jest(probna(dane, [klik("nowa-rozmowa", sesja="galeria"), naucz(), PISZ]), "pole sesja tylko w klik z celem „sesja” albo „menu-sesji”")


def test_klik_z_obcym_polem_odrzucony(dane):
    assert jest(probna(dane, [klik("nowa-rozmowa", sesja=None, dalej=1), naucz()]), "pole dalej nie należy do kroku klik z celem nowa-rozmowa")


def test_nowa_rozmowa_dwa_razy_pod_rzad_bez_prosby_odrzucona(dane):
    assert jest(probna(dane, [klik("nowa-rozmowa"), naucz(), klik("nowa-rozmowa"), naucz()]), "gdy otwarta jest już pusta nowa rozmowa")


def test_nowa_rozmowa_po_pierwszej_prosbie_dozwolona(dane):
    wynik = probna(dane, [klik("nowa-rozmowa"), PISZ, {"typ": "claude", "tekst": "Gotowe."}, klik("nowa-rozmowa"), naucz()])
    assert not jest(wynik, "pusta nowa rozmowa")


def test_nowa_rozmowa_bez_kroku_plik_nie_jest_wyjatkiem(dane):
    assert jest(probna(dane, [klik("nowa-rozmowa"), naucz()]), "droga bez kroku plik ani artefakt")


# sesja

def test_sesja_z_obcym_id_albo_bez_pola(dane):
    assert jest(probna(dane, [klik("sesja", sesja="hotel"), naucz()]), "klik sesja wymaga pola sesja z id wiersza z aplikacja.sesje (jest 'hotel')")
    assert jest(probna(dane, [klik("sesja"), naucz()]), "klik sesja wymaga pola sesja z id wiersza z aplikacja.sesje (jest None)")


def test_sesja_dwa_razy_ten_sam_wiersz_odrzucona(dane):
    wynik = probna(dane, [klik("sesja", sesja="galeria"), naucz(), klik("sesja", sesja="galeria"), naucz()])
    assert jest(wynik, "klik sesja na wierszu „galeria”, który jest już otwarty w tej drodze")


def test_sesja_potem_inna_sesja_dozwolona(dane):
    assert probna(dane, [klik("sesja", sesja="galeria"), naucz(), klik("sesja", sesja="stare-zapytania"), naucz(), klik("sesja", sesja="galeria"), naucz()]) == []


def test_sesja_po_archiwizacji_tego_wiersza_w_tej_drodze_odrzucona(dane):
    wynik = probna(dane, [*ARCHIWUM, klik("sesja", sesja="stare-zapytania"), naucz()])
    assert jest(wynik, "klik sesja na wierszu „stare-zapytania”, który został zarchiwizowany wcześniej w tej drodze")


def test_sesja_w_cwiczeniu_bez_listy_odrzucona():
    scen = bez_listy()
    scen["cwiczenia"][0]["drogi"][0]["kroki"].insert(0, klik("sesja", sesja="galeria"))
    assert jest(bledy(scen), "klik „sesja” tylko w ćwiczeniu z aplikacja.sesje")


def test_po_zmianie_rozmowy_klik_w_stara_sciezke_odrzucony(dane):
    lista = [{"typ": "claude", "tekst": "Zapisałem oferta-galeria.txt.", "plik": "oferta-galeria.txt"}, klik("sesja", sesja="galeria"), naucz(), klik("sciezka")]
    assert jest(probna(dane, lista), "klik w ścieżkę bez wcześniejszej odpowiedzi Claude z polem plik")


# menu-sesji i archive

def test_menu_sesji_z_obcym_id_odrzucone(dane):
    assert jest(probna(dane, [klik("menu-sesji", sesja="hotel"), klik("archive"), naucz()]), "klik menu-sesji wymaga pola sesja z id wiersza z aplikacja.sesje")


def test_menu_sesji_na_zarchiwizowanym_wierszu_odrzucone(dane):
    wynik = probna(dane, [*ARCHIWUM, *MENU, klik("archive"), naucz()])
    assert jest(wynik, "klik menu-sesji na wierszu „stare-zapytania”, który został zarchiwizowany wcześniej w tej drodze")


def test_archive_bez_otwartego_menu_odrzucone(dane):
    assert jest(probna(dane, [klik("archive"), naucz()]), "klik archive bez otwartego menu rozmowy")


def test_archive_dwa_razy_odrzucone(dane):
    assert jest(probna(dane, [*ARCHIWUM, klik("archive"), naucz()]), "klik archive bez otwartego menu rozmowy")


def test_menu_otwarte_na_koncu_drogi_odrzucone(dane):
    assert jest(probna(dane, [*MENU]), "droga kończy się otwartym menu rozmowy: dodaj klik „archive”")


def test_przy_otwartym_menu_rozmowy_dalej_tylko_nauczyciel_i_archive(dane):
    for obcy in (klik("menu-sesji", sesja="galeria"), klik("group-and-sort"), klik("nowa-rozmowa"), klik("sesja", sesja="galeria"), PISZ):
        wynik = probna(dane, [*MENU, obcy, klik("archive"), naucz()])
        assert jest(wynik, "przy otwartym menu rozmowy: dalej tylko nauczyciel i klik „archive”"), obcy
    assert probna(dane, [*MENU, naucz(), klik("archive"), naucz()]) == []


def test_archiwizacja_otwartej_rozmowy_odrzucona(dane):
    wynik = probna(dane, [klik("sesja", sesja="galeria"), naucz(), klik("menu-sesji", sesja="galeria"), klik("archive"), naucz()])
    assert jest(wynik, "archiwizacja otwartej rozmowy „galeria”")


def test_archiwizacja_innej_niz_otwarta_rozmowy_dozwolona(dane):
    assert probna(dane, [klik("sesja", sesja="galeria"), naucz(), *ARCHIWUM]) == []


def test_archive_bez_listy_rozmow_odrzucone():
    scen = bez_listy()
    scen["cwiczenia"][0]["drogi"][0]["kroki"].insert(0, klik("archive"))
    assert jest(bledy(scen), "klik „archive” tylko w ćwiczeniu z aplikacja.sesje")


# group-and-sort, view-all, archived

def test_view_all_bez_menu_group_and_sort_odrzucone(dane):
    assert jest(probna(dane, [*ARCHIWUM, klik("view-all"), naucz()]), "klik view-all bez otwartego menu Group and sort")


def test_menu_group_and_sort_otwarte_na_koncu_drogi_odrzucone(dane):
    assert jest(probna(dane, [*ARCHIWUM, klik("group-and-sort")]), "droga kończy się otwartym menu Group and sort: dodaj klik „view-all”")


def test_przy_otwartym_menu_group_and_sort_dalej_tylko_nauczyciel_i_view_all(dane):
    for obcy in (klik("archived"), klik("nowa-rozmowa"), klik("menu-sesji", sesja="galeria"), PISZ):
        wynik = probna(dane, [*ARCHIWUM, klik("group-and-sort"), obcy, klik("view-all"), naucz()])
        assert jest(wynik, "przy otwartym menu Group and sort: dalej tylko nauczyciel i klik „view-all”"), obcy


def test_archived_bez_widoku_listy_odrzucone(dane):
    assert jest(probna(dane, [*ARCHIWUM, klik("archived")]), "klik archived bez widoku listy rozmów (najpierw klik „view-all”)")


def test_archived_dwa_razy_odrzucone(dane):
    wynik = probna(dane, [*ARCHIWUM, *GRUPA, klik("archived"), klik("archived")])
    assert jest(wynik, "klik archived przy zakładce Archived, która jest już wybrana")


def test_archived_bez_zarchiwizowanej_rozmowy_w_tej_drodze_odrzucone(dane):
    wynik = probna(dane, [*GRUPA, klik("archived"), naucz()])
    assert jest(wynik, "klik archived bez zarchiwizowanej rozmowy w tej drodze: lista byłaby pusta")


def test_droga_bez_archived_konczaca_sie_widokiem_listy_nie_ma_podgladu(dane):
    assert jest(probna(dane, [klik("group-and-sort"), klik("view-all"), naucz()]), "droga bez kroku plik ani artefakt")


@pytest.mark.parametrize(
    "krok",
    [
        {"typ": "pisz", "tekst": "Jeszcze coś."},
        {"typ": "mysli"},
        {"typ": "claude", "tekst": "Gotowe."},
        {"typ": "claude", "tekst": "Zapisałem oferta-galeria.txt.", "plik": "oferta-galeria.txt"},
        klik("sciezka"),
        {"typ": "plik", "nazwa": "oferta-galeria.txt", "linijki": ["a"]},
        klik("nowa-rozmowa"),
        klik("sesja", sesja="galeria"),
        klik("menu-sesji", sesja="galeria"),
        klik("group-and-sort"),
    ],
    ids=lambda k: f"{k['typ']}-{k.get('cel', '')}",
)
def test_po_view_all_dalej_tylko_nauczyciel_i_archived(dane, krok):
    wynik = probna(dane, [*ARCHIWUM, *GRUPA, krok])
    assert jest(wynik, "po View all: dalej tylko nauczyciel i klik „archived”")


def test_po_view_all_nauczyciel_i_archived_dozwolone(dane):
    assert probna(dane, [*ARCHIWUM, *GRUPA, naucz("Druga uwaga."), klik("archived"), naucz("Trzecia uwaga.")]) == []


def test_po_archived_dalej_tylko_nauczyciel(dane):
    wynik = probna(dane, [*ARCHIWUM, *GRUPA, klik("archived"), PISZ])
    assert jest(wynik, "krok pisz po View all: dalej tylko nauczyciel i klik „archived”")


def test_group_and_sort_przed_zamknieciem_menu_rozmowy_nie_wchodzi(dane):
    assert jest(probna(dane, [*MENU, klik("group-and-sort"), klik("view-all")]), "przy otwartym menu rozmowy")


# wyjątek od reguły „droga kończy się plikiem”

@pytest.mark.parametrize("lista", [[klik("sesja", sesja="galeria"), naucz()], ARCHIWUM, [*ARCHIWUM, *GRUPA, klik("archived"), naucz()]])
def test_droga_z_klikiem_sesja_archive_albo_archived_moze_skonczyc_sie_bez_pliku(dane, lista):
    assert probna(dane, lista) == []


@pytest.mark.parametrize("lista", [[PISZ], [klik("nowa-rozmowa"), naucz()], [klik("group-and-sort"), klik("view-all"), naucz()]])
def test_inne_drogi_bez_pliku_artefaktu_i_strony_dalej_sa_bledem(dane, lista):
    assert jest(probna(dane, lista), "droga bez kroku plik ani artefakt")


# fakty w krokach

def test_fakt_kliku_musi_istniec_w_pliku_faktow(dane):
    lista = kroki(dane, "archiwum")
    lista[gdzie(lista, "klik", "archive")]["fakt"] = "nie-ma-takiego-faktu"
    assert jest(bledy(dane), "fakt „nie-ma-takiego-faktu” nie istnieje w pliku faktów")


def test_klik_menu_sesji_z_polem_fakt_z_pliku_faktow_przechodzi(dane):
    lista = kroki(dane, "archiwum")
    assert lista[0]["fakt"] == "aplikacja-archiwizacja-z-menu-w-pasku-bocznym" and bledy(dane) == []
