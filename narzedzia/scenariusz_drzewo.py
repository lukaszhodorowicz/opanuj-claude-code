"""Drzewo folderu w podglądzie symulatora aplikacji: nazwy `Podfolder/plik` w `folder_startowy` (najwyżej jeden ukośnik), ścieżki o dowolnej głębokości w `nowe_pliki`, `folder_startowy_dodatkowe`, `czyta` i `czyta_na_start` (teczka to wszystko przed ostatnim `/`), korzeń `folder_glowny` oraz ścieżki od folderu rozmowy i od korzenia."""

import re


def _niepusty(wartosc) -> bool:
    return isinstance(wartosc, str) and bool(wartosc.strip())


def nazwa_ok(nazwa) -> bool:
    """Nazwa pliku w folderze: `plik` albo `Podfolder/plik`, bez pustych członów i bez `..`."""
    if not _niepusty(nazwa):
        return False
    czesci = nazwa.split("/")
    return len(czesci) <= 2 and all(c.strip() and c != ".." for c in czesci)


def sciezka_ok(sciezka) -> bool:
    """Ścieżka pliku o dowolnej głębokości (`.claude/skills/x/SKILL.md`): niepusty napis bez pustych członów, bez `.` i bez `..`."""
    return _niepusty(sciezka) and all(c.strip() and c not in (".", "..") for c in sciezka.split("/"))


def teczka(sciezka: str) -> str:
    """Teczka karty w podglądzie: wszystko przed ostatnim `/` (pusty napis, gdy plik leży luzem)."""
    return sciezka.rpartition("/")[0]


def sprawdz_gore(dane: dict, blad) -> None:
    """Góra scenariusza: nazwy w `folder_startowy` mają najwyżej jeden `/`, a `folder_glowny` (opcjonalny) to sama nazwa korzenia."""
    lista = dane.get("folder_startowy")
    for i, nazwa in enumerate(lista if isinstance(lista, list) else []):
        if isinstance(nazwa, str) and not nazwa_ok(nazwa):
            blad(
                f"folder_startowy[{i}]",
                f"nazwa „{nazwa}”: najwyżej jeden / (Podfolder/plik), bez pustych członów",
            )
    if "folder_glowny" in dane:
        glowny = dane["folder_glowny"]
        if not _niepusty(glowny) or "/" in glowny or glowny.startswith("~"):
            blad(
                "folder_glowny",
                "folder_glowny to sama nazwa korzenia podglądu, bez / i ~",
            )


def _wymieniony(tekst: str, nazwa: str) -> bool:
    """Ta sama zasada co PK.wymienionePliki w stronie: nazwa jako osobne słowo, nie część dłuższej ścieżki ani nazwy."""
    return bool(
        re.search(rf"(^|[^\w.\-/]){re.escape(nazwa)}(?![\w-]|\.\w)", tekst or "")
    )


class Uklad:
    """Drzewo ćwiczenia: pliki z `folder_startowy` i `aplikacja.folder_startowy_dodatkowe` (ścieżki od korzenia), teczki i folder rozmowy."""

    def __init__(self, start, dodatkowe, nowe, apl, glowny, sa, blad, wiele_folderow=False):
        self.pliki = set(start) | set(dodatkowe)
        self.teczki = {teczka(p) for p in self.pliki if "/" in p}
        folder = apl.get("folder")
        # teczka z `/` w nazwie (`.claude/skills/x`) to etykieta ścieżki, nie folder rozmowy: folder_glowny potrzebują tylko teczki jednoczłonowe
        jednoczlonowe = sorted(t for t in self.teczki if "/" not in t)
        if jednoczlonowe and not _niepusty(glowny):
            blad(sa, f"teczki w folder_startowy ({jednoczlonowe}) wymagają folder_glowny: bez niego podgląd rysuje folder rozmowy wewnątrz korzenia o tej samej nazwie")
        self.przedrostek = (
            ""  # ścieżka folderu rozmowy od korzenia, z `/` na końcu; korzeń = pusty
        )
        if _niepusty(glowny) and _niepusty(folder) and folder != glowny:
            if folder in self.teczki:
                self.przedrostek = folder + "/"
            else:
                blad(
                    sa,
                    f"folder „{folder}” musi być korzeniem podglądu (folder_glowny „{glowny}”) albo teczką z plikami od startu: {sorted(self.teczki) or 'brak teczek'}",
                )
        self.przedrostek_startowy = self.przedrostek  # folder rozmowy startowej; w ćwiczeniu z folderem każdej rozmowy (`wiele_folderow`) nazwy `nowe_pliki` liczą się od korzenia, a folder otwartej rozmowy zmienia się w drodze
        if wiele_folderow:
            self.przedrostek = ""
        self.nowe = {self.przedrostek + n for n in nowe}
        rozmowa = apl.get("rozmowa")  # zły typ zgłasza walidator rozmowy; tu tylko bez wyjątku
        tekst = "\n".join(
            w.get("tekst", "")
            for w in (rozmowa if isinstance(rozmowa, list) else [])
            if isinstance(w, dict) and isinstance(w.get("tekst"), str)
        )
        # plik, o którym mówi rozmowa startowa, Claude utworzył przed ćwiczeniem: w podglądzie leży od początku
        self.na_starcie = self.pliki | {
            p for p in self.nowe if p.startswith(self.przedrostek_startowy) and _wymieniony(tekst, p[len(self.przedrostek_startowy) :])
        }

    def widoczne(self, nowe) -> set:
        """Nazwy plików tak, jak widzi je kursant i pisze Claude: od folderu rozmowy; pliki spoza niego (nad nim albo w sąsiedniej teczce) nie mają takiej nazwy."""
        p = self.przedrostek
        return {x[len(p) :] for x in self.pliki if x.startswith(p)} | set(nowe)


def czyta_na_start(apl, sa, uklad, jest_drogi, blad) -> None:
    """Pole `aplikacja.czyta_na_start`: lista ścieżek od korzenia; tylko w ćwiczeniu z drogami, każda wskazuje plik leżący w folderze od startu."""
    if "czyta_na_start" not in apl:
        return
    sc = f"{sa}/czyta_na_start"
    lista = apl["czyta_na_start"]
    if not jest_drogi:
        blad(
            sc,
            "czyta_na_start tylko w ćwiczeniu z drogami (świeci na początku każdej drogi)",
        )
    if not isinstance(lista, list) or not lista:
        blad(sc, "czyta_na_start musi być niepustą listą ścieżek od korzenia podglądu")
        return
    for i, p in enumerate(lista):
        if not sciezka_ok(p):
            blad(
                f"{sc}[{i}]",
                "ścieżka od korzenia podglądu: niepusty napis bez pustych członów, bez . i bez ..",
            )
        elif p not in uklad.na_starcie:
            blad(
                f"{sc}[{i}]",
                f"ścieżka „{p}” (od korzenia podglądu) nie wskazuje pliku, który leży w folderze od startu",
            )


def krok_czyta(k, sk, tree, blad) -> None:
    """Pole `czyta` kroku `mysli`: lista ścieżek od korzenia, każda wskazuje plik, który w tym miejscu drogi leży w drzewie (`tree`)."""
    if "czyta" not in k:
        return
    if k.get("typ") != "mysli":
        blad(sk, f"pole czyta tylko w kroku mysli (jest w kroku „{k.get('typ')}”)")
        return
    lista = k["czyta"]
    if not isinstance(lista, list) or not lista:
        blad(sk, "czyta musi być niepustą listą ścieżek od korzenia podglądu")
        return
    for i, p in enumerate(lista):
        if not sciezka_ok(p):
            blad(
                f"{sk}/czyta[{i}]",
                "ścieżka od korzenia podglądu: niepusty napis bez pustych członów, bez . i bez ..",
            )
        elif p not in tree:
            blad(
                f"{sk}/czyta[{i}]",
                f"ścieżka „{p}” (od korzenia podglądu) nie wskazuje pliku, który w tym miejscu drogi leży w folderze",
            )
