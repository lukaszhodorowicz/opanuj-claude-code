# CLAUDE.md

Ten plik czyta Claude Code, gdy pracuje w tym repozytorium. Kurs powstaje i jest utrzymywany z Claude Code.

Polski kurs Claude Code dla osób, które nie programują. Treść to lekcje w `moduly/<moduł>/<lekcja>/`, a kod w `narzedzia/` sprawdza treść i składa stronę.

## Zasady treści

- **Jedyne źródło faktów:** oficjalna dokumentacja Claude Code (spis `dane/zrodla/llms.txt`) i adresy z `zrodla_zewnetrzne` w `dane/fakty.yaml`. Nie piszesz niczego z pamięci modelu.
- **Fakt istnieje raz,** w `dane/fakty.yaml`, ze źródłem, datą sprawdzenia i wersją Claude Code. Lekcja odwołuje się do niego komentarzem `<!-- fakt: id -->` za zdaniem, quiz i fiszki polem `fakt`.
- **Zmiana w dokumentacji to zmiana faktu.** Poprawiasz fakt, potem każde miejsce, które się do niego odwołuje (`grep -rn "fakt: <id>" moduly/`).
- **Czytelnik nie programuje.** Pracuje w aplikacji Claude na komputer (zakładka Code).
- **Język:** prosty polski, krótkie zdania, pełne polskie znaki.

## Polecenia

```bash
uv run python -m narzedzia.tresc                       # fakty, quizy, fiszki, odwołania
uv run pytest                                          # testy treści i silnika strony
uv run python -m narzedzia.witryna zbuduj --wyjscie _site   # złożenie strony kursu
```

## Zasady pracy

- Gdy test pada, poprawiasz przyczynę, nie test.
- Opis commita mówi, dlaczego zmiana jest potrzebna.
