"""Sprawdza w symulatorze aplikacji telefon z Remote Control i stronę Settings → Claude Code: pole `aplikacja.telefon` (urządzenie i sesja), pole `aplikacja.rc_nowe_sesje`, kliki `telefon-sesja`, `telefon-wstecz` i `ustawienia-claude-code` oraz pole `na_telefonie` kroku `pisz` (opis: dane/FORMAT-SCENARIUSZA.md, część „Telefon i Remote Control”)."""

import unicodedata

KLIKI = ("telefon-sesja", "telefon-wstecz", "ustawienia-claude-code", "ustawienia-connectors")
POLA_TELEFONU = ("urzadzenie", "sesja")
POLA_KLIKU = ("typ", "cel", "fakt")
MAKS_ZNAKOW = {"urzadzenie": 40, "sesja": 80}  # nazwa komputera w pasku Devices i tytuł sesji w jednym wierszu telefonu; dłuższe ucina wielokropek, więc limit pilnuje czytelności
CEL_USTAWIEN = "ustawienia-claude-code"
CELE_USTAWIEN = ("ustawienia-claude-code", "ustawienia-connectors")  # oba kroki otwierają okno Settings (Claude Code albo Connectors, zakładka Yours): kroki po otwarciu są te same
KOMENDA_USTAWIEN = "/config"  # krok `komenda` z tym tekstem też otwiera okno Settings na stronie Claude Code (fakt aplikacja-config-otwiera-settings-claude-code)


def otwiera_claude_code(k: dict) -> bool:
    """Krok otwiera okno Settings na stronie Claude Code: klik w konto (`ustawienia-claude-code`) albo komenda `/config` wpisana w pole wiadomości."""
    return (k.get("typ") == "klik" and k.get("cel") == CEL_USTAWIEN) or (k.get("typ") == "komenda" and k.get("tekst") == KOMENDA_USTAWIEN)


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


def _kroki(cw: dict) -> list:
    """Wszystkie kroki wszystkich dróg ćwiczenia (puste, gdy ćwiczenie nie ma dróg)."""
    return [k for d in (cw.get("drogi") if isinstance(cw.get("drogi"), list) else []) if isinstance(d, dict) for k in (d.get("kroki") if isinstance(d.get("kroki"), list) else []) if isinstance(k, dict)]


def _napis(wartosc, pole: str, st: str, blad) -> None:
    """Nazwa komputera albo tytuł sesji: niepusty napis w granicach limitu, bez znaków sterujących i niewidocznych (to dane kursu, nie napis interfejsu)."""
    if not _niepusty(wartosc):
        blad(st, f"telefon.{pole} musi być niepustym napisem")
    elif len(wartosc) > MAKS_ZNAKOW[pole]:
        blad(st, f"telefon.{pole} ma {len(wartosc)} znaków, najwyżej {MAKS_ZNAKOW[pole]} (wiersz telefonu jest jednoliniowy)")
    elif any(unicodedata.category(c) in ("Cc", "Cf", "Zl", "Zp") for c in wartosc):
        blad(st, f"telefon.{pole} ma znak sterujący albo niewidoczny")


def pole(cw: dict, s: str, blad) -> None:
    """`aplikacja.telefon` ({urzadzenie, sesja}) i `aplikacja.rc_nowe_sesje` (prawda albo fałsz): oba tylko w ćwiczeniu z drogami. Telefon wymaga sesji lokalnej z włączonym Remote Control (sesja w chmurze nie ma wiersza Remote Control, zrzut 04-22-37) i nie łączy się z paskiem bocznym z rozmowami (`aplikacja.sesje`)."""
    apl = cw.get("aplikacja")
    if not isinstance(apl, dict):
        return
    sa = f"{s}/aplikacja"
    if "rc_nowe_sesje" in apl:
        if not isinstance(apl["rc_nowe_sesje"], bool):
            blad(sa, f"pole rc_nowe_sesje musi być prawdą albo fałszem, jest {apl['rc_nowe_sesje']!r}")
        if "drogi" not in cw:
            blad(sa, "pole rc_nowe_sesje tylko w ćwiczeniu z drogami: stan przełącznika rysuje okno Settings otwierane krokiem klik „ustawienia-claude-code”")
        elif not any(otwiera_claude_code(k) for k in _kroki(cw)):
            blad(sa, "pole rc_nowe_sesje bez kroku klik „ustawienia-claude-code” albo komendy /config: żadna droga nie otwiera okna Settings, więc pole nic nie rysuje")
    if "telefon" not in apl:
        return
    t = apl["telefon"]
    st = f"{sa}/telefon"
    if not isinstance(t, dict):
        blad(sa, "pole telefon musi być obiektem {urzadzenie, sesja}")
        return
    for p in t:
        if p not in POLA_TELEFONU:
            blad(st, f"pole {p} nie należy do telefonu (pola: {', '.join(POLA_TELEFONU)}): reszta ekranu telefonu to szare paski albo napisy ze zrzutów")
    for p in POLA_TELEFONU:
        _napis(t.get(p), p, st, blad)
    if "drogi" not in cw:
        blad(sa, "telefon tylko w ćwiczeniu z drogami: kursant klika wiersz sesji i pisze na telefonie krokami dróg")
    if apl.get("srodowisko") != "Local":
        blad(sa, f"telefon w środowisku „{apl.get('srodowisko')}”: Remote Control łączy z telefonem sesję lokalną, a sesja w chmurze nie ma wiersza Remote Control (zrzut 04-22-37)")
    if apl.get("remote_control") is False:
        blad(sa, "telefon przy remote_control: false: bez włączonego Remote Control sesja z komputera nie pojawia się na liście na telefonie")
    if "sesje" in apl:
        blad(sa, "telefon w ćwiczeniu z aplikacja.sesje: zmiana rozmowy w pasku bocznym nie ma opisanego skutku dla telefonu (nie łączymy)")
    if _niepusty(apl.get("nazwa")) and _niepusty(t.get("sesja")) and apl["nazwa"] != t["sesja"]:
        blad(sa, f"tytuł rozmowy na komputerze (nazwa „{apl['nazwa']}”) inny niż sesja na telefonie („{t['sesja']}”): to ta sama rozmowa, ma jeden tytuł")


def stan(apl) -> dict:
    """Klucze stanu drogi: `tel` (ćwiczenie ma telefon), `tel_ekran` (`lista` na starcie albo `rozmowa`), `tel_ustaw` (okno Settings otwarte), `tel_ustaw_czeka` (zaraz po otwarciu okna najpierw nauczyciel) i `tel_pokazuje` (w drodze był klik telefonu albo ustawień)."""
    return {"tel": isinstance(apl, dict) and isinstance(apl.get("telefon"), dict), "tel_ekran": "lista", "tel_ustaw": False, "tel_ustaw_czeka": False, "tel_pokazuje": False}


def _pisz(k: dict, sk: str, st: dict, blad) -> None:
    """Krok `pisz` z `na_telefonie: true`: telefon musi pokazywać otwartą rozmowę (skill w polu komputera sprawdza `przed_plus`)."""
    if k["na_telefonie"] is not True:
        blad(sk, f"na_telefonie musi być prawdą (true) albo nie występować, jest {k['na_telefonie']!r}")
    if not st["tel"]:
        blad(sk, "na_telefonie w ćwiczeniu bez aplikacja.telefon: nie ma telefonu, na którym kursant pisze")
    elif st["tel_ekran"] != "rozmowa":
        blad(sk, "na_telefonie, gdy telefon pokazuje listę sesji: najpierw klik „telefon-sesja”, który otwiera rozmowę z komputera")


def przed_plus(k: dict, sk: str, st: dict, blad) -> None:
    """Wołane PRZED `scenariusz_plus.kolejnosc`, które przy kroku `pisz` zeruje stan skilla w polu (skill i tekst idą w jednej wiadomości): `pisz` z `na_telefonie` przy skillu wybranym z listy na komputerze to błąd, bo skill idzie z prośbą wpisaną na komputerze, nie z telefonu."""
    if k.get("typ") == "pisz" and k.get("na_telefonie") is True and st.get("plus_pole") == "skill":
        blad(sk, "na_telefonie przy skillu wybranym w polu komputera: skill idzie z prośbą wpisaną na komputerze, nie z telefonu")


def kolejnosc(k: dict, sk: str, st: dict, blad) -> None:
    """Przed każdym krokiem drogi: pole `na_telefonie` tylko w kroku `pisz`, a po otwarciu okna Settings dalej tylko `nauczyciel` (okno zamyka dopiero „Od nowa” albo nowe polecenie; panel, pole i rozmowa stoją pod nim)."""
    typ = k.get("typ")
    if "na_telefonie" in k:
        if typ == "pisz":
            _pisz(k, sk, st, blad)
        else:
            blad(sk, f"pole na_telefonie tylko w kroku pisz, jest w kroku {typ}")
    if st["tel_ustaw"] and typ != "nauczyciel":
        blad(sk, f"krok {typ} przy otwartym oknie Settings: dalej tylko nauczyciel (droga kończy się otwartym oknem)")
    if typ == "nauczyciel":
        st["tel_ustaw_czeka"] = False


def klik(k: dict, sk: str, st: dict, blad) -> None:
    """Klik `telefon-sesja` (z listy do rozmowy), `telefon-wstecz` (z rozmowy do listy), `ustawienia-claude-code` (okno Settings na stronie Claude Code) albo `ustawienia-connectors` (okno Settings na stronie Connectors, zakładka Yours); żaden nie ma pól poza `typ`, `cel` i `fakt`."""
    cel = k.get("cel")
    for p in k:
        if p not in POLA_KLIKU:
            blad(sk, f"pole {p} nie należy do kliku {cel} (pola: {', '.join(POLA_KLIKU)})")
    st["tel_pokazuje"] = True
    if cel in CELE_USTAWIEN:
        st["tel_ustaw"] = st["tel_ustaw_czeka"] = True
    elif not st["tel"]:
        blad(sk, f"klik {cel} w ćwiczeniu bez aplikacja.telefon: nie ma telefonu, na którym kursant klika")
    elif cel == "telefon-sesja":
        if st["tel_ekran"] != "lista":
            blad(sk, "klik „telefon-sesja”, gdy telefon już pokazuje rozmowę: najpierw „telefon-wstecz”")
        st["tel_ekran"] = "rozmowa"
    else:
        if st["tel_ekran"] != "rozmowa":
            blad(sk, "klik „telefon-wstecz”, gdy telefon pokazuje listę sesji: wracać nie ma skąd")
        st["tel_ekran"] = "lista"


def komenda(k: dict, st: dict) -> None:
    """Komenda `/config` otwiera okno Settings na stronie Claude Code: dalej jak po kliku `ustawienia-claude-code` (tylko nauczyciel, droga bez pliku może się tak skończyć)."""
    if k.get("typ") == "komenda" and k.get("tekst") == KOMENDA_USTAWIEN:
        st["tel_pokazuje"] = st["tel_ustaw"] = st["tel_ustaw_czeka"] = True


def koniec(sd: str, st: dict, blad) -> None:
    """Koniec drogi: okno Settings otwarte tuż przed końcem wymaga jeszcze wypowiedzi nauczyciela, który mówi, co kursant widzi."""
    if st["tel_ustaw_czeka"]:
        blad(sd, "droga kończy się zaraz po otwarciu okna Settings: najpierw nauczyciel, który mówi, co kursant widzi")


def pokazuje(st: dict) -> bool:
    """Droga z klikiem telefonu albo ustawień może skończyć się bez kroku plik, artefakt i strona: pokazuje telefon albo otwarte okno Settings."""
    return st["tel_pokazuje"]
