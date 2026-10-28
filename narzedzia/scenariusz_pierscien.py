"""Sprawdza w ćwiczeniu z drogami symulatora aplikacji pierścień zużycia abonamentu: krok `klik` z celem `pierscien` (okienko bez napisów, pola tylko `typ`, `cel`, `fakt`), wyjątek od reguły „droga ma plik albo artefakt” i kolejność kroków po `nowa-rozmowa` w ćwiczeniu z kartą Context: panel szczegółów wraca dopiero z pierwszą prośbą, a karta jest bez procentu do kroku `kontekst` (opis: dane/FORMAT-SCENARIUSZA.md, część „Pierścień zużycia”)."""

KLIKI = ("pierscien",)
POLA_KLIKU = ("typ", "cel", "fakt")
FAKT_PANELU = "aplikacja-sesja-startuje-po-wyslaniu-zadania"  # panel szczegółów pojawia się po starcie sesji, a sesja startuje po wysłaniu zadania (z faktem aplikacja-panel-szczegolow-sesji-karty-obok-czatu)


def stan() -> dict:
    """Klucze stanu drogi: `pierscien_klik` (w drodze był klik `pierscien`), `panel_ukryty` (po `nowa-rozmowa` w ćwiczeniu z kartą Context, do pierwszej prośby) i `karta_pusta` (karta Context jest bez procentu do kroku `kontekst`; czyta ją też scenariusz_kontekst)."""
    return {"pierscien_klik": False, "panel_ukryty": False, "karta_pusta": False}


def pokazuje(st: dict) -> bool:
    """Droga z klikiem `pierscien` może się skończyć bez kroku `plik` i `artefakt`: pokazuje otwarte okienko, a w tekście lekcji idzie bez podglądu pliku."""
    return st["pierscien_klik"]


def kolejnosc(k: dict, sk: str, st: dict, blad) -> None:
    """Przed każdym krokiem drogi: po `nowa-rozmowa` w ćwiczeniu z kartą Context krok `kontekst` przed pierwszym `pisz` i klik `context` przed pierwszym `kontekst` to błąd (panel schowany, karta bez procentu); sam `nowa-rozmowa` zaczyna ten stan."""
    typ = k.get("typ")
    cel = k.get("cel") if typ == "klik" else None
    if typ == "pisz":
        st["panel_ukryty"] = False  # pierwsza prośba w nowej rozmowie: sesja startuje, panel wraca
    elif typ == "kontekst" and st["panel_ukryty"]:
        blad(sk, f"krok kontekst po nowa-rozmowa przed pierwszą prośbą: panel szczegółów pojawia się dopiero po wysłaniu pierwszej prośby (fakt {FAKT_PANELU})")
    elif cel == "context" and (st["panel_ukryty"] or st["karta_pusta"]):
        blad(sk, f"klik w kartę Context po nowa-rozmowa przed pierwszym krokiem kontekst: karta jest bez procentu, a przed pierwszą prośbą panelu w ogóle nie ma (fakt {FAKT_PANELU})")
    if cel == "nowa-rozmowa" and st["kontekst"] is not None:
        st["panel_ukryty"] = st["karta_pusta"] = True  # nowa sesja jeszcze się nie zaczęła


def klik(k: dict, sk: str, st: dict, blad) -> None:
    """Klik `pierscien` (otwiera okienko zużycia i zostawia je otwarte): pola tylko `typ`, `cel`, `fakt`."""
    for p in k:
        if p not in POLA_KLIKU:
            blad(sk, f"pole {p} nie należy do kroku klik z celem pierscien (pola: {', '.join(POLA_KLIKU)})")
    st["pierscien_klik"] = True
