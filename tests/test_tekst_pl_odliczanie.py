"""Testy wypisywania polskich napisów ze scenariusza dla kroku `zgoda` z `odliczanie_ms` i `polecenie` (wzór: tests/dane/hook-zgoda-polecenie.json): pigułka „Claude czeka: N s” trafia na listę, nazwa polecenia terminala nie."""

import copy
import json
from pathlib import Path

from narzedzia.napisy import wczytaj_napisy
from narzedzia.tekst_pl import PLIK_NAPISOW, TEKST_ODLICZANIA, main, polskie_pola, tekst_odliczania

WZOR = json.loads((Path(__file__).parent / "dane" / "hook-zgoda-polecenie.json").read_text(encoding="utf-8"))
NAPISY = wczytaj_napisy(PLIK_NAPISOW)
SCIEZKA = "cwiczenia[0].drogi[0].kroki[7]"


def test_pigulka_odliczania_na_liscie_napisow_kursu():
    pola = dict(polskie_pola(WZOR, NAPISY))
    assert pola[f"{SCIEZKA}.odliczanie_ms"] == "Claude czeka: 6 s"


def test_nazwa_polecenia_terminala_nie_jest_tekstem_kursu():
    pola = polskie_pola(WZOR, NAPISY)
    assert not any(s.endswith(".polecenie") for s, _ in pola)
    assert "zip" not in [t for _, t in pola]


def test_inne_pola_kroku_zgoda_nie_trafiaja_na_liste():
    pola = dict(polskie_pola(WZOR, NAPISY))
    assert f"{SCIEZKA}.fakt" not in pola and f"{SCIEZKA}.typ" not in pola
    assert "cwiczenia[0].drogi[1].kroki[3].plik" not in pola


def test_karta_bez_odliczania_nie_daje_pigulki():
    d = copy.deepcopy(WZOR)
    del d["cwiczenia"][0]["drogi"][0]["kroki"][7]["odliczanie_ms"]
    assert not any(s.endswith(".odliczanie_ms") for s, _ in polskie_pola(d, NAPISY))


def test_odliczanie_poza_zgoda_nie_daje_pigulki():
    s = {"cwiczenia": [{"drogi": [{"kroki": [{"typ": "mysli", "odliczanie_ms": 3000}]}]}]}
    assert polskie_pola(s, NAPISY) == []


def test_etapy_nie_graja_odliczania_wiec_pigulka_nie_trafia_na_liste():
    etapy = json.loads((Path(__file__).parent / "dane" / "okno-zgody-tryby.json").read_text(encoding="utf-8"))
    zgoda = next(k for e in etapy["cwiczenia"][0]["etapy"] for k in e["kroki"] if k["typ"] == "zgoda")
    zgoda["odliczanie_ms"] = 6000
    assert not any(s.endswith(".odliczanie_ms") or t.startswith("Claude czeka") for s, t in polskie_pola(etapy, NAPISY))


def test_sekundy_zaokraglane_w_gore_jak_w_oknie():
    assert [tekst_odliczania(ms) for ms in (1000, 1001, 2500, 5999, 6000, 10000)] == [
        "Claude czeka: 1 s", "Claude czeka: 2 s", "Claude czeka: 3 s", "Claude czeka: 6 s", "Claude czeka: 6 s", "Claude czeka: 10 s"
    ]
    assert TEKST_ODLICZANIA.format(4) == "Claude czeka: 4 s"


def test_polecenie_wypisuje_pigulke_w_linii(tmp_path, capsys):
    (tmp_path / "scenariusz.json").write_text(json.dumps(WZOR, ensure_ascii=False), encoding="utf-8")
    assert main([str(tmp_path)]) == 0
    linie = capsys.readouterr().out.splitlines()
    assert f"{SCIEZKA}.odliczanie_ms\tClaude czeka: 6 s" in linie
