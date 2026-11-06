"""Testy sprawdzania czytelności lekcji: małe dane w tmp_path i prawdziwe lekcje repozytorium.

Kontrakt dla kodera (D-2026-10-26-55, zastępuje limity z D-2026-10-26-54; plik `narzedzia/czytelnosc.py`):
- s1: narzędzie nie ogranicza liczby słów lekcji ani słów przed pierwszym znacznikiem
  `<!-- cwiczenie: ... -->`. Znikają błędy „N słów, limit 450.” i „N słów przed pierwszym
  ćwiczeniem, limit 80.”. Lekcja z 2000 słów i 300 słowami wstępu daje `bledy == []`,
  a `python -m narzedzia.czytelnosc --korzen <katalog>` (`main([...])`) zwraca 0.
- s2: podsumowanie (`sprawdz_czytelnosc(korzen)[1]`) dalej ma jeden wiersz na lekcję w postaci
  „<ścieżka>: N słów” albo „<ścieżka>: N słów, M przed pierwszym ćwiczeniem”, bez dopisków.
  Część `## Źródła` (od tej linii do następnej linii `## ` albo do końca pliku) nie liczy się do N;
  nagłówek kończący część i wszystko za nim liczy się normalnie.
- s3: limit 25 słów wypowiedzi nauczyciela (krok `nauczyciel` i pole `nauczyciel_start`) oraz reguła
  „nauczyciel najdalej 2 kroki po zmianie” bez zmian, także w bardzo długiej lekcji.
- s4: lista `WYJATKI_OD_LIMITU_SLOW` znika razem z błędem „wyjątek dla nieistniejącej lekcji”
  i dopiskiem „(wyjątek od limitu słów)” w podsumowaniu. Wywołanie `sprawdz_czytelnosc(korzen)`
  z jednym argumentem nie zgłasza żadnego błędu o wyjątkach, także w katalogu bez `moduly/skille/`.
  Drugi argument zostaje opcjonalny i nic nie zmienia: trzy testy w
  `tests/test_aplikacja_tryby_zmiana.py` i `tests/test_aplikacja_tryby_folder.py` wołają
  `sprawdz_czytelnosc(tmp_path, ())`.
"""
import json
from pathlib import Path

from narzedzia.czytelnosc import main, sprawdz_czytelnosc

KORZEN = Path(__file__).resolve().parent.parent


def sprawdz(korzen):
    """Pusta lista wyjątków odcina dzisiejszą listę z modułu, żeby s1-s3 padały tylko z powodu limitów; s4 woła funkcję z jednym argumentem."""
    return sprawdz_czytelnosc(korzen, ())


def zrob(tmp_path, lekcja: str, kroki=None, cwiczenie_extra=None) -> Path:
    katalog = tmp_path / "moduly" / "m" / "l"
    katalog.mkdir(parents=True)
    (katalog / "lekcja.md").write_text(lekcja, encoding="utf-8")
    if kroki is not None:
        cw = {"id": "cw1", "zadania": [{"przebiegi": {"bez": kroki}}]}
        cw.update(cwiczenie_extra or {})
        (katalog / "scenariusz.json").write_text(
            json.dumps({"lekcja": "l", "cwiczenia": [cw]}), encoding="utf-8"
        )
    return tmp_path


def slowa(n: int) -> str:
    return " ".join(["słowo"] * n)


NAUCZ = {"typ": "nauczyciel", "tekst": "Patrz na pasek."}
FOLDER = {"typ": "folder", "akcja": "utworz", "nazwa": "x"}


def test_poprawny_przypadek(tmp_path):
    zrob(tmp_path, slowa(40) + "\n<!-- cwiczenie: cw1 -->\n" + slowa(100), [FOLDER, NAUCZ])
    bledy, podsumowanie = sprawdz(tmp_path)
    assert bledy == []
    assert "140 słów" in podsumowanie[0] and "40 przed" in podsumowanie[0]


def test_liczenie_pomija_komentarze_znaczniki_i_adresy(tmp_path):
    tekst = "<!-- fakt: a\nb c d -->\n<b>jeden</b> [dwa trzy](https://x.pl/a/b) ---\n"
    zrob(tmp_path, tekst)
    assert "3 słów" in sprawdz(tmp_path)[1][0]


ZRODLA = "\n## Źródła\n" + slowa(30) + "\n"


def test_s2_czesc_po_zrodlach_liczy_sie(tmp_path):
    # Część po źródłach ma 20 słów: nagłówek „Inna część” (2) i 18 słów treści.
    inna = "\n## Inna część\n" + slowa(18) + "\n"
    zrob(tmp_path, slowa(440) + "\n" + ZRODLA + inna)
    opis = sprawdz(tmp_path)[1][0]
    assert opis.endswith(": 460 słów"), opis


def test_s2_podsumowanie_bez_zrodel(tmp_path):
    zrob(tmp_path, slowa(440) + "\n" + ZRODLA)
    opis = sprawdz(tmp_path)[1][0]
    assert opis.endswith(": 440 słów"), opis


def test_za_dluga_wypowiedz_nauczyciela(tmp_path):
    zrob(tmp_path, "tekst", [{"typ": "nauczyciel", "tekst": slowa(26)}])
    assert any("26 słów, limit 25" in b for b in sprawdz(tmp_path)[0])


def test_za_dlugie_pole_nauczyciel_start(tmp_path):
    zrob(tmp_path, "tekst", [], {"nauczyciel_start": slowa(26)})
    assert any("nauczyciel_start" in b and "limit 25" in b for b in sprawdz(tmp_path)[0])


def test_zmiana_bez_nauczyciela(tmp_path):
    pisz = {"typ": "pisz", "tekst": "a"}
    zrob(tmp_path, "tekst", [FOLDER, pisz, pisz, NAUCZ])
    bledy = sprawdz(tmp_path)[0]
    assert any("przebieg bez, krok 1 (folder): brak nauczyciela w 2 kolejnych krokach" in b for b in bledy)


def test_zmiana_z_nauczycielem_po_jednym_kroku(tmp_path):
    zrob(tmp_path, "tekst", [{"typ": "tryb", "na": "plan"}, {"typ": "czekaj", "ms": 1}, NAUCZ])
    assert sprawdz(tmp_path)[0] == []


def test_zmiana_na_koncu_listy(tmp_path):
    zrob(tmp_path, "tekst", [NAUCZ, FOLDER])
    assert any("krok 2 (folder)" in b for b in sprawdz(tmp_path)[0])


def test_zmiana_w_zagniezdzonej_liscie_dalej(tmp_path):
    menu = {"typ": "menu", "opcje": [{"napis": "a", "dalej": [FOLDER]}]}
    zrob(tmp_path, "tekst", [menu, NAUCZ])
    bledy = sprawdz(tmp_path)[0]
    assert any("opcja 1" in b and "krok 1 (folder)" in b for b in bledy)


def test_prawdziwe_lekcje_przechodza():
    bledy, podsumowanie = sprawdz_czytelnosc(KORZEN)
    assert bledy == []
    assert podsumowanie


# ---------- D-2026-10-26-55: bez limitu słów lekcji i wstępu ----------

PISZ = {"typ": "pisz", "tekst": "a"}


def test_s1_dluga_lekcja_bez_bledu(tmp_path):
    zrob(tmp_path, slowa(2000))
    assert sprawdz(tmp_path)[0] == []


def test_s1_dlugi_wstep_bez_bledu(tmp_path):
    zrob(tmp_path, slowa(300) + "\n<!-- cwiczenie: cw1 -->\n" + slowa(100), [FOLDER, NAUCZ])
    assert sprawdz(tmp_path)[0] == []


def test_s1_polecenie_przechodzi_na_dlugiej_lekcji(tmp_path, capsys):
    zrob(tmp_path, slowa(300) + "\n<!-- cwiczenie: cw1 -->\n" + slowa(1700))
    kod = main(["--korzen", str(tmp_path)])
    wyjscie = capsys.readouterr().out
    assert kod == 0, wyjscie
    assert "moduly/m/l/lekcja.md: 2000 słów, 300 przed pierwszym ćwiczeniem" in wyjscie


def test_s2_podsumowanie_dlugiej_lekcji(tmp_path):
    zrob(tmp_path, slowa(300) + "\n<!-- cwiczenie: cw1 -->\n" + slowa(1700) + ZRODLA)
    bledy, podsumowanie = sprawdz(tmp_path)
    assert bledy == []
    assert podsumowanie == ["moduly/m/l/lekcja.md: 2000 słów, 300 przed pierwszym ćwiczeniem"]


def test_s3_limit_nauczyciela_w_dlugiej_lekcji(tmp_path):
    zrob(tmp_path, slowa(2000), [{"typ": "nauczyciel", "tekst": slowa(26)}])
    bledy = sprawdz(tmp_path)[0]
    assert len(bledy) == 1 and "26 słów, limit 25" in bledy[0], bledy


def test_s3_nauczyciel_po_zmianie_w_dlugiej_lekcji(tmp_path):
    zrob(tmp_path, slowa(300) + "\n<!-- cwiczenie: cw1 -->\n" + slowa(1700), [FOLDER, PISZ, PISZ, NAUCZ])
    bledy = sprawdz(tmp_path)[0]
    assert len(bledy) == 1, bledy
    assert "przebieg bez, krok 1 (folder): brak nauczyciela w 2 kolejnych krokach" in bledy[0]


def test_s4_bez_bledow_o_wyjatkach_w_katalogu_bez_skilli(tmp_path):
    zrob(tmp_path, "tekst")
    bledy, podsumowanie = sprawdz_czytelnosc(tmp_path)
    assert not any("wyjątek" in b for b in bledy), bledy
    assert podsumowanie == ["moduly/m/l/lekcja.md: 1 słów"]


def test_s4_prawdziwe_podsumowanie_bez_dopisku_wyjatku():
    bledy, podsumowanie = sprawdz_czytelnosc(KORZEN)
    assert bledy == []
    assert not any("wyjątek" in p for p in podsumowanie), podsumowanie
