"""Czas gry drogi ćwiczenia aplikacji w ms czasu wirtualnego, liczony wzorami silnika (strona/*.js): budżet ujęcia zrzutu i najdłuższa przerwa między znacznikami, którą skrypt zrzutu musi przeczekać."""

from math import ceil

ZWLOKA_KLIKU = 1200  # skrypt zrzutu przed kliknięciem znacznika czeka 900 ms, po nim 300 ms (narzedzia/zrzuty.py)
PAUZA_CZYTANIA = 600  # strona/aplikacja.js: PAUZA_CZYTANIA_MS przed pierwszym `pisz` (zapas także bez `czyta_na_start`)
ZAPAS_ANIMACJI = 5000  # krok `artefakt` ze slajdami: 900 + 700 + 500 ms i 650 ms na element (strona/aplikacja-slajdy.js)
MIN_PRZERWA = 15000  # najkrótsze czekanie skryptu na kolejny znacznik
ZAPAS_PRZERWY = 3000


def _pisanie(tekst: str) -> int:
    """Pole wiadomości (strona/aplikacja-pole.js): 22 ms na każde dwa znaki, potem 350 ms przed „wysłaniem”."""
    return 22 * ceil(len(tekst) / 2) + 350


def czas_kroku(krok: dict, nast: dict | None) -> int:
    """Ile trwa krok drogi, zanim zacznie się następny (`nast` to następny krok drogi albo None); dla kroku `klik` tylko to, co dzieje się po kliknięciu.
    Nauczyciel czeka tylko przed kolejnym nauczycielem: 1,5 s i 45 ms na znak, od 2,5 do 9 s (`PK.krokNauczyciela`, strona/nauczyciel.js);
    `mysli` trwa `ms` albo 1200; reszta liczb jak w `strona/aplikacja*.js` (kontekst 700, katalog_zamknij 1600, z_boku 900 po pytaniu, wybór poziomu 1500)."""
    typ = krok.get("typ")
    tekst = str(krok.get("tekst") or "")
    if typ == "nauczyciel":
        if not isinstance(nast, dict) or nast.get("typ") != "nauczyciel":
            return 0
        return min(9000, max(2500, 1500 + 45 * len(tekst)))
    if typ == "mysli":
        return int(krok.get("ms") or 1200)
    if typ in ("pisz", "komenda"):
        return _pisanie(tekst)
    if typ == "z_boku":
        return _pisanie(str(krok.get("pytanie") or "")) + 900
    if typ == "kontekst":
        return 700
    if typ == "katalog_zamknij":
        return int(krok.get("ms") or 1600)
    if typ == "zgoda":
        return int(krok.get("odliczanie_ms") or 0)
    if typ == "artefakt":
        return ZAPAS_ANIMACJI
    if typ == "klik":
        return 200 + 450 + (1500 if krok.get("cel") == "poziom" else 0)
    return 0


def czasy_drogi(droga: dict) -> tuple[int, int]:
    """(czas całej drogi, najdłuższa przerwa między dwoma znacznikami) w ms; przerwa liczy się od kliknięcia znacznika (jego skutek) przez kroki pomiędzy do następnego znacznika,
    a dla pierwszego znacznika od startu drogi. Czas drogi zawiera zwłokę skryptu przy każdym kliknięciu."""
    kroki = [k for k in droga.get("kroki") or [] if isinstance(k, dict)]
    razem = przerwa = biezaca = 0
    for j, krok in enumerate(kroki):
        t = czas_kroku(krok, kroki[j + 1] if j + 1 < len(kroki) else None)
        if j == 0 and krok.get("typ") == "pisz":
            t += PAUZA_CZYTANIA
        razem += t
        if krok.get("typ") == "klik":
            razem += ZWLOKA_KLIKU
            przerwa, biezaca = max(przerwa, biezaca), t
        else:
            biezaca += t
    return razem, przerwa


def budzet_drogi(droga: dict) -> int:
    """Budżet czasu wirtualnego dla drogi: jej czas z zapasem 20% i 5 s."""
    return int(czasy_drogi(droga)[0] * 1.2) + 5000


def czekanie_na_znacznik(droga: dict) -> int:
    """Jak długo skrypt zrzutu czeka na kolejny znacznik: najdłuższa przerwa drogi z zapasem, nie krócej niż 15 s."""
    return max(MIN_PRZERWA, czasy_drogi(droga)[1] + ZAPAS_PRZERWY)
