"""Testy wypisywania polskich napisów ze scenariusza: małe dane i prawdziwa lekcja.

KONTRAKT DLA KODERA (uwaga KW3 krytyka karty planu, D-2026-10-26-54)

narzedzia/tekst_pl.py wypisuje polskie pola kroku `plan` (wzór: tests/dane/plan-przyciski.json),
ścieżką w tym samym zapisie co reszta (kropki dla kluczy, [n] dla list):
- `…kroki[5].tytul` (już działa),
- `…kroki[5].sekcje[<i>].naglowek`,
- `…kroki[5].sekcje[<i>].punkty[<j>]` (każdy punkt osobno),
- `…kroki[5].przyciski.revise.poprawka`,
- `…kroki[5].przyciski.<klucz>.kroki[<n>].tekst` dla kroków claude, pisz, nauczyciel,
  także w karcie planu zagnieżdżonej w krokach revise.
Klucze przycisków (accept, auto, revise) i pola techniczne (typ, akcja, nazwa, plik, do) nie
trafiają na listę. Polecenie: `uv run python -m narzedzia.tekst_pl <katalog lekcji>`, jedna linia
na pole: `<ścieżka>\t<tekst>`.
"""
import json
from pathlib import Path

from narzedzia.napisy import wczytaj_napisy
from narzedzia.tekst_pl import PLIK_NAPISOW, main, polskie_pola

KORZEN = Path(__file__).resolve().parent.parent

SCENARIUSZ = {
    "lekcja": "l",
    "cwiczenia": [
        {
            "id": "cw1",
            "tytul": "Pierwsze ćwiczenie",
            "nauczyciel_start": "Zacznij tutaj.",
            "cele": {"oferta.txt": "Napisz ofertę"},
            "zadania": [
                {
                    "przebiegi": {
                        "bez": [
                            {"typ": "pisz", "tekst": "Zrób listę", "fakt": "f1"},
                            {
                                "typ": "menu",
                                "tytul": "Read outside the working directories",
                                "opcje": [{"pl": "Tak, pozwól", "napis": "Yes, allow", "id": "o1"}],
                            },
                        ]
                    }
                }
            ],
        }
    ],
}


def test_male_dane():
    wynik = dict(polskie_pola(SCENARIUSZ, []))
    assert wynik["cwiczenia[0].tytul"] == "Pierwsze ćwiczenie"
    assert wynik["cwiczenia[0].nauczyciel_start"] == "Zacznij tutaj."
    assert wynik["cwiczenia[0].cele.oferta.txt"] == "Napisz ofertę"
    sciezki = list(wynik)
    tekst_pisz = [s for s in sciezki if s.endswith("[0].tekst")]
    assert len(tekst_pisz) == 1 and wynik[tekst_pisz[0]] == "Zrób listę"
    assert any(s.endswith(".opcje[0].pl") for s in sciezki)
    teksty = set(wynik.values())
    assert "f1" not in teksty and "o1" not in teksty and "cw1" not in teksty
    assert "Yes, allow" not in teksty
    assert not any(s.endswith((".fakt", ".id", ".napis")) for s in sciezki)


def test_napis_interfejsu_pominiety():
    napisy = [{"napis": "Read outside the working directories", "gdzie": "menu"}]
    teksty = {t for _, t in polskie_pola(SCENARIUSZ, napisy)}
    assert "Read outside the working directories" not in teksty
    assert "Zrób listę" in teksty


def test_wzor_pomija():
    napisy = [{"wzor": "^Read outside", "gdzie": "menu"}]
    teksty = {t for _, t in polskie_pola(SCENARIUSZ, napisy)}
    assert "Read outside the working directories" not in teksty


def test_linijki():
    s = {"x": {"linijki": ["Jedna", {"tekst": "Dwa", "kto": "a"}]}}
    assert polskie_pola(s, []) == [("x.linijki[0]", "Jedna"), ("x.linijki[1].tekst", "Dwa")]


def test_prawdziwa_lekcja(capsys):
    katalog = KORZEN / "moduly" / "pierwsza-praca" / "sprawdz-i-cofnij"
    scenariusz = json.loads((katalog / "scenariusz.json").read_text(encoding="utf-8"))
    napisy = wczytaj_napisy(PLIK_NAPISOW)
    wynik = polskie_pola(scenariusz, napisy)
    assert wynik
    assert any(s.endswith(".nauczyciel_start") for s, _ in wynik)
    wzorce = [w for w in napisy if "napis" in w]
    assert not any(t == w["napis"] for _, t in wynik for w in wzorce)
    assert main([str(katalog)]) == 0
    linie = capsys.readouterr().out.splitlines()
    assert len(linie) == len(wynik)


def test_brak_scenariusza(tmp_path, capsys):
    assert main([str(tmp_path)]) == 1
    assert "scenariusz.json" in capsys.readouterr().err


def test_tresc_planu_i_polska_zgoda():
    s = {"k": [
        {"typ": "menu", "ramka": "plan", "tresc": "plan bez liter"},
        {"typ": "menu", "ramka": "zgoda", "tresc": "mkdir 2026-09"},
        {"typ": "menu", "ramka": "zgoda", "tresc": "Sprzedaż 2026-09"},
    ]}
    assert polskie_pola(s, []) == [("k[0].tresc", "plan bez liter"), ("k[2].tresc", "Sprzedaż 2026-09")]


def test_tryb_planowania(capsys, tmp_path):
    # dawna, terminalowa wersja lekcji tryb-planowania (git show a58e7a3)
    katalog = tmp_path / "tryb-planowania"
    katalog.mkdir()
    (katalog / "scenariusz.json").write_bytes(
        (KORZEN / "tests" / "dane" / "tryb-planowania-terminal.json").read_bytes()
    )
    scenariusz = json.loads((katalog / "scenariusz.json").read_text(encoding="utf-8"))
    wynik = polskie_pola(scenariusz, wczytaj_napisy(PLIK_NAPISOW))
    assert any(s.endswith(".tresc") and "Porządek w fakturach" in t for s, t in wynik)
    teksty = {t for _, t in wynik}
    # Cytat „Do you want to proceed?” bywa w polskim zdaniu nauczyciela, więc sprawdzam całe napisy.
    assert "mkdir 2026-09 2026-10" not in teksty
    assert "Do you want to proceed?" not in teksty
    assert not any(s.endswith(".tresc") and t.startswith(("mkdir", "mv ")) for s, t in wynik)
    assert main([str(katalog)]) == 0
    linie = capsys.readouterr().out.splitlines()
    assert len(linie) == len(wynik)
    assert all(l.count("\t") == 1 for l in linie)


# --- KW3: polskie pola karty planu ---

PLAN = KORZEN / "tests" / "dane" / "plan-przyciski.json"
KROK_PLANU = "cwiczenia[0].etapy[0].etapy[0].kroki[5]"


def _pola_planu(capsys, tmp_path):
    """Pola z polecenia na prawdziwym pliku wzoru karty planu: słownik ścieżka → tekst."""
    (tmp_path / "scenariusz.json").write_bytes(PLAN.read_bytes())
    assert main([str(tmp_path)]) == 0
    linie = capsys.readouterr().out.splitlines()
    assert all(l.count("\t") == 1 for l in linie)
    return dict(l.split("\t") for l in linie)


def test_kw3_naglowki_sekcji(capsys, tmp_path):
    pola = _pola_planu(capsys, tmp_path)
    assert pola.get(f"{KROK_PLANU}.sekcje[0].naglowek") == "Teczki"
    assert pola.get(f"{KROK_PLANU}.sekcje[1].naglowek") == "Przeniesienia"


def test_kw3_punkty_sekcji(capsys, tmp_path):
    pola = _pola_planu(capsys, tmp_path)
    assert pola.get(f"{KROK_PLANU}.sekcje[0].punkty[0]") == "Założę teczki 2026-09 i 2026-10."
    assert pola.get(f"{KROK_PLANU}.sekcje[1].punkty[1]") == "Do 2026-10 przeniosę fakturę ikea."


def test_kw3_poprawka_revise(capsys, tmp_path):
    pola = _pola_planu(capsys, tmp_path)
    assert pola.get(f"{KROK_PLANU}.przyciski.revise.poprawka") == "Skanu nie przenoś, najpierw go sprawdzę."


def test_kw3_kroki_przyciskow(capsys, tmp_path):
    pola = _pola_planu(capsys, tmp_path)
    p = f"{KROK_PLANU}.przyciski"
    assert pola.get(f"{p}.auto.kroki[0].tekst") == "Zakładam teczki i przenoszę faktury według planu."
    assert pola.get(f"{p}.accept.kroki[0].tekst") == "Zaczynam od teczki 2026-09. Przed każdą zmianą zapytam o zgodę."
    assert pola.get(f"{p}.revise.kroki[1].tekst") == "Dobrze, skan zostaje na miejscu. Oto poprawiony plan."
    nowy = f"{p}.revise.kroki[2]"
    assert pola.get(f"{nowy}.sekcje[0].naglowek") == "Przeniesienia"
    assert pola.get(f"{nowy}.sekcje[0].punkty[1]") == "Skan zostawię na miejscu."
    assert pola.get(f"{nowy}.przyciski.auto.kroki[0].tekst") == "Przenoszę faktury z września. Skan zostaje."
    teksty = set(pola.values())
    assert not teksty & {"accept", "auto", "revise", "utworz", "przenies", "2026-09", "skan_0012.pdf"}
