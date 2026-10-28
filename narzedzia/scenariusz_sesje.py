"""Sprawdza w ćwiczeniu z drogami symulatora aplikacji pasek boczny z rozmowami: pola `aplikacja.sesje` i `aplikacja.nazwa`, kliki `nowa-rozmowa`, `sesja`, `menu-sesji`, `archive`, `group-and-sort`, `view-all`, `archived`, `folder` i `wiadomosc-od` (folder każdej rozmowy: scenariusz_sesje_foldery.py, karta wiadomości: scenariusz_wiadomosc.py), pole `nazwa_sesji` w kroku `claude` oraz kolejność kroków wokół menu i widoku listy (opis: dane/FORMAT-SCENARIUSZA.md, część „Pasek boczny z rozmowami”)."""

import re
import unicodedata

from narzedzia import scenariusz_kontekst, scenariusz_sesje_foldery, scenariusz_wiadomosc

KLIKI = ("nowa-rozmowa", "sesja", "menu-sesji", "archive", "group-and-sort", "view-all", "archived", "folder", "wiadomosc-od")
KLIKI_Z_SESJA = ("sesja", "menu-sesji")  # kliki, które wskazują wiersz polem `sesja`
KLIKI_Z_LISTA = tuple(c for c in KLIKI if c != "nowa-rozmowa")  # kliki, które wymagają paska bocznego z listą (`aplikacja.sesje`)
KLIKI_PODGLADU = ("sesja", "archive", "archived", "wiadomosc-od")  # droga z takim klikiem może skończyć się bez kroku plik, artefakt i strona: podgląd w tekście pokazuje okno z listą
POLA_KLIKU = ("typ", "cel", "sesja", "folder", "fakt")
POLA_WIERSZA = ("id", "rozmowa", "nazwa", "folder", "kontekst")  # kontekst: procent rozmowy na karcie Context po jej otwarciu (scenariusz_kontekst.py)
MAKS_ZNAKOW_NAZWY = 200
FAKT_NAZWY = "nazwa-sesji-do-200-znakow"
FAKT_LISTY = "aplikacja-pasek-boczny-lista-sesji"
FAKT_ARCHIWUM = "aplikacja-archiwizacja-z-menu-w-pasku-bocznym"
FAKT_WIDOKU = "aplikacja-zarchiwizowane-group-and-sort-view-all"


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


def _nazwa(wartosc, s: str, pole: str, blad) -> None:
    """Nazwa rozmowy: niepusty napis do 200 znaków, bez znaków sterujących i niewidocznych (aplikacja zamienia je na spacje, fakt nazwa-sesji-do-200-znakow)."""
    if not _niepusty(wartosc):
        blad(s, f"{pole} musi być niepustym napisem (nazwa nadana rozmowie)")
    elif len(wartosc) > MAKS_ZNAKOW_NAZWY:
        blad(s, f"{pole} ma {len(wartosc)} znaków, najwyżej {MAKS_ZNAKOW_NAZWY} (fakt {FAKT_NAZWY})")
    elif any(unicodedata.category(c) in ("Cc", "Cf", "Zl", "Zp") for c in wartosc):
        blad(s, f"{pole} ma znak sterujący albo niewidoczny: aplikacja zamienia je na spacje (fakt {FAKT_NAZWY})")


def pole(cw: dict, s: str, blad) -> None:
    """`aplikacja.sesje` (lista wierszy paska bocznego pod otwartą rozmową: `id`, `rozmowa`, `nazwa?`) i `aplikacja.nazwa` (nazwa otwartej rozmowy w pasku tytułu): tylko w ćwiczeniu z drogami. Treść `rozmowa` każdego wiersza sprawdza ten sam kod co `aplikacja.rozmowa` (scenariusz_aplikacja)."""
    apl = cw.get("aplikacja")
    if not isinstance(apl, dict):
        return
    sa = f"{s}/aplikacja"
    for p in ("sesje", "nazwa"):
        if p in apl and "drogi" not in cw:
            blad(sa, f"{p} tylko w ćwiczeniu z drogami: pasek boczny z rozmowami i tytuł rozmowy zmieniają kroki dróg (fakt {FAKT_LISTY})")
    if "nazwa" in apl:
        _nazwa(apl["nazwa"], sa, "nazwa", blad)
    scenariusz_sesje_foldery.pole(apl, sa, blad)  # aplikacja.id i sesje[].folder
    if "sesje" not in apl:
        return
    lista = apl["sesje"]
    if not isinstance(lista, list) or not lista:
        blad(sa, "sesje musi być niepustą listą wierszy {id, rozmowa, nazwa?}")
        return
    widziane = set()
    for i, w in enumerate(lista):
        sw = f"{sa}/sesje[{i}]"
        if not isinstance(w, dict):
            blad(sw, "wiersz sesje musi być obiektem {id, rozmowa, nazwa?}")
            continue
        for p in w:
            if p not in POLA_WIERSZA:
                blad(sw, f"pole {p} nie należy do wiersza sesje (pola: {', '.join(POLA_WIERSZA)}): wiersz nie pokazuje żadnego tekstu, nazwa rozmowy stoi tylko w pasku tytułu")
        if not isinstance(w.get("id"), str) or not re.fullmatch(r"[a-z0-9-]+", w["id"]):
            blad(sw, "wiersz sesje wymaga pola id pasującego do ^[a-z0-9-]+$")
        elif w["id"] in widziane:
            blad(sw, f"id wiersza „{w['id']}” powtórzone w aplikacja.sesje")
        widziane.add(w.get("id"))
        if "nazwa" in w:
            _nazwa(w["nazwa"], sw, "nazwa", blad)


def stan(apl: dict, glowny=None, uklad=None) -> dict:
    """Stan drogi w kluczu `sesje`: `ids` (id wierszy z `aplikacja.sesje`), `id_start` (`aplikacja.id`: id rozmowy startowej albo None), `lista` (ćwiczenie ma pasek boczny z listą), `otwarta` (None = rozmowa startowa, id wiersza albo „nowa”), `pusta` (otwarta jest nowa rozmowa bez pierwszej prośby), `prosba` (w otwartej rozmowie była prośba kursanta), `archiwum` (id zarchiwizowanych w tej drodze), `menu` (id wiersza z otwartym menu albo None), `grupa` (otwarte menu Group and sort), `widok` (None, „aktywne” albo „archived”: widok listy rozmów), `pokazuje` (w drodze był klik sesja, archive, archived albo wiadomosc-od), `nazwy` (nazwa każdej rozmowy: None = startowa) i `karty` (karty wiadomości: odbiorca → lista nadawców) oraz klucze folderu każdej rozmowy (scenariusz_sesje_foldery.stan)."""
    wiersze = apl.get("sesje") if isinstance(apl, dict) else None
    lista = [w for w in wiersze if isinstance(w, dict)] if isinstance(wiersze, list) else []
    ids = {w["id"] for w in lista if isinstance(w.get("id"), str)}
    nazwy = {None: apl.get("nazwa") if isinstance(apl, dict) else None, **{w["id"]: w.get("nazwa") for w in lista if isinstance(w.get("id"), str)}}
    id_start = apl.get("id") if isinstance(apl, dict) and isinstance(apl.get("id"), str) else None
    return {"sesje": {"ids": ids, "id_start": id_start, "lista": isinstance(wiersze, list), "otwarta": None, "pusta": False, "prosba": False, "archiwum": set(), "menu": None, "grupa": False, "widok": None, "pokazuje": False, "nazwy": nazwy, "karty": {}, **scenariusz_sesje_foldery.stan(apl if isinstance(apl, dict) else {}, glowny, uklad)}}


def kolejnosc(k: dict, sk: str, st: dict, blad) -> None:
    """Przed każdym krokiem drogi: przy otwartym menu rozmowy dalej tylko `nauczyciel` i klik `archive` (pozostałe pozycje menu to szare paski bez skutku), przy menu Group and sort tylko `nauczyciel` i klik `view-all`, a po View all tylko `nauczyciel` i klik `archived` (dokumentacja nie mówi, jak wrócić z widoku listy do rozmowy; prośba w polu, odpowiedź Claude i plik nie mają tam miejsca)."""
    s = st["sesje"]
    typ, cel = k.get("typ"), k.get("cel") if k.get("typ") == "klik" else None
    if typ == "pisz":
        s["pusta"], s["prosba"] = False, True  # pierwsza prośba w nowej rozmowie: rozmowa dostaje wiersz na liście
    if cel in ("nowa-rozmowa", "sesja", "wiadomosc-od"):
        scenariusz_kontekst.opuszczono_rozmowe(st, s["otwarta"])  # przed scenariusz_pierscien.kolejnosc, który po nowa-rozmowa zeruje kartę
    if typ == "nauczyciel":
        return
    if s["menu"] is not None and cel != "archive":
        blad(sk, f"krok {typ} przy otwartym menu rozmowy: dalej tylko nauczyciel i klik „archive” (pozostałe pozycje menu są szarymi paskami bez skutku; fakt {FAKT_ARCHIWUM})")
    elif s["grupa"] and cel != "view-all":
        blad(sk, f"krok {typ} przy otwartym menu Group and sort: dalej tylko nauczyciel i klik „view-all” (pozostałe wiersze menu są szarymi paskami bez skutku; fakt {FAKT_WIDOKU})")
    elif s["widok"] and cel != "archived":
        blad(sk, f"krok {typ} po View all: dalej tylko nauczyciel i klik „archived” (dokumentacja nie mówi, jak wrócić z widoku listy rozmów do rozmowy; fakt {FAKT_WIDOKU})")


def _sesja(k: dict, sk: str, st: dict, blad) -> str | None:
    """Wiersz wskazany polem `sesja` kliku `sesja` albo `menu-sesji`: id z `aplikacja.sesje` (klik `sesja` przyjmuje też `aplikacja.id` rozmowy startowej), jeszcze niezarchiwizowane w tej drodze; zwraca id albo None."""
    s = st["sesje"]
    sesja = k.get("sesja")
    mozliwe = s["ids"] | ({s["id_start"]} if k["cel"] == "sesja" and s["id_start"] else set())
    if not isinstance(sesja, str) or sesja not in mozliwe:
        blad(sk, f"klik {k['cel']} wymaga pola sesja z id wiersza z aplikacja.sesje{' albo z aplikacja.id' if k['cel'] == 'sesja' and s['id_start'] else ''} (jest {sesja!r})")
    elif sesja in s["archiwum"]:
        blad(sk, f"klik {k['cel']} na wierszu „{sesja}”, który został zarchiwizowany wcześniej w tej drodze: wiersza nie ma już na liście")
    else:
        return sesja
    return None


def _otwarto(st: dict, klucz, zmien: bool = True) -> None:
    """Zmiana otwartej rozmowy na `klucz` (None = startowa, id albo „nowa”): nowa rozmowa zaczyna w folderze rozmowy startowej, ścieżki liczą się od folderu otwartej rozmowy, prośba kursanta z poprzedniej nie liczy się, odpowiedź Claude znika z okna."""
    s = st["sesje"]
    if zmien:
        s["otwarta"] = klucz
        scenariusz_kontekst.otwarto_rozmowe(st, klucz)  # karta Context pokazuje procent otwartej rozmowy
    s["pusta"], s["prosba"] = klucz == "nowa", False
    if klucz == "nowa":
        s["folder_nowej"] = s["foldery"][None]
    scenariusz_sesje_foldery.otwarto(st)
    _zamknij_odpowiedz(st)


def klik(k: dict, sk: str, st: dict, blad) -> None:
    """Klik z celem z `KLIKI`: `nowa-rozmowa` (pusta rozmowa, bez wiersza do pierwszej prośby), `sesja` (otwiera rozmowę wiersza albo startową), `menu-sesji` (menu rozmowy), `archive` (zdejmuje wiersz z listy), `group-and-sort` (menu), `view-all` (widok listy rozmów), `archived` (zakładka), `folder` (teczka nowej rozmowy) i `wiadomosc-od` (otwiera rozmowę nadawcy karty)."""
    s, cel = st["sesje"], k["cel"]
    for p in k:
        if p not in POLA_KLIKU:
            blad(sk, f"pole {p} nie należy do kroku klik z celem {cel} (pola: {', '.join(POLA_KLIKU)})")
    if "sesja" in k and cel not in KLIKI_Z_SESJA:
        blad(sk, f"pole sesja tylko w klik z celem „sesja” albo „menu-sesji” (jest w klik z celem „{cel}”)")
    if "folder" in k and cel != "folder":
        blad(sk, f"pole folder tylko w klik z celem „folder” (jest w klik z celem „{cel}”)")
    if cel in KLIKI_Z_LISTA and not s["lista"]:
        blad(sk, f"klik „{cel}” tylko w ćwiczeniu z aplikacja.sesje: bez listy rozmów nie ma wiersza, menu ani nagłówka do kliknięcia (fakt {FAKT_LISTY})")
    if cel in KLIKI_PODGLADU:
        s["pokazuje"] = True
    if cel == "nowa-rozmowa":
        if s["pusta"]:
            blad(sk, "klik nowa-rozmowa, gdy otwarta jest już pusta nowa rozmowa: kliknięcie niczego by nie zmieniło")
        _otwarto(st, "nowa")
    elif cel == "sesja":
        sesja = _sesja(k, sk, st, blad)
        klucz = None if sesja is not None and sesja == s["id_start"] else sesja
        if sesja is not None and klucz == s["otwarta"]:
            blad(sk, f"klik sesja na wierszu „{sesja}”, który jest już otwarty w tej drodze")
        _otwarto(st, klucz, zmien=sesja is not None)
    elif cel == "wiadomosc-od":
        ok, nadawca = scenariusz_wiadomosc.klik(k, sk, st, blad)
        _otwarto(st, nadawca, zmien=ok)
    elif cel == "folder":
        scenariusz_sesje_foldery.klik(k, sk, st, blad)
    elif cel == "menu-sesji":
        s["menu"] = _sesja(k, sk, st, blad) or "?"
    elif cel == "archive":
        _archiwizuj(sk, s, blad)
    elif cel == "group-and-sort":
        s["grupa"] = True
    else:
        _widok_listy(cel, sk, s, blad)


def _widok_listy(cel: str, sk: str, s: dict, blad) -> None:
    """Klik `view-all` (wymaga otwartego menu Group and sort, otwiera widok listy rozmów) i `archived` (wymaga widoku listy z pierwszą zakładką i zarchiwizowanej rozmowy w tej drodze, wybiera zakładkę Archived)."""
    if cel == "view-all":
        if not s["grupa"]:
            blad(sk, f"klik view-all bez otwartego menu Group and sort: najpierw klik „group-and-sort” (fakt {FAKT_WIDOKU})")
        s["grupa"], s["widok"] = False, "aktywne"
        return
    if s["widok"] != "aktywne":
        blad(sk, f"klik archived {'bez widoku listy rozmów (najpierw klik „view-all”)' if s['widok'] is None else 'przy zakładce Archived, która jest już wybrana'} (fakt {FAKT_WIDOKU})")
    elif not s["archiwum"]:
        blad(sk, f"klik archived bez zarchiwizowanej rozmowy w tej drodze: lista byłaby pusta, a dokumentacja nie mówi, co zakładka pokazuje bez rozmów (fakt {FAKT_WIDOKU})")
    s["widok"] = "archived"


def _archiwizuj(sk: str, s: dict, blad) -> None:
    """Klik `archive`: wymaga otwartego menu rozmowy; wiersz otwartej rozmowy nie jest archiwizowany (dokumentacja nie mówi, co okno pokazuje potem)."""
    menu, s["menu"] = s["menu"], None
    if menu is None:
        blad(sk, f"klik archive bez otwartego menu rozmowy: najpierw klik „menu-sesji” (fakt {FAKT_ARCHIWUM})")
    elif menu == s["otwarta"]:
        blad(sk, f"archiwizacja otwartej rozmowy „{menu}”: dokumentacja nie mówi, co okno pokazuje po archiwizacji rozmowy, w której pracujesz (fakt {FAKT_ARCHIWUM})")
    else:
        s["archiwum"].add(menu)


def _zamknij_odpowiedz(st: dict) -> None:
    """Zmiana rozmowy: ostatnia odpowiedź Claude, jej ścieżka i link znikają z okna, a otwarty plik, widok artefaktu i strona w panelu się zamykają."""
    st["sciezka"] = st["link"] = st["claude"] = st["artefakt"] = None
    st["konczy_slajdami"] = False


def nazwa_sesji(k: dict, sk: str, st: dict, blad) -> None:
    """Pole `nazwa_sesji: {sesja, nazwa}` w kroku `claude`: wiersz z `aplikacja.sesje`, nieotwarty w tej chwili (nazwa otwartej rozmowy: prośba o nią w tej samej rozmowie nie ma źródła), `nazwa` niepusta, najwyżej 200 znaków."""
    s, v = st["sesje"], k["nazwa_sesji"]
    if not isinstance(v, dict) or set(v) != {"sesja", "nazwa"}:
        blad(sk, "nazwa_sesji musi być obiektem {sesja, nazwa}")
        return
    if not s["lista"]:
        blad(sk, f"nazwa_sesji tylko w ćwiczeniu z aplikacja.sesje: nazwę widać dopiero po otwarciu rozmowy z listy (fakt {FAKT_LISTY})")
    elif v["sesja"] not in s["ids"]:
        blad(sk, f"nazwa_sesji: sesja {v['sesja']!r} spoza aplikacja.sesje")
    elif v["sesja"] == s["otwarta"]:
        blad(sk, f"nazwa_sesji dla rozmowy „{v['sesja']}”, która jest otwarta: dokumentacja opisuje prośbę o nazwę innej rozmowy (fakt aplikacja-popros-claude-o-nazwe-lub-archiwum)")
    _nazwa(v["nazwa"], sk, "nazwa_sesji.nazwa", blad)
    if v["sesja"] in s["ids"] and _niepusty(v["nazwa"]):
        s["nazwy"][v["sesja"]] = v["nazwa"]  # od teraz karta wiadomości od tej rozmowy ma ten tytuł


def koniec(sd: str, st: dict, blad) -> None:
    """Koniec drogi: bez otwartego menu rozmowy i bez otwartego menu Group and sort."""
    s = st["sesje"]
    if s["menu"] is not None:
        blad(sd, "droga kończy się otwartym menu rozmowy: dodaj klik „archive”")
    if s["grupa"]:
        blad(sd, "droga kończy się otwartym menu Group and sort: dodaj klik „view-all”")


def pokazuje(st: dict) -> bool:
    """Czy droga ma co pokazać w podglądzie bez kroku plik, artefakt i strona (był w niej klik sesja, archive albo archived)."""
    return st["sesje"]["pokazuje"]
