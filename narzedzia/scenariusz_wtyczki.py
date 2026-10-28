"""Sprawdza w drogach symulatora aplikacji przeglądarkę wtyczek otwieraną z podmenu Plugins menu `+` pozycją `Browse plugins` (krok `klik` z celem `pozycja`): kolejność kroków wokół otwartej przeglądarki, środowisko i pustą rozmowę (opis: dane/FORMAT-SCENARIUSZA.md, część „Menu + i przeglądarka wtyczek”)."""

POZYCJA_WTYCZEK = "Browse plugins"  # pozycja podmenu Plugins (menu +), która otwiera przeglądarkę wtyczek; podmenu otwiera klik w pozycję „Plugins” (scenariusz_plus.py)


def stan(apl) -> dict:
    """Klucze stanu drogi: `wt` (przeglądarka otwarta), `wt_czeka` (zaraz po otwarciu najpierw nauczyciel), `wt_srodowisko` i `wt_pusta` (rozmowa ćwiczenia pusta: nowa sesja)."""
    apl = apl if isinstance(apl, dict) else {}
    return {"wt": False, "wt_czeka": False, "wt_srodowisko": apl.get("srodowisko"), "wt_pusta": not apl.get("rozmowa")}


def ma_przegladarke(droga: dict) -> bool:
    """Droga ma krok `klik` z celem `pozycja` i `na: Browse plugins`: kończy się otwartą przeglądarką, nie plikiem ani artefaktem."""
    kroki = droga.get("kroki") if isinstance(droga, dict) else None
    return any(isinstance(k, dict) and k.get("typ") == "klik" and k.get("cel") == "pozycja" and k.get("na") == POZYCJA_WTYCZEK for k in kroki or [])


def _otwarcie(sk: str, st: dict, blad) -> None:
    """`Browse plugins` przy otwartym podmenu Plugins otwiera przeglądarkę; w środowisku Cloud i w pustej rozmowie to błąd."""
    if st["wt_srodowisko"] == "Cloud":
        blad(sk, f"„{POZYCJA_WTYCZEK}” w środowisku Cloud: przeglądarki wtyczek nie ma w sesjach w chmurze (fakt aplikacja-wtyczki-nie-w-chmurze-i-wsl)")
    if st["wt_pusta"]:
        blad(sk, f"„{POZYCJA_WTYCZEK}” w pustej rozmowie: przeglądarka wtyczek otwiera się w sesji lokalnej albo SSH, a pusta rozmowa to czas przed sesją (fakt aplikacja-add-plugins-otwiera-przegladarke-wtyczek; zrzut 03-58-57 pokazuje podmenu Plugins w nowej sesji, więc fakt czeka na rewizję)")
    st["wt"], st["wt_czeka"] = True, True


def kolejnosc(k: dict, sk: str, st: dict, blad) -> None:
    """Przed każdym krokiem drogi (przed `scenariusz_plus.kolejnosc`): zaraz po otwarciu przeglądarki musi stać `nauczyciel`, a przy otwartej przeglądarce dozwolony jest tylko `nauczyciel` (okno zamyka dopiero „Od nowa” albo nowe polecenie)."""
    typ = k.get("typ")
    if st["wt"] and typ != "nauczyciel":
        blad(sk, f"krok {typ} przy otwartej przeglądarce wtyczek: dalej tylko nauczyciel (droga kończy się otwartą przeglądarką)")
    if typ == "nauczyciel":
        st["wt_czeka"] = False
    elif typ == "klik" and k.get("cel") == "pozycja" and k.get("na") == POZYCJA_WTYCZEK and not st["wt"]:
        _otwarcie(sk, st, blad)


def koniec(sd: str, st: dict, blad) -> None:
    """Koniec drogi: jeśli przeglądarka została otwarta, ostatnim krokiem musi być `nauczyciel` (zaraz po otwarciu jest wymagany, więc to pilnuje `wt_czeka`)."""
    if st["wt"] and st["wt_czeka"]:
        blad(sd, "droga kończy się zaraz po otwarciu przeglądarki wtyczek: najpierw nauczyciel, który mówi, co kursant widzi")
