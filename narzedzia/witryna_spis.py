"""Zbiera spis opublikowanych lekcji (moduly/<modul>/<lekcja>/lekcja.md z okruszkami albo ze slugiem w planie) i plan kolejnych modułów z moduly/PLAN-MODULOW.md."""

import re
from dataclasses import dataclass, field
from pathlib import Path

from narzedzia.znacznik_lekcji import wydziel

NAGLOWEK_MODULU = re.compile(r"^###\s+Moduł\s+(\d+)\.\s+(.+?)\s*$")
KATALOG_MODULU = re.compile(r"^Katalog:\s+`moduly/([\w-]+)`")
LEKCJA_W_PLANIE = re.compile(r"^\s+(\d+)\.\s+\*\*(.+?)\*\*")
SLUG_W_PLANIE = re.compile(r"slug `([\w-]+)`")


@dataclass(frozen=True)
class Lekcja:
    modul: int
    nazwa_modulu: str
    katalog_modulu: str
    katalog: Path
    numer: int
    tytul: str
    liczba: int = 0  # „Lekcja X z Y” z okruszków: Y, liczba lekcji modułu według autora

    @property
    def adres(self) -> str:
        """Adres strony lekcji względem strony startowej, np. „tryby-pracy/okno-zgody/”."""
        return f"{self.katalog_modulu}/{self.katalog.name}/"


@dataclass
class Modul:
    numer: int
    nazwa: str
    katalog: str
    lekcje: list = field(default_factory=list)
    slugi: dict = field(default_factory=dict)  # tylko w planie: slug lekcji -> numer, gdy plan go podaje („slug `co-jest-gdzie`”)


def tekst_tytulu(tresc_md: str, rezerwa: str) -> str:
    """Tytuł z pierwszego nagłówka „# ” jako zwykły tekst (bez **, * i `)."""
    for linia in tresc_md.splitlines():
        if linia.startswith("# "):
            return re.sub(r"[*`]", "", linia[2:]).strip()
    return rezerwa


def zbierz_lekcje(korzen: Path) -> list[Lekcja]:
    """Lekcje w kolejności modułów i numerów: z okruszków „Moduł N: … · Lekcja X z Y”, a bez okruszków z miejsca,
    które plan modułów podaje przy slugu (lekcja 0.0 co-jest-gdzie); plik bez jednego i drugiego nie jest lekcją kursu."""
    z_planu = {
        (m.katalog, slug): (m, numer)
        for m in wczytaj_plan(korzen / "moduly" / "PLAN-MODULOW.md")
        for slug, numer in m.slugi.items()
    }
    lekcje = []
    bez_okruszkow = []
    for plik in sorted((korzen / "moduly").glob("*/*/lekcja.md")):
        tresc = plik.read_text(encoding="utf-8")
        polozenie, _ = wydziel(tresc)
        if polozenie is None:
            if (miejsce := z_planu.get((plik.parent.parent.name, plik.parent.name))) is None:
                bez_okruszkow.append((plik, tresc))
                continue
            modul, numer = miejsce
            lekcje.append(
                Lekcja(
                    modul=modul.numer,
                    nazwa_modulu=modul.nazwa,
                    katalog_modulu=plik.parent.parent.name,
                    katalog=plik.parent,
                    numer=numer,
                    tytul=tekst_tytulu(tresc, plik.parent.name),
                    liczba=-1,  # liczby lekcji modułu plan nie podaje; -1 nie da ramki „Koniec modułu”
                )
            )
            continue
        lekcje.append(
            Lekcja(
                modul=polozenie.modul,
                nazwa_modulu=polozenie.nazwa_modulu,
                katalog_modulu=plik.parent.parent.name,
                katalog=plik.parent,
                numer=polozenie.numer,
                tytul=tekst_tytulu(tresc, plik.parent.name),
                liczba=polozenie.liczba,
            )
        )
    # Bez okruszków i bez planu (repozytorium publiczne nie ma planu): lekcja w module, który ma lekcje z okruszkami,
    # to jego wstęp, numer 0 (tak stoi lekcja 0.0 co-jest-gdzie); w module bez takich lekcji nie jest lekcją kursu.
    moduly = {l.katalog_modulu: l for l in lekcje}
    for plik, tresc in bez_okruszkow:
        if (sasiad := moduly.get(plik.parent.parent.name)) is None:
            continue
        lekcje.append(
            Lekcja(
                modul=sasiad.modul,
                nazwa_modulu=sasiad.nazwa_modulu,
                katalog_modulu=sasiad.katalog_modulu,
                katalog=plik.parent,
                numer=0,
                tytul=tekst_tytulu(tresc, plik.parent.name),
                liczba=-1,
            )
        )
    lekcje.sort(key=lambda l: (l.modul, l.numer, l.katalog.name))
    return lekcje


def grupuj(lekcje: list[Lekcja]) -> list[Modul]:
    """Moduły w kolejności numerów; nazwa modułu z okruszków jego pierwszej lekcji."""
    moduly: dict[int, Modul] = {}
    for lekcja in lekcje:
        modul = moduly.setdefault(
            lekcja.modul,
            Modul(lekcja.modul, lekcja.nazwa_modulu, lekcja.katalog_modulu),
        )
        modul.lekcje.append(lekcja)
    return [moduly[n] for n in sorted(moduly)]


def wczytaj_plan(sciezka: Path) -> list[Modul]:
    """Moduły z planu kursu z tytułami lekcji (pole lekcje to lista napisów); brak pliku daje pustą listę."""
    if not sciezka.is_file():
        return []
    plan: list[Modul] = []
    w_lekcjach = False
    for linia in sciezka.read_text(encoding="utf-8").splitlines():
        if naglowek := NAGLOWEK_MODULU.match(linia):
            plan.append(Modul(int(naglowek.group(1)), naglowek.group(2), ""))
            w_lekcjach = False
        elif linia.startswith("## "):
            w_lekcjach = False
            if plan:
                break  # moduły kończą się na pierwszej sekcji „## ” po nich
        elif plan and (katalog := KATALOG_MODULU.match(linia)):
            plan[-1].katalog = katalog.group(1)
        elif plan and linia.startswith("- **Lekcje:**"):
            w_lekcjach = True
        elif plan and w_lekcjach and (lekcja := LEKCJA_W_PLANIE.match(linia)):
            plan[-1].lekcje.append(lekcja.group(2))
            if slug := SLUG_W_PLANIE.search(linia):
                plan[-1].slugi[slug.group(1)] = int(lekcja.group(1))
        elif linia.startswith("- "):
            w_lekcjach = False
    return plan


def zapowiedzi(plan: list[Modul], opublikowane: list[Modul]) -> list[Modul]:
    """Moduły z planu, z których żadna lekcja nie jest jeszcze opublikowana (porównanie po katalogu modułu każdej lekcji)."""
    gotowe = {l.katalog_modulu for m in opublikowane for l in m.lekcje}
    return [m for m in plan if m.katalog not in gotowe]
