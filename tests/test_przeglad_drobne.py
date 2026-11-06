"""Testy drobnych poprawek z przeglądu: zły znacznik podglądu w lekcji i scenariusz niebędący obiektem."""
import json

import pytest

from narzedzia.czytelnosc import sprawdz_scenariusz
from narzedzia.strona import zloz_strone

SCENARIUSZ = {
    "lekcja": "x",
    "folder_startowy": [],
    "cwiczenia": [{"id": "cw1", "terminale": [{"id": "bez"}]}],
}


def _lekcja(tmp_path, znacznik):
    (tmp_path / "lekcja.md").write_text(
        f"# Tytuł\n\n<!-- cwiczenie: cw1 -->\n\n{znacznik}\n", encoding="utf-8"
    )
    (tmp_path / "scenariusz.json").write_text(json.dumps(SCENARIUSZ), encoding="utf-8")
    return tmp_path


def test_podglad_z_dobrym_cwiczeniem_i_terminalem(tmp_path):
    zloz_strone(_lekcja(tmp_path, "<!-- podglad: cw1 bez -->"))


@pytest.mark.parametrize("znacznik", ["<!-- podglad: cw9 bez -->", "<!-- podglad: cw1 nie-ma -->"])
def test_zly_podglad_zatrzymuje_generator(tmp_path, znacznik):
    with pytest.raises(ValueError, match="podglądu"):
        zloz_strone(_lekcja(tmp_path, znacznik))


def test_scenariusz_lista_daje_komunikat(tmp_path):
    plik = tmp_path / "scenariusz.json"
    plik.write_text("[1, 2]", encoding="utf-8")
    bledy = sprawdz_scenariusz(plik, "x")
    assert len(bledy) == 1 and "obiektem" in bledy[0]
