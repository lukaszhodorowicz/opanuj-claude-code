"""Testy walidatora karty wiadomości od innej rozmowy (wzór: tests/dane/kilka-rozmow-foldery-i-wiadomosc.json, ćwiczenie cw2): pole `wiadomosc: {do, tekst}` kroku `claude` i klik `wiadomosc-od`."""

import copy

from tests.pomoc_foldery import apl, bledy, cwiczenie, gdzie, jest, klik, kopia, kroki, naucz, wiadomosc


def k2(d):
    return kroki(d, "wiadomosc", "cw2")


def test_wiadomosc_do_spoza_listy_rozmow_odrzucona():
    d = kopia()
    wiadomosc(d)["wiadomosc"]["do"] = "nie-ma-takiej"
    assert jest(bledy(d), "wiadomosc.do: rozmowa 'nie-ma-takiej' spoza aplikacja.sesje i aplikacja.id")


def test_wiadomosc_do_samej_siebie_odrzucona():
    d = kopia()
    wiadomosc(d)["wiadomosc"]["do"] = "posty"  # otwarta jest rozmowa startowa (aplikacja.id = posty)
    assert jest(bledy(d), "wiadomość do samej siebie")


def test_wiadomosc_do_rozmowy_startowej_z_innej_rozmowy_dozwolona():
    d = kopia()
    c = cwiczenie(d, "cw2")
    c["drogi"] = [{"id": "wstecz", "etykieta": "Wstecz", "kroki": [
        klik("sesja", sesja="cennik"), naucz(),
        {"typ": "pisz", "tekst": "Daj znać rozmowie Posty na listopad."},
        {"typ": "mysli"},
        {"typ": "claude", "tekst": "Wysłałem wiadomość.", "wiadomosc": {"do": "posty", "tekst": "Cennik ma nową cenę: 210 zł."}},
        klik("sesja", sesja="posty"), naucz(),
        klik("wiadomosc-od"), naucz()]}]
    assert bledy(d) == []


def test_wiadomosc_do_rozmowy_zarchiwizowanej_w_tej_drodze_odrzucona():
    d = kopia()
    k = k2(d)
    i = gdzie(k, "pisz", nr=1)
    k[i:i] = [klik("sesja", sesja="cennik"), klik("menu-sesji", sesja="hurtownia"), klik("archive"), klik("sesja", sesja="posty"), naucz()]
    wiadomosc(d)["wiadomosc"]["do"] = "hurtownia"
    assert jest(bledy(d), "która została zarchiwizowana w tej drodze")


def test_wiadomosc_z_pustym_tekstem_odrzucona():
    d = kopia()
    wiadomosc(d)["wiadomosc"]["tekst"] = "  "
    assert jest(bledy(d), "wiadomosc.tekst musi być niepustym napisem")


def test_wiadomosc_z_polem_spoza_do_i_tekst_odrzucona():
    d = kopia()
    wiadomosc(d)["wiadomosc"]["od"] = "posty"
    assert jest(bledy(d), "wiadomosc musi być obiektem {do, tekst}")


def test_wiadomosc_nie_jest_obiektem_odrzucona():
    d = kopia()
    wiadomosc(d)["wiadomosc"] = "cennik"
    assert jest(bledy(d), "wiadomosc musi być obiektem")


def test_wiadomosc_w_kroku_innym_niz_claude_odrzucona():
    d = kopia()
    k = k2(d)
    k[gdzie(k, "mysli", nr=1)]["wiadomosc"] = {"do": "cennik", "tekst": "x"}
    assert jest(bledy(d), "pole wiadomosc tylko w kroku claude")


def test_wiadomosc_w_cwiczeniu_bez_sesje_odrzucona():
    d = kopia()
    del apl(d, "cw2")["sesje"]
    d["cwiczenia"][1]["drogi"][0]["kroki"] = [x for x in k2(d) if x.get("cel") != "sesja" and x.get("cel") != "wiadomosc-od"]
    assert jest(bledy(d), "wiadomosc tylko w ćwiczeniu z aplikacja.sesje")


def test_wiadomosc_od_rozmowy_bez_nazwy_odrzucona():
    d = kopia()
    del apl(d, "cw2")["nazwa"]
    assert jest(bledy(d), "wiadomosc od rozmowy bez nazwy")


def test_wiadomosc_z_nowej_rozmowy_odrzucona():
    d = kopia()
    k = k2(d)
    k.insert(0, klik("nowa-rozmowa"))
    assert jest(bledy(d), "nowa rozmowa nie ma nazwy")


def test_wiadomosc_bez_prosby_kursanta_odrzucona():
    d = kopia()
    k = k2(d)
    for i in sorted((i for i, x in enumerate(k) if x["typ"] == "pisz"), reverse=True):
        del k[i]
    assert jest(bledy(d), "wiadomosc bez prośby kursanta")


def test_klik_wiadomosc_od_bez_karty_odrzucony():
    d = kopia()
    k = k2(d)
    k.insert(gdzie(k, "klik", "sesja"), klik("wiadomosc-od"))
    assert jest(bledy(d), "klik wiadomosc-od w rozmowie bez karty wiadomości")


def test_klik_wiadomosc_od_z_polem_odrzucony():
    d = kopia()
    k = k2(d)
    k[gdzie(k, "klik", "wiadomosc-od")]["sesja"] = "posty"
    assert jest(bledy(d), "pole sesja tylko w klik z celem")


def test_klik_wiadomosc_od_gdy_nadawca_zarchiwizowany_odrzucony():
    d = kopia()
    c = cwiczenie(d, "cw2")
    c["drogi"] = [{"id": "archiwum", "etykieta": "Archiwum", "kroki": [
        klik("sesja", sesja="cennik"), naucz(),
        {"typ": "pisz", "tekst": "Daj znać rozmowie Posty na listopad."},
        {"typ": "mysli"},
        {"typ": "claude", "tekst": "Wysłałem wiadomość.", "wiadomosc": {"do": "posty", "tekst": "Cennik ma nową cenę: 210 zł."}},
        klik("sesja", sesja="posty"), naucz(),
        klik("menu-sesji", sesja="cennik"), klik("archive"),
        klik("wiadomosc-od"), naucz()]}]
    assert jest(bledy(d), "nadawca „cennik” został zarchiwizowany w tej drodze")


def test_klik_wiadomosc_od_otwiera_rozmowe_nadawcy_a_kolejny_klik_sesja_na_nia_jest_odrzucony():
    d = kopia()
    k = k2(d)
    k.insert(gdzie(k, "klik", "wiadomosc-od") + 1, klik("sesja", sesja="posty"))
    assert jest(bledy(d), "który jest już otwarty w tej drodze")


def test_karta_znika_w_drugiej_drodze_stan_nie_przecieka():
    d = kopia()
    c = cwiczenie(d, "cw2")
    druga = copy.deepcopy(c["drogi"][0])
    druga["id"] = "druga"
    c["drogi"].append(druga)
    assert bledy(d) == []
    c["drogi"][1]["kroki"] = [x for x in druga["kroki"] if "wiadomosc" not in x]
    assert jest(bledy(d), "klik wiadomosc-od w rozmowie bez karty wiadomości")


def test_pole_wiadomosc_tekst_za_dlugi_odrzucone():
    d = kopia()
    wiadomosc(d)["wiadomosc"]["tekst"] = "x" * 601
    assert jest(bledy(d), "do 600 znaków")
