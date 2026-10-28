"""Walidator katalogu skilla: pilnuje standardu Agent Skills, żeby skill działał w Claude Code i na claude.ai."""

import re
import sys
from pathlib import Path

import yaml

SPEC = "https://agentskills.io/specification"
DOKI = "https://code.claude.com/docs/en/skills"
POLA = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
ZASTRZEZONE = ("synced", "anthropic-skills")
WZOR_NAZWY = re.compile(r"[a-z0-9-]*")


def _blad(tekst: str, zrodlo: str) -> str:
    return f"{tekst} ({zrodlo})"


def _frontmatter(linie: list[str]) -> tuple[list[str], list[str] | None, list[str]]:
    """Zwraca (błędy, linie frontmattera albo None, linie treści)."""
    if not linie or linie[0].rstrip("\r") != "---":
        return [_blad("Pierwsza linia SKILL.md musi być dokładnie `---`; Claude Code czyta frontmatter tylko wtedy", DOKI)], None, linie
    for i in range(1, len(linie)):
        if linie[i].rstrip("\r") == "---":
            return [], linie[1:i], linie[i + 1:]
    return [_blad("Frontmatter nie ma zamykającej linii `---`", DOKI)], None, linie[1:]


def _sprawdz_nazwe(nazwa: object, katalog: Path) -> list[str]:
    if nazwa is None:
        return [_blad("Brak wymaganego pola `name`", SPEC)]
    if not isinstance(nazwa, str):
        return [_blad("Pole `name` musi być tekstem", SPEC)]
    bl = []
    if not 1 <= len(nazwa) <= 64:
        bl.append(_blad(f"Pole `name` ma {len(nazwa)} znaków, a musi mieć od 1 do 64", SPEC))
    if not WZOR_NAZWY.fullmatch(nazwa):
        bl.append(_blad("Pole `name` może zawierać tylko małe litery a-z, cyfry i `-`", SPEC))
    if nazwa.startswith("-") or nazwa.endswith("-"):
        bl.append(_blad("Pole `name` nie może zaczynać się ani kończyć znakiem `-`", SPEC))
    if "--" in nazwa:
        bl.append(_blad("Pole `name` nie może zawierać dwóch myślników pod rząd `--`", SPEC))
    if nazwa != katalog.name:
        bl.append(_blad(f"Pole `name` („{nazwa}”) musi być równe nazwie katalogu („{katalog.name}”)", SPEC))
    return bl


def _zastrzezona(nazwa: str) -> bool:
    m = nazwa.lower()
    return m in ZASTRZEZONE or m.startswith("anthropic-skills:")


def _sprawdz_pola(meta: dict, katalog: Path) -> list[str]:
    bl = []
    for pole in meta:
        if pole not in POLA:
            bl.append(_blad(
                f"Niedozwolone pole `{pole}` we frontmatterze; wgranie skilla na claude.ai kończy się wtedy twardym błędem, "
                f"dozwolone: {', '.join(sorted(POLA))}", DOKI))
    bl += _sprawdz_nazwe(meta.get("name"), katalog)
    for kto, nazwa in (("name", meta.get("name")), ("nazwa katalogu", katalog.name)):
        if isinstance(nazwa, str) and _zastrzezona(nazwa):
            bl.append(_blad(f"Wartość „{nazwa}” ({kto}) jest zastrzeżona i nie może być nazwą skilla", DOKI))
    opis = meta.get("description")
    if opis is None:
        bl.append(_blad("Brak wymaganego pola `description`", SPEC))
    elif not isinstance(opis, str):
        bl.append(_blad("Pole `description` musi być tekstem", SPEC))
    elif not 1 <= len(opis.strip()) <= 1024:
        bl.append(_blad(f"Pole `description` ma {len(opis.strip())} znaków po obcięciu białych znaków, a musi mieć od 1 do 1024", SPEC))
    if "compatibility" in meta:
        kz = meta["compatibility"]
        if not isinstance(kz, str) or not 1 <= len(kz.strip()) <= 500:
            bl.append(_blad("Pole `compatibility` musi być tekstem o długości od 1 do 500 znaków", SPEC))
    if "metadata" in meta and not isinstance(meta["metadata"], dict):
        bl.append(_blad("Pole `metadata` musi być mapą (klucz: wartość)", DOKI))
    return bl


def sprawdz(katalog: Path) -> list[str]:
    """Zwraca listę błędów po polsku; pusta lista = skill poprawny."""
    katalog = Path(katalog)
    plik = katalog / "SKILL.md"
    if not plik.is_file():
        return [_blad("Brak pliku SKILL.md w katalogu skilla", SPEC)]
    linie = plik.read_text(encoding="utf-8").splitlines()
    bl, fm, tresc = _frontmatter(linie)
    if fm is not None:
        try:
            meta = yaml.safe_load("\n".join(fm))
        except yaml.YAMLError as e:
            meta = None
            bl.append(_blad(f"Frontmatter nie jest poprawnym YAML: {str(e).splitlines()[0]}", DOKI))
        else:
            if not isinstance(meta, dict):
                bl.append(_blad("Frontmatter musi być mapą (pole: wartość)", DOKI))
            else:
                bl += _sprawdz_pola(meta, katalog)
        if not "\n".join(tresc).strip():
            bl.append(_blad("Treść SKILL.md po frontmatterze jest pusta", SPEC))
    if len(linie) >= 500:
        bl.append(_blad(f"SKILL.md ma {len(linie)} linii, a musi mieć mniej niż 500", DOKI))
    for nr, linia in enumerate(linie, 1):
        if fm is not None and nr <= len(fm) + 2:
            continue
        if linia.startswith("!`") or linia.startswith("```!"):
            bl.append(_blad(f"Linia {nr} zaczyna się od wstrzykiwania poleceń, które nie działa w claude.ai ani przez API", DOKI))
    return bl


def main(argv: list[str]) -> int:
    if not argv:
        print("Użycie: python -m narzedzia.skill <katalog> [<katalog>...]", file=sys.stderr)
        return 2
    kod = 0
    for arg in argv:
        for b in sprawdz(Path(arg)):
            print(f"{arg}: {b}")
            kod = 1
    return kod


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
