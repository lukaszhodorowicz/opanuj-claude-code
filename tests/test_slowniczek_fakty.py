"""Testy odczytu faktów z pliku słowniczka."""
from narzedzia.slowniczek_fakty import fakty_w_slowniczku


def test_brak_pliku(tmp_path):
    assert fakty_w_slowniczku(tmp_path / "brak.yaml", {"a"}) == set()


def test_zwraca_tylko_znane_id(tmp_path):
    plik = tmp_path / "s.yaml"
    plik.write_text(
        "pojecia:\n"
        "  - {pojecie: A, fakt: slowniczek-a}\n"
        "  - {pojecie: B, fakt: slowniczek-nieznany}\n",
        encoding="utf-8",
    )
    assert fakty_w_slowniczku(plik, {"slowniczek-a", "inny"}) == {"slowniczek-a"}


def test_wpis_bez_faktu(tmp_path):
    plik = tmp_path / "s.yaml"
    plik.write_text("pojecia:\n  - {pojecie: A}\n  - tekst\n", encoding="utf-8")
    assert fakty_w_slowniczku(plik, {"x"}) == set()


def test_pusty_plik(tmp_path):
    plik = tmp_path / "s.yaml"
    plik.write_text("", encoding="utf-8")
    assert fakty_w_slowniczku(plik, {"x"}) == set()
