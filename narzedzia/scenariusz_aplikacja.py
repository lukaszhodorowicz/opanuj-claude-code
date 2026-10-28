"""Sprawdza ćwiczenie rodzaju `aplikacja` (symulator zakładki Code aplikacji Claude): napisy interfejsu z listy `gdzie: aplikacja`, licznik `+N -M`, rozmowę, zmiany w plikach, kroki do kliknięcia i drogi (prośba kursanta, odpowiedź ze ścieżką albo linkiem, otwarty plik albo artefakt)."""

from narzedzia.scenariusz_aplikacja_drogi import MAKS_MS, bez_odpowiedzi as _bez_odpowiedzi, sprawdz_drogi as _drogi  # MAKS_MS: czyta też scenariusz_tryby
from narzedzia.scenariusz_folder_pliki import dodatkowe as _dodatkowe, nowe_pliki as _nowe_pliki
from narzedzia import scenariusz_harmonogram  # aplikacja.harmonogram: zadanie według harmonogramu
from narzedzia import scenariusz_telefon  # pola aplikacja.telefon i aplikacja.rc_nowe_sesje
from narzedzia import scenariusz_ustawienia  # pola aplikacja.konto_ustawien i aplikacja.konektory_do_polaczenia
from narzedzia import scenariusz_artefakt, scenariusz_bez_zmiany, scenariusz_panel, scenariusz_drzewo, scenariusz_katalog, scenariusz_kontekst, scenariusz_sesje, scenariusz_sesje_foldery, scenariusz_zgoda_drogi  # drzewo: teczki, czyta, czyta_na_start; pola bez_zmiany i link (krok claude), krok artefakt, widok_klienta; zgoda_drogi: bez_odliczania_w_etapach; kontekst: pole aplikacja.kontekst i panel drogi; katalog: zaczyna_od_plusa (rozmowa pusta przed sesją); sesje: pasek boczny z rozmowami (aplikacja.sesje, aplikacja.nazwa); sesje_foldery: folder każdej rozmowy; panel: pola remote_control i bypass_dostepny

from narzedzia import scenariusz_model  # pola aplikacja.model i aplikacja.wysilek: nazwa modelu i poziom wysiłku na przycisku w rzędzie pod polem

GDZIE = "aplikacja"
SRODOWISKA = ("Local", "Cloud", "SSH")
TRYBY_APLIKACJI = ("Auto", "Manual", "Accept edits", "Plan")  # kolejność listy trybów ze zrzutu Łukasza 27.10.2026 (04-41-10)
KTO = ("ty", "claude")
ZMIANY_LINIJKI = ("dodana", "usunieta")
KLIKI = ("licznik", "changes")
BEZ_UWAG = ("linijka", "uwaga", "plik")
PANEL = ("widoczny", "schowany")


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


def licznik(zmiany) -> str:
    """Napis licznika zmian „+N -M” liczony z linijek wszystkich plików (tak samo jak PK.licznikZmian w strona/aplikacja-ikony.js)."""
    dodane = usuniete = 0
    for plik in zmiany if isinstance(zmiany, list) else []:
        linijki = plik.get("linijki") if isinstance(plik, dict) else None
        for linijka in linijki if isinstance(linijki, list) else []:
            if isinstance(linijka, dict):
                dodane += linijka.get("zmiana") == "dodana"
                usuniete += linijka.get("zmiana") == "usunieta"
    return f"+{dodane} -{usuniete}"


def _napis(wartosc, dozwolone, s, pole, napisy, blad) -> None:
    """Pole udające interfejs: napis z listy napisów (gdzie: aplikacja) i z dozwolonego zestawu."""
    if not napisy.jest(wartosc, GDZIE):
        blad(s, f"{pole} „{wartosc}” spoza listy napisów interfejsu aplikacji")
    elif wartosc not in dozwolone:
        blad(s, f"{pole} „{wartosc}” spoza {'/'.join(dozwolone)}")


def _rozmowa(rozmowa, s, fakt, blad, pusta_ok=False) -> None:
    """Lista rozmowa; pusta tylko, gdy `pusta_ok` (ćwiczenie z drogami i `czyta_na_start` albo ćwiczenie z `artefakt_otwarty`: nowa sesja bez wiadomości)."""
    if not isinstance(rozmowa, list) or (not rozmowa and not pusta_ok):
        blad(s, "aplikacja wymaga niepustej listy rozmowa")
        return
    for i, w in enumerate(rozmowa):
        sw = f"{s}/rozmowa[{i}]"
        if not isinstance(w, dict):
            blad(sw, "wiadomość musi być obiektem")
            continue
        if w.get("kto") not in KTO:
            blad(sw, f"kto „{w.get('kto')}” spoza {'/'.join(KTO)}")
        if not _niepusty(w.get("tekst")):
            blad(sw, "wiadomość wymaga niepustego pola tekst")
        fakt(w, sw)


def _zmiany(zmiany, s, blad) -> None:
    """Sprawdza pliki zmiany: nazwa pliku i linijki z co najmniej jedną zmianą."""
    if not isinstance(zmiany, list) or not zmiany:
        blad(s, "aplikacja wymaga niepustej listy zmiany")
        return
    for i, p in enumerate(zmiany):
        sp = f"{s}/zmiany[{i}]"
        if not isinstance(p, dict):
            blad(sp, "plik zmiany musi być obiektem")
            continue
        if not _niepusty(p.get("plik")) or "/" in p.get("plik", ""):
            blad(sp, "plik zmiany wymaga pola plik (sama nazwa, bez /)")
        linijki = p.get("linijki")
        if not isinstance(linijki, list) or not linijki:
            blad(sp, "plik zmiany wymaga niepustej listy linijki")
            continue
        for j, l in enumerate(linijki):
            sl = f"{sp}/linijki[{j}]"
            if not isinstance(l, dict) or not isinstance(l.get("tekst"), str):
                blad(sl, "linijka wymaga pola tekst")
            elif "zmiana" in l and l["zmiana"] not in ZMIANY_LINIJKI:
                blad(sl, f"zmiana „{l['zmiana']}” spoza {'/'.join(ZMIANY_LINIJKI)}")
        if not any(isinstance(l, dict) and l.get("zmiana") for l in linijki):
            blad(sp, "plik zmiany bez żadnej linijki dodanej ani usuniętej")


def _krok(k, sk, fakt, blad) -> None:
    """Krok: klik w licznik albo w przycisk Changes (oba otwierają widok zmian), polecenie i wypowiedź nauczyciela."""
    if not isinstance(k, dict):
        blad(sk, "krok musi być obiektem")
        return
    for pole in ("etykieta", "nauczyciel"):
        if not _niepusty(k.get(pole)):
            blad(sk, f"krok wymaga niepustego pola {pole}")
    if "opis" in k and not _niepusty(k["opis"]):
        blad(sk, "pole opis musi być niepustym napisem")
    fakt(k, sk)
    if k.get("klik") not in KLIKI:
        blad(sk, f"klik „{k.get('klik')}” spoza {'/'.join(KLIKI)}")
    for pole in BEZ_UWAG:
        if pole in k:
            # próba z Łukaszem 25.10.2026: w folderze bez gita uwagi przy linijce nie da się dopisać
            blad(sk, f"pole {pole}: symulator nie pokazuje uwag przy linijce")


def sprawdz_aplikacje(cw: dict, s: str, napisy, fakt, blad, pliki=(), glowny=None) -> None:
    """Ćwiczenie `aplikacja`: obiekt `aplikacja` (srodowisko, folder, tryb, panel?, rozmowa, zmiany?) i lista `kroki` albo `drogi`.

    `pliki` to nazwy z `folder_startowy` scenariusza, `glowny` to jego `folder_glowny` (korzeń podglądu): ścieżka w odpowiedzi Claude (liczona od folderu rozmowy) musi być jedną z tych plików, z `aplikacja.folder_startowy_dodatkowe` albo z `nowe_pliki` ćwiczenia.
    """
    scenariusz_artefakt.kto_otworzy(cw, s, blad)  # pole usunięte, błąd także w ćwiczeniu z etapami
    scenariusz_kontekst.pole(cw, s, napisy, blad)  # aplikacja.kontekst: tylko w ćwiczeniu z drogami
    scenariusz_kontekst.pole_sesji_bez_karty(cw, s, blad)  # aplikacja.sesje[].kontekst: tylko z aplikacja.kontekst
    scenariusz_model.pole(cw, s, napisy, blad)  # aplikacja.model i aplikacja.wysilek: z listy modeli i poziomów ze zrzutów
    scenariusz_sesje.pole(cw, s, blad)  # aplikacja.sesje i aplikacja.nazwa: tylko w ćwiczeniu z drogami
    scenariusz_harmonogram.pole(cw, s, napisy, blad)  # aplikacja.harmonogram: tylko w ćwiczeniu z drogami
    scenariusz_panel.pole(cw, s, blad)  # aplikacja.remote_control i aplikacja.bypass_dostepny: prawda albo fałsz (też w ćwiczeniu z etapami)
    scenariusz_telefon.pole(cw, s, blad)  # aplikacja.telefon i aplikacja.rc_nowe_sesje: tylko w ćwiczeniu z drogami
    scenariusz_ustawienia.pole(cw, s, napisy, blad)  # aplikacja.konto_ustawien (wariant lewej kolumny Settings) i aplikacja.konektory_do_polaczenia (karta Connectors zwinięta)
    # podpięcie: menu trybu i karta zgody (dane/FORMAT-SCENARIUSZA-TRYBY.md)
    if "etapy" in cw:
        from narzedzia.scenariusz_tryby import sprawdz_tryby

        scenariusz_zgoda_drogi.bez_odliczania_w_etapach(cw["etapy"], f"{s}/etapy", blad)
        return sprawdz_tryby(cw, s, napisy, fakt, blad, pliki)
    apl = cw.get("aplikacja")
    if not isinstance(apl, dict):
        blad(s, "rodzaj aplikacja wymaga obiektu aplikacja")
        apl = {}
    sa = f"{s}/aplikacja"
    _napis(apl.get("srodowisko"), SRODOWISKA, sa, "srodowisko", napisy, blad)
    _napis(apl.get("tryb"), TRYBY_APLIKACJI, sa, "tryb", napisy, blad)
    folder = apl.get("folder")
    if not _niepusty(folder) or "/" in folder or folder.startswith("~"):
        blad(sa, "aplikacja wymaga pola folder (sama nazwa folderu, bez / i ~)")
    pusta_ok = ("drogi" in cw and bool(apl.get("czyta_na_start"))) or "artefakt_otwarty" in apl or scenariusz_katalog.zaczyna_od_plusa(cw)  # nowa sesja bez wiadomości: pliki czytane na starcie, artefakt otwarty od startu albo każda droga zaczyna od klik plus (dodawanie konektora przed sesją)
    _rozmowa(apl.get("rozmowa"), sa, fakt, blad, pusta_ok)
    for i, w in enumerate(apl.get("sesje") if isinstance(apl.get("sesje"), list) else []):
        if isinstance(w, dict):
            _rozmowa(w.get("rozmowa"), f"{sa}/sesje[{i}]", fakt, blad)  # dawne dymki wiersza listy: jak aplikacja.rozmowa, niepuste
    if "panel" in apl and apl["panel"] not in PANEL:
        blad(sa, f"panel „{apl['panel']}” spoza {'/'.join(PANEL)}")
    if ("kroki" in cw) == ("drogi" in cw):
        blad(s, "ćwiczenie aplikacji ma albo listę kroki, albo listę drogi")
    start = {p for p in pliki if isinstance(p, str)}
    dodatkowe = _dodatkowe(apl, sa, start, blad)
    surowe = [n for n in cw["nowe_pliki"] if isinstance(n, str)] if isinstance(cw.get("nowe_pliki"), list) else []
    wiele_folderow = scenariusz_sesje_foldery.jest(apl)  # folder każdej rozmowy: nowe_pliki od korzenia, ścieżki w rozmowie od jej folderu
    uklad = scenariusz_drzewo.Uklad(start, dodatkowe, surowe, apl, glowny, sa, blad, wiele_folderow)
    scenariusz_sesje_foldery.foldery(apl, sa, uklad, glowny, blad)
    nowe = _nowe_pliki(cw, s, start, blad, dodatkowe, uklad.przedrostek)
    scenariusz_drzewo.czyta_na_start(apl, sa, uklad, "drogi" in cw, blad)
    # pola widoczne dla kursanta (plik, nazwa, nowe_pliki, bez_zmiany) liczą się od folderu rozmowy, czyta i czyta_na_start od korzenia
    scenariusz_bez_zmiany.sprawdz(cw, s, scenariusz_sesje_foldery.widoczne_wszedzie(uklad, glowny) if wiele_folderow else uklad.widoczne(()), blad)
    otwarty = scenariusz_artefakt.sprawdz_cwiczenie(cw, apl, sa, s, napisy, blad)
    if "drogi" in cw:
        scenariusz_kontekst.panel_drogi(apl, sa, blad)  # panel schowany albo (z polem kontekst) widoczny z kartą Context; zmiany nigdy
        uzyte = _drogi(cw.get("drogi"), s, uklad.widoczne(nowe), otwarty, fakt, blad, uklad, napisy, apl, glowny)
        if isinstance(cw.get("drogi"), list):
            _bez_odpowiedzi(cw["drogi"], nowe, s, blad, uzyte if wiele_folderow else None)
        return
    _bez_odpowiedzi([], nowe, s, blad)
    if apl.get("panel") == "schowany":
        blad(sa, "panel „schowany” tylko w ćwiczeniu z drogami: kroki klikają licznik w panelu")
    _zmiany(apl.get("zmiany"), sa, blad)
    napis_licznika = licznik(apl.get("zmiany"))
    if not napisy.jest(napis_licznika, GDZIE):
        blad(
            sa,
            f"licznik „{napis_licznika}” nie pasuje do wzoru z listy napisów interfejsu aplikacji",
        )
    kroki = cw.get("kroki")
    if not isinstance(kroki, list) or not kroki:
        blad(s, "rodzaj aplikacja wymaga niepustej listy kroki")
        return
    for i, k in enumerate(kroki):
        _krok(k, f"{s}/kroki[{i}]", fakt, blad)
