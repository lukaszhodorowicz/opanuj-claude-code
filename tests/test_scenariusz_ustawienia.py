"""Testy walidatora paczki 4B silnika (wzór: tests/dane/ustawienia-konta.json): pole `aplikacja.konto_ustawien` (wariant lewej kolumny Settings), pole `aplikacja.konektory_do_polaczenia` (karta Connectors zwinięta) i klik `ustawienia-connectors` (Settings → Connectors, zakładka Yours)."""

import copy
import json

import pytest

from tests.pomoc_sesje import DANE, bledy, jest

WZOR = json.loads((DANE / "ustawienia-konta.json").read_text(encoding="utf-8"))


def kopia():
    return copy.deepcopy(WZOR)


def apl(d, nr=0):
    return d["cwiczenia"][nr]["aplikacja"]


def kroki(d, nr=0):
    return d["cwiczenia"][nr]["drogi"][0]["kroki"]


def test_wzor_jest_poprawny():
    assert bledy(WZOR) == []


@pytest.mark.parametrize("konto", ["A", "B"])
def test_konto_ustawien_a_i_b_przechodza(konto):
    d = kopia()
    apl(d)["konto_ustawien"] = konto
    assert bledy(d) == []


@pytest.mark.parametrize("konto", ["C", "a", "", None, 1, True])
def test_konto_ustawien_spoza_a_b_to_blad(konto):
    d = kopia()
    apl(d)["konto_ustawien"] = konto
    assert jest(bledy(d), "pole konto_ustawien"), konto


def test_konto_ustawien_bez_kroku_otwierajacego_okno_settings_to_blad():
    d = kopia()
    d["cwiczenia"][0]["drogi"][0]["kroki"] = [{"typ": "nauczyciel", "tekst": "Zobacz okno."}]
    assert jest(bledy(d), "bez kroku, który otwiera okno Settings")


@pytest.mark.parametrize("cel", ["ustawienia-claude-code", "ustawienia-connectors"])
def test_konto_ustawien_z_klikiem_konta_przechodzi(cel):
    d = kopia()
    kroki(d)[0]["cel"] = cel
    assert not jest(bledy(d), "konto_ustawien")


def test_konto_ustawien_w_cwiczeniu_z_krokami_to_blad():
    from tests.pomoc_sesje import z_krokami

    d = z_krokami()
    d["cwiczenia"][0]["aplikacja"]["konto_ustawien"] = "A"
    assert jest(bledy(d), "pole konto_ustawien tylko w ćwiczeniu z drogami")


@pytest.mark.parametrize("n", [1, 4, 13, 99])
def test_konektory_do_polaczenia_liczba_1_99_przechodzi(n):
    d = kopia()
    apl(d)["konektory_do_polaczenia"] = n
    assert bledy(d) == []


@pytest.mark.parametrize("n", [0, -1, 100, 1000, 2.5, "13", None, True, False])
def test_konektory_do_polaczenia_spoza_zakresu_albo_nie_liczba_to_blad(n):
    d = kopia()
    apl(d)["konektory_do_polaczenia"] = n
    assert jest(bledy(d), "pole konektory_do_polaczenia"), n


KOMUNIKAT_PANEL = "pole konektory_do_polaczenia przy schowanym panelu szczegółów"


def test_konektory_do_polaczenia_przy_panelu_schowany_to_blad_z_komunikatem_o_panelu():
    """Sam warunek `panel: "schowany"` (pole `kontekst` zostaje): komunikat o schowanym panelu pochodzi od pola, bo bez pola go nie ma."""
    d = kopia()
    del apl(d)["konektory_do_polaczenia"]  # wzór ma pole (13): najpierw bez niego
    apl(d)["panel"] = "schowany"
    assert apl(d)["kontekst"] == 9
    bez_pola = bledy(d)
    assert not jest(bez_pola, KOMUNIKAT_PANEL), "bez pola konektory_do_polaczenia panel schowany nie daje tego komunikatu"
    apl(d)["konektory_do_polaczenia"] = 5
    z_polem = bledy(d)
    assert jest(z_polem, KOMUNIKAT_PANEL)
    assert [b for b in z_polem if KOMUNIKAT_PANEL in b and "panelu szczegółów" in b and "z polem kontekst" in b], "komunikat mówi, że w drogach panel jest widoczny tylko z polem kontekst"


def test_konektory_do_polaczenia_w_drogach_bez_kontekstu_to_blad():
    """Inny warunek niż `panel: "schowany"`: ćwiczenie z drogami bez `kontekst` ma panel schowany samo z siebie (panel jest widoczny tylko z polem `kontekst`), więc pole konektorów nie ma gdzie się narysować."""
    d = kopia()
    del apl(d, 1)["kontekst"]
    assert "panel" not in apl(d, 1)
    apl(d, 1)["konektory_do_polaczenia"] = 5
    assert jest(bledy(d), KOMUNIKAT_PANEL)


def test_konektory_do_polaczenia_w_cwiczeniu_z_krokami_przechodzi():
    from tests.pomoc_sesje import z_krokami

    d = z_krokami()
    d["cwiczenia"][0]["aplikacja"]["konektory_do_polaczenia"] = 13
    assert bledy(d) == []


def test_ustawienia_connectors_ma_te_same_reguly_co_ustawienia_claude_code():
    d = kopia()
    k = kroki(d, 1)
    assert k[0] == {"typ": "klik", "cel": "ustawienia-connectors"}
    k.append({"typ": "klik", "cel": "pozycja", "na": "Browse plugins"})
    assert jest(bledy(d), "przy otwartym oknie Settings"), "po otwarciu okna dalej tylko nauczyciel"
    d = kopia()
    kroki(d, 1).pop()  # zdjęty nauczyciel
    assert jest(bledy(d), "droga kończy się zaraz po otwarciu okna Settings")
    d = kopia()
    kroki(d, 1)[0]["nieznane"] = 1
    assert jest(bledy(d), "pole nieznane nie należy do kliku ustawienia-connectors")


def test_ustawienia_connectors_bez_telefonu_przechodzi_i_nie_wymaga_pliku():
    assert bledy(WZOR) == []
    assert not any(k.get("typ") == "plik" for k in kroki(WZOR, 1))


def test_rytm_nauczyciela_po_kliku_ustawienia_connectors():
    from narzedzia import czytelnosc

    assert "ustawienia-connectors" in czytelnosc.KLIKI_TELEFONU


def test_podglad_drogi_z_ustawienia_connectors_to_blad_skladania(tmp_path):
    from narzedzia import strona

    (tmp_path / "lekcja.md").write_text("# Próba\n\n<!-- cwiczenie: cw2 -->\n\n<!-- podglad: cw2 konektory -->\n", encoding="utf-8")
    (tmp_path / "scenariusz.json").write_text(json.dumps(WZOR, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="nie ma kroku plik, artefakt ani strona"):
        strona.zloz_strone(tmp_path)
