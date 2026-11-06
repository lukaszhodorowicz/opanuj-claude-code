"""Testy eksportu fiszek do Anki na mini-korzeniu próbnym."""
import json
import sqlite3
import zipfile
from pathlib import Path

import yaml

from narzedzia.fiszki_anki import zapisz

PROBNY = Path(__file__).resolve().parent / "dane" / "tresc"


def notatki(apkg: Path, tmp: Path) -> list[tuple]:
    with zipfile.ZipFile(apkg) as z:
        z.extract("collection.anki2", tmp)
    polaczenie = sqlite3.connect(tmp / "collection.anki2")
    try:
        return polaczenie.execute("select guid, flds from notes order by guid").fetchall()
    finally:
        polaczenie.close()


def test_apkg_powstaje_z_wszystkimi_notatkami(tmp_path):
    wyjscie = tmp_path / "build" / "probna.apkg"
    assert zapisz(PROBNY, wyjscie) == 2
    assert wyjscie.is_file()
    assert len(notatki(wyjscie, tmp_path)) == 2


def test_guid_stale_miedzy_przebiegami(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir()
    b.mkdir()
    zapisz(PROBNY, a / "x.apkg")
    zapisz(PROBNY, b / "x.apkg")
    assert [n[0] for n in notatki(a / "x.apkg", a)] == [n[0] for n in notatki(b / "x.apkg", b)]


def korzen_z_fiszkami(katalog: Path, modul: str, fiszki: list[dict]) -> Path:
    """Buduje minimalny korzeń z jednym modułem i podanymi fiszkami."""
    (katalog / "moduly" / modul).mkdir(parents=True)
    (katalog / "moduly" / modul / "fiszki.yaml").write_text(
        yaml.safe_dump({"fiszki": fiszki}, allow_unicode=True), encoding="utf-8"
    )
    return katalog


def test_guid_zalezy_od_modulu_i_przodu_nie_od_tylu(tmp_path):
    k1 = korzen_z_fiszkami(tmp_path / "k1", "m", [{"przod": "P", "tyl": "tył A"}])
    k2 = korzen_z_fiszkami(tmp_path / "k2", "m", [{"przod": "P", "tyl": "tył B"}])
    k3 = korzen_z_fiszkami(tmp_path / "k3", "m", [{"przod": "Q", "tyl": "tył A"}])
    guidy = []
    for k in (k1, k2, k3):
        zapisz(k, k / "x.apkg")
        guidy.append(notatki(k / "x.apkg", k)[0][0])
    assert guidy[0] == guidy[1]
    assert guidy[0] != guidy[2]


def test_nazwy_talii_nadrzedna_i_podtalia(tmp_path):
    k = korzen_z_fiszkami(tmp_path, "modul1", [{"przod": "P", "tyl": "T"}])
    zapisz(k, k / "x.apkg")
    with zipfile.ZipFile(k / "x.apkg") as z:
        z.extract("collection.anki2", tmp_path)
    polaczenie = sqlite3.connect(tmp_path / "collection.anki2")
    try:
        talie = json.loads(polaczenie.execute("select decks from col").fetchone()[0])
    finally:
        polaczenie.close()
    nazwy = {t["name"] for t in talie.values()}
    assert "Przewodnik po Claude Code" in nazwy
    assert "Przewodnik po Claude Code::modul1" in nazwy


def test_pola_sa_zamieniane_na_html(tmp_path):
    k = korzen_z_fiszkami(
        tmp_path, "m", [{"przod": "Gdzie `x`?", "tyl": "W <nazwa>\ndalej `kod`"}]
    )
    zapisz(k, k / "x.apkg")
    pola = notatki(k / "x.apkg", k)[0][1].split("\x1f")
    assert pola[0] == "Gdzie <code>x</code>?"
    assert "&lt;nazwa&gt;" in pola[1]
    assert "<br>" in pola[1]
    assert "<code>kod</code>" in pola[1]
