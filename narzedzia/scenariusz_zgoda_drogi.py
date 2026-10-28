"""Sprawdza w drogach symulatora aplikacji krok `zgoda` (karta zgody na zapis w folderze chronionym `.claude/`, na polecenie terminala albo, z polem `witryna`, na działanie na cudzej stronie: wtedy reguły daje scenariusz_zgoda_strona), jego odliczanie `odliczanie_ms` (w etapach nie działa i jest odrzucane), klik w ptaszek (`klik` z celem `zatwierdz`) oraz kolejność kroków wokół karty (opis: dane/FORMAT-SCENARIUSZA.md)."""

import re

from narzedzia import scenariusz_zgoda_strona
from narzedzia.scenariusz_drzewo import sciezka_ok

TRYBY = ("Manual", "Accept edits")  # tryby, w których zapis w folderze chronionym i polecenie spoza listy wymagają zgody (fakty accept-edits-sciezki-chronione-pytaja, accept-edits-aplikacja-pyta-o-inne-polecenia)
POLA = ("typ", "plik", "polecenie", "witryna", "odliczanie_ms", "fakt")
CHRONIONY = ".claude/"
SAMODZIELNE = ("mkdir", "touch", "rm", "rmdir", "mv", "cp", "sed")  # Accept edits zatwierdza je sam (fakt accept-edits-polecenia-na-plikach)
ODLICZANIE_MS = (1000, 10000)
BEZ_KARTY = ("nauczyciel", "mysli")  # kroki dozwolone między zatwierdzeniem a odpowiedzią Claude


def stan(tryb) -> dict:
    """Klucze stanu drogi: `zgoda` (karta, która czeka na decyzję: para (`plik`, ścieżka), (`polecenie`, nazwa) albo (`witryna`, strona), albo None), `zatwierdzona` (taka sama para po kliku `zatwierdz`, na którą ma odpowiedzieć następny krok `claude`, albo None), `claude` (tekst ostatniej odpowiedzi Claude albo None), `tryb` ćwiczenia i klucze karty przeglądarki (scenariusz_zgoda_strona.stan)."""
    return {"zgoda": None, "zatwierdzona": None, "claude": None, "tryb": tryb, **scenariusz_zgoda_strona.stan()}


def kolejnosc(k: dict, sk: str, st: dict, blad) -> None:
    """Przed każdym krokiem drogi: gdy karta czeka, dozwolony jest tylko `nauczyciel` albo klik `zatwierdz` (przy karcie z `witryna` klik w jeden z trzech przycisków); po zatwierdzeniu następne `claude` wskazuje ten plik (karta na zapis) albo po prostu odpowiada (karta na polecenie); po decyzji przy karcie z `witryna` następny krok to `strona` albo `claude`; między nimi tylko `nauczyciel` i `mysli`. Pole `odliczanie_ms` stoi tylko w kroku `zgoda`."""
    typ = k.get("typ")
    if "odliczanie_ms" in k and typ != "zgoda":
        blad(sk, f"pole odliczanie_ms należy tylko do kroku zgoda (jest w kroku {typ})")
    if st["zgoda"] and st["zgoda"][0] == "witryna":
        scenariusz_zgoda_strona.przy_karcie(k, sk, blad)
    elif st["zgoda"]:
        if typ != "nauczyciel" and not (typ == "klik" and k.get("cel") == "zatwierdz"):
            blad(sk, f"krok {typ} przy karcie zgody, która czeka: Claude czeka na decyzję, dalej tylko nauczyciel albo klik „zatwierdz” (fakt tryb-manual-aplikacja-czeka-na-zatwierdzenie)")
    elif st["zatwierdzona"] and typ not in BEZ_KARTY:
        rodzaj, cel = st["zatwierdzona"]
        st["zatwierdzona"] = None
        if typ != "claude":
            blad(sk, f"krok {typ} po zatwierdzeniu {'zapisu' if rodzaj == 'plik' else 'polecenia'}: najpierw odpowiedź Claude" + (f" z plikiem „{cel}” w polu plik" if rodzaj == "plik" else ""))
        elif rodzaj == "plik" and k.get("plik") != cel:
            blad(sk, f"po zatwierdzeniu zapisu następny krok claude musi wskazać plik „{cel}” w polu plik")
    elif st["po_decyzji"] and typ not in BEZ_KARTY:
        scenariusz_zgoda_strona.po_decyzji(k, sk, st, blad)
    if typ == "claude":
        st["claude"] = k["tekst"] if isinstance(k.get("tekst"), str) else ""


def _odliczanie(k: dict, sk: str, blad) -> None:
    """`odliczanie_ms`: liczba całkowita 1000-10000 i obowiązkowe pole `fakt` (odliczanie mówi o czasie programu)."""
    if "odliczanie_ms" not in k:
        return
    ms = k["odliczanie_ms"]
    if type(ms) is not int or not ODLICZANIE_MS[0] <= ms <= ODLICZANIE_MS[1]:
        blad(sk, f"odliczanie_ms musi być liczbą całkowitą od {ODLICZANIE_MS[0]} do {ODLICZANIE_MS[1]} (milisekundy), jest {ms!r}")
    if not (isinstance(k.get("fakt"), str) and k["fakt"].strip()):
        blad(sk, "odliczanie_ms wymaga pola fakt: odliczanie mówi o czasie programu, więc krok musi mieć fakt")


def _plik(k: dict, sk: str, st: dict, pliki, blad) -> None:
    """Wariant `plik`: ścieżka w `.claude/` z `folder_startowy`, `folder_startowy_dodatkowe` albo `nowe_pliki` (ścieżki od folderu rozmowy)."""
    plik = k.get("plik")
    if not sciezka_ok(plik):
        blad(sk, "zgoda wymaga pola plik: ścieżka od folderu rozmowy, niepusty napis bez pustych członów")
    elif not plik.startswith(CHRONIONY):
        blad(sk, f"karta zgody w drodze to wariant „folder chroniony” (bez nazwy pliku i bez podglądu linijek): plik „{plik}” musi leżeć w {CHRONIONY}; zwykły plik w trybie Accept edits zapisuje się bez pytania (fakt accept-edits-sciezki-chronione-pytaja)")
    elif plik not in pliki:
        blad(sk, f"plik „{plik}” nie istnieje w folder_startowy ani w nowe_pliki (plik z poprzedniego ćwiczenia dopisz w aplikacja.folder_startowy_dodatkowe)")
    st["zgoda"] = ("plik", plik if isinstance(plik, str) else "?")


def _polecenie(k: dict, sk: str, st: dict, blad) -> None:
    """Wariant `polecenie`: nazwa polecenia (niepusty napis bez spacji); w Accept edits nie z listy `SAMODZIELNE`; musi paść w ostatniej odpowiedzi Claude przed kartą, bo karta jej nie pokazuje."""
    nazwa = k["polecenie"]
    if not isinstance(nazwa, str) or not nazwa or re.search(r"\s", nazwa):
        blad(sk, "zgoda: pole polecenie to nazwa polecenia (pierwsze słowo, nie cała linia): niepusty napis bez spacji")
    else:
        if st["tryb"] == "Accept edits" and nazwa in SAMODZIELNE:
            blad(sk, f"Accept edits sam zatwierdza polecenie {nazwa}, karta byłaby fałszem (fakt accept-edits-polecenia-na-plikach); polecenie spoza listy: {', '.join(SAMODZIELNE)}")
        if st["claude"] is None:
            blad(sk, f"zgoda na polecenie „{nazwa}” bez wcześniejszej odpowiedzi Claude: Claude musi nazwać polecenie, o które pyta, karta go nie pokazuje")
        elif not re.search(rf"(?<!\w){re.escape(nazwa)}(?!\w)", st["claude"]):
            blad(sk, f"polecenie „{nazwa}” nie występuje w tekście najbliższej wcześniejszej odpowiedzi Claude: Claude musi nazwać polecenie, o które pyta, karta go nie pokazuje")
    st["zgoda"] = ("polecenie", nazwa if isinstance(nazwa, str) else "?")


def krok(k: dict, sk: str, st: dict, pliki, blad) -> None:
    """Krok `zgoda`: jedno z pól `plik` (zapis w `.claude/`), `polecenie` (polecenie terminala) albo `witryna` (karta przeglądarki, scenariusz_zgoda_strona), `odliczanie_ms` i `fakt`; tryb Manual albo Accept edits (z `witryna` także Auto)."""
    for pole in k:
        if pole == "linijki":
            blad(sk, "karta zgody w drodze nie ma linijek: dokumentacja nie opisuje wyglądu okna zgody na zapis w folderze chronionym ani na polecenie, więc karta ma tylko ikony")
        elif pole not in POLA:
            blad(sk, f"pole {pole} nie należy do kroku zgoda (pola: {', '.join(POLA)})")
    witryna = "witryna" in k
    if witryna and st["tryb"] not in scenariusz_zgoda_strona.TRYBY:
        blad(sk, scenariusz_zgoda_strona.blad_trybu(st["tryb"]))
    elif not witryna and st["tryb"] not in TRYBY:
        blad(sk, f"karta zgody w drodze tylko w trybie {' albo '.join(TRYBY)} (teraz „{st['tryb']}”): żaden fakt nie mówi o zgodzie na zapis w .claude ani na polecenie w innych trybach")
    if not witryna:
        _odliczanie(k, sk, blad)
    if sum(p in k for p in ("plik", "polecenie", "witryna")) != 1:
        if witryna:
            blad(sk, "krok zgoda ma dokładnie jedno z pól plik, polecenie albo witryna (karta przeglądarki): witryna razem z plik albo polecenie to błąd")
        else:
            blad(sk, "krok zgoda ma pole plik albo polecenie, dokładnie jedno z nich (oba pola naraz albo żadne to błąd; trzecim wariantem jest pole witryna, karta przeglądarki)")
        st["zgoda"] = ("plik", "?")
    elif witryna:
        scenariusz_zgoda_strona.karta(k, sk, st, blad)
    elif "polecenie" in k:
        _polecenie(k, sk, st, blad)
    else:
        _plik(k, sk, st, pliki, blad)


def bez_odliczania_w_etapach(wezel, s: str, blad) -> None:
    """Ćwiczenie z `etapy`: pole `odliczanie_ms` w dowolnym miejscu listy etapów (kroki etapu, drogi etapów, kroki przycisków karty planu) to błąd, bo odtwarzacz etapów go nie obsługuje."""
    if isinstance(wezel, dict):
        if "odliczanie_ms" in wezel:
            blad(s, "odliczanie_ms działa tylko w karcie zgody w drogach (ćwiczenie z drogami): odtwarzacz etapów go nie obsługuje")
        for klucz, wartosc in wezel.items():
            bez_odliczania_w_etapach(wartosc, f"{s}/{klucz}", blad)
    elif isinstance(wezel, list):
        for i, wartosc in enumerate(wezel):
            bez_odliczania_w_etapach(wartosc, f"{s}[{i}]", blad)


def zatwierdz(sk: str, st: dict, blad) -> None:
    """Klik `zatwierdz`: wymaga czekającej karty; po nim następna odpowiedź Claude ma wskazać zapisany plik (karta na zapis) albo odpowiedzieć (karta na polecenie)."""
    if st["zgoda"] and st["zgoda"][0] == "witryna":
        return scenariusz_zgoda_strona.klik_zatwierdz(sk, st, blad)
    if not st["zgoda"]:
        blad(sk, "klik zatwierdz bez karty zgody, która czeka na decyzję")
    st["zatwierdzona"], st["zgoda"] = st["zgoda"], None


def koniec(sd: str, st: dict, blad) -> None:
    """Koniec drogi: bez karty, która czeka, i bez zatwierdzenia, na które Claude nie odpowiedział."""
    if st["zgoda"]:
        cel = scenariusz_zgoda_strona.CELE_PO_KARCIE if st["zgoda"][0] == "witryna" else "„zatwierdz”"
        blad(sd, f"droga kończy się kartą zgody, która czeka na decyzję: dodaj klik {cel}")
    scenariusz_zgoda_strona.koniec(sd, st, blad)
    if st["zatwierdzona"]:
        rodzaj, cel = st["zatwierdzona"]
        if rodzaj == "plik":
            blad(sd, f"po zatwierdzeniu zapisu droga nie ma odpowiedzi Claude z plikiem „{cel}” w polu plik")
        else:
            blad(sd, f"po zatwierdzeniu polecenia „{cel}” droga nie ma odpowiedzi Claude")
