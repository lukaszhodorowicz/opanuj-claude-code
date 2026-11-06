"""Testy walidatora (KD1): po kroku `claude` z `w_tle_koniec` w drodze stoi krok `plik`, bo panel zadań w tle, który stał, zajmuje plik (wzór: tests/dane/subagent-zbiera-panel-w-tle.json)."""

from tests.pomoc_w_tle import bledy, dane, indeks, jest, kroki  # noqa: F401


def test_wzor_ma_krok_plik_po_koncu_pracy_w_tle(dane):
    k = kroki(dane)
    koniec = next(i for i, x in enumerate(k) if x.get("w_tle_koniec"))
    assert any(x["typ"] == "plik" for x in k[koniec + 1:])
    assert bledy(dane) == []


def test_droga_konczaca_sie_bez_pliku_po_koncu_pracy_w_tle_odrzucona(dane):
    k = kroki(dane)
    koniec = next(i for i, x in enumerate(k) if x.get("w_tle_koniec"))
    dane["cwiczenia"][0]["drogi"][0]["kroki"] = [x for i, x in enumerate(k) if i <= koniec or x["typ"] == "nauczyciel"]
    dane["cwiczenia"][0]["drogi"][0]["kroki"].insert(0, {"typ": "plik", "nazwa": "plan-remontu.txt", "linijki": ["x"]})  # plik przed końcem pracy nie liczy się
    assert jest(bledy(dane), "po nim nie ma kroku plik: panel zadań w tle zostałby otwarty po końcu pracy")


def test_plik_przed_koncem_pracy_w_tle_nie_wystarcza(dane):
    k = kroki(dane)
    koniec = next(i for i, x in enumerate(k) if x.get("w_tle_koniec"))
    klik_sciezki = next(i for i in range(koniec + 1, len(k)) if k[i]["typ"] == "klik" and k[i]["cel"] == "sciezka")
    del k[klik_sciezki:klik_sciezki + 2]  # klik w ścieżkę i krok plik po końcu pracy
    assert jest(bledy(dane), "po nim nie ma kroku plik")
