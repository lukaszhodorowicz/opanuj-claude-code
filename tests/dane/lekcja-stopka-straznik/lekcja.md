<em>Przewodnik po Claude Code · Moduł 1: Tryby pracy · Lekcja 4 z 4</em>

# Tryb auto: strażnik zamiast pytań

Dwa ćwiczenia w symulatorze

W trybie Auto (automatycznym) Claude pracuje bez zwykłych pytań o zgodę. <!-- fakt: auto-aplikacja-opis-trybu --> Zanim uruchomi polecenie terminala, sprawdza je w tle drugi model AI, strażnik. <!-- fakt: auto-aplikacja-opis-trybu --> <!-- fakt: auto-klasyfikator-ocenia-przed-wykonaniem -->

Wybierz Auto: Claude zmieni plik i spakuje umowy bez karty zgody. <!-- fakt: aplikacja-tryb-wybierasz-w-przelaczniku --> <!-- fakt: aplikacja-auto-i-accept-edits-stosuja-zmiany --> <!-- fakt: auto-aplikacja-opis-trybu -->

<!-- cwiczenie: cw1 -->

## Co tu się stało?

<!-- kolumny -->

#### Zmiana zestawienia

1. Claude przeczytał umowy i zmienił zestawienie bez karty zgody. <!-- fakt: aplikacja-auto-i-accept-edits-stosuja-zmiany -->
2. Strażnik nie ocenia odczytów ani zmian zwykłych plików w folderze. <!-- fakt: auto-odczyty-i-zmiany-w-folderze-bez-klasyfikatora -->

#### Paczka zip

1. Claude spakował umowy poleceniem zip.
2. Przed takim poleceniem strażnik sprawdził, czy pasuje ono do Twojej prośby. <!-- fakt: auto-aplikacja-opis-trybu -->

<!-- /kolumny -->

Teraz dopisz do prośby granicę: jedno zdanie, że pakowanie ma poczekać. Granica je zatrzyma, a zdejmiesz ją dopiero wiadomością. <!-- fakt: auto-granice-z-rozmowy --> <!-- fakt: auto-granica-trwa-do-zdjecia-wiadomoscia -->

<!-- cwiczenie: cw2 -->

## Co tu się stało?

<!-- kolumny -->

#### Blokada

1. Zdanie „Nie pakuj niczego, dopóki nie przejrzę zestawienia” strażnik uznał za granicę. <!-- fakt: auto-granice-z-rozmowy -->
2. Zablokował pakowanie, a Claude dostał powód blokady. <!-- fakt: auto-claude-dostaje-powod-blokady -->
3. Zmiana zestawienia przeszła, bo strażnik nie ocenia takich zmian. <!-- fakt: auto-odczyty-i-zmiany-w-folderze-bez-klasyfikatora -->

#### Granica zdjęta

1. Claude sam uznał zestawienie za gotowe, ale granica dalej obowiązywała. <!-- fakt: auto-granica-trwa-do-zdjecia-wiadomoscia -->
2. Zdjęła ją dopiero Twoja wiadomość. <!-- fakt: auto-granica-trwa-do-zdjecia-wiadomoscia -->

<!-- /kolumny -->

Po 3 blokadach z rzędu albo 20 łącznie tryb Auto się wstrzymuje i Claude Code znów pyta o zgodę. <!-- fakt: auto-wstrzymanie-po-blokadach -->

## Jak włączyć tryb Auto

<!-- kolumny -->

#### W aplikacji Claude na komputer

1. W zakładce Code kliknij przełącznik trybu pod polem wiadomości. <!-- fakt: aplikacja-przelacznik-pod-polem-wiadomosci --> Na Macu listę trybów otworzysz też skrótem <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>M</kbd>. <!-- fakt: aplikacja-skrot-menu-trybu -->
2. Kliknij **Auto**. Widać go tylko, gdy masz do niego dostęp. <!-- fakt: aplikacja-dostepne-tryby --> <!-- fakt: auto-aplikacja-opis-trybu -->

#### Jeśli pracujesz w terminalu

1. Nowa sesja w terminalu zwykle zaczyna się w trybie Auto. <!-- fakt: tryb-startowy-terminal-auto --> Bez dostępu do Auto zaczyna się w trybie Manual. <!-- fakt: tryb-startowy-manual-gdy-auto-niedostepne -->
2. W innym trybie naciskaj <kbd>Shift</kbd> + <kbd>Tab</kbd>, aż pasek stanu pokaże <em>⏵⏵ auto mode on</em>. <!-- fakt: pasek-napisy-trybow --> <!-- fakt: cykl-shift-tab-od-auto --> W aplikacji ten skrót nie zmienia trybu. <!-- fakt: cykl-aplikacja-brak-shift-tab -->
3. Przy pierwszym odczycie pliku spoza folderu program pyta o zgodę w oknie <em>Read outside the working directories</em> (odczyt spoza folderów roboczych). <!-- fakt: auto-pierwszy-odczyt-spoza-folderu-pyta --> <!-- fakt: okno-odczyt-spoza-folderu-tytul-i-pytanie-terminal -->
   - „Yes, and keep allowing…” (tak, zawsze): kolejne takie odczyty przejdą bez pytania. <!-- fakt: odczyt-spoza-folderu-yes-keep-allowing -->
   - „No, and block…” (nie, blokuj): narzędzia do czytania plików odmówią takich odczytów w każdej sesji i w każdym trybie. <!-- fakt: odczyt-spoza-folderu-no-block-na-stale -->
   - Odpowiedzi z „ask again next time” (zapytaj następnym razem) działają tylko ten raz. <!-- fakt: odczyt-spoza-folderu-yes-ask-again --> <!-- fakt: odczyt-spoza-folderu-no-ask-again -->
   - Po każdej z tych odpowiedzi Claude pracuje dalej. <!-- fakt: odczyt-spoza-folderu-claude-pracuje-dalej -->

<!-- /kolumny -->

## Kiedy włączać tryb Auto, a kiedy nie

<!-- kolumny -->

#### Włącz

- Gdy ufasz, że praca idzie w dobrym kierunku. <!-- fakt: auto-nie-gwarantuje-bezpieczenstwa -->
- Gdy jeden krok ma poczekać na Ciebie. Napisz to jednym zdaniem. <!-- fakt: auto-granice-z-rozmowy -->

#### Nie włączaj

- Do wrażliwych operacji, które trzeba przejrzeć samodzielnie. Tryb Auto nie gwarantuje bezpieczeństwa. <!-- fakt: auto-nie-gwarantuje-bezpieczenstwa -->
- Gdy granica ma obowiązywać zawsze. Zdanie z rozmowy nie jest zapisaną regułą i może zniknąć, gdy Claude streści długą rozmowę. <!-- fakt: auto-granice-z-rozmowy -->

<!-- /kolumny -->

## Źródła

Dokumentacja Claude Code:

- [Choose a permission mode](https://code.claude.com/docs/en/permission-modes)
- [Desktop application](https://code.claude.com/docs/en/desktop)
- [Get started with the desktop app](https://code.claude.com/docs/en/desktop-quickstart)

Sprawdzone 23–25.10.2026, Claude Code 2.1.309–2.1.310. Ćwiczenia ułożyliśmy według tych stron. Napis okna w terminalu pochodzi z programu.
