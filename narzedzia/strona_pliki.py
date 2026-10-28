"""Spis plików silnika (JS i CSS z katalogu strona/), które generator strony lekcji wkleja do HTML, w kolejności ładowania."""

PLIKI_JS = ("terminal.js", "folder.js", "folder-tresc.js", "nauczyciel.js", "przebieg.js", "aplikacja-ikony.js", "aplikacja-ekran.js", "aplikacja-kontekst-tresc.js", "aplikacja-panel.js", "aplikacja-okno.js", "aplikacja-przegladarka.js", "aplikacja-slajdy.js", "aplikacja-artefakt.js", "aplikacja-folder.js", "aplikacja-folder-cwiczenie.js", "aplikacja-zgoda.js", "aplikacja-tryby-zmiany.js", "aplikacja-tryby-drogi.js", "aplikacja-plan.js", "aplikacja-tryby-menu.js", "aplikacja-tryby.js", "aplikacja-drogi-zgoda.js", "aplikacja-drogi-odliczanie.js", "aplikacja-drogi-strona.js", "aplikacja-przeplyw.js", "aplikacja-drogi-podglad.js", "aplikacja-pole.js", "aplikacja-kontekst.js", "aplikacja-z-boku.js", "aplikacja-plus-dane.js", "aplikacja-plus.js", "aplikacja-ustawienia-dane.js", "aplikacja-ustawienia.js", "aplikacja-katalog.js", "aplikacja-wtyczki.js", "aplikacja-sesje.js", "aplikacja-sesje-foldery.js", "aplikacja-sesje-wiadomosc.js", "aplikacja-sesje-gra.js", "aplikacja-w-tle-widok.js", "aplikacja-w-tle.js", "aplikacja-model.js", "aplikacja-pierscien.js", "aplikacja-harmonogram-widok.js", "aplikacja-harmonogram.js", "aplikacja-telefon-dane.js", "aplikacja-telefon-widok.js", "aplikacja-telefon.js", "aplikacja-ustawienia-cc.js", "aplikacja-kroki.js", "aplikacja.js", "silnik.js")
PLIKI_CSS = (
    "styl-strona.css",
    "styl-cwiczenie.css",
    "styl-dymek.css",
    "styl-okno.css",
    "styl-folder.css",
    "styl-terminal.css",
    "styl-quiz.css",
    "styl-aplikacja.css", "styl-aplikacja-zmiany.css", "styl-aplikacja-przegladarka.css", "styl-aplikacja-artefakt.css", "styl-aplikacja-slajdy.css", "styl-aplikacja-folder.css", "styl-aplikacja-tryby.css", "styl-aplikacja-plan.css", "styl-aplikacja-kontekst.css", "styl-aplikacja-z-boku.css", "styl-aplikacja-plus.css", "styl-aplikacja-plus-menu.css", "styl-aplikacja-ustawienia.css", "styl-aplikacja-kafelki.css", "styl-aplikacja-katalog.css", "styl-aplikacja-wtyczki.css", "styl-aplikacja-sesje.css", "styl-aplikacja-sesje-foldery.css", "styl-aplikacja-sesje-wiadomosc.css", "styl-aplikacja-w-tle.css", "styl-aplikacja-przeplyw.css", "styl-aplikacja-model.css", "styl-aplikacja-pierscien.css", "styl-aplikacja-harmonogram.css", "styl-aplikacja-harmonogram-okno.css", "styl-aplikacja-harmonogram-zaaw.css", "styl-aplikacja-harmonogram-zadanie.css", "styl-aplikacja-ekran.css", "styl-aplikacja-kontekst-tresc.css", "styl-aplikacja-menu-ekran.css",
    "styl-aplikacja-telefon.css", "styl-aplikacja-telefon-rozmowa.css", "styl-aplikacja-ustawienia-cc.css",
)
PLIKI_JS = ("slowniczek.js", *PLIKI_JS)  # podpowiedzi pojęć ze słowniczka (D-2026-10-27-51): na początku, żeby działały także przy błędzie w silniku
PLIKI_CSS = (*PLIKI_CSS, "styl-slowniczek.css")
# paczka 4 część A: napisy pola i menu rzędu przed aplikacja-kroki.js, styl na końcu (po stylach modelu i menu)
_PRZED_KROKAMI = PLIKI_JS.index("aplikacja-kroki.js")
PLIKI_JS = PLIKI_JS[:_PRZED_KROKAMI] + ("aplikacja-napisy-pola.js", "aplikacja-menu-rzedu.js") + PLIKI_JS[_PRZED_KROKAMI:]
PLIKI_CSS = PLIKI_CSS + ("styl-aplikacja-pole.css",)
PLIKI_JS = (*PLIKI_JS[: PLIKI_JS.index("aplikacja-ustawienia.js") + 1], "aplikacja-ustawienia-konta.js", "aplikacja-ustawienia-konektory.js", *PLIKI_JS[PLIKI_JS.index("aplikacja-ustawienia.js") + 1 :])  # paczka 4B: lewa kolumna Settings w wariantach kont i strona Connectors; zaraz po aplikacja-ustawienia.js (ikony katalogu)
PLIKI_CSS = (*PLIKI_CSS, "styl-aplikacja-ustawienia-konektory.css", "styl-aplikacja-konektory-panel.css")
# panel pliku, menu pliku i dymek ikony paska tytułu (zrzuty Łukasza 15-27-18, 15-27-25, 15-27-51, 15-28-18): dane, wygląd i gra przed aplikacja-kroki.js, styl na końcu
_PRZED_KROKAMI = PLIKI_JS.index("aplikacja-kroki.js")
PLIKI_JS = PLIKI_JS[:_PRZED_KROKAMI] + ("aplikacja-plik-dane.js", "aplikacja-plik-panel.js", "aplikacja-plik-gra.js") + PLIKI_JS[_PRZED_KROKAMI:]
PLIKI_CSS = (*PLIKI_CSS, "styl-aplikacja-plik.css")
# paczka 4 część B (ekrany ze zrzutów 15-28-39, 15-31-46 i 15-32-22): menu panelu Browser, menu sesji z paska tytułu z widokiem rozmowy i edytor prezentacji w oknie; przed aplikacja-kroki.js, po slajdach i artefakcie, z których korzystają
_PRZED_KROKAMI_B = PLIKI_JS.index("aplikacja-kroki.js")
PLIKI_JS = (*PLIKI_JS[:_PRZED_KROKAMI_B], "aplikacja-menu-b.js", "aplikacja-browser-dane.js", "aplikacja-browser.js", "aplikacja-menu-tytulu.js", "aplikacja-edytor.js", "aplikacja-edytor-gra.js", *PLIKI_JS[_PRZED_KROKAMI_B:])
PLIKI_CSS = (*PLIKI_CSS, "styl-aplikacja-menu-b.css", "styl-aplikacja-browser.css", "styl-aplikacja-edytor.css")

# zwarte polecenia i przewijanie do okna ćwiczenia (kurs-polecenia): przed aplikacja-kroki.js, silnik.js zostaje ostatni; skrypt sam czeka na koniec wczytywania strony
_PRZED_KROKAMI_C = PLIKI_JS.index("aplikacja-kroki.js")
PLIKI_JS = (*PLIKI_JS[:_PRZED_KROKAMI_C], "polecenia-przewijanie.js", "wyjasnienie.js", *PLIKI_JS[_PRZED_KROKAMI_C:])  # wyjasnienie.js: odwracana karta schematu (D-2026-10-28-01)
PLIKI_CSS = (*PLIKI_CSS, "styl-wyjasnienie.css")
