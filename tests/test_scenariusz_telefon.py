"""Testy walidatora telefonu z Remote Control i strony Settings → Claude Code (wzór: tests/dane/telefon.json): pole `aplikacja.telefon`, warunki jego użycia, kliki `telefon-sesja`, `telefon-wstecz` i `ustawienia-claude-code`, pole `na_telefonie` kroku `pisz`, pole `aplikacja.rc_nowe_sesje`, rytm nauczyciela, polskie pola do filtrów języka i podgląd drogi bez kroku plik."""

import json
from pathlib import Path

import pytest

from narzedzia import czytelnosc, scenariusz_telefon, strona_podglad, tekst_pl
from tests.pomoc_telefon import NAPISY, WZOR, apl, bledy, dane, indeks, jest, kroki  # noqa: F401 (dane to fixture)


def test_wzor_przechodzi_bez_bledow(dane):
    assert bledy(dane) == []


# pole aplikacja.telefon


@pytest.mark.parametrize("zly", ["MacBook-Air", ["MacBook-Air"], None, 5])
def test_telefon_musi_byc_obiektem(dane, zly):
    apl(dane)["telefon"] = zly
    assert jest(bledy(dane), "pole telefon musi być obiektem")


def test_telefon_z_obcym_polem_to_blad_z_lista_pol(dane):
    apl(dane)["telefon"]["model"] = "Opus"
    assert jest(bledy(dane), "pole model nie należy do telefonu (pola: urzadzenie, sesja)")


@pytest.mark.parametrize("pole", ["urzadzenie", "sesja"])
@pytest.mark.parametrize("wartosc", ["", "   ", None, 7])
def test_telefon_pole_musi_byc_niepustym_napisem(dane, pole, wartosc):
    apl(dane)["telefon"][pole] = wartosc
    assert jest(bledy(dane), f"telefon.{pole} musi być niepustym napisem")


def test_telefon_brak_pola_to_blad(dane):
    del apl(dane)["telefon"]["urzadzenie"]
    assert jest(bledy(dane), "telefon.urzadzenie musi być niepustym napisem")


@pytest.mark.parametrize("pole,maks", [("urzadzenie", 40), ("sesja", 80)])
def test_telefon_limit_znakow(dane, pole, maks):
    apl(dane)["nazwa"] = "x" * maks if pole == "sesja" else apl(dane)["nazwa"]
    apl(dane)["telefon"][pole] = "x" * maks
    assert not jest(bledy(dane), f"telefon.{pole} ma")
    apl(dane)["telefon"][pole] = "x" * (maks + 1)
    assert jest(bledy(dane), f"telefon.{pole} ma {maks + 1} znaków, najwyżej {maks}")


@pytest.mark.parametrize("znak", ["\n", "\t", "​", " "])
def test_telefon_znak_sterujacy_albo_niewidoczny_to_blad(dane, znak):
    apl(dane)["telefon"]["urzadzenie"] = f"Mac{znak}Book"
    assert jest(bledy(dane), "telefon.urzadzenie ma znak sterujący albo niewidoczny")


# warunki użycia telefonu


def test_telefon_w_chmurze_to_blad(dane):
    apl(dane)["srodowisko"] = "Cloud"
    assert jest(bledy(dane), "telefon w środowisku „Cloud”")


def test_telefon_z_wylaczonym_remote_control_to_blad_z_czytelnym_komunikatem(dane):
    apl(dane)["remote_control"] = False
    assert jest(bledy(dane), "telefon przy remote_control: false: bez włączonego Remote Control sesja z komputera nie pojawia się na liście na telefonie")


def test_telefon_z_wlaczonym_remote_control_przechodzi(dane):
    apl(dane)["remote_control"] = True
    assert bledy(dane) == []


def test_telefon_poza_cwiczeniem_z_drogami_to_blad(dane):
    cw = dane["cwiczenia"][0]
    cw["kroki"] = [{"klik": "licznik", "etykieta": "x", "nauczyciel": "y"}]
    del cw["drogi"]
    assert jest(bledy(dane), "telefon tylko w ćwiczeniu z drogami")


def test_telefon_z_paskiem_bocznym_rozmow_to_blad(dane):
    apl(dane)["sesje"] = [{"id": "inna", "rozmowa": [{"kto": "ty", "tekst": "Cześć"}]}]
    assert jest(bledy(dane), "telefon w ćwiczeniu z aplikacja.sesje")


def test_tytul_rozmowy_na_komputerze_i_sesja_na_telefonie_to_ten_sam_napis(dane):
    apl(dane)["nazwa"] = "Inny tytuł"
    assert jest(bledy(dane), "tytuł rozmowy na komputerze (nazwa „Inny tytuł”) inny niż sesja na telefonie („Harmonogram wesela”)")


def test_bez_nazwy_rozmowy_na_komputerze_sesja_na_telefonie_wystarcza(dane):
    del apl(dane)["nazwa"]
    assert bledy(dane) == []


# kliki telefonu i pole na_telefonie


def test_wstecz_na_liscie_to_blad(dane):
    kroki(dane).insert(0, {"typ": "klik", "cel": "telefon-wstecz"})
    assert jest(bledy(dane), "klik „telefon-wstecz”, gdy telefon pokazuje listę sesji")


def test_druga_sesja_bez_powrotu_to_blad(dane):
    k = kroki(dane)
    k.insert(indeks(dane, "klik", "telefon-sesja") + 1, {"typ": "klik", "cel": "telefon-sesja"})
    assert jest(bledy(dane), "klik „telefon-sesja”, gdy telefon już pokazuje rozmowę")


def test_pisz_na_telefonie_przed_otwarciem_rozmowy_to_blad(dane):
    k = kroki(dane)
    i = indeks(dane, "pisz")
    pisz = k.pop(i)
    k.insert(indeks(dane, "klik", "telefon-sesja"), pisz)
    assert jest(bledy(dane), "na_telefonie, gdy telefon pokazuje listę sesji: najpierw klik „telefon-sesja”")


def test_pisz_na_telefonie_po_powrocie_na_liste_to_blad(dane):
    k = kroki(dane)
    k.insert(indeks(dane, "pisz"), {"typ": "klik", "cel": "telefon-wstecz"})
    k.insert(indeks(dane, "pisz"), {"typ": "nauczyciel", "tekst": "Lista."})
    assert jest(bledy(dane), "na_telefonie, gdy telefon pokazuje listę sesji")


@pytest.mark.parametrize("wartosc", [False, "tak", 1, None])
def test_na_telefonie_musi_byc_prawda(dane, wartosc):
    kroki(dane)[indeks(dane, "pisz")]["na_telefonie"] = wartosc
    assert jest(bledy(dane), "na_telefonie musi być prawdą (true) albo nie występować")


@pytest.mark.parametrize("typ", ["claude", "mysli", "nauczyciel"])
def test_na_telefonie_tylko_w_kroku_pisz(dane, typ):
    kroki(dane)[indeks(dane, typ)]["na_telefonie"] = True
    assert jest(bledy(dane), f"pole na_telefonie tylko w kroku pisz, jest w kroku {typ}")


def test_zwykly_pisz_przy_otwartej_rozmowie_na_telefonie_przechodzi(dane):
    del kroki(dane)[indeks(dane, "pisz")]["na_telefonie"]
    assert bledy(dane) == []


def test_klik_telefonu_bez_aplikacja_telefon_to_blad(dane):
    del apl(dane)["telefon"]
    assert jest(bledy(dane), "klik telefon-sesja w ćwiczeniu bez aplikacja.telefon")
    assert jest(bledy(dane), "na_telefonie w ćwiczeniu bez aplikacja.telefon")


@pytest.mark.parametrize("cel", ["telefon-sesja", "telefon-wstecz", "ustawienia-claude-code"])
def test_klik_telefonu_z_obcym_polem_to_blad(dane, cel):
    kroki(dane).insert(0, {"typ": "klik", "cel": cel, "nr": 1})
    assert jest(bledy(dane), f"pole nr nie należy do kliku {cel} (pola: typ, cel, fakt)")


def test_klik_telefonu_przyjmuje_pole_fakt(dane):
    kroki(dane)[indeks(dane, "klik", "telefon-sesja")]["fakt"] = "aplikacja-enter-wysyla-zadanie"
    assert bledy(dane) == []


def test_przed_plus_zglasza_pisz_na_telefonie_przy_skillu_w_polu_komputera():
    """Stan `plus_pole` mówi, że skill stoi w polu komputera; w pełnym walidatorze `przed_plus` czyta go, zanim scenariusz_plus zeruje go przy kroku `pisz`."""
    stan = {**scenariusz_telefon.stan({"telefon": {}}), "tel_ekran": "rozmowa", "plus_pole": "skill"}
    zgloszone = []
    scenariusz_telefon.przed_plus({"typ": "pisz", "tekst": "x", "na_telefonie": True}, "k", stan, lambda s, t: zgloszone.append(t))
    assert zgloszone == ["na_telefonie przy skillu wybranym w polu komputera: skill idzie z prośbą wpisaną na komputerze, nie z telefonu"]
    zgloszone.clear()
    for krok, plus_pole in (({"typ": "pisz", "tekst": "x"}, "skill"), ({"typ": "pisz", "tekst": "x", "na_telefonie": True}, None), ({"typ": "nauczyciel", "tekst": "x"}, "skill")):
        scenariusz_telefon.przed_plus(krok, "k", {**stan, "plus_pole": plus_pole}, lambda s, t: zgloszone.append(t))
    assert zgloszone == [], "zwykły pisz przy skillu, pisz na telefonie bez skilla i inne kroki nie są błędem"


SKILL_KOMUNIKAT = "na_telefonie przy skillu wybranym w polu komputera: skill idzie z prośbą wpisaną na komputerze, nie z telefonu"


def _skill_z_telefonem() -> dict:
    """Wzór z listą „/” (tests/dane/gotowe-skille-plus-ukosnik.json), droga „plus”: telefon otwarty przed menu, skill wybrany z menu + w polu komputera, prośba z telefonu."""
    d = json.loads((Path(__file__).parent / "dane" / "gotowe-skille-plus-ukosnik.json").read_text(encoding="utf-8"))
    cw = d["cwiczenia"][0]
    cw["aplikacja"]["telefon"] = {"urzadzenie": "MacBook-Air", "sesja": "Porównanie sprzedaży"}
    k = cw["drogi"][0]["kroki"]
    k[:0] = [{"typ": "klik", "cel": "telefon-sesja"}, {"typ": "nauczyciel", "tekst": "Telefon pokazuje tę samą rozmowę co komputer."}]
    k[next(i for i, x in enumerate(k) if x["typ"] == "pisz")]["na_telefonie"] = True
    return d


def test_pelny_walidator_odrzuca_pisz_na_telefonie_przy_skillu_z_menu_plus():
    wynik = bledy(_skill_z_telefonem())
    assert jest(wynik, SKILL_KOMUNIKAT), wynik
    assert len([b for b in wynik if SKILL_KOMUNIKAT in b]) == 1 and len(wynik) == 1, "to jedyny błąd tej drogi"


def test_pelny_walidator_przyjmuje_zwykly_pisz_przy_skillu_gdy_telefon_jest_otwarty():
    d = _skill_z_telefonem()
    for k in d["cwiczenia"][0]["drogi"][0]["kroki"]:
        k.pop("na_telefonie", None)
    assert bledy(d) == [], "bez na_telefonie skill z menu i pisz na komputerze działają jak dotąd, także przy otwartym telefonie"


def test_pelny_walidator_przyjmuje_pisz_na_telefonie_bez_skilla_w_polu_komputera():
    d = _skill_z_telefonem()
    k = d["cwiczenia"][0]["drogi"][0]["kroki"]
    k[:] = [x for x in k if x.get("cel") not in ("plus", "pozycja", "wiersz")]
    k[:] = [x for x in k if x["typ"] != "nauczyciel" or "Telefon" in x["tekst"] or "Ten sam" in x["tekst"]]
    assert bledy(d) == []


def test_wzor_listy_ukosnik_bez_telefonu_nadal_przechodzi_bez_zmian():
    d = json.loads((Path(__file__).parent / "dane" / "gotowe-skille-plus-ukosnik.json").read_text(encoding="utf-8"))
    assert bledy(d) == []


# okno Settings → Claude Code


def test_po_otwarciu_ustawien_dalej_tylko_nauczyciel(dane):
    k = kroki(dane, 1)
    k.insert(2, {"typ": "mysli"})
    assert jest(bledy(dane), "krok mysli przy otwartym oknie Settings: dalej tylko nauczyciel")


def test_droga_konczaca_sie_tuz_po_otwarciu_ustawien_to_blad(dane):
    del kroki(dane, 1)[1]
    assert jest(bledy(dane), "droga kończy się zaraz po otwarciu okna Settings: najpierw nauczyciel")


def test_wiele_wypowiedzi_nauczyciela_po_ustawieniach_przechodzi(dane):
    kroki(dane, 1).append({"typ": "nauczyciel", "tekst": "Drugie zdanie."})
    assert bledy(dane) == []


@pytest.mark.parametrize("wartosc", ["tak", 1, None, "true"])
def test_rc_nowe_sesje_tylko_prawda_albo_falsz(dane, wartosc):
    apl(dane, 1)["rc_nowe_sesje"] = wartosc
    assert jest(bledy(dane), "pole rc_nowe_sesje musi być prawdą albo fałszem")


@pytest.mark.parametrize("wartosc", [True, False])
def test_rc_nowe_sesje_prawda_albo_falsz_przechodzi(dane, wartosc):
    apl(dane, 1)["rc_nowe_sesje"] = wartosc
    assert bledy(dane) == []


def test_rc_nowe_sesje_bez_kroku_otwierajacego_ustawienia_to_blad(dane):
    apl(dane, 0)["rc_nowe_sesje"] = True
    assert jest(bledy(dane), "pole rc_nowe_sesje bez kroku klik „ustawienia-claude-code”")


def test_ustawienia_dzialaja_bez_telefonu_i_bez_pola_rc(dane):
    del apl(dane, 1)["rc_nowe_sesje"]
    assert bledy(dane) == []


# droga bez kroku plik, polskie pola, rytm nauczyciela, podgląd


def test_droga_z_klikiem_telefonu_albo_ustawien_moze_nie_miec_kroku_plik(dane):
    for cw, droga in ((0, 1), (1, 0)):
        assert not any(k["typ"] == "plik" for k in kroki(dane, cw, droga))
    assert bledy(dane) == []


def test_zwykla_droga_bez_pliku_dalej_jest_bledem(dane):
    kroki(dane, 0, 1)[:] = [{"typ": "nauczyciel", "tekst": "Nic się nie dzieje."}]
    assert jest(bledy(dane), "droga bez kroku plik ani artefakt (ani strona)")


def test_tytul_sesji_na_telefonie_trafia_do_polskich_pol_a_nazwa_urzadzenia_nie(dane):
    pola = dict(tekst_pl.polskie_pola(dane, NAPISY))
    assert pola["cwiczenia[0].aplikacja.telefon.sesja"] == "Harmonogram wesela"
    assert not any(s.endswith("telefon.urzadzenie") for s in pola)
    assert not any("kroki[1].sesja" in s for s in pola), "pole sesja kliku (id wiersza) nie jest polskim napisem"


def _rytm(dane, tmp_path):
    plik = tmp_path / "scenariusz.json"
    plik.write_text(json.dumps(dane, ensure_ascii=False), encoding="utf-8")
    return czytelnosc.sprawdz_scenariusz(plik, "telefon.json")


def test_wzor_ma_poprawny_rytm_nauczyciela(dane, tmp_path):
    assert _rytm(dane, tmp_path) == []


@pytest.mark.parametrize("cw,droga,cel", [(0, 0, "telefon-sesja"), (0, 1, "telefon-wstecz"), (1, 0, "ustawienia-claude-code")])
def test_po_kliku_telefonu_i_ustawien_nauczyciel_odzywa_sie_najdalej_w_drugim_kroku(dane, tmp_path, cw, droga, cel):
    k = kroki(dane, cw, droga)
    i = next(n for n, x in enumerate(k) if x.get("cel") == cel)
    k[i + 1 :] = [{"typ": "mysli"}, {"typ": "mysli"}, {"typ": "nauczyciel", "tekst": "Za późno."}]
    wynik = _rytm(dane, tmp_path)
    nazwa = f"ćwiczenie cw{cw + 1}, droga {dane['cwiczenia'][cw]['drogi'][droga]['id']}, krok {i + 1} (klik)"
    assert any(nazwa in b and "brak nauczyciela w 2 kolejnych krokach" in b for b in wynik), wynik


@pytest.mark.parametrize("cw,droga,cel", [(0, 0, "telefon-sesja"), (0, 1, "telefon-wstecz"), (1, 0, "ustawienia-claude-code")])
def test_nauczyciel_w_drugim_kroku_po_kliku_wystarcza(dane, tmp_path, cw, droga, cel):
    k = kroki(dane, cw, droga)
    i = next(n for n, x in enumerate(k) if x.get("cel") == cel)
    k[i + 1 :] = [{"typ": "mysli"}, {"typ": "nauczyciel", "tekst": "W porządku."}]
    assert not any(f"krok {i + 1} (klik)" in b for b in _rytm(dane, tmp_path))


def test_podglad_drogi_z_telefonem_bez_pliku_to_blad_skladania(dane):
    html = '<div class="podglad" data-cw="cw1" data-t="wstecz"></div>'
    with pytest.raises(ValueError, match="droga nie ma kroku plik, artefakt ani strona"):
        strona_podglad.sprawdz_podglady(html, dane)


def test_podglad_drogi_z_plikiem_przy_telefonie_przechodzi(dane):
    html = '<div class="podglad" data-cw="cw1" data-t="z-telefonu"></div>'
    strona_podglad.sprawdz_podglady(html, dane)
