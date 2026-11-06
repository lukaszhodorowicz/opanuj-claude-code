"""Testy narzędzi wokół folderu każdej rozmowy i karty wiadomości (wzór: tests/dane/kilka-rozmow-foldery-i-wiadomosc.json): rytm nauczyciela (narzedzia/czytelnosc.py), podgląd drogi w tekście lekcji (narzedzia/strona_podglad.py), polskie napisy dla filtrów języka (narzedzia/tekst_pl.py), składanie strony z nowymi plikami silnika, długość i opis nowych plików oraz opis formatu cytujący fakty tego wzoru (dane/FORMAT-SCENARIUSZA.md): fakty `aplikacja-kazda-rozmowa-to-sesja`, `aplikacja-rzad-pod-polem-srodowisko-folder-tryb-model`, `aplikacja-kontrolka-folderu-obok-selektora`, `aplikacja-rzad-pod-polem-folder-z-nazwa-kadr`, `aplikacja-pasek-boczny-grupa-folderu`, `aplikacja-pasek-boczny-grupy-z-naglowkami-kadr`, `aplikacja-powrot-do-sesji-klik-w-pasku-bocznym`, `aplikacja-wiadomosc-karta-z-tytulem-nadawcy`, `aplikacja-claude-czyta-inne-sesje-zwykla-prosba` i `aplikacja-wiadomosc-nie-dojdzie-do-archiwum`."""

import json

import pytest
import yaml

from narzedzia import czytelnosc, strona, strona_podglad
from narzedzia import scenariusz as sc
from narzedzia.tekst_pl import polskie_pola
from tests.pomoc_foldery import KORZEN, NAPISY, apl, bledy, cwiczenie, gdzie, kopia, kroki, naucz

FAKTY = (
    "aplikacja-kazda-rozmowa-to-sesja", "aplikacja-rzad-pod-polem-srodowisko-folder-tryb-model", "aplikacja-kontrolka-folderu-obok-selektora",
    "aplikacja-rzad-pod-polem-folder-z-nazwa-kadr", "aplikacja-pasek-boczny-grupa-folderu", "aplikacja-pasek-boczny-grupy-z-naglowkami-kadr",
    "aplikacja-powrot-do-sesji-klik-w-pasku-bocznym", "aplikacja-wiadomosc-karta-z-tytulem-nadawcy", "aplikacja-claude-czyta-inne-sesje-zwykla-prosba",
    "aplikacja-wiadomosc-nie-dojdzie-do-archiwum",
)


def lekcja_z_scenariuszem(tmp_path, d):
    katalog = tmp_path / "moduly" / "m" / "l"
    katalog.mkdir(parents=True, exist_ok=True)
    (katalog / "lekcja.md").write_text("# Lekcja\n\nTekst.\n", encoding="utf-8")
    (katalog / "scenariusz.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return tmp_path


def test_wzor_przechodzi_czytelnosc(tmp_path):
    assert czytelnosc.sprawdz_czytelnosc(lekcja_z_scenariuszem(tmp_path, kopia()))[0] == []


@pytest.mark.parametrize("cel,cw,droga_id", [("folder", "cw1", "druga"), ("wiadomosc-od", "cw2", "wiadomosc")])
def test_brak_nauczyciela_po_kliku_folder_albo_wiadomosc_od_to_blad(tmp_path, cel, cw, droga_id):
    d = kopia()
    k = kroki(d, droga_id, cw)
    i = gdzie(k, "klik", cel)
    del k[i + 1]  # nauczyciel zaraz po kliku
    k.insert(i + 1, {"typ": "mysli"})
    k.insert(i + 2, {"typ": "mysli"})
    wynik = czytelnosc.sprawdz_czytelnosc(lekcja_z_scenariuszem(tmp_path, d))[0]
    assert any(f"klik" in b and "brak nauczyciela" in b for b in wynik), wynik


@pytest.mark.parametrize("droga_id", ["druga"])
def test_podglad_drogi_cw1_przechodzi(droga_id):
    strona_podglad.sprawdz_podglady('<div class="podglad" data-cw="cw1" data-t="druga"></div>', kopia())


def test_podglad_drogi_cw2_przechodzi_a_klik_wiadomosc_od_sam_daje_podglad():
    strona_podglad.sprawdz_podglady('<div class="podglad" data-cw="cw2" data-t="wiadomosc"></div>', kopia())
    d = kopia()
    c = cwiczenie(d, "cw2")
    c["drogi"][0]["kroki"] = [k for k in c["drogi"][0]["kroki"] if k["typ"] not in ("plik",) and k.get("cel") != "sciezka" and k.get("cel") != "sesja"]
    # droga bez kroku plik i bez kliku sesja nie kończy się podglądem, ale klik wiadomosc-od go daje
    assert any(k.get("cel") == "wiadomosc-od" for k in c["drogi"][0]["kroki"])
    strona_podglad.sprawdz_podglady('<div class="podglad" data-cw="cw2" data-t="wiadomosc"></div>', d)


def test_tekst_pl_wypisuje_tekst_wiadomosci_i_nazwy_rozmow_ale_nie_nazw_folderow():
    pola = dict(polskie_pola(kopia(), NAPISY))
    tekst = [t for s, t in pola.items() if s.endswith("wiadomosc.tekst")]
    assert tekst == ["Posty na listopad mają już nową cenę wieńca z chryzantem: 210 zł. Poprawiłem plik posty-wience.txt w teczce Posty-listopad."]
    assert pola["cwiczenia[1].aplikacja.nazwa"] == "Posty na listopad" and pola["cwiczenia[1].aplikacja.sesje[0].nazwa"] == "Cennik wieńców"
    assert not any(s.endswith(".folder") or s.endswith(".id") or s.endswith(".do") for s in pola)


def test_strona_sklada_sie_z_wzoru_z_nowymi_plikami_silnika(tmp_path):
    (tmp_path / "lekcja.md").write_text("# Próba\n\n<!-- cwiczenie: cw1 -->\n\n<!-- cwiczenie: cw2 -->\n", encoding="utf-8")
    (tmp_path / "scenariusz.json").write_text(json.dumps(kopia(), ensure_ascii=False), encoding="utf-8")
    html = strona.zloz_strone(tmp_path)
    for fragment in ("PK.folderyRozmow", "PK.wierszeGrupFolderow", "PK.kartaWiadomosci", ".apl-grupa-folderu", ".apl-wiadomosc", ".apl-chip-folder"):
        assert fragment in html, fragment


def test_nowe_pliki_silnika_do_300_linii_i_z_opisem_na_poczatku():
    for nazwa in ("aplikacja-sesje-foldery.js", "aplikacja-sesje-wiadomosc.js", "aplikacja-sesje-gra.js", "aplikacja-folder-cwiczenie.js", "styl-aplikacja-sesje-foldery.css", "styl-aplikacja-sesje-wiadomosc.css"):
        tekst = (KORZEN / "strona" / nazwa).read_text(encoding="utf-8")
        assert len(tekst.splitlines()) <= 300, nazwa
        assert tekst.startswith("/* "), nazwa
    for nazwa in ("scenariusz_sesje.py", "scenariusz_sesje_foldery.py", "scenariusz_wiadomosc.py", "scenariusz_aplikacja_drogi.py", "scenariusz_aplikacja.py"):
        tekst = (KORZEN / "narzedzia" / nazwa).read_text(encoding="utf-8")
        assert len(tekst.splitlines()) <= 300, nazwa
        assert tekst.startswith('"""'), nazwa


def test_fakty_wzoru_leza_w_pliku_faktow_z_cytatem_i_zrodlem_a_wzor_je_cytuje():
    fakty = {f["id"]: f for f in yaml.safe_load((KORZEN / "dane" / "fakty.yaml").read_text(encoding="utf-8"))["fakty"]}
    for id_ in FAKTY:
        assert fakty[id_]["cytat"] and fakty[id_]["zrodlo"].startswith(("https://code.claude.com/docs/en/", "https://github.com/anthropics/claude-code/issues/")), id_
    uzyte = {k["fakt"] for c in kopia()["cwiczenia"] for d in c["drogi"] for k in d["kroki"] if "fakt" in k}
    assert {"aplikacja-wiadomosc-karta-z-tytulem-nadawcy", "aplikacja-claude-czyta-inne-sesje-zwykla-prosba", "aplikacja-kontrolka-folderu-obok-selektora"} <= uzyte


def test_opis_formatu_cytuje_fakty_o_grupach_folderow_i_archiwum_i_nie_ma_celu_running_tasks():
    from narzedzia.fakty_silnika import fakty_w_formacie

    cytowane = fakty_w_formacie(KORZEN, set(FAKTY))
    for id_ in ("aplikacja-pasek-boczny-grupa-folderu", "aplikacja-pasek-boczny-grupy-z-naglowkami-kadr", "aplikacja-rzad-pod-polem-folder-z-nazwa-kadr", "aplikacja-wiadomosc-nie-dojdzie-do-archiwum"):
        assert id_ in cytowane, id_
    opis = (KORZEN / "dane" / "FORMAT-SCENARIUSZA.md").read_text(encoding="utf-8")
    assert "klik wcześniejszy, zaraz po odpowiedzi albo po karcie, też się liczy;" not in opis, "stary opis dla wszystkich celów"
    assert "klik bez czekającego kroku przepada" in opis
    assert "celu `running-tasks` nie ma" in opis
