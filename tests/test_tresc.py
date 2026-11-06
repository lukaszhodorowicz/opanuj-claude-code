"""Testy sprawdzania treści: prawdziwe pliki repozytorium i przypadki na danych próbnych."""
import shutil
from pathlib import Path

import pytest

from narzedzia.tresc import sprawdz_tresc

KORZEN = Path(__file__).resolve().parent.parent
PROBNY = Path(__file__).resolve().parent / "dane" / "tresc"


def test_prawdziwa_tresc_bez_bledow():
    if not (KORZEN / "dane" / "fakty.yaml").is_file() or not (KORZEN / "moduly").is_dir():
        pytest.skip("brak dane/fakty.yaml albo moduly/ - treść jeszcze nie powstała")
    assert sprawdz_tresc(KORZEN) == []


@pytest.fixture
def kopia(tmp_path):
    cel = tmp_path / "korzen"
    shutil.copytree(PROBNY, cel)
    return cel


def zmien(plik: Path, stare: str, nowe: str):
    tekst = plik.read_text(encoding="utf-8")
    assert stare in tekst
    plik.write_text(tekst.replace(stare, nowe), encoding="utf-8")


def test_poprawny_przypadek(kopia):
    assert sprawdz_tresc(kopia) == []


def test_osierocony_fakt(kopia):
    zmien(kopia / "moduly/probny/lekcja.md", "<!-- fakt: skill-opis-limit -->", "")
    zmien(kopia / "moduly/probny/quiz.yaml", "fakt: skill-opis-limit", "fakt: skill-specyfikacja")
    zmien(kopia / "moduly/probny/fiszki.yaml", "fakt: skill-opis-limit", "fakt: skill-specyfikacja")
    assert any("osierocony" in b and "skill-opis-limit" in b for b in sprawdz_tresc(kopia))


def test_odwolanie_do_nieistniejacego_faktu(kopia):
    zmien(kopia / "moduly/probny/lekcja.md", "skill-opis-limit", "nie-ma-takiego")
    assert any("nieistniejącego faktu" in b and "nie-ma-takiego" in b for b in sprawdz_tresc(kopia))


def test_zrodlo_spoza_spisu(kopia):
    zmien(kopia / "dane/fakty.yaml", "docs/en/skills.md#frontmatter-reference", "docs/en/nie-ma.md")
    assert any("nie jest w spisie" in b for b in sprawdz_tresc(kopia))


def test_zly_indeks_poprawna(kopia):
    zmien(kopia / "moduly/probny/quiz.yaml", "poprawna: 0", "poprawna: 3")
    assert any("poza zakresem" in b for b in sprawdz_tresc(kopia))


def test_zdublowany_przod_fiszki(kopia):
    zmien(kopia / "moduly/probny/fiszki.yaml", "Czy opis ma limit?", "Co opisuje specyfikacja skilli?")
    assert any("się powtarza" in b for b in sprawdz_tresc(kopia))


def test_modul_bez_strony_w_mapie(kopia):
    zmien(kopia / "dane/mapa-pokrycia.yaml", "modul: probny", "modul: inny")
    assert any("w mapie brak strony" in b for b in sprawdz_tresc(kopia))


def test_brak_quizu(kopia):
    (kopia / "moduly/probny/quiz.yaml").unlink()
    assert any("brak pliku quiz.yaml" in b for b in sprawdz_tresc(kopia))


@pytest.mark.parametrize(
    "komentarz",
    [
        "<!-- fakt: skill-opis-limit, skill-specyfikacja -->",
        "<!-- fakt skill-opis-limit -->",
        "<!--fakt:Zly_Id-->",
        "<!-- fakt: -->",
    ],
)
def test_zle_zapisane_odwolanie_w_lekcji(kopia, komentarz):
    zmien(kopia / "moduly/probny/lekcja.md", "<!-- fakt: skill-opis-limit -->", komentarz)
    bledy = sprawdz_tresc(kopia)
    assert any("źle zapisane odwołanie" in b and "linia 3" in b and komentarz in b for b in bledy)


def test_odwolanie_bez_odstepow_jest_poprawne(kopia):
    zmien(kopia / "moduly/probny/lekcja.md", "<!-- fakt: skill-opis-limit -->", "<!--fakt:skill-opis-limit-->")
    assert sprawdz_tresc(kopia) == []


@pytest.mark.parametrize("data", ["20261023", "2026-W43-5", "2026-13-40"])
def test_data_sprawdzono_tylko_rrrr_mm_dd(kopia, data):
    zmien(kopia / "dane/fakty.yaml", "sprawdzono: 2026-10-23\n    wersja: \"2.1.309\"\n  - id: skill-spec",
          f"sprawdzono: \"{data}\"\n    wersja: \"2.1.309\"\n  - id: skill-spec")
    assert any("nie jest datą" in b for b in sprawdz_tresc(kopia))


def test_id_faktu_z_koncowym_znakiem_nowej_linii(kopia):
    zmien(kopia / "dane/fakty.yaml", "id: skill-opis-limit", 'id: "skill-opis-limit\\n"')
    assert any("niepoprawny id" in b for b in sprawdz_tresc(kopia))


def test_wersja_liczba_ma_osobny_komunikat(kopia):
    zmien(kopia / "dane/fakty.yaml", 'wersja: "2.1.309"', "wersja: 2.1")
    bledy = sprawdz_tresc(kopia)
    assert any("wersja” musi być tekstem w cudzysłowie" in b for b in bledy)
    assert not any("brak pola „wersja”" in b for b in bledy)


@pytest.fixture
def kopia_z_podkatalogiem(kopia):
    """Kopia danych próbnych z drugim modułem „wielo”, którego lekcja leży w podkatalogu."""
    shutil.copytree(kopia / "moduly/probny", kopia / "moduly/wielo/lekcja-a")
    with (kopia / "dane/mapa-pokrycia.yaml").open("a", encoding="utf-8") as f:
        f.write(
            "- url: https://code.claude.com/docs/en/wielo.md\n"
            "  tytul: Wielo\n  sekcja: Sekcja\n  status: modul\n  modul: wielo\n"
        )
    return kopia


def test_modul_z_lekcja_w_podkatalogu_przechodzi(kopia_z_podkatalogiem):
    (kopia_z_podkatalogiem / "moduly/wielo/BRIEF.md").write_text("plik roboczy", encoding="utf-8")
    assert sprawdz_tresc(kopia_z_podkatalogiem) == []


def test_lekcja_w_podkatalogu_bez_quizu(kopia_z_podkatalogiem):
    (kopia_z_podkatalogiem / "moduly/wielo/lekcja-a/quiz.yaml").unlink()
    bledy = sprawdz_tresc(kopia_z_podkatalogiem)
    assert any("wielo/lekcja-a" in b and "brak pliku quiz.yaml" in b for b in bledy)


def test_modul_tylko_z_plikami_roboczymi_nie_daje_bledu(kopia):
    (kopia / "moduly/wstepny").mkdir()
    (kopia / "moduly/wstepny/BRIEF.md").write_text("plik roboczy", encoding="utf-8")
    assert sprawdz_tresc(kopia) == []


def _scenariusz(kopia, tresc: str):
    (kopia / "moduly/probny/scenariusz.json").write_text(tresc, encoding="utf-8")


def test_fakt_tylko_w_scenariuszu_nie_jest_sierota(kopia):
    zmien(kopia / "moduly/probny/lekcja.md", "<!-- fakt: skill-opis-limit -->", "")
    zmien(kopia / "moduly/probny/quiz.yaml", "fakt: skill-opis-limit", "fakt: skill-specyfikacja")
    zmien(kopia / "moduly/probny/fiszki.yaml", "fakt: skill-opis-limit", "fakt: skill-specyfikacja")
    assert any("osierocony" in b and "skill-opis-limit" in b for b in sprawdz_tresc(kopia))
    _scenariusz(kopia, '{"kroki": [{"wybory": [{"fakt": "skill-opis-limit"}]}]}')
    assert sprawdz_tresc(kopia) == []


def test_nieistniejacy_fakt_w_scenariuszu(kopia):
    _scenariusz(kopia, '{"kroki": [{"fakt": "nie-ma-takiego"}]}')
    assert any("nieistniejącego faktu" in b and "nie-ma-takiego" in b and "probny" in b for b in sprawdz_tresc(kopia))


def test_zly_json_scenariusza(kopia):
    _scenariusz(kopia, "{nie json")
    assert any("scenariusz.json nie daje się wczytać" in b for b in sprawdz_tresc(kopia))


def _bez_odwolan_do_skill_opis_limit(kopia):
    zmien(kopia / "moduly/probny/lekcja.md", "<!-- fakt: skill-opis-limit -->", "")
    zmien(kopia / "moduly/probny/quiz.yaml", "fakt: skill-opis-limit", "fakt: skill-specyfikacja")
    zmien(kopia / "moduly/probny/fiszki.yaml", "fakt: skill-opis-limit", "fakt: skill-specyfikacja")


def _napis_ze_zrodlem(kopia, zrodlo: str):
    (kopia / "dane" / "napisy-interfejsu.yaml").write_text(
        "napisy:\n"
        '  - napis: "Share"\n'
        "    gdzie: claude.ai\n"
        f'    zrodlo: "{zrodlo}"\n',
        encoding="utf-8",
    )


def test_fakt_cytowany_w_zrodle_napisu_nie_jest_sierota(kopia):
    _bez_odwolan_do_skill_opis_limit(kopia)
    assert any("osierocony" in b and "skill-opis-limit" in b for b in sprawdz_tresc(kopia))
    _napis_ze_zrodlem(
        kopia,
        "https://code.claude.com/docs/en/artifacts.md (kontrolka Share; fakt skill-opis-limit), sprawdzono 2026-10-25",
    )
    assert sprawdz_tresc(kopia) == []


def test_samo_id_bez_slowa_fakt_w_napisie_nie_wystarcza(kopia):
    _bez_odwolan_do_skill_opis_limit(kopia)
    _napis_ze_zrodlem(
        kopia,
        "https://code.claude.com/docs/en/skill-opis-limit.md (kontrolka Share), sprawdzono 2026-10-25",
    )
    assert any("osierocony" in b and "skill-opis-limit" in b for b in sprawdz_tresc(kopia))


# Kontrakt dla kodera (skutki s1-s6: fakt cytowany w opisie formatu silnika nie jest sierotą).
# - Pliki: każdy `dane/FORMAT-SCENARIUSZA*.md` w korzeniu (dziś FORMAT-SCENARIUSZA.md
#   i FORMAT-SCENARIUSZA-TRYBY.md). Brak takich plików: działanie jak dotąd, bez wyjątku.
# - Cytat: słowo „fakt” albo „fakty”, spacja, potem jedno albo kilka id w odwrotnych
#   apostrofach, rozdzielonych „, ” albo „ i ”: fakt `a-b`, (fakty `a-b`, `c-d`),
#   fakty `a-b` i `c-d` (ostatnia postać stoi dziś w FORMAT-SCENARIUSZA-TRYBY.md).
# - Id w odwrotnych apostrofach bez „fakt”/„fakty” przed listą nie jest użyciem.
# - Dopasowanie całego id: cytat `abc-def` nie czyni użytym faktu `abc`.
# - Id z cytatu, którego nie ma w dane/fakty.yaml, nie daje błędu (te skutki go nie opisują).
# - Komunikaty sprawdzenia lekcji i komunikat „osierocony” bez zmian.


def _format(kopia, plik: str, tresc: str):
    (kopia / "dane" / plik).write_text(tresc, encoding="utf-8")


def _dopisz_fakty(kopia, *ids: str):
    with (kopia / "dane/fakty.yaml").open("a", encoding="utf-8") as f:
        for fid in ids:
            f.write(
                f"  - id: {fid}\n"
                '    tresc: "Zachowanie silnika."\n'
                "    zrodlo: https://code.claude.com/docs/en/skills.md\n"
                "    sprawdzono: 2026-10-26\n"
                '    wersja: "2.1.309"\n'
            )


def _osierocone(bledy: list[str]) -> set[str]:
    return {b.split("„")[1].split("”")[0] for b in bledy if "osierocony" in b}


def test_s1_fakt_cytowany_w_formacie_scenariusza_nie_jest_sierota(kopia):
    _bez_odwolan_do_skill_opis_limit(kopia)
    assert "skill-opis-limit" in _osierocone(sprawdz_tresc(kopia))
    _format(
        kopia,
        "FORMAT-SCENARIUSZA.md",
        "## Zachowania\n\n- Kliknięcie ścieżki otwiera panel (fakt `skill-opis-limit`).\n",
    )
    assert sprawdz_tresc(kopia) == []


@pytest.mark.parametrize(
    "cytat",
    [
        "(fakty `silnik-tryb-a`, `silnik-tryb-b`)",
        "(fakty `silnik-tryb-a` i `silnik-tryb-b`)",
    ],
)
def test_s2_lista_faktow_w_formacie_trybow(kopia, cytat):
    _dopisz_fakty(kopia, "silnik-tryb-a", "silnik-tryb-b")
    assert {"silnik-tryb-a", "silnik-tryb-b"} <= _osierocone(sprawdz_tresc(kopia))
    _format(kopia, "FORMAT-SCENARIUSZA-TRYBY.md", f"- **Menu** wybiera tryb {cytat}.\n")
    assert sprawdz_tresc(kopia) == []


def test_s3_samo_id_w_apostrofach_bez_slowa_fakt_nie_wystarcza(kopia):
    _bez_odwolan_do_skill_opis_limit(kopia)
    _format(kopia, "FORMAT-SCENARIUSZA.md", "- Pole ma wzór `skill-opis-limit`.\n")
    assert "skill-opis-limit" in _osierocone(sprawdz_tresc(kopia))


def test_s4_id_bedace_poczatkiem_cytowanego_id_zostaje_sierota(kopia):
    _bez_odwolan_do_skill_opis_limit(kopia)
    _format(
        kopia,
        "FORMAT-SCENARIUSZA.md",
        "- Panel (fakt `skill-opis-limit-dlugi`).\n- Lista (fakty `skill-opis-limit-x`, `skill-opis-limitu`).\n",
    )
    assert "skill-opis-limit" in _osierocone(sprawdz_tresc(kopia))


def test_s5_bez_plikow_formatu_dziala_jak_dotad(kopia):
    assert not list((kopia / "dane").glob("FORMAT-SCENARIUSZA*.md"))
    assert sprawdz_tresc(kopia) == []
    _bez_odwolan_do_skill_opis_limit(kopia)
    assert _osierocone(sprawdz_tresc(kopia)) == {"skill-opis-limit"}


def test_s6_fakt_bez_odwolan_dalej_sierota_przy_plikach_formatu(kopia):
    _bez_odwolan_do_skill_opis_limit(kopia)
    _format(kopia, "FORMAT-SCENARIUSZA.md", "- Panel (fakt `skill-specyfikacja`).\n")
    _format(kopia, "FORMAT-SCENARIUSZA-TRYBY.md", "- Menu (fakty `skill-specyfikacja`).\n")
    assert _osierocone(sprawdz_tresc(kopia)) == {"skill-opis-limit"}


def test_s6_sprawdzenie_lekcji_bez_zmian_przy_plikach_formatu(kopia):
    _format(kopia, "FORMAT-SCENARIUSZA.md", "- Panel (fakt `nie-ma-takiego`).\n")
    zmien(kopia / "moduly/probny/lekcja.md", "skill-opis-limit", "nie-ma-takiego")
    bledy = sprawdz_tresc(kopia)
    assert any("nieistniejącego faktu" in b and "nie-ma-takiego" in b and "probny" in b for b in bledy)
