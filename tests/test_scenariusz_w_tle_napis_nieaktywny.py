"""Testy walidatora (KD4): napis „N running tasks” pod odpowiedzią jest nieaktywny, więc celu `running-tasks` nie ma i scenariusz z takim klikiem jest błędny; panel zadań otwiera tylko pozycja `Background tasks` w menu ⋮ (wzór: tests/dane/subagent-zbiera-panel-w-tle.json; fakt `aplikacja-link-running-tasks-w-rozmowie` opisuje wygląd napisu, fakt `aplikacja-klik-running-tasks-otwiera-panel` nie wskazuje, co się klika)."""

from narzedzia import czytelnosc, scenariusz_w_tle
from tests.pomoc_w_tle import bledy, dane, indeks, jest, kroki  # noqa: F401


def test_klik_running_tasks_odrzucony_jako_nieznany_cel(dane):
    k = kroki(dane)
    k.insert(indeks(dane, "klik", "menu-paska"), {"typ": "klik", "cel": "running-tasks"})
    assert jest(bledy(dane), "klik „running-tasks”: w drogach klika się tylko")
    assert jest(bledy(dane), "odnośnik „N running tasks” jest nieaktywny")


def test_klik_running_tasks_zamiast_menu_odrzucony(dane):
    k = kroki(dane)
    i = indeks(dane, "klik", "menu-paska")
    k[i:i + 2] = [{"typ": "klik", "cel": "running-tasks"}]
    assert jest(bledy(dane), "klik „running-tasks”")


def test_cele_pracy_w_tle_nie_zawieraja_running_tasks():
    assert "running-tasks" not in scenariusz_w_tle.KLIKI
    assert "running-tasks" not in czytelnosc.KLIKI_PASKA_BOCZNEGO


def test_napis_nadal_wymaga_wzoru_z_listy_napisow(dane):
    w = next(k for k in kroki(dane) if "w_tle" in k)["w_tle"]
    assert len(w) >= 2 and bledy(dane) == []
