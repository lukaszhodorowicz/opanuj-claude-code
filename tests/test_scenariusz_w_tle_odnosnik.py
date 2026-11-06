"""Testy nieaktywnego napisu „N running tasks” (rysowany przy co najmniej dwóch pracach w tle, napis z listy napisów), napisów, rytmu nauczyciela i filtrów języka w pracy w tle symulatora aplikacji (wzór: tests/dane/subagent-zbiera-panel-w-tle.json; walidator: tests/test_scenariusz_w_tle.py; klik `running-tasks` jako błąd: tests/test_scenariusz_w_tle_napis_nieaktywny.py)."""

import copy
import re

from narzedzia import czytelnosc
from narzedzia import scenariusz as sc
from narzedzia.tekst_pl import polskie_pola
from tests.pomoc_w_tle import KORZEN, NAPISY, bledy, dane, indeks, jest, kroki  # noqa: F401


def test_jedna_praca_w_tle_nie_wymaga_napisu_running_tasks(dane):
    """Przy jednej pracy napisu nie ma (wzór napisu: liczba od 2), więc „1 running tasks” spoza listy napisów nie jest błędem."""
    w = next(k for k in kroki(dane) if "w_tle" in k)["w_tle"]
    del w[1]
    assert not sc._Napisy(NAPISY).jest("1 running tasks", "aplikacja")
    assert not jest(bledy(dane), "running tasks")


def test_klik_wpisu_przy_otwartym_menu_odrzucony(dane):
    """Klik we wpis zaraz po otwarciu menu ⋮, zanim kursant kliknie Background tasks: menu stoi, dalej tylko nauczyciel i klik background-tasks."""
    k = kroki(dane)
    k.insert(indeks(dane, "klik", "menu-paska") + 1, {"typ": "klik", "cel": "wpis-w-tle", "nr": 1})
    assert jest(bledy(dane), "krok klik przy otwartym menu ⋮")


def test_napis_odnosnika_pasuje_do_wzoru_z_listy_napisow():
    lista = sc._Napisy(NAPISY)
    for n in (2, 3, 10, 19):
        assert lista.jest(f"{n} running tasks", "aplikacja"), n
    for n in (0, 1):
        assert not lista.jest(f"{n} running tasks", "aplikacja"), n


def test_napisy_pracy_w_tle_sa_na_liscie_napisow_interfejsu_i_w_stalej_strony():
    js = (KORZEN / "strona" / "aplikacja-w-tle-widok.js").read_text(encoding="utf-8")
    blok = re.search(r"PK\.NAPISY_W_TLE = \{(.*?)\};", js, re.S).group(1)
    napisy = re.findall(r':\s*"([^"]+)"', blok)
    assert napisy == ["Background tasks", "Running", "Agent", "View transcript"]
    lista = sc._Napisy(NAPISY)
    assert all(lista.jest(n, "aplikacja") for n in napisy)
    assert "running tasks" in js and lista.jest("2 running tasks", "aplikacja")


def test_strona_nie_rysuje_napisow_bez_zrodla():
    kod = "".join(re.sub(r"/\*.*?\*/", "", (KORZEN / "strona" / n).read_text(encoding="utf-8"), flags=re.S) for n in ("aplikacja-w-tle.js", "aplikacja-w-tle-widok.js"))
    for napis in ("Finished", "Files", "iOS Sim", "Keep computer awake", "Only for this session", "Stop", "Clear", "Tokens", "tokens", "tool uses", "Bash", "Counted"):
        assert napis not in kod, f"napis „{napis}” nie ma wpisu w napisach interfejsu: ma być szarym paskiem albo wcale"


def test_rytm_nauczyciela_po_background_tasks_i_wpisie(dane):
    k = kroki(dane)
    for cel in ("background-tasks", "wpis-w-tle"):
        d = copy.deepcopy(dane)
        kr = kroki(d)
        i = indeks(d, "klik", cel)
        assert kr[i + 1]["typ"] == "nauczyciel"
        kr[i + 1] = {"typ": "mysli"}  # nauczyciel zamieniony na pauzę
        kr.insert(i + 2, {"typ": "mysli"})
        kr.insert(i + 3, {"typ": "mysli"})
        d_plik = d["cwiczenia"][0]
        zle = czytelnosc._sprawdz_liste_krokow(d_plik["drogi"][0]["kroki"], "", "t", czytelnosc.ZMIANY_APLIKACJI)
        assert any(f"krok {i + 1} (klik)" in b and "brak nauczyciela" in b for b in zle), cel
    assert czytelnosc._sprawdz_liste_krokow(k, "", "t", czytelnosc.ZMIANY_APLIKACJI) == []


def test_tytul_zadanie_i_wynik_trafiaja_do_filtrow_jezyka(dane):
    pola = dict(polskie_pola(dane, NAPISY))
    prace = next(k for k in kroki(dane) if "w_tle" in k)["w_tle"]
    for i, praca in enumerate(prace):
        szukane = {"tytul": praca["tytul"], "zadanie": praca["zadanie"], "wynik[0]": praca["wynik"][0]}
        for pole, tekst in szukane.items():
            sciezki = [s for s in pola if s.endswith(f".w_tle[{i}].{pole}")]
            assert len(sciezki) == 1 and pola[sciezki[0]] == tekst, (i, pole)
