/* Symulator aplikacji Claude, dane panelu pliku, menu pliku i dymka ikony paska tytułu: napisy ze zrzutów Łukasza z 27.10.2026 (materialy/zrzuty-lukasza/ w pamięci projektu: panel pliku 15-27-18, menu „…” panelu 15-27-25, menu prawego kliku na karcie pliku 15-27-51, dymek pierwszej ikony paska tytułu 15-28-18). Kod rysujący jest w strona/aplikacja-plik-panel.js, gra w strona/aplikacja-plik-gra.js. Stałe zapisane jak JSON (cudzysłowy przy kluczach): tests/test_aplikacja_plik_ekrany.py czyta je stąd i sprawdza w dane/napisy-interfejsu.yaml (gdzie: aplikacja) oraz w narzedzia/scenariusz_plik_ekran.py. */

/* Menu „…” panelu pliku od góry, grupy oddzielone kreską. `skrot` i `wartosc` to szary napis po prawej, `podmenu` to strzałka ›, `ptak` to pole wyboru (true: niebieski ✓, false: bez ✓; stan ze zrzutu, a pozycje nie mają skutku). */
PK.MENU_PLIKU = [
  [{"napis": "Show file tree", "skrot": "⇧ ⌘ Y"}, {"napis": "File tree position", "wartosc": "Automatic", "podmenu": true}],
  [{"napis": "Preview tabs", "ptak": true}, {"napis": "Auto save", "ptak": true}, {"napis": "Tab key indents", "ptak": true}],
  [{"napis": "Word wrap", "ptak": true}, {"napis": "Indent guides", "ptak": true}, {"napis": "Show whitespace", "ptak": false}, {"napis": "Scroll past end", "ptak": false}, {"napis": "Tab size", "wartosc": "4", "podmenu": true}]
];

/* Menu prawego kliku na karcie pliku w rozmowie, grupy oddzielone kreską. Podmenu (Copy, Open in) nie ma zrzutu, więc się nie otwiera. */
PK.MENU_KARTY_PLIKU = [
  [{"napis": "Attach as context"}, {"napis": "Copy", "podmenu": true}],
  [{"napis": "Open in", "podmenu": true}, {"napis": "Show in Finder"}]
];

/* Znaczek rodzaju pliku na karcie w rozmowie: tylko .txt (zrzut 15-27-18 pokazuje „TXT”, innych znaczków żaden zrzut nie ma). */
PK.RODZAJ_KARTY_PLIKU = {".txt": "TXT"};

/* Dymek ikony paska tytułu: tylko pierwsza ikona (zrzut 15-28-18). Dymków pozostałych ikon żaden zrzut nie pokazuje, więc nie powstają. */
PK.DYMKI_PASKA = {"1": "Show session rail"};
