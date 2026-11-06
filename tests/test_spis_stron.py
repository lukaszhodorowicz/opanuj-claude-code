"""Testy wczytywania spisu stron na prawdziwej migawce llms.txt."""
from pathlib import Path

from narzedzia.spis_stron import wczytaj_strony

KORZEN = Path(__file__).resolve().parent.parent
SPIS = KORZEN / "dane" / "zrodla" / "llms.txt"


def test_228_unikalnych_stron():
    strony = wczytaj_strony(SPIS)
    adresy = [s["url"] for s in strony]
    assert len(strony) == 228
    assert len(set(adresy)) == 228


def test_zadna_z_llms_i_tylko_en_md():
    for s in wczytaj_strony(SPIS):
        assert "_llms" not in s["url"]
        assert s["url"].startswith("https://code.claude.com/docs/en/")
        assert s["url"].endswith(".md")


def test_kazda_z_tytulem_i_sekcja():
    for s in wczytaj_strony(SPIS):
        assert s["tytul"].strip()
        assert s["sekcja"].strip()


def test_pierwsze_wystapienie_i_kolejnosc():
    strony = wczytaj_strony(SPIS)
    assert strony[0]["url"] == "https://code.claude.com/docs/en/overview.md"
    assert strony[0]["sekcja"] == "Getting started"
