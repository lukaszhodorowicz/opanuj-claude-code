"""Testy walidatora paska bocznego z rozmowami, część 1: pola `aplikacja.sesje` i `aplikacja.nazwa`, pole `nazwa_sesji` w kroku `claude` i długość nazwy (wzór: tests/dane/aplikacja-sesje.json, opis: dane/FORMAT-SCENARIUSZA.md, część „Pasek boczny z rozmowami”)."""

import pytest

from narzedzia import scenariusz as sc
from tests.pomoc_sesje import DANE, bez_listy, bledy, cwiczenie, gdzie, jest, kopia, kroki, z_krokami


@pytest.fixture
def dane():
    return kopia()


def test_wzor_przechodzi_walidator_i_komenda_scenariusza(dane, capsys):
    assert bledy(dane) == []
    assert [c["id"] for c in dane["cwiczenia"]] == ["cw1", "cw2"]
    assert [d["id"] for d in cwiczenie(dane, "cw1")["drogi"]] == ["nowa", "stara"]
    assert [d["id"] for d in cwiczenie(dane)["drogi"]] == ["nazwa", "archiwum"]
    assert sc.main([str(DANE / "aplikacja-sesje.json")]) == 0
    assert "aplikacja-sesje.json: ok" in capsys.readouterr().out


def test_wzor_ma_trzy_rozmowy_na_liscie_otwarta_dzisiejsza_i_dwie_z_sesje(dane):
    apl = cwiczenie(dane)["aplikacja"]
    assert apl["rozmowa"][0]["tekst"].startswith("Czy w cennik-uslug.txt") and "nazwa" not in apl
    assert [w["id"] for w in apl["sesje"]] == ["galeria", "stare-zapytania"]
    assert all("nazwa" not in w and len(w["rozmowa"]) >= 2 for w in apl["sesje"])


# aplikacja.sesje

def test_sesje_poza_cwiczeniem_z_drogami_odrzucone():
    scen = z_krokami()
    cw = scen["cwiczenia"][0]
    cw["aplikacja"]["sesje"] = [{"id": "a", "rozmowa": [{"kto": "ty", "tekst": "x"}]}]
    cw["aplikacja"]["nazwa"] = "Nazwa"
    wynik = bledy(scen)
    assert jest(wynik, "sesje tylko w ćwiczeniu z drogami") and jest(wynik, "nazwa tylko w ćwiczeniu z drogami")


@pytest.mark.parametrize("wartosc", [[], {}, "galeria", None])
def test_sesje_musi_byc_niepusta_lista(dane, wartosc):
    cwiczenie(dane)["aplikacja"]["sesje"] = wartosc
    assert jest(bledy(dane), "sesje musi być niepustą listą wierszy")


def test_wiersz_sesje_nie_obiekt(dane):
    cwiczenie(dane)["aplikacja"]["sesje"].append("galeria")
    assert jest(bledy(dane), "wiersz sesje musi być obiektem")


def test_wiersz_sesje_z_obcym_polem_odrzucony_bo_nie_pokazuje_tekstu(dane):
    cwiczenie(dane)["aplikacja"]["sesje"][0]["tytul"] = "Galeria"
    assert jest(bledy(dane), "pole tytul nie należy do wiersza sesje")


@pytest.mark.parametrize("id_", ["", "Galeria", "ga leria", "galeria_2", 5, None])
def test_id_wiersza_musi_pasowac_do_wzoru(dane, id_):
    cwiczenie(dane)["aplikacja"]["sesje"][0]["id"] = id_
    assert jest(bledy(dane), "wiersz sesje wymaga pola id pasującego do ^[a-z0-9-]+$")


def test_id_wiersza_powtorzone(dane):
    cwiczenie(dane)["aplikacja"]["sesje"][1]["id"] = "galeria"
    assert jest(bledy(dane), "id wiersza „galeria” powtórzone w aplikacja.sesje")


@pytest.mark.parametrize("rozmowa", [None, [], "tekst"])
def test_wiersz_bez_niepustej_rozmowy_odrzucony(dane, rozmowa):
    cwiczenie(dane)["aplikacja"]["sesje"][0]["rozmowa"] = rozmowa
    assert jest(bledy(dane), "sesje[0]: aplikacja wymaga niepustej listy rozmowa")


def test_rozmowa_wiersza_sprawdzana_jak_aplikacja_rozmowa(dane):
    wiadomosci = cwiczenie(dane)["aplikacja"]["sesje"][1]["rozmowa"]
    wiadomosci[0]["kto"] = "ktos"
    wiadomosci[1]["tekst"] = " "
    wiadomosci[1]["fakt"] = "nie-ma-takiego-faktu"
    wynik = bledy(dane)
    assert jest(wynik, "sesje[1]/rozmowa[0]: kto „ktos” spoza ty/claude")
    assert jest(wynik, "sesje[1]/rozmowa[1]: wiadomość wymaga niepustego pola tekst")
    assert jest(wynik, "fakt „nie-ma-takiego-faktu” nie istnieje w pliku faktów")


def test_nazwa_wiersza_z_wzoru_dozwolona_i_widoczna_dla_filtrow_jezyka(dane):
    from narzedzia.tekst_pl import polskie_pola

    cwiczenie(dane)["aplikacja"]["sesje"][0]["nazwa"] = "Oferta Galeria Pasaż"
    cwiczenie(dane)["aplikacja"]["nazwa"] = "Cennik 2027"
    assert bledy(dane) == []
    pola = dict(polskie_pola(dane, sc.wczytaj_napisy(sc.KORZEN / "dane" / "napisy-interfejsu.yaml")))
    assert pola["cwiczenia[1].aplikacja.sesje[0].nazwa"] == "Oferta Galeria Pasaż"
    assert pola["cwiczenia[1].aplikacja.nazwa"] == "Cennik 2027"
    assert pola["cwiczenia[1].drogi[0].kroki[2].nazwa_sesji.nazwa"] == "Oferta Galeria Pasaż 2027"
    assert not [s for s in pola if s.endswith(".kroki[6].nazwa") or ".plik" in s and s.endswith(".nazwa")], "nazwa pliku w kroku plik to nie nazwa rozmowy"


# nazwa: długość i znaki

@pytest.mark.parametrize("miejsce", ["otwarta", "wiersz", "nazwa_sesji"])
def test_nazwa_do_200_znakow(dane, miejsce):
    def ustaw(tekst):
        if miejsce == "otwarta":
            cwiczenie(dane)["aplikacja"]["nazwa"] = tekst
        elif miejsce == "wiersz":
            cwiczenie(dane)["aplikacja"]["sesje"][0]["nazwa"] = tekst
        else:
            kroki(dane, "nazwa")[gdzie(kroki(dane, "nazwa"), "claude")]["nazwa_sesji"]["nazwa"] = tekst

    ustaw("a" * 200)
    assert bledy(dane) == []
    ustaw("a" * 201)
    assert jest(bledy(dane), "ma 201 znaków, najwyżej 200 (fakt nazwa-sesji-do-200-znakow)")


@pytest.mark.parametrize("nazwa", ["", "   ", 5, None, ["Oferta"]])
def test_nazwa_musi_byc_niepustym_napisem(dane, nazwa):
    cwiczenie(dane)["aplikacja"]["nazwa"] = nazwa
    assert jest(bledy(dane), "nazwa musi być niepustym napisem")


@pytest.mark.parametrize("znak", ["\n", "\t", "​", " ", "\x07"])
def test_nazwa_ze_znakiem_sterujacym_albo_niewidocznym_odrzucona(dane, znak):
    cwiczenie(dane)["aplikacja"]["nazwa"] = f"Oferta{znak}Galeria"
    assert jest(bledy(dane), "ma znak sterujący albo niewidoczny: aplikacja zamienia je na spacje")


# nazwa_sesji w kroku claude

def claude(d):
    lista = kroki(d, "nazwa")
    return lista[gdzie(lista, "claude")]


def test_nazwa_sesji_obiekt_z_dokladnie_dwoma_polami(dane):
    claude(dane)["nazwa_sesji"] = {"sesja": "galeria"}
    assert jest(bledy(dane), "nazwa_sesji musi być obiektem {sesja, nazwa}")
    claude(dane)["nazwa_sesji"] = {"sesja": "galeria", "nazwa": "Oferta", "dalej": 1}
    assert jest(bledy(dane), "nazwa_sesji musi być obiektem {sesja, nazwa}")
    claude(dane)["nazwa_sesji"] = "Oferta"
    assert jest(bledy(dane), "nazwa_sesji musi być obiektem {sesja, nazwa}")


def test_nazwa_sesji_dla_wiersza_spoza_listy(dane):
    claude(dane)["nazwa_sesji"]["sesja"] = "hotel"
    assert jest(bledy(dane), "nazwa_sesji: sesja 'hotel' spoza aplikacja.sesje")


def test_nazwa_sesji_dla_rozmowy_otwartej_odrzucona(dane):
    lista = kroki(dane, "nazwa")
    lista.insert(0, {"typ": "klik", "cel": "sesja", "sesja": "galeria"})
    lista.insert(1, {"typ": "nauczyciel", "tekst": "Rozmowa otwarta."})
    wynik = bledy(dane)
    assert jest(wynik, "nazwa_sesji dla rozmowy „galeria”, która jest otwarta")


def test_nazwa_sesji_dla_rozmowy_otwartej_a_potem_innej_dozwolona(dane):
    lista = kroki(dane, "nazwa")
    lista.insert(0, {"typ": "klik", "cel": "sesja", "sesja": "stare-zapytania"})
    lista.insert(1, {"typ": "nauczyciel", "tekst": "Otwarta jest inna rozmowa."})
    del lista[lista.index(next(k for k in lista if k["typ"] == "klik" and k.get("sesja") == "galeria"))]
    assert not jest(bledy(dane), "nazwa_sesji dla rozmowy")


def test_nazwa_sesji_w_cwiczeniu_bez_listy_odrzucona():
    scen = bez_listy()
    cw = scen["cwiczenia"][0]
    k = next(k for d in cw["drogi"] for k in d["kroki"] if k["typ"] == "claude")
    k["nazwa_sesji"] = {"sesja": "galeria", "nazwa": "Oferta"}
    assert jest(bledy(scen), "nazwa_sesji tylko w ćwiczeniu z aplikacja.sesje")


def test_nazwa_sesji_nazwa_pusta_i_za_dluga(dane):
    claude(dane)["nazwa_sesji"]["nazwa"] = " "
    assert jest(bledy(dane), "nazwa_sesji.nazwa musi być niepustym napisem")
    claude(dane)["nazwa_sesji"]["nazwa"] = "x" * 250
    assert jest(bledy(dane), "nazwa_sesji.nazwa ma 250 znaków, najwyżej 200")


def test_droga_nazwa_z_wzoru_konczy_sie_klikiem_sesja_bez_kroku_plik(dane):
    lista = kroki(dane, "nazwa")
    assert not any(k["typ"] in ("plik", "artefakt", "strona") for k in lista)
    assert lista[gdzie(lista, "klik", "sesja")]["sesja"] == "galeria"
    assert bledy(dane) == []
