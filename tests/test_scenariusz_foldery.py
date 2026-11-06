"""Testy walidatora folderu każdej rozmowy (wzór: tests/dane/kilka-rozmow-foldery-i-wiadomosc.json): `aplikacja.id`, `sesje[].folder`, klik `folder` w nowej rozmowie przed pierwszą prośbą, ścieżki liczone od folderu otwartej rozmowy i klik `sesja` na rozmowę startową."""

from tests.pomoc_foldery import apl, bledy, cwiczenie, gdzie, jest, kopia, kroki, klik, naucz


def test_wzor_przechodzi_walidator():
    assert bledy(kopia()) == []


def test_klik_folder_po_pierwszej_prosbie_odrzucony():
    d = kopia()
    k = kroki(d)
    k.insert(gdzie(k, "pisz") + 1, klik("folder", folder="Cennik-swieta"))
    assert jest(bledy(d), "klik folder poza nową rozmową przed pierwszą prośbą")


def test_klik_folder_w_rozmowie_ktora_nie_jest_nowa_odrzucony():
    d = kopia()
    k = kroki(d)
    k.insert(0, klik("folder", folder="Posty-listopad"))
    assert jest(bledy(d), "klik folder poza nową rozmową przed pierwszą prośbą")


def test_klik_folder_na_biezaca_teczke_odrzucony():
    d = kopia()
    k = kroki(d)
    k[gdzie(k, "klik", "folder")]["folder"] = "Cennik-swieta"  # nowa rozmowa zaczyna w folderze rozmowy startowej
    assert jest(bledy(d), "która jest już folderem nowej rozmowy")


def test_klik_folder_na_teczke_spoza_podgladu_odrzucony():
    d = kopia()
    k = kroki(d)
    k[gdzie(k, "klik", "folder")]["folder"] = "Nieistniejaca"
    assert jest(bledy(d), "spoza korzenia i teczek podglądu")


def test_klik_folder_bez_pola_folder_odrzucony():
    d = kopia()
    k = kroki(d)
    del k[gdzie(k, "klik", "folder")]["folder"]
    assert jest(bledy(d), "klik folder wymaga pola folder")


def test_klik_folder_na_korzen_podgladu_dozwolony():
    d = kopia()
    k = kroki(d)
    k[gdzie(k, "klik", "folder")]["folder"] = "Kwiaciarnia"
    assert not jest(bledy(d), "klik folder")


def test_pole_folder_w_innym_kliku_odrzucone():
    d = kopia()
    k = kroki(d)
    k[gdzie(k, "klik", "nowa-rozmowa")]["folder"] = "Posty-listopad"
    assert jest(bledy(d), "pole folder tylko w klik z celem „folder”")


def test_klik_folder_bez_folderu_w_wierszach_odrzucony():
    d = kopia()
    for w in apl(d)["sesje"]:
        del w["folder"]
    assert jest(bledy(d), "klik folder tylko w ćwiczeniu z folderem każdej rozmowy")


def test_wiersz_bez_folderu_gdy_inne_go_maja_odrzucony():
    d = kopia()
    del apl(d, "cw2")["sesje"][1]["folder"]
    assert jest(bledy(d), "wiersz bez pola folder, gdy inne wiersze je mają")


def test_folder_wiersza_spoza_teczek_odrzucony():
    d = kopia()
    apl(d)["sesje"][0]["folder"] = "Gdzies-indziej"
    assert jest(bledy(d), "musi być korzeniem podglądu albo teczką z plikami od startu")


def test_folder_wiersza_z_ukosnikiem_odrzucony():
    d = kopia()
    apl(d)["sesje"][0]["folder"] = "Kwiaciarnia/Cennik-swieta"
    assert jest(bledy(d), "sama nazwa folderu")


def test_folder_kazdej_rozmowy_wymaga_folder_glowny():
    d = kopia()
    del d["folder_glowny"]
    assert jest(bledy(d), "wymaga folder_glowny")


def test_id_rozmowy_startowej_zgodne_z_wzorem_i_niepowtarzalne():
    d = kopia()
    apl(d)["id"] = "Cennik Wienców"
    assert jest(bledy(d), "aplikacja.id musi pasować do ^[a-z0-9-]+$")
    d = kopia()
    apl(d)["id"] = "hurtownia"
    assert jest(bledy(d), "powtórzone w aplikacja.sesje")


def test_id_rozmowy_startowej_bez_listy_sesje_odrzucone():
    d = kopia()
    del apl(d)["sesje"]
    k = kroki(d)
    d["cwiczenia"][0]["drogi"][0]["kroki"] = [x for x in k if x.get("cel") not in ("nowa-rozmowa", "folder", "sesja")]
    assert jest(bledy(d), "id rozmowy startowej tylko w ćwiczeniu z aplikacja.sesje")


def test_klik_sesja_na_rozmowe_startowa_bez_jej_id_odrzucony():
    d = kopia()
    del apl(d)["id"]
    assert jest(bledy(d), "klik sesja wymaga pola sesja z id wiersza z aplikacja.sesje")


def test_klik_sesja_na_rozmowe_startowa_gdy_jest_otwarta_odrzucony():
    d = kopia()
    k = kroki(d)
    k.insert(0, klik("sesja", sesja="cennik"))
    assert jest(bledy(d), "który jest już otwarty w tej drodze")


def test_menu_rozmowy_startowej_nie_przyjmuje_jej_id():
    d = kopia()
    k = kroki(d)
    k.insert(gdzie(k, "klik", "sesja"), klik("menu-sesji", sesja="cennik"))
    assert jest(bledy(d), "klik menu-sesji wymaga pola sesja z id wiersza")


def test_plik_odpowiedzi_liczy_sie_od_folderu_otwartej_rozmowy():
    d = kopia()
    k = kroki(d)
    k[gdzie(k, "claude")]["plik"] = "cennik-wience.txt"  # leży w Cennik-swieta, a rozmowa pracuje w Posty-listopad
    k[gdzie(k, "claude")]["tekst"] = "Poprawiłem cennik-wience.txt."
    assert jest(bledy(d), "plik „cennik-wience.txt” nie istnieje")


def test_plik_odpowiedzi_od_korzenia_odrzucony_w_ćwiczeniu_z_folderami():
    d = kopia()
    k = kroki(d)
    k[gdzie(k, "claude")]["plik"] = "Posty-listopad/posty-wience.txt"
    k[gdzie(k, "claude")]["tekst"] = "Zapisałem Posty-listopad/posty-wience.txt."
    assert jest(bledy(d), "nie istnieje")


def test_nowe_pliki_licza_sie_od_korzenia_i_wymagaja_odpowiedzi_claude():
    d = kopia()
    cwiczenie(d, "cw1")["nowe_pliki"].append("Posty-listopad/inny.txt")
    assert jest(bledy(d), "nowy plik „Posty-listopad/inny.txt” bez odpowiedzi Claude")


def test_czyta_dalej_od_korzenia():
    d = kopia()
    k = kroki(d)
    k[gdzie(k, "mysli")]["czyta"] = ["plan-postow.txt"]
    assert jest(bledy(d), "nie wskazuje pliku")


def test_nauczyciel_po_kliku_folder_wymagany_przez_rytm(tmp_path):
    from narzedzia.czytelnosc import _sprawdz_liste_krokow, ZMIANY_APLIKACJI

    k = [klik("folder", folder="X"), {"typ": "pisz", "tekst": "a"}, {"typ": "mysli"}, naucz()]
    assert any("brak nauczyciela" in b for b in _sprawdz_liste_krokow(k, "", "t", ZMIANY_APLIKACJI))
    k = [klik("wiadomosc-od"), {"typ": "pisz", "tekst": "a"}, {"typ": "mysli"}, naucz()]
    assert any("brak nauczyciela" in b for b in _sprawdz_liste_krokow(k, "", "t", ZMIANY_APLIKACJI))
    k = [klik("folder", folder="X"), naucz()]
    assert _sprawdz_liste_krokow(k, "", "t", ZMIANY_APLIKACJI) == []
