# Jak pomóc przy kursie

Dziękuję, że chcesz poprawić kurs „Opanuj Claude Code w godzinę”. Każda zgłoszona pomyłka trafia do wszystkich, którzy uczą się po nas.

## Znalazłeś błąd albo coś się zestarzało

Claude Code zmienia się co kilka dni, więc lekcja może się rozjechać z aplikacją. Załóż zgłoszenie (Issues, „Błąd w lekcji”) i napisz:

1. Którą lekcję czytasz (adres strony).
2. Co jest w lekcji, a co widzisz w aplikacji Claude.
3. Wersję aplikacji, jeśli ją znasz.

Pytanie do lekcji albo pomysł na nową zadaj w zakładce Discussions albo na [Discordzie](https://discord.gg/4U348jA9b4).

## Chcesz poprawić lekcję sam

1. Zrób fork repozytorium i gałąź z poprawką.
2. Lekcje leżą w `moduly/<moduł>/<lekcja>/`: `lekcja.md`, `quiz.yaml`, `fiszki.yaml`, `scenariusz.json`.
3. Każde twierdzenie o Claude Code stoi na fakcie z `dane/fakty.yaml` (źródło w oficjalnej dokumentacji, data i wersja). Zmieniasz zdanie o działaniu aplikacji, to najpierw poprawiasz albo dopisujesz fakt, potem lekcję. Za zdaniem w lekcji zostawiasz komentarz `<!-- fakt: id -->`.
4. Sprawdź treść u siebie:

   ```bash
   uv run python -m narzedzia.tresc
   uv run pytest
   ```

5. Otwórz pull request z jednym zdaniem, dlaczego zmiana jest potrzebna.

## Zasady pisania

- Czytelnik nie programuje. Pracuje w aplikacji Claude na komputer.
- Prosty polski, krótkie zdania, pełne polskie znaki.
- Bez anglicyzmów poza nazwami narzędzi i pól w aplikacji.
- Nic z pamięci: tylko to, co stoi w dokumentacji Claude Code.

## Licencja

Wysyłając zmianę, zgadzasz się na jej publikację na licencji MIT, jak cały kurs.
