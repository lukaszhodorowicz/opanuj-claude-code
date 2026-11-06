"""Testy walidatora (KD1 z przeglądu): w ćwiczeniu z folderem każdej rozmowy nowy plik z `nowe_pliki` (ścieżka od korzenia) musi leżeć w folderze rozmowy, w której pada `claude.plik`; plik w teczce A nie liczy się jako odpowiedź w rozmowie z teczki B (wzór: tests/dane/kilka-rozmow-foldery-i-wiadomosc.json)."""

from tests.pomoc_foldery import bledy, cwiczenie, gdzie, jest, kopia, kroki


def test_wzor_przechodzi_a_nowy_plik_w_folderze_rozmowy_z_odpowiedzia_nie_jest_bledem():
    assert bledy(kopia()) == []


def test_nowy_plik_w_innej_teczce_niz_folder_rozmowy_z_odpowiedzia_odrzucony():
    d = kopia()
    # Claude podaje posty-wience.txt w rozmowie z teczki Posty-listopad, a nowy plik leży w Cennik-swieta pod tą samą nazwą
    cwiczenie(d, "cw1")["nowe_pliki"].append("Cennik-swieta/posty-wience.txt")
    wynik = bledy(d)
    assert jest(wynik, "nowy plik „Cennik-swieta/posty-wience.txt” bez odpowiedzi Claude")
    assert not jest(wynik, "nowy plik „Posty-listopad/posty-wience.txt” bez odpowiedzi Claude")


def test_nowy_plik_wskazany_w_rozmowie_z_wlasnej_teczki_przechodzi_takze_gdy_nazwa_to_koncowka_innej():
    d = kopia()
    k = kroki(d)
    cwiczenie(d, "cw1")["nowe_pliki"] = ["Posty-listopad/posty-wience.txt"]
    k[gdzie(k, "claude")]["plik"] = "posty-wience.txt"
    assert bledy(d) == []
