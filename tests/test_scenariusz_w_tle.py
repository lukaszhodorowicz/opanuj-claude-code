"""Testy walidatora pracy w tle w drogach symulatora aplikacji (wzór: tests/dane/subagent-zbiera-panel-w-tle.json): lista `w_tle` i `w_tle_koniec` kroku `claude`, kliki `menu-paska`, `background-tasks`, `running-tasks` i `wpis-w-tle`, kolejność kroków wokół menu ⋮ i panelu, rytm nauczyciela, napisy dla filtrów języka i fakty z lekcji 9.2 cytowane w teście, żeby nie były sierotami w gałęzi silnika: fakty `aplikacja-panel-zadan-w-tle-co-pokazuje`, `aplikacja-menu-paska-panele-bez-przycisku`, `aplikacja-wpis-w-tle-wynik-w-panelu-subagenta`, `aplikacja-panel-zadan-grupa-running-wpis-agent`, `aplikacja-link-running-tasks-w-rozmowie`, `aplikacja-klik-running-tasks-otwiera-panel`, `aplikacja-panel-zadan-finished-i-clear`, `aplikacja-menu-trzy-kropki-pozycje` i `aplikacja-wiersz-subagenta-i-panel-subagenta`."""

import copy

import pytest

from tests.pomoc_w_tle import FAKTY_E3, KORZEN, bledy, dane, indeks, jest, kroki  # noqa: F401


def test_wzor_przechodzi_i_ma_wszystkie_kroki_pracy_w_tle(dane):
    assert bledy(dane) == []
    assert [k["cel"] for k in kroki(dane) if k["typ"] == "klik" and k["cel"] != "sciezka"] == ["menu-paska", "background-tasks", "wpis-w-tle"]
    assert any("w_tle" in k for k in kroki(dane)) and any(k.get("w_tle_koniec") for k in kroki(dane))


def test_fakty_e3_leza_w_pliku_faktow_z_cytatem_i_zrodlem():
    import yaml

    fakty = {f["id"]: f for f in yaml.safe_load((KORZEN / "dane" / "fakty.yaml").read_text(encoding="utf-8"))["fakty"]}
    for id_ in FAKTY_E3:
        assert fakty[id_]["cytat"] and fakty[id_]["zrodlo"].startswith(("https://code.claude.com/docs/en/", "https://github.com/anthropics/claude-code/issues/")), id_


def test_wzor_ma_dwa_subagenty_i_odnosnik(dane):
    w = next(k for k in kroki(dane) if "w_tle" in k)["w_tle"]
    assert [x["rodzaj"] for x in w] == ["subagent", "subagent"]
    assert all(x["tytul"] and x["zadanie"] and x["wynik"] for x in w)


# kolejność: Z10 i Z16

def test_menu_paska_przed_praca_w_tle_odrzucone(dane):
    k = kroki(dane)
    k.insert(0, {"typ": "klik", "cel": "menu-paska"})
    assert jest(bledy(dane), "przed pierwszą pracą w tle")


def test_menu_paska_przed_krokiem_claude_z_w_tle_odrzucone(dane):
    k = kroki(dane)
    k.insert(indeks(dane, "claude"), k.pop(indeks(dane, "klik", "menu-paska")))
    assert jest(bledy(dane), "przed pierwszą pracą w tle")


def test_background_tasks_bez_otwartego_menu_odrzucone(dane):
    del kroki(dane)[indeks(dane, "klik", "menu-paska")]
    assert jest(bledy(dane), "bez otwartego menu ⋮")


def test_wpis_w_tle_bez_panelu_odrzucony(dane):
    del kroki(dane)[indeks(dane, "klik", "background-tasks")]
    wynik = bledy(dane)
    assert jest(wynik, "przy otwartym menu ⋮") or jest(wynik, "bez otwartego panelu zadań")


def test_wpis_w_tle_z_nieistniejacym_nr_odrzucony(dane):
    for nr in (3, 0, -1, "1", True, None):
        d = copy.deepcopy(dane)
        kroki(d)[indeks(d, "klik", "wpis-w-tle")]["nr"] = nr
        assert jest(bledy(d), "nr musi być liczbą całkowitą od 1 do 2"), nr
    kroki(dane)[indeks(dane, "klik", "wpis-w-tle")]["nr"] = 2
    assert bledy(dane) == []


def test_wpis_w_tle_bez_nr_odrzucony(dane):
    del kroki(dane)[indeks(dane, "klik", "wpis-w-tle")]["nr"]
    assert jest(bledy(dane), "nr musi być liczbą całkowitą")


def test_wpis_przeplywu_nie_ma_panelu_subagenta():
    # wpis przepływu powstaje z kliku once na karcie zgody (wzór lekcji 9.4), nie z ręcznego w_tle
    from tests.pomoc_przeplyw import WZOR as WZOR_PRZEPLYWU

    d = copy.deepcopy(WZOR_PRZEPLYWU)
    assert bledy(d) == []
    kroki(d).insert(indeks(d, "klik", "background-tasks") + 1, {"typ": "klik", "cel": "wpis-w-tle", "nr": 1})
    assert jest(bledy(d), "panel subagenta ma tylko subagent")


@pytest.mark.parametrize("cel", ["menu-paska", "background-tasks", "wpis-w-tle"])
def test_klik_e3_po_kroku_konczacym_odrzucony(dane, cel):
    k = kroki(dane)
    dodatkowy = {"typ": "klik", "cel": cel, **({"nr": 1} if cel == "wpis-w-tle" else {})}
    koniec = next(i for i, x in enumerate(k) if x.get("w_tle_koniec"))
    k.insert(koniec + 1, dodatkowy)
    assert jest(bledy(dane), "po kroku z w_tle_koniec")


def test_nowa_praca_w_tle_po_kroku_konczacym_odrzucona(dane):
    k = kroki(dane)
    koniec = next(i for i, x in enumerate(k) if x.get("w_tle_koniec"))
    k.insert(koniec + 1, {"typ": "claude", "tekst": "Kolejny subagent.", "w_tle": [{"rodzaj": "subagent", "tytul": "Kolejne zadanie", "zadanie": "Zrób coś.", "wynik": ["Linijka."]}]})
    assert jest(bledy(dane), "po kroku z w_tle_koniec")


def test_w_tle_koniec_bez_pracy_w_tle_odrzucone(dane):
    k = kroki(dane)
    del k[indeks(dane, "claude")]["w_tle"]
    assert jest(bledy(dane), "w_tle_koniec bez wcześniejszej pracy w tle")


def test_w_tle_koniec_musi_byc_prawda(dane):
    kroki(dane)[next(i for i, x in enumerate(kroki(dane)) if x.get("w_tle_koniec"))]["w_tle_koniec"] = False
    assert jest(bledy(dane), "w_tle_koniec musi być prawdą")


def test_menu_stoi_do_wyboru_pozycji(dane):
    k = kroki(dane)
    k.insert(indeks(dane, "klik", "menu-paska") + 1, {"typ": "mysli"})
    assert jest(bledy(dane), "przy otwartym menu ⋮")


def test_nauczyciel_przy_otwartym_menu_dozwolony(dane):
    k = kroki(dane)
    k.insert(indeks(dane, "klik", "menu-paska") + 1, {"typ": "nauczyciel", "tekst": "Wybierz pozycję z napisem."})
    assert bledy(dane) == []


def test_droga_nie_konczy_sie_otwartym_menu(dane):
    k = kroki(dane)
    del k[indeks(dane, "klik", "background-tasks"):]
    assert jest(bledy(dane), "kończy się otwartym menu ⋮") or jest(bledy(dane), "przy otwartym menu")


def test_ponowne_menu_przy_otwartym_panelu_odrzucone(dane):
    k = kroki(dane)
    k.insert(indeks(dane, "klik", "background-tasks") + 2, {"typ": "klik", "cel": "menu-paska"})
    assert jest(bledy(dane), "przy otwartym panelu zadań")


def test_plik_zajmuje_miejsce_panelu_i_menu_mozna_otworzyc_ponownie(dane):
    k = kroki(dane)
    # plik zamyka panel: po nim (bez kroku końcowego) ⋮ znów działa
    k[next(i for i, x in enumerate(k) if x.get("w_tle_koniec"))].pop("w_tle_koniec")
    k.extend([{"typ": "klik", "cel": "menu-paska"}, {"typ": "klik", "cel": "background-tasks"}, {"typ": "nauczyciel", "tekst": "Panel jest znów otwarty."}])
    assert bledy(dane) == []


# pola

def test_pola_w_tle(dane):
    sw = next(k for k in kroki(dane) if "w_tle" in k)
    for zle, fragment in (
        ({"rodzaj": "subagent"}, "niepustą listą"),
        ([], "niepustą listą"),
        (["nie obiekt"], "praca w tle musi być obiektem"),
    ):
        d = copy.deepcopy(dane)
        next(k for k in kroki(d) if "w_tle" in k)["w_tle"] = zle
        assert jest(bledy(d), fragment), zle
    wpis = sw["w_tle"][0]
    for zmiana, fragment in (
        ({"rodzaj": "polecenie"}, "spoza subagent/przeplyw"),
        ({"tytul": " "}, "tytul musi być niepustym napisem"),
        ({"tytul": "x" * 81}, "tytul: najwyżej 80 znaków"),
        ({"zadanie": ""}, "zadanie musi być niepustym napisem"),
        ({"wynik": []}, "wynik subagenta musi być listą"),
        ({"wynik": [" "]}, "wynik subagenta musi być listą"),
        ({"wynik": "tekst"}, "wynik subagenta musi być listą"),
        ({"nazwa": "x"}, "nie należy do w_tle"),
    ):
        d = copy.deepcopy(dane)
        next(k for k in kroki(d) if "w_tle" in k)["w_tle"][0] = {**wpis, **zmiana}
        assert jest(bledy(d), fragment), zmiana
    for brak in ("tytul", "zadanie", "wynik"):
        d = copy.deepcopy(dane)
        del next(k for k in kroki(d) if "w_tle" in k)["w_tle"][0][brak]
        assert bledy(d), brak


def test_przeplyw_ma_tylko_tytul_i_powstaje_tylko_z_karty_zgody(dane):
    w = next(k for k in kroki(dane) if "w_tle" in k)["w_tle"]
    w[1] = {"rodzaj": "przeplyw", "tytul": "Przepływ", "zadanie": "x"}
    assert jest(bledy(dane), "zadanie tylko przy rodzaju subagent")
    w[1] = {"rodzaj": "przeplyw", "tytul": "Przepływ", "wynik": ["x"]}
    assert jest(bledy(dane), "wynik tylko przy rodzaju subagent")
    w[1] = {"rodzaj": "przeplyw", "tytul": "Przepływ"}
    assert jest(bledy(dane), "przeplyw tylko z karty zgody")


def test_w_tle_i_koniec_w_jednym_kroku_odrzucone(dane):
    next(k for k in kroki(dane) if "w_tle" in k)["w_tle_koniec"] = True
    assert jest(bledy(dane), "w_tle i w_tle_koniec w jednym kroku")


def test_najwyzej_szesc_prac_w_tle(dane):
    w = next(k for k in kroki(dane) if "w_tle" in k)["w_tle"]
    w.extend(copy.deepcopy(w) * 3)
    assert jest(bledy(dane), "najwyżej 6 prac w tle")


def test_pola_klikow_e3(dane):
    for cel, extra in (("menu-paska", {"nr": 1}), ("background-tasks", {"na": "x"}), ("wpis-w-tle", {"na": "x"})):
        d = copy.deepcopy(dane)
        kroki(d)[indeks(d, "klik", cel)].update(extra)
        assert jest(bledy(d), "nie należy do kliku"), cel


def test_fakt_kroku_e3_musi_istniec(dane):
    kroki(dane)[indeks(dane, "klik", "menu-paska")]["fakt"] = "nie-ma-takiego-faktu"
    assert jest(bledy(dane), "nie istnieje w pliku faktów")


def test_w_tle_w_cwiczeniu_z_sesjami_odrzucone(dane):
    dane["cwiczenia"][0]["aplikacja"]["sesje"] = [{"id": "inna", "rozmowa": [{"kto": "ty", "tekst": "Inna rozmowa."}]}]
    assert jest(bledy(dane), "aplikacja.sesje")


