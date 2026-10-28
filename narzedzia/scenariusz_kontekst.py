"""Sprawdza w ćwiczeniu z drogami symulatora aplikacji karta Context i pytanie z boku: pole `aplikacja.kontekst` (procent na starcie), panel szczegółów widoczny tylko z tym polem, kroki `kontekst`, `komenda` i `z_boku` oraz kliki `context` i `zamknij-z-boku` (opis: dane/FORMAT-SCENARIUSZA.md, część „Karta Context, polecenia w polu wiadomości i pytanie z boku”)."""

GDZIE = "aplikacja"
TYPY = ("kontekst", "komenda", "z_boku")
KLIKI = ("context", "zamknij-z-boku")
KOMENDY = ("/compact", "/btw", "/config")  # polecenia, które symulator gra: /compact tylko wpisuje się i znika, /btw otwiera panel pytania z boku, /config okno Settings na stronie Claude Code (stan okna: scenariusz_telefon.komenda)
POLA = {
    "kontekst": ("typ", "procent", "fakt"),
    "komenda": ("typ", "tekst", "fakt"),
    "z_boku": ("typ", "pytanie", "odpowiedz", "fakt"),
}
PRZY_PANELU = ("nauczyciel", "z_boku")  # kroki dozwolone, gdy panel pytania z boku jest otwarty (poza kliknięciem krzyżyka)


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


def _procent(wartosc, s, pole, napisy, blad) -> bool:
    """Procent na karcie: liczba całkowita 0-100, a jego napis „N%” pasuje do wzoru z listy napisów interfejsu aplikacji."""
    if type(wartosc) is not int or not 0 <= wartosc <= 100:
        blad(s, f"{pole} musi być liczbą całkowitą od 0 do 100 (procent zajętego kontekstu), jest {wartosc!r}")
        return False
    if not napisy.jest(f"{wartosc}%", GDZIE):
        blad(s, f"{pole}: napis „{wartosc}%” nie pasuje do wzoru z listy napisów interfejsu aplikacji")
        return False
    return True


def pole(cw: dict, s: str, napisy, blad) -> None:
    """`aplikacja.kontekst` (procent na starcie karty Context): tylko w ćwiczeniu z drogami albo z etapami (w etapach to sam procent na karcie, którą kursant może rozwinąć; kroków `kontekst`, `komenda` i `z_boku` etapy nie mają), liczba całkowita 0-100 z napisem „N%” zgodnym ze wzorem z listy napisów."""
    apl = cw.get("aplikacja")
    if not isinstance(apl, dict) or "kontekst" not in apl:
        return
    sa = f"{s}/aplikacja"
    if "drogi" not in cw and "etapy" not in cw:
        blad(sa, "kontekst tylko w ćwiczeniu z drogami albo z etapami: karta Context stoi w panelu szczegółów, a kroki go nie grają")
    _procent(apl["kontekst"], sa, "kontekst", napisy, blad)
    # procent rozmowy z paska bocznego: opcjonalne pole `kontekst` wiersza aplikacja.sesje
    for i, w in enumerate(apl.get("sesje") if isinstance(apl.get("sesje"), list) else []):
        if isinstance(w, dict) and "kontekst" in w:
            _procent(w["kontekst"], f"{sa}/sesje[{i}]", "kontekst", napisy, blad)


def pole_sesji_bez_karty(cw: dict, s: str, blad) -> None:
    """Wiersz `aplikacja.sesje` z polem `kontekst` w ćwiczeniu bez `aplikacja.kontekst`: karty Context w panelu nie ma, więc procent rozmowy nie ma gdzie stanąć."""
    apl = cw.get("aplikacja")
    if not isinstance(apl, dict) or "kontekst" in apl:
        return
    for i, w in enumerate(apl.get("sesje") if isinstance(apl.get("sesje"), list) else []):
        if isinstance(w, dict) and "kontekst" in w:
            blad(f"{s}/aplikacja/sesje[{i}]", "pole kontekst wiersza sesje bez aplikacja.kontekst: karta Context stoi w panelu szczegółów, którego to ćwiczenie nie ma")


def panel_drogi(apl: dict, sa: str, blad) -> None:
    """Ćwiczenie z drogami: panel „schowany” (licznika po prośbie kursanta nie podaje żaden fakt), a z `aplikacja.kontekst` panel widoczny z kartą Context i kartą Changes bez licznika; pole `zmiany` nigdy."""
    if "kontekst" in apl:
        if apl.get("panel", "widoczny") != "widoczny":
            blad(sa, "kontekst wymaga panelu „widoczny”: karta Context stoi w panelu szczegółów (fakt aplikacja-panel-szczegolow-ukryj-i-pokaz)")
    elif apl.get("panel") != "schowany":
        blad(sa, "ćwiczenie z drogami wymaga panel „schowany”: licznika po prośbie kursanta nie podaje żaden fakt (panel „widoczny” tylko z polem kontekst: karta Context, karta Changes bez licznika)")
    if "zmiany" in apl:
        blad(sa, "ćwiczenie z drogami nie ma pola zmiany: licznika po prośbie kursanta nie podaje żaden fakt")


def stan(cw_apl: dict) -> dict:
    """Klucze stanu drogi: `kontekst` (procent na karcie albo None, gdy ćwiczenie nie ma karty), `karta_otwarta`, `z_boku` (panel pytania z boku jest otwarty) i `kontekst_pola` (procent rozmów z pola `kontekst` wierszy aplikacja.sesje: id → procent)."""
    start = cw_apl.get("kontekst") if isinstance(cw_apl, dict) else None
    wiersze = cw_apl.get("sesje") if isinstance(cw_apl, dict) and isinstance(cw_apl.get("sesje"), list) else []
    pola = {w["id"]: w["kontekst"] for w in wiersze if isinstance(w, dict) and isinstance(w.get("id"), str) and type(w.get("kontekst")) is int}
    return {"kontekst": start if type(start) is int else None, "karta_otwarta": False, "z_boku": False, "kontekst_pola": pola}


def kolejnosc(k: dict, sk: str, st: dict, blad) -> None:
    """Przed każdym krokiem drogi: przy otwartym panelu pytania z boku dalej tylko `nauczyciel`, `z_boku` i klik `zamknij-z-boku`, bo główna rozmowa się wtedy nie zmienia, a karty Context nie widać (fakt aplikacja-pytanie-z-boku-nic-nie-wraca-do-rozmowy)."""
    typ = k.get("typ")
    if st["z_boku"] and typ not in PRZY_PANELU and not (typ == "klik" and k.get("cel") == "zamknij-z-boku"):
        blad(sk, f"krok {typ} przy otwartym panelu pytania z boku: dalej tylko nauczyciel, z_boku i klik „zamknij-z-boku” (główna rozmowa się nie zmienia, karta Context jest schowana; fakt aplikacja-pytanie-z-boku-nic-nie-wraca-do-rozmowy)")


def krok(k: dict, sk: str, st: dict, napisy, blad) -> None:
    """Krok `kontekst` (nowy procent na karcie), `komenda` (`/compact` albo `/btw` w polu wiadomości) albo `z_boku` (pytanie i odpowiedź w panelu pytania z boku)."""
    typ = k["typ"]
    for p in k:
        if p not in POLA[typ]:
            blad(sk, f"pole {p} nie należy do kroku {typ} (pola: {', '.join(POLA[typ])})")
    if typ == "kontekst":
        _kontekst(k, sk, st, napisy, blad)
    elif typ == "komenda":
        _komenda(k, sk, st, napisy, blad)
    else:
        _z_boku(k, sk, st, blad)


def _kontekst(k, sk, st, napisy, blad) -> None:
    if st["kontekst"] is None:
        blad(sk, "krok kontekst bez aplikacja.kontekst: karta Context stoi w panelu szczegółów, którego to ćwiczenie nie ma")
    if not _procent(k.get("procent"), sk, "procent", napisy, blad):
        return
    if k["procent"] == st["kontekst"] and not st.get("karta_pusta"):  # po nowa-rozmowa karta nie ma procentu: procent starej rozmowy nie liczy się (scenariusz_pierscien.py)
        blad(sk, f"procent {k['procent']}% jest już na karcie Context: krok kontekst ma ją zmienić")
    st["kontekst"] = k["procent"]
    st["karta_pusta"] = False


def _komenda(k, sk, st, napisy, blad) -> None:
    """Tekst to dokładnie `/compact`, `/btw` albo `/config` (bez dalszego tekstu: żaden fakt nie mówi, jak aplikacja przyjmuje polecenie z treścią w polu wiadomości); `/btw` otwiera panel pytania z boku, `/config` okno Settings (stan okna: `scenariusz_telefon.komenda`)."""
    tekst = k.get("tekst")
    if not napisy.jest(tekst, GDZIE):
        blad(sk, f"komenda „{tekst}” spoza listy napisów interfejsu aplikacji")
    elif tekst not in KOMENDY:
        blad(sk, f"komenda „{tekst}”: symulator gra tylko {' i '.join(KOMENDY[:2])} oraz {KOMENDY[2]} (wynik /context w rozmowie nie jest rysowany)")
    if tekst == "/btw":
        st["z_boku"] = True
        st["artefakt"] = None  # panel zajmuje miejsce otwartego pliku albo strony artefaktu (jak krok plik): kolejny artefakt wymaga znów kliku w link


def _z_boku(k, sk, st, blad) -> None:
    """Pytanie kursanta i odpowiedź Claude w panelu: panel musi być otwarty poleceniem `/btw`."""
    for p in ("pytanie", "odpowiedz"):
        if not _niepusty(k.get(p)):
            blad(sk, f"krok z_boku wymaga niepustego pola {p}")
    if not st["z_boku"]:
        blad(sk, "krok z_boku bez otwartego panelu pytania z boku: najpierw komenda /btw (fakt aplikacja-btw-otwiera-boczna-rozmowe)")


def klik(k: dict, sk: str, st: dict, blad) -> None:
    """Klik `context` (otwiera kartę Context; wymaga karty, jeszcze zamkniętej) i `zamknij-z-boku` (zamyka otwarty panel pytania z boku)."""
    if k.get("cel") == "context":
        if st["kontekst"] is None:
            blad(sk, "klik w kartę Context bez aplikacja.kontekst: ćwiczenie nie ma panelu z tą kartą")
        elif st["karta_otwarta"]:
            blad(sk, "klik w kartę Context, która jest już otwarta w tej drodze")
        st["karta_otwarta"] = True
    else:
        if not st["z_boku"]:
            blad(sk, "klik zamknij-z-boku bez otwartego panelu pytania z boku: najpierw komenda /btw")
        st["z_boku"] = False


def opuszczono_rozmowe(st: dict, otwarta) -> None:
    """Tuż przed kliknięciem, które zmienia otwartą rozmowę (`otwarta`: None to startowa, id wiersza albo „nowa”): ostatni procent karty Context tej rozmowy idzie do pamięci, żeby powrót do niej go przywrócił (strona/aplikacja-kontekst.js)."""
    if st.get("kontekst") is not None:
        st.setdefault("kontekst_rozmowy", {})[otwarta] = (st["kontekst"], bool(st.get("karta_pusta")))


def otwarto_rozmowe(st: dict, klucz) -> None:
    """Po kliknięciu, które otworzyło rozmowę `klucz` z paska bocznego (nie nową): karta Context pokazuje jej procent, zamknięta. Rozmowa już widziana wraca do swojego ostatniego procentu, rozmowa z polem `kontekst` wiersza zaczyna od niego, a bez pola karta ma szary pasek zamiast liczby (żaden fakt nie podaje jej procentu). Panel szczegółów jest widoczny (rozmowa już działa)."""
    if st.get("kontekst") is None or klucz == "nowa":
        return
    zapis = st.get("kontekst_rozmowy", {}).get(klucz)
    pole = st.get("kontekst_pola", {}).get(klucz)
    if zapis:
        st["kontekst"], st["karta_pusta"] = zapis
    elif pole is not None:
        st["kontekst"], st["karta_pusta"] = pole, False
    else:
        st["karta_pusta"] = True  # szary pasek: procent poprzedniej rozmowy się nie liczy
    st["karta_otwarta"] = False
    st["panel_ukryty"] = False
