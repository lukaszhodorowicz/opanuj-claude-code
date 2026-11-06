"""Testy narzędzi wokół paska bocznego z rozmowami: napisy interfejsu rysowane przez stronę (Archive, Group and sort, View all, Archived), rytm nauczyciela po klikach w pasek boczny (narzedzia/czytelnosc.py), podgląd drogi bez kroku plik w tekście lekcji (narzedzia/strona_podglad.py), polskie napisy dla filtrów języka (narzedzia/tekst_pl.py), składanie lekcji z paskiem bocznym (wzór: tests/dane/aplikacja-sesje.json)."""

import json
import re

import pytest

from narzedzia import czytelnosc, strona, strona_podglad
from narzedzia import scenariusz as sc
from narzedzia.tekst_pl import polskie_pola
from tests.pomoc_sesje import KORZEN, NAPISY, droga, gdzie, kopia, kroki, naucz


# napisy interfejsu

def test_napisy_paska_bocznego_sa_na_liscie_napisow_interfejsu():
    js = (KORZEN / "strona" / "aplikacja-sesje.js").read_text(encoding="utf-8")
    blok = re.search(r"PK\.NAPISY_SESJI = \{(.*?)\};", js, re.S).group(1)
    napisy = re.findall(r':\s*"([^"]+)"', blok)
    lista = sc._Napisy(NAPISY)
    assert napisy == ["Archive", "Group and sort", "View all", "Archived"]
    assert all(lista.jest(n, "aplikacja") for n in napisy)


def test_nowa_rozmowa_ma_napis_z_listy_a_inne_pozycje_menu_nie_maja_napisow_w_kodzie():
    js = re.sub(r"/\*.*?\*/", "", (KORZEN / "strona" / "aplikacja-sesje.js").read_text(encoding="utf-8"), flags=re.S)  # bez komentarzy: liczą się napisy w kodzie
    assert "+ New" not in js, "napis „+ New” rysuje PK.NAPISY_APLIKACJI"
    for napis in ("Pin", "Rename", "Fork", "Move to group", "Delete", "Open in", "Group by", "Sort by", "Display", "Search", "Active", "New session"):
        assert napis not in js, f"napis „{napis}” nie ma źródła w dokumentacji: pozycja ma być szarym paskiem"


def test_fakty_przeniesione_z_modulu_6_leza_w_pliku_faktow_ze_zrodlem_i_cytatem():
    import yaml

    fakty = {f["id"]: f for f in yaml.safe_load((KORZEN / "dane" / "fakty.yaml").read_text(encoding="utf-8"))["fakty"]}
    for id_ in ("aplikacja-pasek-boczny-lista-sesji", "aplikacja-kazda-rozmowa-to-sesja", "aplikacja-nowa-sesja-new-albo-cmd-n", "aplikacja-powrot-do-sesji-klik-w-pasku-bocznym", "aplikacja-archiwizacja-z-menu-w-pasku-bocznym", "aplikacja-zarchiwizowane-group-and-sort-view-all", "aplikacja-zmiana-nazwy-klik-tytulu", "aplikacja-popros-claude-o-nazwe-lub-archiwum", "nazwa-sesji-do-200-znakow"):
        assert fakty[id_]["cytat"] and fakty[id_]["zrodlo"].startswith("https://code.claude.com/docs/en/"), id_


# rytm nauczyciela (czytelnosc.py)

def lekcja_z_scenariuszem(tmp_path, d):
    katalog = tmp_path / "moduly" / "m" / "l"
    katalog.mkdir(parents=True, exist_ok=True)
    (katalog / "lekcja.md").write_text("# Lekcja\n\nTekst.\n", encoding="utf-8")
    (katalog / "scenariusz.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return tmp_path


def czytelnosc_bledy(tmp_path, d):
    return czytelnosc.sprawdz_czytelnosc(lekcja_z_scenariuszem(tmp_path, d))[0]


def test_wzor_z_nauczycielem_po_klikach_przechodzi_czytelnosc(tmp_path):
    assert czytelnosc_bledy(tmp_path, kopia()) == []


@pytest.mark.parametrize("cel", ["nowa-rozmowa", "sesja", "archive", "view-all", "archived"])
def test_brak_nauczyciela_po_kliku_w_pasek_boczny_to_blad(tmp_path, cel):
    d = kopia()
    for c in d["cwiczenia"]:
        for dr in c["drogi"]:
            for k in dr["kroki"]:
                if k["typ"] == "klik" and k.get("cel") == cel:
                    dr["kroki"] = [x for x in dr["kroki"] if x["typ"] != "nauczyciel"]
                    break
    wynik = czytelnosc_bledy(tmp_path, d)
    assert any(f"klik" in b and "brak nauczyciela w 2 kolejnych krokach" in b for b in wynik), (cel, wynik)


@pytest.mark.parametrize("cel", ["menu-sesji", "group-and-sort"])
def test_klik_menu_sesji_i_group_and_sort_nie_wymagaja_nauczyciela_zaraz_po_sobie(tmp_path, cel):
    d = {"cwiczenia": [{"id": "cw2", "drogi": [{"id": "x", "kroki": [{"typ": "klik", "cel": cel, "sesja": "a"}, {"typ": "klik", "cel": "archive"}, {"typ": "nauczyciel", "tekst": "ok"}]}]}]}
    assert czytelnosc_bledy(tmp_path, d) == []


def test_nauczyciel_po_dwoch_krokach_od_kliku_wystarcza(tmp_path):
    d = {"cwiczenia": [{"id": "cw1", "drogi": [{"id": "x", "kroki": [{"typ": "klik", "cel": "nowa-rozmowa"}, {"typ": "mysli"}, {"typ": "nauczyciel", "tekst": "ok"}]}]}]}
    assert czytelnosc_bledy(tmp_path, d) == []
    d["cwiczenia"][0]["drogi"][0]["kroki"].insert(1, {"typ": "mysli"})
    assert czytelnosc_bledy(tmp_path, d)


def test_klik_w_przebiegu_terminala_z_celem_paska_bocznego_nie_wymaga_nauczyciela(tmp_path):
    d = {"cwiczenia": [{"id": "cw1", "zadania": [{"przebiegi": {"t": [{"typ": "klik", "cel": "sesja"}]}}]}]}
    assert czytelnosc_bledy(tmp_path, d) == []


# podgląd drogi w tekście lekcji

def znacznik(droga_id, cw="cw2"):
    return f'<div class="podglad" data-cw="{cw}" data-t="{droga_id}"></div>'


@pytest.mark.parametrize("cw,id_", [("cw2", "nazwa"), ("cw2", "archiwum"), ("cw1", "nowa"), ("cw1", "stara")])
def test_podglad_drog_ze_wzoru_przechodzi(cw, id_):
    strona_podglad.sprawdz_podglady(znacznik(id_, cw), kopia())


def test_podglad_drogi_bez_klikow_sesja_archive_archived_i_bez_pliku_to_blad_skladania():
    d = kopia()
    droga(d, "archiwum")["kroki"] = [{"typ": "klik", "cel": "group-and-sort"}, {"typ": "klik", "cel": "view-all"}, naucz()]
    with pytest.raises(ValueError, match="droga nie ma kroku plik, artefakt ani strona"):
        strona_podglad.sprawdz_podglady(znacznik("archiwum"), d)


@pytest.mark.parametrize("cel", ["sesja", "archive", "archived"])
def test_podglad_drogi_z_klikiem_sesja_archive_albo_archived_przechodzi(cel):
    d = kopia()
    droga(d, "nazwa")["kroki"] = [{"typ": "klik", "cel": cel}, naucz()]
    strona_podglad.sprawdz_podglady(znacznik("nazwa"), d)


@pytest.mark.parametrize("cel", ["nowa-rozmowa", "menu-sesji", "group-and-sort", "view-all"])
def test_podglad_drogi_tylko_z_innymi_klikami_paska_bocznego_to_blad(cel):
    d = kopia()
    droga(d, "nazwa")["kroki"] = [{"typ": "klik", "cel": cel}, naucz()]
    with pytest.raises(ValueError, match="droga nie ma kroku plik, artefakt ani strona"):
        strona_podglad.sprawdz_podglady(znacznik("nazwa"), d)


# polskie napisy dla filtrów języka

def test_tekst_pl_wypisuje_nazwy_rozmow_ale_nie_nazwy_plikow_i_folderow():
    d = kopia()
    d["cwiczenia"][1]["aplikacja"]["nazwa"] = "Cennik 2027"
    d["cwiczenia"][1]["aplikacja"]["sesje"][1]["nazwa"] = "Hotel Mewa"
    pola = dict(polskie_pola(d, sc.wczytaj_napisy(KORZEN / "dane" / "napisy-interfejsu.yaml")))
    assert pola["cwiczenia[1].aplikacja.nazwa"] == "Cennik 2027"
    assert pola["cwiczenia[1].aplikacja.sesje[1].nazwa"] == "Hotel Mewa"
    nazwane = [s for s in pola if s.endswith(".nazwa")]
    assert sorted(nazwane) == ["cwiczenia[1].aplikacja.nazwa", "cwiczenia[1].aplikacja.sesje[1].nazwa", "cwiczenia[1].drogi[0].kroki[2].nazwa_sesji.nazwa"]
    assert not any("oferta-galeria.txt" == t and s.endswith(".nazwa") for s, t in pola.items())


# składanie strony

def test_strona_skladana_z_wzoru_ma_pasek_boczny_i_nowe_pliki_silnika(tmp_path):
    scen = kopia()
    (tmp_path / "lekcja.md").write_text("# Próba\n\n<!-- cwiczenie: cw1 -->\n\n<!-- cwiczenie: cw2 -->\n", encoding="utf-8")
    (tmp_path / "scenariusz.json").write_text(json.dumps(scen, ensure_ascii=False), encoding="utf-8")
    html = strona.zloz_strone(tmp_path)
    for fragment in ("PK.sesjeCwiczenia", "PK.krokiAplikacji", "PK.sesjePodglad", ".apl-menu-sesji", ".apl-sesje-widok"):
        assert fragment in html, fragment
    assert html.count("PK.aplikacja = function") == 1


def test_pliki_silnika_do_300_linii_i_z_opisem_na_poczatku():
    for nazwa in ("aplikacja.js", "aplikacja-kroki.js", "aplikacja-sesje.js", "aplikacja-sesje-gra.js", "aplikacja-okno.js", "styl-aplikacja-sesje.css"):
        tekst = (KORZEN / "strona" / nazwa).read_text(encoding="utf-8")
        assert len(tekst.splitlines()) <= 300, nazwa
        assert tekst.startswith("/* "), nazwa
    assert len((KORZEN / "narzedzia" / "scenariusz_sesje.py").read_text(encoding="utf-8").splitlines()) <= 300
    assert (KORZEN / "narzedzia" / "scenariusz_sesje.py").read_text(encoding="utf-8").startswith('"""')
