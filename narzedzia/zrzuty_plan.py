"""Plan ujęć zrzutów lekcji ze `scenariusz.json` i `zrzuty.json` (nazwy, rozmiary, budżet czasu, kliknięcia); sam Chrome obsługuje `narzedzia/zrzuty.py`."""

import json
from pathlib import Path

from narzedzia.zrzuty_czas import budzet_drogi, czekanie_na_znacznik

DOMYSLNE = {"szer": 1280, "wys": 1500, "budzet": 20000}


def _kroki_po_opcji_0(kroki: list) -> tuple[int, int]:
    """Zwraca (liczba okien wyboru, suma pauz w ms) na drodze, która w każdym oknie bierze opcję 0."""
    menu = ms = 0
    for krok in kroki:
        if not isinstance(krok, dict):
            continue
        ms += int(krok.get("ms") or 0)
        if krok.get("typ") == "menu":
            menu += 1
            opcje = krok.get("opcje") or []
            if opcje and isinstance(opcje[0], dict):
                m, t = _kroki_po_opcji_0(opcje[0].get("dalej") or [])
                menu, ms = menu + m, ms + t
    return menu, ms


def _koszt_przebiegu(zadanie: dict) -> tuple[int, int]:
    """Okna wyboru (suma ze wszystkich okien ćwiczenia) i najdłuższy czas pauz jednego przebiegu."""
    menu = ms = 0
    for kroki in (zadanie.get("przebiegi") or {}).values():
        m, t = _kroki_po_opcji_0(kroki)
        menu, ms = menu + m, max(ms, t)
    return menu, ms


def plan_ujec(katalog: Path) -> dict[str, dict]:
    """Plan ujęć lekcji ze `scenariusz.json`, z poprawkami z `zrzuty.json` (jeśli leży obok).

    Ujęcie `<id>-po-przebiegu`: w ćwiczeniu aplikacji z drogami pole `droga` (id ćwiczenia) każe skryptowi przejść całą drogę
    pierwszego polecenia, klikając po kolei element ze znacznikiem „kliknij tutaj”, aż znaczników nie będzie (budżet i czekanie na kolejny
    znacznik liczone z kroków drogi wzorami silnika, `narzedzia/zrzuty_czas.py`). Wpis w `zrzuty.json` z listą `klik` albo z `"droga": false` wyłącza to przechodzenie: wtedy gra tylko pierwsze polecenie
    i to, co wpis wymienia."""
    katalog = Path(katalog)
    scenariusz = json.loads((katalog / "scenariusz.json").read_text(encoding="utf-8"))
    cwiczenia = [
        c
        for c in scenariusz.get("cwiczenia") or []
        if isinstance(c, dict) and c.get("id")
    ]
    plan: dict[str, dict] = {"start-1280": {"szer": 1280, "wys": 6000, "budzet": 20000}}
    pierwsze_drogi: dict[str, dict] = {}  # id ćwiczenia aplikacji z drogami -> jego pierwsza droga
    for cw in cwiczenia:
        zadania = cw.get("zadania") or [{}]
        zadanie = zadania[0] if isinstance(zadania[0], dict) else {}
        menu, ms = _koszt_przebiegu(zadanie)
        ujecie = {
            "szer": 1280,
            "wys": 1500,
            "budzet": 15000 + ms + 3000 * menu,
            "do": cw["id"],
        }
        if not zadanie.get("start_od_razu"):
            ujecie["polecenie"] = cw["id"]
        if menu:
            ujecie["opcje"] = [[cw["id"], 0]] * menu
        drogi = cw.get("drogi") if cw.get("rodzaj") == "aplikacja" else None
        if isinstance(drogi, list) and drogi and isinstance(drogi[0], dict):
            pierwsze_drogi[cw["id"]] = drogi[0]
            ujecie["droga"] = cw["id"]
            ujecie["droga_przerwa"] = czekanie_na_znacznik(drogi[0])
            ujecie["budzet"] += budzet_drogi(drogi[0])
        plan[f"{cw['id']}-po-przebiegu"] = ujecie
    if cwiczenia:
        pierwsze = cwiczenia[0]["id"]
        plan[f"{pierwsze}-390"] = {
            "szer": 390,
            "wys": 2000,
            "budzet": 20000,
            "do": pierwsze,
        }
    wlasne = katalog / "zrzuty.json"
    if wlasne.is_file():
        for nazwa, wpis in json.loads(wlasne.read_text(encoding="utf-8")).items():
            ujecie = {**plan.get(nazwa, DOMYSLNE), **wpis}
            if "klik" in wpis and "droga" not in wpis:
                ujecie.pop("droga", None)
            if ujecie.get("droga") is True:  # `"droga": true`: ćwiczenie to to samo, od którego zaczyna się ujęcie
                ujecie["droga"] = ujecie.get("polecenie") or ujecie.get("do") or True
            droga = pierwsze_drogi.get(ujecie.get("droga")) if isinstance(ujecie.get("droga"), str) else None
            if droga and wpis.get("droga"):  # droga włączona wpisem: czekanie i (bez własnego `budzet`) budżet z jej kroków
                ujecie.setdefault("droga_przerwa", czekanie_na_znacznik(droga))
                if "budzet" not in wpis:
                    ujecie["budzet"] = max(ujecie["budzet"], 15000 + budzet_drogi(droga))
            plan[nazwa] = ujecie
    return plan
