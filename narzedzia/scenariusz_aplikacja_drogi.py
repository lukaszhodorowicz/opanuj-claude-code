"""Sprawdza drogi ćwiczenia rodzaju `aplikacja`: kroki każdej drogi (prośba kursanta, odpowiedź ze ścieżką albo linkiem, klik, otwarty plik, artefakt albo strona, karta zgody, karta Context), ich kolejność i to, że droga ma co pokazać w podglądzie."""

import re

from narzedzia import scenariusz_artefakt, scenariusz_drzewo, scenariusz_katalog, scenariusz_kontekst, scenariusz_model, scenariusz_pierscien, scenariusz_plus, scenariusz_przeplyw, scenariusz_sesje, scenariusz_sesje_foldery, scenariusz_w_tle, scenariusz_wiadomosc, scenariusz_wtyczki, scenariusz_zgoda_drogi, scenariusz_zgoda_strona
from narzedzia import scenariusz_harmonogram  # zadanie według harmonogramu: strona Scheduled tasks, okno New scheduled task, strona zadania
from narzedzia.scenariusz_strona import sprawdz_strone
from narzedzia import scenariusz_koniec_drogi, scenariusz_menu_rzedu  # menu_rzedu: lista trybów (tryb-menu, tryb) i menu środowiska (srodowisko-menu); koniec_drogi: droga bez pliku (model, kontekst, tryb)
from narzedzia import scenariusz_plik_ekran  # menu „…” panelu pliku, karta pliku z menu prawego kliku i dymek ikony paska tytułu (klik plik-menu, plik-karta-menu, plik-karta-pozycja, ikona-tytulu; pole karta_pliku kroku claude)
from narzedzia import scenariusz_ekrany_b  # paczka 4 część B: panel Browser z menu „…” (przegladarka, przegladarka-menu), menu sesji z Transcript view (strzalka-tytulu, transcript-view, widok-transkrypcji) i edytor prezentacji w oknie (edytor-rozwin)
from narzedzia import scenariusz_telefon  # telefon z Remote Control i okno Settings → Claude Code (aplikacja.telefon, kliki telefon-sesja, telefon-wstecz, ustawienia-claude-code, pole na_telefonie)

TYPY_DROGI = ("pisz", "mysli", "claude", "klik", "plik", "nauczyciel", "artefakt", "zgoda", "ukosnik", "katalog_zamknij", *scenariusz_kontekst.TYPY, *scenariusz_zgoda_strona.TYPY, *scenariusz_przeplyw.TYPY)
KLIKI_DROGI = ("sciezka", "link", "zatwierdz", *scenariusz_plus.CELE, *scenariusz_katalog.CELE, *scenariusz_kontekst.KLIKI, *scenariusz_zgoda_strona.KLIKI, *scenariusz_sesje.KLIKI, *scenariusz_model.KLIKI, *scenariusz_pierscien.KLIKI, *scenariusz_w_tle.KLIKI, *scenariusz_przeplyw.KLIKI)
KLIKI_DROGI = (*KLIKI_DROGI, *scenariusz_harmonogram.CELE)
KLIKI_DROGI = (*KLIKI_DROGI, *scenariusz_telefon.KLIKI)
KLIKI_DROGI = (*KLIKI_DROGI, *scenariusz_menu_rzedu.KLIKI, *scenariusz_ekrany_b.KLIKI)
KLIKI_DROGI = (*KLIKI_DROGI, *scenariusz_plik_ekran.KLIKI)
MAKS_MS = 10000


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


def krok_drogi(k, sk, stan, pliki, fakt, blad, napisy) -> None:
    """Jeden krok drogi; `stan` pamięta ścieżkę i link z ostatniej odpowiedzi Claude, to, czy poprzedni krok był klikiem w nie, i tytuł otwartego artefaktu."""
    typ = k.get("typ")
    scenariusz_drzewo.krok_czyta(k, sk, stan["drzewo"], blad)
    scenariusz_zgoda_drogi.kolejnosc(k, sk, stan, blad)
    scenariusz_katalog.kolejnosc(k, sk, stan, blad)  # przed plus: widzi menu jeszcze otwarte
    scenariusz_wtyczki.kolejnosc(k, sk, stan, blad)  # przed plus: widzi menu jeszcze otwarte
    scenariusz_telefon.przed_plus(k, sk, stan, blad)  # skill w polu komputera przy pisz na telefonie: stan sprzed zerowania przez scenariusz_plus
    scenariusz_plus.kolejnosc(k, sk, stan, blad)
    scenariusz_kontekst.kolejnosc(k, sk, stan, blad)
    scenariusz_sesje.kolejnosc(k, sk, stan, blad)
    scenariusz_model.kolejnosc(k, sk, stan, blad)
    scenariusz_menu_rzedu.kolejnosc(k, sk, stan, blad)
    scenariusz_plik_ekran.kolejnosc(k, sk, stan, blad)
    scenariusz_ekrany_b.kolejnosc(k, sk, stan, blad)  # menu „…” Browser, menu sesji i edytor w oknie: po otwarciu dalej tylko nauczyciel (i pozycje podmenu)
    scenariusz_pierscien.kolejnosc(k, sk, stan, blad)  # po sesje: widzi nowa-rozmowa i pierwszą prośbę
    scenariusz_wiadomosc.krok(k, sk, stan, blad)  # pole wiadomosc kroku claude (karta w rozmowie odbiorcy); stan sprzed tego kroku
    scenariusz_w_tle.kolejnosc(k, sk, stan, blad)
    scenariusz_przeplyw.kolejnosc(k, sk, stan, blad)
    scenariusz_harmonogram.kolejnosc(k, sk, stan, blad)  # przy stronie harmonogramu rozmowa jest schowana
    scenariusz_telefon.kolejnosc(k, sk, stan, blad)  # pole na_telefonie i okno Settings otwarte
    po_kliku, stan["po_kliku"] = stan["po_kliku"], None
    po_linku, stan["po_linku"] = stan["po_linku"], None
    if po_kliku and typ != "plik":
        blad(sk, "po kroku klik w ścieżkę musi być krok plik")
    if po_linku and typ != "artefakt":
        blad(sk, "po kroku klik w link musi być krok artefakt")
    if typ not in TYPY_DROGI:
        blad(sk, f"typ „{typ}” spoza {'/'.join(TYPY_DROGI)}")
        return
    fakt(k, sk)
    if typ in ("pisz", "claude", "nauczyciel") and not _niepusty(k.get("tekst")):
        blad(sk, f"krok {typ} wymaga niepustego pola tekst")
    if typ == "pisz":
        stan["sciezka"] = stan["link"] = None  # nowa prośba: ścieżka i link z wcześniejszej odpowiedzi już nie są celem
    elif typ == "mysli":
        if "tekst" in k:
            blad(sk, "mysli bez tekstu: dokumentacja aplikacji nie podaje napisu przy pracy Claude")
        if "ms" in k and (type(k["ms"]) is not int or not 0 < k["ms"] <= MAKS_MS):
            blad(sk, f"ms musi być liczbą całkowitą od 1 do {MAKS_MS}")
    elif typ == "claude":
        plik = k.get("plik")
        if stan["sesje"]["e1"]:
            pliki = scenariusz_sesje_foldery.widoczne(pliki, stan["przedrostek"])  # folder każdej rozmowy: nazwy od folderu otwartej rozmowy
        stan["sciezka"] = plik if _niepusty(plik) else None
        stan["link"] = scenariusz_artefakt.link_odpowiedzi(k, sk, blad)
        if "nazwa_sesji" in k:
            scenariusz_sesje.nazwa_sesji(k, sk, stan, blad)
        if "w_tle" in k or "w_tle_koniec" in k:
            scenariusz_w_tle.claude(k, sk, stan, napisy, blad)
        if "karta_pliku" in k:
            scenariusz_plik_ekran.claude(k, sk, stan, napisy, blad)
        stan["skrocony"] = stan["skrocony"] or stan["link"] == scenariusz_artefakt.SKROCONY
        if "plik" in k and not _niepusty(plik):
            blad(sk, "pole plik musi być niepustym napisem")
        elif _niepusty(plik):
            if plik not in pliki:
                blad(sk, f"plik „{plik}” nie istnieje w folder_startowy ani w nowe_pliki (plik z poprzedniego ćwiczenia dopisz w aplikacja.folder_startowy_dodatkowe)")
            if plik not in str(k.get("tekst", "")):
                blad(sk, f"tekst odpowiedzi nie zawiera ścieżki „{plik}”")
            stan["drzewo"].add(stan["przedrostek"] + plik)  # od teraz plik leży w drzewie (ścieżka od korzenia)
            stan["claude_pliki"].add(stan["przedrostek"] + plik)  # ścieżka od korzenia pliku podanego przez Claude w folderze otwartej rozmowy
    elif typ == "klik":
        if k.get("cel") not in KLIKI_DROGI:
            blad(sk, f"klik „{k.get('cel')}”: w drogach klika się tylko ścieżkę pliku (cel „sciezka”), link z odpowiedzi (cel „link”), ptaszek karty zgody (cel „zatwierdz”), przycisk +, pozycję menu, wiersz listy i kafelek katalogu (cele „plus”, „pozycja”, „wiersz”, „konektor”), przyciski karty przeglądarki (cele „allow_once”, „always_allow”, „deny”), nagłówek karty Context (cel „context”) albo krzyżyk pytania z boku (cel „zamknij-z-boku”), w ćwiczeniu z aplikacja.sesje także pasek boczny z rozmowami (cele „nowa-rozmowa”, „sesja”, „menu-sesji”, „archive”, „group-and-sort”, „view-all”, „archived”, „folder”, „wiadomosc-od”), a w menu wyboru modelu cele „wybor-modelu”, „effort” i „poziom”, pierścień zużycia abonamentu w rzędzie pod polem (cel „pierscien”), menu ⋮, panel zadań w tle i wpis w panelu (cele „menu-paska”, „background-tasks”, „wpis-w-tle”; odnośnik „N running tasks” jest nieaktywny, nie ma celu), przycisk Once karty przepływu (cel „once”), a w ćwiczeniu z aplikacja.harmonogram pozycję Scheduled w pasku bocznym i strony harmonogramu (cele „scheduled”, „new-task”, „advanced-settings”, „create”, „run-now”), na telefonie wiersz sesji i strzałka wstecz (cele „telefon-sesja”, „telefon-wstecz”), konto w pasku bocznym otwierające Settings → Claude Code (cel „ustawienia-claude-code”), przełącznik trybu i jego listę (cele „tryb-menu” i „tryb” z polem na), w sesji „Local” menu środowiska (cel „srodowisko-menu”), menu „…” otwartego pliku (cel „plik-menu”), kartę pliku z odpowiedzi i jej menu (cele „plik-karta-menu”, „plik-karta-pozycja”) i pierwszą ikonę paska tytułu (cel „ikona-tytulu”), pusty panel Browser i jego menu „…” (cele „przegladarka”, „przegladarka-menu”), menu sesji ze strzałki przy tytule (cele „strzalka-tytulu”, „transcript-view”, „widok-transkrypcji” z polem na) i rozwinięcie edytora prezentacji (cel „edytor-rozwin”), licznika nie ma")
        elif k["cel"] in (*scenariusz_plus.CELE, *scenariusz_katalog.CELE):
            pass  # kolejność i pola sprawdza scenariusz_plus.kolejnosc albo scenariusz_katalog.kolejnosc
        elif k["cel"] in scenariusz_telefon.KLIKI:
            scenariusz_telefon.klik(k, sk, stan, blad)
        elif k["cel"] in scenariusz_kontekst.KLIKI:
            scenariusz_kontekst.klik(k, sk, stan, blad)
        elif k["cel"] in scenariusz_zgoda_strona.KLIKI:
            scenariusz_zgoda_strona.klik(k, sk, stan, blad)
        elif k["cel"] in scenariusz_sesje.KLIKI:
            scenariusz_sesje.klik(k, sk, stan, blad)
        elif k["cel"] in scenariusz_menu_rzedu.KLIKI:
            scenariusz_menu_rzedu.klik(k, sk, stan, napisy, blad)
        elif k["cel"] in scenariusz_plik_ekran.KLIKI:
            scenariusz_plik_ekran.klik(k, sk, stan, napisy, blad)
        elif k["cel"] in scenariusz_ekrany_b.KLIKI:
            scenariusz_ekrany_b.klik(k, sk, stan, napisy, blad)
        elif k["cel"] in scenariusz_model.KLIKI:
            scenariusz_model.klik(k, sk, stan, napisy, blad)
        elif k["cel"] in scenariusz_pierscien.KLIKI:
            scenariusz_pierscien.klik(k, sk, stan, blad)
        elif k["cel"] in scenariusz_w_tle.KLIKI:
            scenariusz_w_tle.klik(k, sk, stan, blad)
        elif k["cel"] in scenariusz_przeplyw.KLIKI:
            scenariusz_przeplyw.klik(k, sk, stan, napisy, blad)
        elif k["cel"] in scenariusz_harmonogram.CELE:
            scenariusz_harmonogram.klik(k, sk, stan, blad)
        elif k["cel"] == "zatwierdz":
            scenariusz_zgoda_drogi.zatwierdz(sk, stan, blad)
        elif k["cel"] == "link":
            if not stan["link"]:
                blad(sk, "klik w link bez wcześniejszej odpowiedzi Claude z polem link")
            stan["po_linku"] = stan["link"]
        elif not stan["sciezka"]:
            blad(sk, "klik w ścieżkę bez wcześniejszej odpowiedzi Claude z polem plik")
        else:
            stan["po_kliku"] = stan["sciezka"]
    elif typ == "zgoda":
        scenariusz_zgoda_drogi.krok(k, sk, stan, pliki, blad)
    elif typ == "strona":
        scenariusz_zgoda_strona.krok(k, sk, stan, blad)
    elif typ == "przeplyw":
        scenariusz_przeplyw.krok(k, sk, stan, blad)
    elif typ in scenariusz_kontekst.TYPY:
        scenariusz_kontekst.krok(k, sk, stan, napisy, blad)
        scenariusz_telefon.komenda(k, stan)  # komenda /config otwiera okno Settings: dalej tylko nauczyciel
    elif typ == "artefakt":
        scenariusz_artefakt.krok(k, sk, stan, po_linku, blad)
    elif typ == "plik":
        stan["pliki"] += 1
        stan["konczy_slajdami"] = False  # ostatni podgląd to plik
        stan["artefakt"] = None  # plik zajmuje panel Browser: widok artefaktu się zamyka, kolejny artefakt wymaga znów klik w link
        if not po_kliku:
            blad(sk, "plik otwiera się tylko zaraz po kroku klik w ścieżkę")
        elif k.get("nazwa") != po_kliku:
            blad(sk, f"nazwa „{k.get('nazwa')}” inna niż kliknięta ścieżka „{po_kliku}”")
        if "strona" in k:  # plik .html: rysunek strony w panelu Browser zamiast linijek
            return sprawdz_strone(k, sk, blad)
        linijki = k.get("linijki")
        if not isinstance(linijki, list) or not any(_niepusty(l) for l in linijki):
            blad(sk, "plik wymaga listy linijki z co najmniej jedną niepustą")
        elif not all(isinstance(l, str) for l in linijki):
            blad(sk, "każda linijka pliku musi być napisem")


def sprawdz_drogi(drogi, s, pliki, otwarty, fakt, blad, uklad, napisy, apl, glowny=None) -> set:
    """Drogi do wyboru: każda zaczyna od tej samej rozmowy; polecenie nad oknem odpala kroki drogi po kolei. Zwraca ścieżki od korzenia plików podanych przez Claude w folderze otwartej rozmowy (pole `plik` kroków `claude` wszystkich dróg)."""
    uzyte_pliki: set = set()
    if not isinstance(drogi, list) or not drogi:
        blad(s, "rodzaj aplikacja wymaga niepustej listy drogi")
        return uzyte_pliki
    widziane = set()
    for i, d in enumerate(drogi):
        sd = f"{s}/drogi[{i}]"
        if not isinstance(d, dict):
            blad(sd, "droga musi być obiektem")
            continue
        if not isinstance(d.get("id"), str) or not re.fullmatch(r"[a-z0-9-]+", d["id"]):
            blad(sd, "droga wymaga pola id pasującego do ^[a-z0-9-]+$")
        elif d["id"] in widziane:
            blad(sd, f"id drogi „{d['id']}” powtórzone w ćwiczeniu")
        widziane.add(d.get("id"))
        if not _niepusty(d.get("etykieta")):
            blad(sd, "droga wymaga niepustego pola etykieta")
        if "opis" in d and not _niepusty(d["opis"]):
            blad(sd, "pole opis musi być niepustym napisem")
        kroki = d.get("kroki")
        if not isinstance(kroki, list) or not kroki:
            blad(sd, "droga wymaga niepustej listy kroki")
            continue
        stan = {"sciezka": None, "link": None, "po_kliku": None, "po_linku": None, "pliki": 0, "artefakt": otwarty, "widoki": 0, "przedrostek": uklad.przedrostek_startowy, "drzewo": set(uklad.na_starcie), "skrocony": False, "konczy_slajdami": False, "claude_pliki": set(), **scenariusz_zgoda_drogi.stan(apl.get("tryb")), **scenariusz_kontekst.stan(apl), **scenariusz_plus.stan(napisy, apl), **scenariusz_katalog.stan(apl, napisy), **scenariusz_wtyczki.stan(apl), **scenariusz_sesje.stan(apl, glowny, uklad), **scenariusz_model.stan(), **scenariusz_menu_rzedu.stan(apl), **scenariusz_plik_ekran.stan(apl), **scenariusz_ekrany_b.stan(apl), **scenariusz_pierscien.stan(), **scenariusz_w_tle.stan(apl), **scenariusz_przeplyw.stan(apl)}
        stan.update(scenariusz_harmonogram.stan(apl))
        stan.update(scenariusz_telefon.stan(apl))
        for j, k in enumerate(kroki):
            if isinstance(k, dict):
                krok_drogi(k, f"{sd}/kroki[{j}]", stan, pliki, fakt, blad, napisy)
            else:
                blad(f"{sd}/kroki[{j}]", "krok musi być obiektem")
        if stan["po_kliku"]:
            blad(sd, "po kroku klik w ścieżkę musi być krok plik")
        if stan["po_linku"]:
            blad(sd, "po kroku klik w link musi być krok artefakt")
        scenariusz_zgoda_drogi.koniec(sd, stan, blad)
        scenariusz_plus.koniec(sd, stan, blad)
        scenariusz_katalog.koniec(sd, stan, blad)
        scenariusz_wtyczki.koniec(sd, stan, blad)
        scenariusz_sesje.koniec(sd, stan, blad)
        scenariusz_model.koniec(sd, stan, blad)
        scenariusz_menu_rzedu.koniec(sd, stan, blad)
        scenariusz_w_tle.koniec(sd, stan, blad)
        scenariusz_przeplyw.koniec(sd, stan, blad)
        scenariusz_telefon.koniec(sd, stan, blad)
        scenariusz_artefakt.droga_ze_skroconym(stan, sd, blad)
        uzyte_pliki |= stan["claude_pliki"]
        if scenariusz_harmonogram.pokazuje(stan):
            continue  # droga ze stroną harmonogramu pokazuje ją zamiast pliku, artefaktu i strony
        if scenariusz_telefon.pokazuje(stan):
            continue  # droga z klikiem telefonu albo ustawień kończy się telefonem albo otwartym oknem Settings: podgląd w tekście lekcji dla niej to błąd składania (strona_podglad.py)
        if scenariusz_ekrany_b.pokazuje(stan):
            continue  # droga kończąca się otwartym panelem Browser, menu sesji albo rozwiniętym edytorem pokazuje ten ekran w oknie: plik ani artefakt nie jest jej potrzebny (podgląd w tekście lekcji dla niej to błąd składania)
        if scenariusz_koniec_drogi.pokazuje(kroki, apl):
            continue  # droga kończąca się wyborem poziomu wysiłku (innego niż bieżący), krokiem kontekst, wyborem trybu albo menu środowiska pokazuje zmianę w oknie: plik ani artefakt nie jest jej potrzebny
        powtorzony = scenariusz_koniec_drogi.poziom_bez_zmiany(kroki, apl)
        if not stan["pliki"] and not stan["widoki"] and not stan["strony"] and not stan["odmowa"] and not scenariusz_katalog.ma_katalog(d) and not scenariusz_wtyczki.ma_przegladarke(d) and not scenariusz_sesje.pokazuje(stan) and not scenariusz_pierscien.pokazuje(stan):  # droga z odmową (Deny), z katalogiem konektorów (kończy się rozmową), z przeglądarką wtyczek (kończy się otwartym oknem), z klikiem sesja, archive lub archived (okno z listą rozmów) albo z klikiem pierscien (otwarte okienko zużycia) może nic nie pokazać
            blad(sd, f"droga kończy się wyborem poziomu „{powtorzony}”, który już stoi (aplikacja.wysilek albo domyślny Medium, albo poziom z wcześniejszego kliku w tej drodze): klik niczego nie zmienia, a droga nie ma kroku plik, artefakt ani strona" if powtorzony else "droga bez kroku plik ani artefakt (ani strona): podgląd nie ma czego pokazać")
    return uzyte_pliki


def bez_odpowiedzi(drogi, nowe, s, blad, od_korzenia=None) -> None:
    """Każdy nowy plik musi wystąpić jako `plik` w jakimś kroku `claude` (inaczej Claude go nigdy nie tworzy). W ćwiczeniu z folderem każdej rozmowy (`od_korzenia` to zbiór ścieżek od korzenia z `sprawdz_drogi`) nowy plik to ścieżka od korzenia i musi leżeć w folderze rozmowy, w której pada `claude.plik`."""
    uzyte = {
        k.get("plik")
        for d in drogi if isinstance(d, dict) and isinstance(d.get("kroki"), list)
        for k in d["kroki"] if isinstance(k, dict) and k.get("typ") == "claude"
    }
    if od_korzenia is not None:
        uzyte = od_korzenia
    for nazwa in sorted(nowe - uzyte):
        blad(s, f"nowy plik „{nazwa}” bez odpowiedzi Claude: żaden krok claude nie podaje go w polu plik")
