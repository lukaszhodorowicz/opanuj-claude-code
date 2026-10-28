"""Wyjątek od reguły „droga ćwiczenia aplikacji kończy się plikiem, artefaktem albo stroną”: droga, która kończy się wyborem poziomu wysiłku, który zmienia bieżący, nowym procentem na karcie Context (krok `kontekst`), wyborem trybu albo otwarciem menu środowiska, pokazuje tę zmianę w oknie, więc podgląd pliku nie jest jej potrzebny (opis: dane/FORMAT-SCENARIUSZA.md, część „Paczka 4A”, punkt „Droga bez pliku”). Samo kliknięcie w kartę Context nie jest wyjątkiem."""

from narzedzia.scenariusz_model import WYSILKI

CELE_BEZ_PLIKU = ("tryb", "srodowisko-menu", "plik-karta-menu", "plik-karta-pozycja", "ikona-tytulu")  # kliki, których skutek widać w oknie: wybrany tryb, otwarte menu środowiska (`tryb-menu` otwiera listę, ale droga musi ją zamknąć wyborem `tryb`)
TYPY_BEZ_PLIKU = ("kontekst",)  # krok z nowym procentem na karcie Context
DOMYSLNY_WYSILEK = "Medium"  # bieżący poziom, gdy `aplikacja.wysilek` pominięto (też bez `aplikacja.model`)


def _biezacy(apl) -> int:
    """Numer (1-5) bieżącego poziomu wysiłku na starcie: z `aplikacja.wysilek`, inaczej Medium."""
    nazwa = apl.get("wysilek") if isinstance(apl, dict) else None
    return WYSILKI.index(nazwa if nazwa in WYSILKI else DOMYSLNY_WYSILEK) + 1


def _ostatni(kroki):
    """Ostatni krok drogi poza wypowiedziami nauczyciela albo None."""
    for k in reversed(kroki if isinstance(kroki, list) else []):
        if isinstance(k, dict) and k.get("typ") != "nauczyciel":
            return k
    return None


def poziom_bez_zmiany(kroki, apl):
    """Nazwa poziomu, gdy droga kończy się klikiem `poziom`, który wybiera poziom już bieżący (na starcie `aplikacja.wysilek` albo Medium, po wcześniejszych klikach `poziom` drogi ten z poprzedniego); inaczej None. Taki klik niczego w oknie nie zmienia, więc nie jest wyjątkiem od reguły pliku (jak `tryb` równy bieżącemu trybowi)."""
    ostatni = _ostatni(kroki)
    if not (ostatni and ostatni.get("typ") == "klik" and ostatni.get("cel") == "poziom"):
        return None
    biezacy = _biezacy(apl)
    for k in kroki:
        if k is ostatni:
            break
        if isinstance(k, dict) and k.get("typ") == "klik" and k.get("cel") == "poziom" and type(k.get("poziom")) is int:
            biezacy = k["poziom"]
    return WYSILKI[biezacy - 1] if ostatni.get("poziom") == biezacy else None


def pokazuje(kroki, apl=None) -> bool:
    """Czy ostatni krok drogi (pomijając końcowe wypowiedzi nauczyciela) to krok `kontekst`, klik `tryb`, `srodowisko-menu`, `plik-karta-menu`, `plik-karta-pozycja` albo `ikona-tytulu`, albo klik `poziom` wybierający poziom inny niż bieżący: droga może wtedy skończyć się bez kroku `plik`, `artefakt` i `strona`."""
    ostatni = _ostatni(kroki)
    if not ostatni:
        return False
    if ostatni.get("typ") in TYPY_BEZ_PLIKU:
        return True
    if ostatni.get("typ") != "klik":
        return False
    if ostatni.get("cel") == "poziom":
        return poziom_bez_zmiany(kroki, apl) is None
    return ostatni.get("cel") in CELE_BEZ_PLIKU
